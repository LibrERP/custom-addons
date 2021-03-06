# -*- encoding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2020-2020 Didotech srl
#    (<http://www.didotech.com/>).
#
#    Created on : 2020-11-27
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

from odoo import api, fields, models, tools, SUPERUSER_ID, _


class CountryRegion(models.Model):
    _name = 'res.country.region'
    _description = 'Region'
    _order = 'name'

    name = fields.Char(
        string='Country Name', required=True, translate=True,
        help='The full name of the region.')
    code = fields.Char(
        string='Country Code',
        help='The ISO region code follows ISO 3166 rules.')
    image = fields.Binary(attachment=True)
    country_id = fields.Many2one('res.country',
                                 string='National region of',
                                 index=True)
    country_group_ids = fields.Many2many('res.country.group',
                                         'res_country_group_id',
                                         'res_country_region_id',
                                         string='Aggregate of Regions',
                                         index=True)
    state_ids = fields.One2many('res.country.state', 'region_id',
                                string='States/Provinces')


class Country(models.Model):
    _inherit = 'res.country'

    region_ids = fields.One2many('res.country.region', 'country_id',
                                 string='Regions')


class CountryGroup(models.Model):
    _inherit = 'res.country.group'

    region_ids = fields.Many2many('res.country.region',
                                  'res_country_region_id',
                                  'res_country_group_id',
                                  string='Regions aggregated',
                                  index=True)


class CountryState(models.Model):
    _inherit = 'res.country.state'

    image = fields.Binary(attachment=True)
    region_id = fields.Many2one('res.country.region', string='Region',
                                index=True)

