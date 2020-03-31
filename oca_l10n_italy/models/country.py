# © 2020 Didotech srl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields


class ResCountry(models.Model):
    _inherit = 'res.country'

    zcode = fields.Char(string="FC Code", required=False,  size=4)

    def init(self):
        import csv
        import os

        current_dir = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(current_dir, '../data/res_country_zcode.csv')) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';')

            for row in csv_reader:
                if row[0][0].lower() == 'z':
                    country = self.search([
                        ('code', '=', row[1])
                    ])
                    if country:
                        # country.zcode = row[0]
                        country.write({
                            'zcode': row[0]
                        })
