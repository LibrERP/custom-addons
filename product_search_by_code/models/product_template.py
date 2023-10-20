# © 2023 Marco Tosato - Didotech srl (www.didotech.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
        """
        If order argument is missing and there is an order_by key
        specified in the context, the value of the order_by isa
        used to sort the search result
        """

        order_from_context = self.env.context.get('order_by', None)
        actual_order = order or order_from_context

        res = super().search(
            args,
            offset=offset,
            limit=limit,
            order=actual_order,
            count=count
        )

        return res
    # end search

# end ProductTemplate
