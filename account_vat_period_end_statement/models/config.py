# Copyright 2015 Alessandro Camilli <a.camilli@openforce.it>
# Copyright 2020 Odoo Community Association (OCA) <https://odoo-community.org>
#
#
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, fields


class ResCompany(models.Model):
    _inherit = 'res.company'

    of_account_end_vat_statement_interest = fields.Boolean(
        'Interest on End Vat Statement',
        help="Apply interest on end vat statement")
    of_account_end_vat_statement_interest_percent = fields.Float(
        'Interest on End Vat Statement - %',
        help="Apply interest on end vat statement")
    of_account_end_vat_statement_interest_account_id = fields.Many2one(
        'account.account', 'Interest on End Vat Statement - Account',
        help="Apply interest on end vat statement")
