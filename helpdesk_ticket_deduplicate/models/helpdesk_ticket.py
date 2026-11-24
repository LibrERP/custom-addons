# © 2026 Andrei Levin - Codebeex srl (www.codebeex.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import _, fields, models
from odoo.exceptions import UserError

# Pairs (ticket, other ticket) that received the same incoming email,
# both still active and not in a cancelled stage.
_SHARED_EMAIL_SQL = """
    SELECT msg.res_id, other.res_id
      FROM mail_message msg
      JOIN mail_message other
        ON other.message_id = msg.message_id
       AND other.model = 'helpdesk.ticket'
       AND other.res_id != msg.res_id
      JOIN helpdesk_ticket ticket ON ticket.id = msg.res_id
      LEFT JOIN helpdesk_stage stage ON stage.id = ticket.stage_id
      JOIN helpdesk_ticket other_ticket ON other_ticket.id = other.res_id
      LEFT JOIN helpdesk_stage other_stage ON other_stage.id = other_ticket.stage_id
     WHERE msg.model = 'helpdesk.ticket'
       AND msg.message_type = 'email'
       AND msg.message_id IS NOT NULL
       -- archived or cancelled tickets neither warn nor are warned about
       AND ticket.active AND other_ticket.active
       AND stage.is_cancel IS NOT TRUE AND other_stage.is_cancel IS NOT TRUE
"""


class HelpdeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'

    duplicated_ticket_ids = fields.Many2many(
        comodel_name='helpdesk.ticket',
        compute='_compute_duplicated_ticket_ids',
        search='_search_duplicated_ticket_ids',
        string='Duplicated Tickets',
        help="Other tickets that received the same email (same Message-Id). "
             "It happens when a customer writes to more than one helpdesk "
             "address at once: the mail gateway creates one ticket per address. "
             "Archived and cancelled tickets are ignored.",
    )

    def _flush_duplicate_fields(self):
        self.env['mail.message'].flush_model(['message_id', 'model', 'res_id', 'message_type'])
        self.env['helpdesk.ticket'].flush_model(['active', 'stage_id'])
        self.env['helpdesk.stage'].flush_model(['is_cancel'])

    def _compute_duplicated_ticket_ids(self):
        ticket_to_duplicates = self._fetch_duplicated_tickets()
        for ticket in self:
            ticket.duplicated_ticket_ids = ticket_to_duplicates.get(ticket._origin.id, self.browse())

    def _fetch_duplicated_tickets(self):
        """Return {ticket id: other visible tickets sharing an incoming email}."""
        ticket_ids = [tid for tid in self._origin.ids if tid]
        if not ticket_ids:
            return {}
        self._flush_duplicate_fields()
        self.env.cr.execute(
            f"SELECT res_id, ARRAY_AGG(DISTINCT other_id) FROM ({_SHARED_EMAIL_SQL} AND msg.res_id = ANY(%s)) "
            "AS pairs(res_id, other_id) GROUP BY res_id",
            [ticket_ids],
        )
        rows = self.env.cr.fetchall()
        if not rows:
            return {}
        # Only show tickets the user is allowed to see (record rules, active).
        visible = self.search([('id', 'in', list({tid for _res, ids in rows for tid in ids}))])
        return {res_id: visible.filtered(lambda t, ids=set(ids): t.id in ids) for res_id, ids in rows}

    def action_open_business_doc(self):
        """Called by the x2many_buttons widget when a duplicate is clicked."""
        self.ensure_one()
        return {
            'name': _("Ticket"),
            'type': 'ir.actions.act_window',
            'res_model': 'helpdesk.ticket',
            'res_id': self.id,
            'view_mode': 'form',
            'views': [(False, 'form')],
        }

    def _search_duplicated_ticket_ids(self, operator, value):
        """Support ('duplicated_ticket_ids', '!=', False) / ('=', False).

        A ticket matches when another ticket the user can see (record rules,
        active) received the same email, consistent with the form warning.
        """
        if operator not in ('=', '!=') or value not in (False, None):
            raise UserError(_("Unsupported search on Duplicated Tickets."))
        self._flush_duplicate_fields()
        self.env.cr.execute(_SHARED_EMAIL_SQL)
        pairs = self.env.cr.fetchall()
        visible_others = set(self.search([('id', 'in', list({other for _res, other in pairs}))]).ids)
        ids = list({res_id for res_id, other in pairs if other in visible_others})
        return [('id', 'in' if operator == '!=' else 'not in', ids)]
