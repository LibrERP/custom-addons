# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
#

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ResCompany(models.Model):
    _inherit = 'res.company'

    number_of_processes = fields.Integer(
        string='Numero di processi per la fatturazione',
    )

