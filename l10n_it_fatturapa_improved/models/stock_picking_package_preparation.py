# © 2021 Andrei Levin <andrei.levin@didotech.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api, _


class StockPickingPackagePreparationLine(models.Model):

    _inherit = 'stock.picking.package.preparation.line'

    @api.multi
    def _prepare_invoice_line(self, qty, invoice_id=None):
        results = super()._prepare_invoice_line(qty, invoice_id)

        results['related_documents'] = [(4, document.id) for document in self.sale_line_id.related_documents]

        return results
