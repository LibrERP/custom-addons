# © 2022 Andrei Levin <andrei.levin@didotech.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import api, fields, models


class SaleOrder (models.Model):
    _inherit = 'sale.order'

    @api.onchange('partner_shipping_id')
    def set_cig_cup(self):
        if self.partner_shipping_id and (self.partner_shipping_id.cig or self.partner_shipping_id.cup):
            document = self.related_documents.filtered(lambda doc: doc.cig or doc.cup)
            if not document or (document and document.cig != self.partner_shipping_id.cig or document.cup != self.partner_shipping_id.cup):
                # delete existent cig and cup line if any
                if document:
                    doc_to_unlink_id = document.id
                else:
                    doc_to_unlink_id = False

                self.related_documents = [
                    (0, False, {
                        'type': 'agreement',
                        'name': self.partner_shipping_id.cig or self.partner_shipping_id.cup,
                        'cig': self.partner_shipping_id.cig,
                        'cup': self.partner_shipping_id.cup
                    })
                ]
                if doc_to_unlink_id:
                    self.related_documents += [(2, doc_to_unlink_id)]
        elif self.partner_shipping_id:
            # delete existent cig and cup line if any
            document = self.related_documents.filtered(lambda doc: doc.cig or doc.cup)
            if document:
                doc_to_unlink_id = document.id
            else:
                doc_to_unlink_id = False
            if doc_to_unlink_id:
                self.related_documents = [(2, doc_to_unlink_id)]
