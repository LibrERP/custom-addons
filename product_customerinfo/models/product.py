from odoo import models, fields, api


class CustomerInfo(models.Model):
    _name = 'product.customerinfo'
    _description = "Client related info"

    name = fields.Many2one(
        'res.partner', 'Customer',
        ondelete='cascade', required=True,
        domain=[('customer', '=', True)],
        help="Product acquirer"
    )
    product_id = fields.Many2one(
        comodel_name="product.product", string="Product Variant", ondelete='cascade',
        help="Product acquirer"
    )
    product_tmpl_id = fields.Many2one(
        comodel_name="product.template", string="Product Template",
        index=True, ondelete='cascade'
    )
    product_code = fields.Char("Code", required=True)
    product_code_type = fields.Selection(string="Code Type", selection=[
        ('ean', 'EAN'),
        ('asin', 'ASIN')
    ], required=True)
    company_id = fields.Many2one(
        'res.company', 'Company',
        default=lambda self: self.env.user.company_id.id, index=1)

    # _sql_constraints = [(
    #     'unique_code',
    #     'unique(code, partner_id, product_id, product_tmpl_id)',
    #     'Code is already set for current product'
    # )]

    @api.model_create_multi
    def create(self, values):
        for values_set in values:
            if 'product_id' in values_set and values_set['product_id']:
                product = self.env['product.product'].browse(values_set['product_id'])
                values_set['product_tmpl_id'] = product.product_tmpl_id.id
        return super().create(values)


class ProductProduct(models.Model):
    _inherit = 'product.product'

    buyer_ids = fields.One2many('product.customerinfo', 'product_id', 'Customers', help="Define buyer info")

    # @api.model_create_multi
    # def create(self, values):
    #
    #     return super().create(values)
    #
    # @api.multi
    # def write(self, values):
    #
    #     return super().write(values)
