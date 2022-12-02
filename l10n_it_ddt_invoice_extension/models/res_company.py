from odoo import models, fields


class ResCompany(models.Model):
    _inherit = 'res.company'

    invoice_from_ddt_product_values_source = fields.Selection(
        [
            ('sale.order.line', 'Ordine di Vendita'),
            ('td.line', 'DDT'),
        ],
        string='Sorgente valori per generazione righe fattura',
        default='sale.order.line',
        required=True,
    )
# end ResCompany
