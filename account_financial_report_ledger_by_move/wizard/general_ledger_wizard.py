
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from odoo import api, fields, models, _
from odoo.tools.safe_eval import safe_eval
from odoo.tools import pycompat


class GeneralLedgerReportWizard(models.TransientModel):
    """General ledger report wizard."""
    _inherit = 'general.ledger.report.wizard'
    _description = "General Ledger Report Wizard"

    group_by_move = fields.Boolean(
        string='Raggruppato per Registrazione',
    )

    @api.multi
    def button_export_html(self):
        self.ensure_one()
        action = self.env.ref(
            'account_financial_report.action_report_general_ledger')
        action_data = action.read()[0]
        context1 = action_data.get('context', {})
        if isinstance(context1, pycompat.string_types):
            context1 = safe_eval(context1)
        model = self.env['report_general_ledger']
        report = model.create(self._prepare_report_general_ledger())
        report.compute_data_for_report()
        context1['active_id'] = report.id
        context1['active_ids'] = report.ids
        action_data['context'] = context1
        return action_data

    @api.multi
    def button_export_pdf(self):
        self.ensure_one()
        report_type = 'qweb-pdf'
        return self._export(report_type)

    @api.multi
    def button_export_xlsx(self):
        self.ensure_one()
        report_type = 'xlsx'
        return self._export(report_type)

    def _prepare_report_general_ledger(self):
        res = super()._prepare_report_general_ledger()
        res['group_by_move'] = self.group_by_move
        return res

    def _export(self, report_type):
        """Default export is PDF."""
        model = self.env['report_general_ledger']
        report = model.create(self._prepare_report_general_ledger())
        report.compute_data_for_report()
        return report.print_report(report_type)
