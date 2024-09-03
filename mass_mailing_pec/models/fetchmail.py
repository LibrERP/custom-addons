# © 2024 Andrei Levin <andrei.levin@codebeex.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import _, api, Command, fields, models
import locale
import logging
_logger = logging.getLogger(__name__)
_logger.setLevel(logging.DEBUG)

# pip install mail-parser
import mailparser
from datetime import timedelta


class Fetchmail(models.Model):
    _inherit = "fetchmail.server"

    is_pec = fields.Boolean("PEC server")
    last_pec_error_message = fields.Text("Last PEC Error Message", readonly=True)
    pec_error_count = fields.Integer("PEC error count", readonly=True)

    # def fetch_mail_server_type_imap(self, server, error_messages, **additional_context):
    #     # Set the locale to English
    #     locale.setlocale(locale.LC_TIME, 'en_US.UTF-8')
    #
    #     imap = None
    #     try:
    #         imap = server.connect()
    #         imap.select()
    #
    #         # since = server.date - timedelta(days=1)
    #         since = server.date
    #
    #         result, msg_ids = imap.search(None, f'(SINCE "{since.strftime("%d-%b-%Y")}")')
    #         for num in msg_ids[0].split():
    #             result, msg_data = imap.fetch(num, "(RFC822)")
    #             # imap.store(num, "-FLAGS", "\\Seen")
    #
    #             try:
    #                 if msg_data:
    #                     mail = mailparser.parse_from_bytes(msg_data[0][1])
    #                     x_status = mail.X_Ricevuta or ''
    #                     x_reference = mail.X_Riferimento_Message_ID or ''
    #                     mail_trace = self.env['mailing.trace'].search([
    #                         ('message_id', '=', x_reference)
    #                     ])
    #                     if mail_trace and not mail_trace.pec_status == 'avvenuta-consegna':
    #                         if x_status in ('avvenuta-consegna', 'accettazione'):
    #                             mail_trace.pec_status = x_status
    #
    #                     _logger.debug(f"{x_reference}: {x_status}")
    #
    #                 # if message is processed without exceptions
    #                 server.last_pec_error_message = ""
    #             except Exception as e:
    #                 error_messages.append(server.set_pec_failure(e))
    #                 continue
    #
    #             # imap.store(num, "+FLAGS", "\\Seen")
    #             # We need to commit because message is processed:
    #             # Possible next exceptions, out of try, should not
    #             # rollback processed messages
    #             self._cr.commit()  # pylint: disable=invalid-commit
    #     except Exception as e:
    #         error_messages.append(server.set_pec_failure(e))
    #     finally:
    #         if imap:
    #             imap.close()
    #             imap.logout()

    def fetch_mail_server_type_imap(self, server, error_messages, **additional_context):
        # Set the locale to English
        locale.setlocale(locale.LC_TIME, 'en_US.UTF-8')

        with server.connect() as imap:
            try:
                imap.select()

                # since = server.date - timedelta(days=1)
                since = server.date

                result, msg_ids = imap.search(None, f'(SINCE "{since.strftime("%d-%b-%Y")}")')
                for num in msg_ids[0].split():
                    result, msg_data = imap.fetch(num, "(RFC822)")
                    # imap.store(num, "-FLAGS", "\\Seen")

                    try:
                        if msg_data:
                            mail = mailparser.parse_from_bytes(msg_data[0][1])
                            x_status = mail.X_Ricevuta or ''
                            x_reference = mail.X_Riferimento_Message_ID or ''
                            mail_trace = self.env['mailing.trace'].search([
                                ('message_id', '=', x_reference)
                            ])
                            if mail_trace and not mail_trace.pec_status == 'avvenuta-consegna':
                                if x_status in ('avvenuta-consegna', 'accettazione'):
                                    mail_trace.pec_status = x_status

                            _logger.debug(f"{x_reference}: {x_status}")

                        # if message is processed without exceptions
                        server.last_pec_error_message = ""
                    except Exception as e:
                        error_messages.append(server.set_pec_failure(e))
                        continue

                    # imap.store(num, "+FLAGS", "\\Seen")
                    # We need to commit because message is processed:
                    # Possible next exceptions, out of try, should not
                    # rollback processed messages
                    self._cr.commit()  # pylint: disable=invalid-commit
            except Exception as e:
                error_messages.append(server.set_pec_failure(e))

    def fetch_mail(self):
        for server in self:
            if not server.is_pec:
                super(Fetchmail, server).fetch_mail()
            else:
                additional_context = {"fetchmail_cron_running": True}
                # Setting fetchmail_cron_running to avoid to disable cron while
                # cron is running (otherwise it would be done by setting
                # server.state = 'draft',
                # see _update_cron method)
                server = server.with_context(**additional_context)

                _logger.info(
                    "start checking for new pec emails on %s server %s",
                    server.server_type,
                    server.name,
                )
                additional_context["fetchmail_server_id"] = server.id
                additional_context["server_type"] = server.server_type
                error_messages = list()
                if server.server_type == "imap":
                    server.fetch_mail_server_type_imap(
                        server, error_messages, **additional_context
                    )
                elif server.server_type == "pop":
                    # server.fetch_mail_server_type_pop(
                    #     server, mail_thread, error_messages, **additional_context
                    # )
                    message = f"Usage of POP server {server.name} for pec emails is not implemented"
                    error_messages.append(message)

                if error_messages:
                    server.notify_and_log(error_messages)
                    server.pec_error_count += 1
                    max_retry = self.env["ir.config_parameter"].get_param(
                        "fetchmail.pec.max.retry"
                    )
                    if server.pec_error_count > int(max_retry):
                        # Setting to draft prevents new e-invoices to
                        # be sent via PEC.
                        # Resetting server state only after N fails.
                        # So that the system can try to fetch again after
                        # temporary connection errors
                        server.state = "draft"
                        server.notify_about_server_reset()
                else:
                    server.pec_error_count = 0
            server.write({"date": fields.Datetime.now()})
        return True

    def set_pec_failure(self, exception):
        self.ensure_one()
        _logger.info(
            "Failure when fetching emails "
            f"using {self.server_type} server {self.name}.",
            exc_info=True,
        )

        exception_msg = str(exception)
        # `str` on Odoo exceptions does not return
        # a nice representation of the error
        odoo_exc_string = getattr(exception, "name", None)
        if odoo_exc_string:
            exception_msg = odoo_exc_string

        self.last_pec_error_message = exception_msg
        return exception_msg

    def notify_about_server_reset(self):
        self.ensure_one()
        self.notify_and_log(
            _(
                "PEC server %(name)s has been reset. "
                "Last error message is '%(error_message)s'"
            )
            % {"name": self.name, "error_message": self.last_pec_error_message}
        )

    def notify_and_log(self, message):
        """
        Send an email to partners in
        self.e_inv_notify_partner_ids containing message.

        :param: message
        :type message: list of str, or str
        """
        self.ensure_one()
        if isinstance(message, list):
            message = "<br/>".join(message)

        self.env["mail.mail"].create(
            {
                "subject": _("Fetchmail PEC server [%s] error") % self.name,
                "body_html": message,
                "recipient_ids": [(6, 0, [self.env.user.partner_id.id])],
            }
        ).send()
        _logger.info(
            f"Notifying partner {self.env.user.partner_id.name} about PEC server {self.name} error"
        )
