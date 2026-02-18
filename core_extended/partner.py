# -*- encoding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2020-2021 Didotech srl
#    (<http://www.didotech.com/>).
#
#    Created on : 2021-01-09
#    Author : Fabio Colognesi
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from odoo import models, fields, api, _

EUROPE = {
            'AT': 'Austria',
            'BE': 'Belgio',
            'BG': 'Bulgaria',
            'CY': 'Cipro',
            'HR': 'Croazia',
            'DK': 'Danimarca',
            'EE': 'Estonia',
            'FI': 'Finlandia',
            'FR': 'Francia',
            'DE': 'Germania',
            # 'GB': 'Gran Bretagna',
            'EL': 'Grecia',
            'IE': 'Irlanda',
            'IT': 'Italia',
            'LV': 'Lettonia',
            'LT': 'Lituania',
            'LU': 'Lussemburgo',
            'MT': 'Malta',
            'NL': 'Olanda',
            'PL': 'Polonia',
            'PT': 'Portogallo',
            'CZ': 'Repubblica Ceca',
            'SK': 'Repubblica Slovacca',
            'RO': 'Romania',
            'SI': 'Slovenia',
            'ES': 'Spagna',
            'SE': 'Svezia',
            'HU': 'Ungheria',
        }


class Partner(models.Model):
    _inherit = "res.partner"

    def get_country_kind(self):
        """
            Check if partner country is national, in EU or foreigner at all
            Returns:
                      0 if partner country is the same as res.company (or no country set)
                     -1 if partner country is out of EUROPE dictionary
                      1 if partner country is into   EUROPE dictionary
        """
        ret = 0
        if self.env.user.company_id and self.env.user.company_id.partner_id:
            if self.env.user.company_id.partner_id.country_id and self.country_id:
                company_country_code = self.env.user.company_id.partner_id.country_id.code.upper()
                country_code = self.country_id.code.upper()
                if not(country_code == company_country_code):
                    if country_code in EUROPE:
                        ret = 1
                    else:
                        ret = -1
        return ret

    def get_country_kind_as_char(self):
        """
            Check if partner country is national, in EU or foreigner at all
            Returns:
                    "0"  if partner country is the same as res.company (or no country set)
                    "-1" if partner country is out of EUROPE dictionary
                    '1"  if partner country is into   EUROPE dictionary
            Useful for fields.Selection in which value is char type.
        """
        return "{}".format(self.get_country_kind())
