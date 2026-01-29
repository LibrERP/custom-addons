# © 2026 Andrei Levin <andrei.levin@codebeex.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from codicefiscale import get_sex, get_birthday, build, control_code

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
import datetime


OMOCODE_MAP = {
    'L': '0', 'M': '1', 'N': '2', 'P': '3', 'Q': '4',
    'R': '5', 'S': '6', 'T': '7', 'U': '8', 'V': '9',
}

OMOCODE_POSITIONS = {6, 7, 9, 10, 12, 13, 14}


def normalize_omocode(cf: str) -> str:
    """
    Normalize a Codice Fiscale by replacing omocode letters with digits.
    Control character (index 15) is recalculated.
    """
    cf = cf.upper()[:-1]
    chars = list(cf)

    for i in OMOCODE_POSITIONS:
        if chars[i] in OMOCODE_MAP:
            chars[i] = OMOCODE_MAP[chars[i]]

    code = "".join(chars)
    return code + control_code(code)


class ResPartner(models.Model):
    _inherit = "res.partner"

    @api.constrains(
        "fiscalcode",
        "company_type",
    )
    def check_fiscalcode(self):
        if super().check_fiscalcode():
            for partner in self:
                if not partner.is_company and not partner.cf_check_personal_data():
                    msg = _("The fiscal code '%s' isn't valid.") % partner.fiscalcode
                    raise ValidationError(msg)

    def cf_check_personal_data(self) -> bool:
        if self.fiscalcode:
            fc = self.fiscalcode

            fc_built = build(
                surname=self.lastname,
                name=self.firstname,
                sex=get_sex(fc),
                birthday=datetime.datetime.strptime(get_birthday(fc), "%d-%m-%y"),  # format: DD/MM/YYYY
                municipality=fc[-5:-1]  # nome comune o codice catastale
            )

            if fc.upper() == fc_built:
                return True
            else:
                if control_code(fc[:-1]) == fc[-1]:
                    return normalize_omocode(fc) == normalize_omocode(fc_built)
                else:
                    return False
        else:
            return True
