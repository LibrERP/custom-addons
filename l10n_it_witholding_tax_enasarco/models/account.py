# Copyright 2015 Alessandro Camilli (<http://www.openforce.it>)
# Copyright 2018 Lorenzo Battistini - Agile Business Group
# Copyright 2023 Didotech s.r.l. https://www.didotech.com
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api, _
import odoo.addons.decimal_precision as dp
from odoo.exceptions import ValidationError


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    @api.multi
    def action_move_create(self):
        '''
        Split amount withholding tax on account move lines
        '''
        dp_obj = self.env['decimal.precision']
        res = super(AccountInvoice, self).action_move_create()
        for inv in self:
            if inv.withholding_tax_line_ids:
                enasarco = inv.withholding_tax_line_ids.filtered(lambda l: l.withholding_tax_id.wt_types == 'enasarco')
                if enasarco:
                    # if False:
                    amount = enasarco.tax
                    move_vals = {
                        'ref': _('WT %s - %s')
                               % (
                                   enasarco.withholding_tax_id.code,
                                   inv.move_id.name,
                               ),
                        'journal_id': enasarco.withholding_tax_id.journal_id.id,
                        'date': inv.move_id.date,
                        'type': 'entry',
                    }
                    move_lines = []
                    for type in ('partner', 'tax'):
                        ml_vals = {
                            'ref': _('WT %s - %s - %s')
                                   % (
                                       enasarco.withholding_tax_id.code,
                                       inv.partner_id.name,
                                       inv.move_id.name,
                                   ),
                            'name': '%s' % inv.move_id.name,
                            'date': move_vals['date'],
                            'partner_id': inv.partner_id.id,
                        }
                        # Credit/Debit line
                        if type == 'partner':
                            # fornitore in dare
                            ml_vals['account_id'] = inv.account_id.id
                            ml_vals[
                                'withholding_tax_generated_by_move_id'
                            ] = inv.move_id.id
                            if inv.type in [
                                'in_refund',
                                'out_refund',
                            ]:
                                ml_vals['credit'] = abs(amount)
                            else:
                                ml_vals['debit'] = abs(amount)
                        # Authority tax line
                        elif type == 'tax':
                            # conto di debito
                            ml_vals['name'] = '%s - %s' % (
                                enasarco.withholding_tax_id.code,
                                inv.move_id.name,
                            )
                            ml_vals[
                                'withholding_tax_generated_by_move_id'
                            ] = inv.move_id.id

                            if inv.type in [
                                'in_refund',
                                'out_refund',
                            ]:
                                ml_vals['debit'] = abs(amount)
                                ml_vals[
                                    'account_id'
                                ] = enasarco.withholding_tax_id.account_receivable_id.id
                            else:
                                ml_vals['credit'] = abs(amount)
                                ml_vals[
                                    'account_id'
                                ] = enasarco.withholding_tax_id.account_payable_id.id

                        # self.env['account.move.line'].create(move_vals)
                        move_lines.append((0, 0, ml_vals))

                    move_vals['line_ids'] = move_lines
                    move = self.env['account.move'].create(move_vals)
                    move.post()
                    # Save move in the wt move
                    # self.wt_account_move_id = move.id

                    # reconcile tax debit line
                    filter_account_id = inv.account_id
                    tec_line = inv.move_id.line_ids.filtered(
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

        return res
