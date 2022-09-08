# © 2008-2014 Alistek
# © 2016-2018 Savoir-faire Linux
# © 2018 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# © 2022 Didotech srl (https://www.didotech.com)
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl).

from odoo import models, fields, api, tools, _
from odoo.tools.safe_eval import safe_eval


class IrActionsReport(models.Model):
    _inherit = 'ir.actions.report'

    def _get_aeroo_lang(self, record):
        """Get the lang to use in the report for a given record.

        :rtype: res.company
        """
        lang = (
            safe_eval(self.aeroo_lang_eval, self._get_aeroo_variable_eval_context(record))
            if self.aeroo_lang_eval else None
        )
        return lang or 'en_US'

