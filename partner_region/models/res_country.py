# © 2020-2023 Fabio Colognesi - Didotech srl
# © 2024-2026 Fabio Colognesi - Codebeex srl (www.codebeex.com)
#
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# noinspection PyStatementEffect

from odoo import fields, models


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
                                         'res_country_region_country_group_rel',
                                         'region_id',
                                         'country_group_id',
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
                                  'res_country_region_country_group_rel',
                                  'country_group_id',
                                  'region_id',
                                  string='Regions aggregated',
                                  index=True)


class CountryState(models.Model):
    _inherit = 'res.country.state'

    image = fields.Binary(attachment=True)
    region_id = fields.Many2one('res.country.region', string='Region',
                                index=True)
