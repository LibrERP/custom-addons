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

    def _get_aeroo_currency(self, record):
        """Get the currency to use in the report for a given record.

        The currency is used if the template of the report is different
        per currency.

        :rtype: res.currency
        """
        return (
            safe_eval(self.aeroo_currency_eval, self._get_aeroo_variable_eval_context(record))
            if self.aeroo_currency_eval else None
        )

    def _get_aeroo_timezone(self, record):
        """Get the timezone to use in the report for a given record.

        :rtype: res.company
        """
        return (
            safe_eval(self.aeroo_tz_eval, self._get_aeroo_variable_eval_context(record))
            if self.aeroo_tz_eval else None
        )

    def _get_aeroo_company(self, record):
        """Get the company to use in the report for a given record.

        The company is used if the template of the report is different
        per company.

        :rtype: res.company
        """
        return (
            safe_eval(self.aeroo_company_eval, self._get_aeroo_variable_eval_context(record))
            if self.aeroo_company_eval else self.env.user.company_id
        )

    def _get_aeroo_country(self, record):
        """Get the country to use in the report for a given record.

        The country is used if the template of the report is different
        per country.

        :rtype: res.country
        """
        return (
            safe_eval(self.aeroo_country_eval, self._get_aeroo_variable_eval_context(record))
            if self.aeroo_country_eval else None
        )

