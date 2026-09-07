# © 2025-2026 Andrei Levin <andrei.levin@codebeex.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import _, api, Command, fields, models


class AccountMove(models.Model):
    _inherit = 'account.move'

    l10n_it_project_contract_code = fields.Char('Codice della commessa o della convenzione', help='2.1.2.5 <CodiceCommessaConvenzione>', size=100)
    l10n_it_narration = fields.Text('Causale', help='2.1.1.11 <Causale>')
    l10n_it_data_type = fields.Char('Tipo dato', help='2.2.1.16.1 <TipoDato>')
    l10n_it_text_ref = fields.Char('Rif. testo', help='2.2.1.16.2 <RiferimentoTesto>')

    def _l10n_it_edi_get_values(self, pdf_values=None):
        values = super()._l10n_it_edi_get_values(pdf_values=pdf_values)

        values['l10n_it_narration'] = self.l10n_it_narration
        values['seller_info']['l10n_it_partner_code'] = values['partner'].l10n_it_partner_code
        values['l10n_it_project_contract_code'] = self.l10n_it_project_contract_code

        return values

    def _l10n_it_edi_add_base_lines_xml_values(self, base_lines_aggregated_values, is_downpayment):
        self.ensure_one()

        super()._l10n_it_edi_add_base_lines_xml_values(
            base_lines_aggregated_values=base_lines_aggregated_values,
            is_downpayment=is_downpayment
        )
        for index, (base_line, aggregated_values) in enumerate(base_lines_aggregated_values, start=1):
            line = base_line['record']
            base_line['it_values']['l10n_it_admin_ref'] = line.l10n_it_admin_ref
            base_line['it_values']['l10n_it_data_type'] = self.l10n_it_data_type
            base_line['it_values']['l10n_it_text_ref'] = self.l10n_it_text_ref


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    l10n_it_admin_ref = fields.Char("Rif. Ammin.", size=20, copy=False, help='2.2.1.15 <RiferimentoAmministrazione>')
