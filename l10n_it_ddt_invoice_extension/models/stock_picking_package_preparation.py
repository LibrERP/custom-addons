from odoo import models, fields, api, _


class StockPickingPackagePreparationLine(models.Model):

    _inherit = 'stock.picking.package.preparation.line'

    @api.multi
    def _prepare_invoice_line(self, qty, invoice_id=None):
        """
        Prepare the dict of values to create the new invoice line for a
        ddt line.

        :param qty: float quantity to invoice
        :param invoice_id: possible existing invoice
        """
        self.ensure_one()

        res = super()._prepare_invoice_line(qty, invoice_id=invoice_id)

        system_settings = self.env['res.config.settings'].search([])[0]
        values_source = system_settings.invoice_from_ddt_product_values_source

        if values_source == 'sale.order.line':
            # Get price and discount from related sale order line
            so_line = self.sale_line_id

            res.update({
                'discount': so_line.discount,
                'price_unit': so_line.price_unit,
            })

        elif values_source == 'td.line':
            # Get price and discount from TD (aka DDT)
            # Nothing to do here since it's the exact
            # behaviour of the original method
            pass

        else:
            assert False, (
                f'res.config.settings -> invoice_from_ddt_product_values_source '
                f'has an unknown value of {values_source}'
            )

        # end if

        return res
    # end _prepare_invoice_line
# end StockPickingPackagePreparationLine
