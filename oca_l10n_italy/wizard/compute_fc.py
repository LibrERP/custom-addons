# © 2020 Didotech srl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging
_logger = logging.getLogger(__name__)

try:
    from codicefiscale import build

except ImportError:
    _logger.warning(
        "codicefiscale library not found. "
        "If you plan to use it, please install the codicefiscale library"
        " from https://pypi.python.org/pypi/codicefiscale")


class WizardComputeFc(models.TransientModel):
    _inherit = 'wizard.compute.fc'

    born_abroad = fields.Boolean(string="Born abroad")
    country_id = fields.Many2one(comodel_name="res.country", string="The country of birth", required=False, domain=[
        ('zcode', '!=', False)
    ])
    birth_city = fields.Many2one('res.city.it.code.distinct',
                                 required=False,
                                 string="City of birth")
    birth_province = fields.Many2one('res.country.state',
                                     required=False,
                                     string="Province")

    @api.multi
    def compute_fc(self):
        active_id = self._context.get('active_id')
        partner = self.env['res.partner'].browse(active_id)
        for f in self:
            if f.fiscalcode_surname and f.fiscalcode_firstname and f.birth_date and f.sex:
                if f.born_abroad and f.country_id:
                    nat_code = f.country_id.zcode
                else:
                    if f.birth_city:
                        nat_code = self._get_national_code(
                            f.birth_city.name, f.birth_province.code, f.birth_date)
                    else:
                        raise UserError(_('Birth city is missing'))

                if nat_code:
                    c_f = build(f.fiscalcode_surname, f.fiscalcode_firstname,
                                f.birth_date, f.sex, nat_code)
                else:
                    raise UserError(_('National code is missing'))
            else:
                raise UserError(_('One or more fields are missing'))

            if partner.fiscalcode and partner.fiscalcode != c_f:
                raise UserError(_(
                    'Existing fiscal code %(partner_fiscalcode)s is different '
                    'from the computed one (%(compute)s). If you want to use'
                    ' the computed one, remove the existing one' % {
                        'partner_fiscalcode': partner.fiscalcode,
                        'compute': c_f}))
            partner.fiscalcode = c_f
            partner.company_type = 'person'
        return {'type': 'ir.actions.act_window_close'}
