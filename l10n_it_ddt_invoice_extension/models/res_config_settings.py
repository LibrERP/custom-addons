from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    invoice_from_ddt_product_values_source = fields.Selection(
        related='company_id.invoice_from_ddt_product_values_source',
        string='Sorgente valori per generazione righe fattura',
        default='sale.order.line',
        required=True,
        readonly=False,
    )
# end ResConfigSettings
