# -*- encoding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2022 Didotech srl
#    (<http://www.didotech.com/>).
#
#    Created on : 2022-10-28
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

from odoo import api, models, fields, _
from odoo.exceptions import UserError


class ResPartner(models.Model):
    _inherit = "res.partner"

    @api.onchange('zip')
    def on_change_zip(self):
        zip_code = self.zip
        if zip_code and len(zip_code) > 3:
            res_city = self.env['res.city']
            city_ids = res_city.search([('zip_ids.name', '=ilike', zip_code)])
            if not city_ids:
                city_ids = res_city.search([('zip_ids.name', 'ilike', zip_code[:3])])
                city_ids = city_ids[0] if city_ids else res_city

            if len(city_ids) == 1:
                self.state_id = city_ids.state_id
                self.city = city_ids.name
                self.country_id = self.state_id.country_id
                self.zip = zip_code

    @api.onchange('city')
    def on_change_city(self):
        if self.city:
            city_ids = self.env['res.city'].search([('name', '=ilike', self.city.title())])
            if city_ids:
                city_row = city_ids[0] if city_ids else res_city
                if not self.zip:
                    self.zip = city_row.zip_ids[0].name

                self.state_id = city_row.state_id
                self.city = city_row.name.title()
                self.country_id = self.state_id.country_id

    @api.onchange('state_id')
    def on_change_state_id(self):
        if self.state_id:
            self.country_id = self.state_id.country_id
