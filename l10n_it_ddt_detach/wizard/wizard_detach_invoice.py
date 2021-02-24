# © 2021 Andrei Levin - Didotech srl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class WizardDetachInvoice(models.TransientModel):
    _name = 'wizard.detach.invoice'

    def action_detach_invoice(self):
        for td in self.env['stock.picking.package.preparation'].browse(self.env.context['active_ids']):
            td.invoice_id = False
            td.to_be_invoiced = True
        return True
