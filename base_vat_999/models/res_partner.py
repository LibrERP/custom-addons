# © 2024 Andrei Levin <andrei.levin@codebeex.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import models


class ResPartner(models.Model):
    _inherit = "res.partner"

    def check_vat_de(self, vat):
        '''
        Check Germany VAT number.
        '''

        if vat == '999999999':
            return True
        else:
            import stdnum.de.vat
            return stdnum.de.vat.is_valid(vat)
