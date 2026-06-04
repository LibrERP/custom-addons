# Copyright 2024 Giuseppe Borruso - Dinamiche Aziendali srl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class AccountPaymentMethodInherit(models.Model):
    _inherit = "account.payment.method"

    pain_version = fields.Selection(
        selection_add=[
            ("CBIBdySDDReq.00.01.00", "CBIBdySDDReq.00.01.00 (CBI SDD Italy)"),
            ("CBIBdySDDReq.00.01.01", "CBIBdySDDReq.00.01.01 (CBI SDD Italy)"),
        ],
    )

    def get_xsd_file_path(self):
        self.ensure_one()
        if self.pain_version in ["CBIBdySDDReq.00.01.00", "CBIBdySDDReq.00.01.01"]:
            path = "l10n_it_sdd_cbi/data/%s.xsd" % self.pain_version
            return path
        return super(AccountPaymentMethodInherit, self).get_xsd_file_path()