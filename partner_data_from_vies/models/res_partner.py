# Copyright (C) 2015 Forest and Biomass Romania
# Copyright (C) 2020 OdooERP Romania
# Copyright © 2021 Didotech srl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging

from odoo import _, api, models
# from odoo.exceptions import ValidationError
from .pyvies import Vies

_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = "res.partner"

    def vies_data(self, vat):
        vat = vat.strip().upper()

        try:
            result = Vies().request(vat, bypass_ratelimit=True)
        except Exception as e:
            error = _(e)
            _logger.error(_(u'Error on {vat}: {error}').format(vat=vat, error=error))
            return False

        # Raise error if partner is not listed on Vies
        if hasattr(result, 'company_name') and result.company_name and not result.company_address[:3] == '***':
            address_values = hasattr(result, 'company_address') and result.company_address.split('\n')
            values = {
                'name': result.company_name.title().replace('!', ' ')
            }
            if len(address_values) >= 2:
                values.update({
                    # 'type': 'default',
                    'street': address_values[0].title(),
                    'zip': address_values[1].split(' ')[0].title(),
                    'city': address_values[1][
                            len(address_values[1].split(' ')[0]) + 1:len(address_values[1]) - 3].title()
                })

            if result.country_code:
                country_code = result.country_code
            else:
                # Get country by country code
                country_code, vat_number = self._split_vat(vat)

            country = self.env["res.country"].search([("code", "ilike", country_code)])
            if country:
                values["country_id"] = country[0].id

            # address_value should consist of at least 2 elements
            if country_code == 'IT':

                if address_values == ['SOGGETTO IDENTIFICATO MA NON RESIDENTE IN ITALIA']:
                    _logger.warning(
                        f'Not updating address infos for "{vat}" '
                        'since VIES returned this message '
                        '"SOGGETTO IDENTIFICATO MA NON RESIDENTE IN ITALIA".'
                    )
                elif len(address_values) >= 2:
                    code_state = address_values[1][-2:]
                    state = self.env['res.country.state'].search([
                        ("code", "ilike", code_state),
                        ("country_id", '=', country.id)
                    ])
                    if state:
                        values["state_id"] = state[0].id
                    # end if
                else:
                    _logger.warning(
                        f'Not updating address infos for "{vat}" '
                        f'since VIES returned unsupported data.'
                    )
                # end if

            return values
        else:
            # raise ValidationError(_("The partner is not listed on Vies " "Webservice."))
            return {}

    @api.multi
    def get_vies_data(self):
        self.ensure_one()
        if self.vat:
            return self.vies_data(self.vat)
        else:
            return {}

    @api.onchange("vat")
    def vies_vat_change(self):
        if self.vat:

            result = self.get_vies_data()

            # Check content of the "result" variable before calling update:
            # if and Exception is raised while contacting VIES server the
            # get_vies_data() method returns False
            if result:
                self.update(result)
            # end if
        # end if
    # end vies_vat_change
