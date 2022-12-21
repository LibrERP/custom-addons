# © 2021-2022 Marco Tosato (Didotech srl)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import api, fields, models, _


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    sp_amount_base = fields.Float(
        string='Valore base imponibile della consegna',
        compute='_compute_sp_amounts',
    )

    sp_amount_vat = fields.Float(
        string='Valore iva applicata alla consegna',
        compute='_compute_sp_amounts',
    )

    sp_amount_total = fields.Float(
        string='Valore iva applicata alla consegna',
        compute='_compute_sp_amounts',
    )

    @api.depends('move_line_ids_without_package', 'move_line_ids')
    def _compute_sp_amounts(self):
        for sp in self:
            product_vals = sp.get_amounts_by_product()
            sp.value_amount_base = sum([prod['amount_base'] for prod in product_vals.values()])
            sp.value_amount_vat = sum([prod['amount_vat'] for prod in product_vals.values()])
        # end for
    # end _compute_amount_base_and_vat

    def get_products_base_and_vat(self):
        self.ensure_one()

        products_data = dict()
        product_values = dict()

        sale_order = self.sale_id

        o_lines = sale_order.order_line
        m_lines = self.move_line_ids

        # Collect price and quantity for each line of the sale.order
        # and index them by related product id
        for oln in o_lines:

            prod = oln.product_id
            products_data[prod.id] = {
                'amount_base': oln.price_subtotal,
                'amount_vat': oln.price_tax,
                'qty': oln.product_qty,
                'tax': oln.tax_id
            }
        # end for

        for mln in m_lines:

            prod_id = mln.product_id.id
            prod_info = products_data[prod_id]

            product_values[prod_id] = {
                'amount_base': prod_info['amount_base'] / prod_info['qty'] * mln.qty_done,
                'amount_vat': prod_info['amount_vat'] / prod_info['qty'] * mln.qty_done,
                'tax': prod_info['tax']
            }
        # end for
        return product_values
    # end get_products_base_and_vat
# end StockPicking
