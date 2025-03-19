# © 2025 Andrei Levin <andrei.levin@codebeex.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = "res.partner"

    @api.constrains('rea_office', 'rea_code', 'company_id')
    def constrain_rea_code(self):
        for partner in self:
            if partner.parent_id or not partner.rea_office or not partner.rea_code or partner.parent_orig_id:
                continue
            rea_domain = [
                ('rea_office', '=', partner.rea_office.id),
                ('rea_code', '=', partner.rea_code),
                ('company_id', '=', partner.company_id.id),
                ('id', '!=', partner.id),
            ]
            other_rea_partners = self.search(rea_domain)
            if other_rea_partners:
                raise ValidationError(_(
                    "The REA Code and Office Province must "
                    "be unique per company.\n"
                    "Please edit '{this_partner}' "
                    "or '{other_partners}' and try again.")
                    .format(
                        this_partner=partner.display_name,
                        other_partners=', '.join(
                            other_rea_partners.mapped('display_name'))
                ))
