# Copyright 2017 Grant Thornton Spain - Ismael Calvo <ismael.calvo@es.gt.com>
# Copyright 2020 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools import config


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.multi
    def _get_version_ids(self):
        for record in self:
            if record.parent_orig_id:
                record.version_ids = self.search([
                    '|', ('parent_orig_id', '=', record.parent_orig_id.id), ('id', '=', record.parent_orig_id.id),
                    '|', ('active', '=', False), ('active', '=', True),
                    ('id', '!=', record.id)
                ])
            else:
                record.version_ids = []

    vat = fields.Char()
    parent_orig_id = fields.Many2one(comodel_name="res.partner", string="Original Partner", required=False, )
    version_ids = fields.One2many(
        comodel_name="res.partner",
        compute="_get_version_ids",
        string="Old Versions", required=False, readonly=True)

    @api.constrains('vat', 'company_id')
    def _check_vat_unique(self):
        for record in self:
            if record.parent_id or not record.vat or record.parent_orig_id:
                continue
            test_condition = (config['test_enable'] and
                              not self.env.context.get('test_vat'))
            if test_condition:
                continue
            if self.env['res.partner'].sudo().with_context(
                active_test=False,
            ).search_count([
                ('parent_id', '=', False),
                ('parent_orig_id', '=', False),
                ('vat', '=', record.vat),
                ('id', '!=', record.id),
                "|",
                ("company_id", "=", False),
                ("company_id", "=", record.company_id.id),
            ]):
                raise ValidationError((_(
                    "The VAT %s already exists in another "
                    "partner."
                ) + " " + _(
                    "NOTE: This partner may be archived."
                )) % record.vat)

    def action_rebranding_copy(self):
        self.ensure_one()

        parent_orig_id = self.parent_orig_id.id or self.id
        new_partner = super().copy({'parent_orig_id': parent_orig_id})

        self.active = False

        for child in self.child_ids:
            child.parent_id = new_partner.id

        for bank in self.bank_ids:
            bank.partner_id = new_partner.id

        # module agreement_legal is installed
        if hasattr(self, 'agreement_ids'):
            for agreement in self.agreement_ids:
                agreement.partner_id = new_partner.id

        # module account_duedates is installed
        if hasattr(self, 'partner_duedates_dr_ids'):
            for due_date in self.partner_duedates_dr_ids:
                due_date.partner_id = new_partner.id

        # module partner_affiliate is installed
        # if hasattr(self, 'affiliate_ids'):
        #     for affiliate in affiliate_ids:
        #         affiliate.parent_id

        # module partner_identification is installed
        if hasattr(self, 'id_numbers'):
            for number in self.id_numbers:
                number.partner_id = new_partner.id

        return {
            'name': self.name,
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'res.partner',
            'res_id': new_partner.id,
            'target': 'current',
            'context': {'form_view_initial_mode': 'edit'}
        }
