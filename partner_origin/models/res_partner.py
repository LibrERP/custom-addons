# © 2022 Andrei Levin <andrei.levin@didotech.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import fields, models, api, _
from odoo.exceptions import Warning


class ResPartner(models.Model):
    _inherit = 'res.partner'

    contact_origin_ids = fields.Many2many('res.partner.contact.origin', string='Contact Origin')

    @api.model
    def create(self, values):
        if values.get('customer') and not values.get('parent_id'):
            if not values.get('contact_origin_ids'):
                # raise Warning(_('Per favore seleziona Provenienza Contatto'))
                raise Warning(_('Please set Contact Origin'))
            elif values.get('contact_origin_ids'):
                origin_ids = [contact[2] for contact in values['contact_origin_ids'] if contact[2]]
                if not origin_ids:
                    raise Warning(_('Please set Contact Origin'))

        return super().create(values)

    def write(self, values):
        for partner in self:
            if partner.customer:
                # When we create a new contact write is called before contact_origin_ids are written
                # so the next line will generate an error
                # if not partner.contact_origin_ids and not values.get('contact_origin_ids'):
                #     raise orm.except_orm(_('Warning'), 'Per favore seleziona Provenienza Contatto')

                if values.get('contact_origin_ids'):
                    origin_ids = [contact[2] for contact in values['contact_origin_ids'] if contact[2]]
                    if not origin_ids:
                        raise Warning(_('Per favore seleziona Provenienza Contatto'))

        return super().write(values)


class ContactOrigin(models.Model):
    _name = 'res.partner.contact.origin'
    description = 'Origin Partner'

    name = fields.Char('Name', required=True, translate=True)
    active = fields.Boolean('Active', help="The active field allows you to hide the category without removing it.",
                            index=True, default=True)

    _order = 'name'
