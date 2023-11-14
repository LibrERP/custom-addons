# © 2023 Andrei Levin <andrei.levin@didotech.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import _, api, fields, models
import logging

_logger = logging.getLogger(__name__)


class ProductPricelist(models.Model):
    _inherit = "product.pricelist"

    def update_wishlist(self, website_id=1):
        for count, pricelist in enumerate(self.filtered(lambda p: p.id != 1), start=1):
            if pricelist.item_ids:
                # partners = self.env['res.partner'].search([
                #     ('property_product_pricelist', '=', pricelist.id)
                # ])
                partners = self.env['res.partner'].search([
                    '|',
                    ('pricelist_ids', 'in', pricelist.id),
                    ('parent_id.pricelist_ids', 'in', pricelist.id)
                ])
                for partner in partners:
                    if partner.user_ids and partner.user_ids[0].has_group('base.group_portal'):
                        _logger.info(f"{count} Updating wishlist for Pricelist '{pricelist.name}'")
                        wish_products = self.env['product.wishlist'].search([
                            # ('partner_id', '=', partner.property_product_pricelist.id),
                            ('partner_id', '=', partner.id),
                        ])

                        new_wish_product_templates = set(pricelist.item_ids.product_tmpl_id).difference(wish_products.product_id.product_tmpl_id)
                        for wish in new_wish_product_templates:
                            # create new products
                            if wish.product_variant_id:
                                self.env['product.wishlist'].create({
                                    'partner_id': partner.id,
                                    'product_id': wish.product_variant_id.id,
                                    'pricelist_id': pricelist.id,
                                    'active': True,
                                    'website_id': website_id
                                })
                            else:
                                pass

                        if wish_products:
                            # Update existing products
                            for item in pricelist.item_ids:
                                wish = wish_products.filtered(lambda w: w.product_id.product_tmpl_id.id == item.product_tmpl_id.id)
                                if wish:
                                    wish.pricelist_id = pricelist.id
                                    # wish.price = item.percent_price

                        # delete products not in the pricelist anymore
                        dead_wish_products = set(wish_products.product_id.product_tmpl_id).difference(pricelist.item_ids.product_tmpl_id)
                        dead_wish_products and wish_products.filtered(lambda w: w.product_id.product_tmpl_id in dead_wish_products).unlink()

    def cron_update_wishlist(self, website_id):
        pricelists = self.search([])
        pricelists.update_wishlist(website_id)
