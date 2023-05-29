# Copyright 2015 Alessandro Camilli (<http://www.openforce.it>)
# Copyright 2018 Lorenzo Battistini - Agile Business Group
# Copyright 2023 Didotech s.r.l. https://www.didotech.com
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class WithholdingTaxMove(models.Model):
    _inherit = 'withholding.tax.move'
    _description = 'Withholding Tax Move'

    def generate_account_move(self):
        wt_st = self.statement_id
        if wt_st.withholding_tax_id.wt_types != 'enasarco':
            if self.wt_account_move_id:
                raise ValidationError(
                    _('Warning! Wt account move already exists: %s')
                    % (self.wt_account_move_id.name)
                )
            # Move - head
            move_vals = {
                'ref': _('WT %s - %s')
                % (
                    self.withholding_tax_id.code,
                    self.credit_debit_line_id.move_id.name,
                ),
                'journal_id': self.withholding_tax_id.journal_id.id,
                'date': self.payment_line_id.move_id.date,
            }
            # Move - lines
            move_lines = []
            for type in ('partner', 'tax'):
                ml_vals = {
                    'ref': _('WT %s - %s - %s')
                    % (
                        self.withholding_tax_id.code,
                        self.partner_id.name,
                        self.credit_debit_line_id.move_id.name,
                    ),
                    'name': '%s' % (self.credit_debit_line_id.move_id.name),
                    'date': move_vals['date'],
                    'partner_id': self.payment_line_id.partner_id.id,
                }
                # Credit/Debit line
                if type == 'partner':
                    ml_vals['account_id'] = self.credit_debit_line_id.account_id.id
                    ml_vals[
                        'withholding_tax_generated_by_move_id'
                    ] = self.payment_line_id.move_id.id
                    if self.payment_line_id.credit:
                        ml_vals['credit'] = abs(self.amount)
                    else:
                        ml_vals['debit'] = abs(self.amount)
                # Authority tax line
                elif type == 'tax':
                    ml_vals['name'] = '%s - %s' % (
                        self.withholding_tax_id.code,
                        self.credit_debit_line_id.move_id.name,
                    )

                    # FIX set this line as move generated to avoid recalculation
                    ml_vals[
                        'withholding_tax_generated_by_move_id'
                    ] = self.payment_line_id.move_id.id

                    if self.payment_line_id.credit:
                        ml_vals['debit'] = abs(self.amount)
                        if self.credit_debit_line_id.invoice_id.type in [
                            'in_refund',
                            'out_refund',
                        ]:
                            ml_vals[
                                'account_id'
                            ] = self.withholding_tax_id.account_payable_id.id
                        else:
                            ml_vals[
                                'account_id'
                            ] = self.withholding_tax_id.account_receivable_id.id
                    else:
                        ml_vals['credit'] = abs(self.amount)
                        if self.credit_debit_line_id.invoice_id.type in [
                            'in_refund',
                            'out_refund',
                        ]:
                            ml_vals[
                                'account_id'
                            ] = self.withholding_tax_id.account_receivable_id.id
                        else:
                            ml_vals[
                                'account_id'
                            ] = self.withholding_tax_id.account_payable_id.id
                # self.env['account.move.line'].create(move_vals)
                move_lines.append((0, 0, ml_vals))

            move_vals['line_ids'] = move_lines
            move = self.env['account.move'].create(move_vals)
            move.post()
            # Save move in the wt move
            self.wt_account_move_id = move.id

            # reconcile tax debit line
            filter_account_id = self.statement_id.invoice_id.account_id
            tec_line = self.statement_id.move_id.line_ids.filtered(
                lambda x: x.account_id == filter_account_id
                and x.line_type == 'debit'
                and x.payment_method.code == 'tax'
            )

            supplier_line = move.line_ids.filtered(
                lambda x: x.account_id == filter_account_id
            )

            if supplier_line and tec_line:
                line_to_rec = self.env['account.move.line']
                line_to_rec += tec_line + supplier_line
                line_to_rec.reconcile()

