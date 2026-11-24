# © 2026 Andrei Levin - Codebeex srl (www.codebeex.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import models


class HelpdeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'

    def _get_last_sol_of_customer(self):
        """Never guess the Sales Order Item from the customer.

        Standard helpdesk_sale_timesheet fills an empty ticket ``sale_line_id``
        with the first prepaid-hours line of the customer's most recent
        confirmed order, whatever its product or relation to the ticket.
        That silently bills timesheets on unrelated lines, so the guess is
        disabled: the Sales Order Item stays empty until a user sets it
        (or the ticket's project has an explicit Sales Order Item).
        """
        return self.env['sale.order.line']
