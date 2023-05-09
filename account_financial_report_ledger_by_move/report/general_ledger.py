# © 2023 fabio.giovannelli@didotech.com  Didotech.com
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api, _


class GeneralLedgerReport(models.TransientModel):
    _inherit = 'report_general_ledger'

    group_by_move = fields.Boolean(
        string='Raggruppato per Registrazione',
    )

    @api.multi
    def compute_data_for_report(self,
                                with_line_details=True,
                                with_partners=True):
        self.ensure_one()
        # calcolo delle linee con tutti i flag impostati
        res = super().compute_data_for_report(with_line_details, with_partners)
        self._cr.commit()
        # se il nuovo flag viene impostato
        # viene alimentata la tabella con i raggruppamenti
        if self.group_by_move:
            self._inject_move_values_from_move_lines()

    def _inject_move_values_from_move_lines(self):
        entries = {}
        move_model = self.env['report_general_ledger_move']
        for account in self.account_ids:
            # print(account)
            if not account.partner_ids:
                entries[account.code] = {}
                if account.move_line_ids:
                    for rep_line in account.move_line_ids:
                        if 'account' not in entries[account.code]:
                            entries[account.code]['account'] = {}
                        if rep_line.entry not in entries[account.code]['account']:
                            cumul_balance = 0
                            entries[account.code]['account'][rep_line.entry] = {}
                            # if rep_line.partner:
                            #     partner_model = self.env['res.partner']
                                # oartner_id = partner_model.search([
                                #     ('name', '=', rep_line.partner),
                                #     (),
                                # ])
                            #     cumul_balance += rep_line.cumul_balance
                            #
                            #     entries[account.code]['account'][rep_line.entry][rep_line.partner] = {
                            #         'entry': rep_line.entry,
                            #         'move_id': rep_line.move_line_id.move_id.id,
                            #         'journal': rep_line.journal,
                            #         'account': rep_line.account,
                            #         'credit': rep_line.credit,
                            #         'debit': rep_line.debit,
                            #         'date': rep_line.date,
                            #         'partner': rep_line.partner,
                            #         'report_account_id': account.id,
                            #         'report_partner_id': False,
                            #         'cumul_balance': cumul_balance
                            #     }
                            # else:
                            cumul_balance += rep_line.cumul_balance

                            entries[account.code]['account'][rep_line.entry] = {
                                'entry': rep_line.entry,
                                'move_id': rep_line.move_line_id.move_id.id,
                                'journal': rep_line.journal,
                                'account': rep_line.account,
                                'credit': rep_line.credit,
                                'debit': rep_line.debit,
                                'date': rep_line.date,
                                'partner': rep_line.partner,
                                'report_account_id': account.id,
                                'report_partner_id': False,
                                'cumul_balance': cumul_balance
                            }

                        else:
                            cumul_balance += rep_line.cumul_balance
                            # if rep_line.partner:
                            #     entries[account.code]['account'][rep_line.entry][rep_line.partner]['credit'] += rep_line.credit
                            #     entries[account.code]['account'][rep_line.entry][rep_line.partner]['debit'] += rep_line.debit
                            #     entries[account.code]['account'][rep_line.entry][rep_line.partner]['cumul_balance'] += cumul_balance
                            # else:
                            entries[account.code]['account'][rep_line.entry]['credit'] += rep_line.credit
                            entries[account.code]['account'][rep_line.entry]['debit'] += rep_line.debit
                            entries[account.code]['account'][rep_line.entry]['cumul_balance'] += cumul_balance
            else:
                entries[account.code] = {}
                for partner in account.partner_ids:
                    if partner.move_line_ids:
                        for rep_line in partner.move_line_ids:
                            if 'partner' not in entries[account.code]:
                                entries[rep_line.account]['partner'] = {}
                            if rep_line.partner not in entries[account.code]['partner']:
                                cumul_balance = 0
                                entries[account.code]['partner'][rep_line.partner] = {}
                            if rep_line.entry not in entries[rep_line.account]['partner'][rep_line.partner]:
                                cumul_balance += rep_line.cumul_balance
                                entries[account.code]['partner'][rep_line.partner][rep_line.entry] = {}
                                entries[account.code]['partner'][rep_line.partner][rep_line.entry] = {
                                    'entry': rep_line.entry,
                                    'move_id': rep_line.move_line_id.move_id.id,
                                    'journal': rep_line.journal,
                                    'account': rep_line.account,
                                    'credit': rep_line.credit,
                                    'debit': rep_line.debit,
                                    'date': rep_line.date,
                                    'partner': rep_line.partner,
                                    'report_account_id': False,
                                    'report_partner_id': partner.id,
                                    'cumul_balance': cumul_balance
                                }

                                # entries[rep_line.account] = {}
                            else:
                                cumul_balance += rep_line.cumul_balance
                                entries[account.code]['partner'][rep_line.partner][rep_line.entry][
                                    'credit'] += rep_line.credit
                                entries[account.code]['partner'][rep_line.partner][rep_line.entry][
                                    'debit'] += rep_line.debit
                                entries[account.code]['partner'][rep_line.partner][rep_line.entry][
                                    'cumul_balance'] = cumul_balance

        # print("len(entries)")
        # print(len(entries))
        for k, line in entries.items():
            vals = {}
            if 'account' in line:
                # print(list(line['account'].values()))
                data_account = list(line['account'].values())
                for ent in data_account:
                    vals = {
                        'report_account_id': ent['report_account_id'],
                        'report_partner_id': ent['report_partner_id'],
                        'move_id': ent['move_id'],
                        'date': ent['date'],
                        'entry': ent['entry'],
                        'journal': ent['journal'],
                        'account': ent['account'],
                        'taxes_description': '',
                        'partner': ent['partner'],
                        'label': '',
                        'cost_center': '',
                        'tags': '',
                        'debit': ent['debit'],
                        'credit': ent['credit'],
                        'cumul_balance': ent['cumul_balance'],
                        'currency_id': False,
                        'amount_currency': 0.0
                    }
                    try:
                        move_model.create(vals)
                    except Exception as e:
                        print(vals)
                        print(e)
            elif 'partner' in line:
                # print(list(line['partner'].values()))
                tdata = list(line['partner'].values())
                data_partner = []
                for el in tdata:
                    for kv, valuee in el.items():
                        data_partner.append(valuee)
                for ent in data_partner:
                    # print(ent)
                    vals = {
                        'report_account_id': ent['report_account_id'],
                        'report_partner_id': ent['report_partner_id'],
                        'move_id': ent['move_id'],
                        'date': ent['date'],
                        'entry': ent['entry'],
                        'journal': ent['journal'],
                        'account': ent['account'],
                        'taxes_description': '',
                        'partner': ent['partner'],
                        'label': '',
                        'cost_center': '',
                        'tags': '',
                        'debit': ent['debit'],
                        'credit': ent['credit'],
                        'cumul_balance': ent['cumul_balance'],
                        'currency_id': False,
                        'amount_currency': 0.0
                    }
                    try:
                        move_model.create(vals)
                    except Exception as e:
                        print(vals)
                        print(e)
            else:
                continue
        print('finito')


