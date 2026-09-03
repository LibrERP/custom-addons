# © 2026 Andrei Levin <andrei.levin@codebeex.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import api, models


class ReportSaleOrder(models.AbstractModel):
    _name = "report.sale.report_saleorder"
    _description = "Sale Order Report (with child orders)"

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env["sale.order"].browse(docids)._get_orders_with_children()
        return {
            "doc_ids": docs.ids,
            "doc_model": "sale.order",
            "docs": docs,
            "data": data,
        }


class ReportSaleOrderProForma(models.AbstractModel):
    _name = "report.sale.report_saleorder_pro_forma"
    _description = "Sale Order Pro-Forma Report (with child orders)"

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env["sale.order"].browse(docids)._get_orders_with_children()
        return {
            "doc_ids": docs.ids,
            "doc_model": "sale.order",
            "docs": docs,
            "data": data,
        }
