# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2014 Andrea Cometa - Perito informatico
#    All Rights Reserved
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from odoo import models, fields, _
from odoo.exceptions import UserError


class IrSequenceRecovery(models.Model):
    _name = "ir.sequence.recovery"
    _description = "ir.sequence.recovery"

    active = fields.Boolean('Active')
    name = fields.Char('Class Name', size=32)
    sequence_id = fields.Many2one('ir.sequence', 'Sequence')
    sequence = fields.Char('Sequence Number', size=32)
    date = fields.Date('Date')
    create_uid = fields.Many2one('res.users', 'Creation User')
    write_uid = fields.Many2one('res.users', 'Deactivate User')

    _defaults = {
        'date': fields.Date.context_today,
        'active': True
    }

    _order = "date, sequence asc, name"

    def set(self, ids, class_name, sequence_field='name',
            sequence_code='', sequence_id=False):
        # ----- init
        class_model = self.env[class_name]
        recovery_ids = []
        # ----- Extract the sequence id if it's not passed
        seq_id = sequence_id
        if sequence_code and not sequence_id:
            sequence_code_ids = self.env['ir.sequence'].search([('name', '=', sequence_code)])
            if sequence_code_ids:
                seq_id = sequence_code_ids[0]
        # ----- For each record deleted save the parameters
        for o in class_model.browse(ids):
            sequence = o[sequence_field]
            if sequence:
                vals = {
                    'name': class_name,
                    'sequence': sequence,
                    'sequence_id': seq_id,
                    'active': True
                }
                list_ids = self.search(
                    [('name', '=', class_name),
                     ('sequence', '=', sequence), ('sequence_id', '=', seq_id)])
                if list_ids:
                    recovery_id = list_ids[0]
                else:
                    recovery_id = self.create(vals)
                recovery_ids.append(recovery_id.id)
        return recovery_ids


class IrSequence(models.Model):
    _name = "ir.sequence"
    _inherit = "ir.sequence"

    def next_by_id(self, sequence_id=None):
        # import pdb; pdb.set_trace()
        if sequence_id is None:
            return super(IrSequence, self).next_by_id()
        recovery_model = self.env['ir.sequence.recovery']
        recovery_ids = recovery_model.search([('sequence_id', '=', sequence_id),
                                              ('active', '=', True)],
                                             order='sequence ASC',
                                             limit=1)
        if recovery_ids:
            # ----- If found it, it recoveries the sequence and return it
            recovery_id = recovery_ids[0]
            sequence = recovery_id.sequence
            recovery_id.write({'active': False})
        else:
            sequence = super(IrSequence, self).next_by_id()
        return sequence

    def next_by_code(self, sequence_code):
        # import pdb; pdb.set_trace()
        recovery_model = self.env['ir.sequence.recovery']
        recovery_ids = recovery_model.search([('name', '=', sequence_code),
                                              ('active', '=', True)])
        if recovery_ids:
            # ----- If found it, it recoveries the sequence and return it
            recovery_id = recovery_ids[0]
            sequence = recovery_id.sequence
            recovery_id.write({'active': False})
        else:
            sequence = super(IrSequence, self).next_by_code(sequence_code)
        return sequence

    def reset_nogap(self, number_reset):
        if self.use_date_range:
            dt = fields.Date.today()
            year = fields.Date.from_string(dt).strftime('%Y')
            date_from = '{}-01-01'.format(year)
            date_to = '{}-12-31'.format(year)
            table = 'ir_sequence_date_range'
            query = "SELECT number_next FROM %s WHERE id=%s " \
                    " AND date_from >= '%s'" \
                    " AND date_from <= '%s'" \
                    "FOR UPDATE NOWAIT"
            self._cr.execute(query % (table, self.id, date_from, date_to))
            self._cr.execute("UPDATE %s SET number_next=%s WHERE id=%s "
                             " AND date_from >= '%s'"
                             " AND date_from <= '%s'"
                             % (table, number_reset, self.id, date_from,
                                date_to))
        else:
            table = 'ir_sequence'
            query = "SELECT number_next FROM %s WHERE id=%s FOR UPDATE NOWAIT"
            self._cr.execute(query % (table, self.id))
            self._cr.execute("UPDATE %s SET number_next=%s WHERE id=%s "
                             % (table, number_reset, self.id))

        self.invalidate_cache(['number_next'], [self.id])

    def alter_sequence(self, seq_name, number_increment=None, number_next=None):
        """ Alter a PostreSQL sequence. """
        if number_increment == 0:
            raise UserError(_("Step must not be zero."))
        query = "SELECT relname FROM pg_class WHERE relkind=%s AND relname=%s"
        self._cr.execute(query, ('S', seq_name))
        if not self._cr.fetchone():
            return
        statement = "ALTER SEQUENCE %s" % (seq_name, )
        if number_increment is not None:
            statement += " INCREMENT BY %d" % (number_increment, )
        if number_next is not None:
            statement += " RESTART WITH %d" % (number_next, )
        self._cr.execute(statement)