class GeneralLedgerReportMove(models.TransientModel):

    _name = 'report_general_ledger_move'
    _inherit = 'account_financial_report_abstract'

    report_account_id = fields.Many2one(
        comodel_name='report_general_ledger_account',
        ondelete='cascade',
        # index=True
    )
    report_partner_id = fields.Many2one(
        comodel_name='report_general_ledger_partner',
        ondelete='cascade',
        # index=True
    )

    # Data fields, used to keep link with real object
    move_id = fields.Many2one('account.move')

    # Data fields, used for report display
    date = fields.Date()
    entry = fields.Char()
    journal = fields.Char()
    account = fields.Char()
    taxes_description = fields.Char()
    partner = fields.Char()
    label = fields.Char()
    cost_center = fields.Char()
    tags = fields.Char()
    matching_number = fields.Char()
    debit = fields.Float(digits=(16, 2))
    credit = fields.Float(digits=(16, 2))
    cumul_balance = fields.Float(digits=(16, 2))
    currency_id = fields.Many2one('res.currency')
    amount_currency = fields.Float(digits=(16, 2))


class GeneralLedgerReportAccount(models.TransientModel):

    _inherit = 'report_general_ledger_account'

    # Data fields, used to browse report data
    move_ids = fields.One2many(
        comodel_name='report_general_ledger_move',
        inverse_name='report_account_id'
    )


class GeneralLedgerReportPartner(models.TransientModel):

    _inherit = 'report_general_ledger_partner'

    # Data fields, used to browse report data
    move_ids = fields.One2many(
        comodel_name='report_general_ledger_move',
        inverse_name='report_partner_id'
    )

