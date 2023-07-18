##############################################################################
#
#    Copyright (C) 2022-2023 Didotech SRL
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import logging

from odoo import api, fields, models, tools, _

_logger = logging.getLogger(__name__)


class PosOrder(models.Model):
    _inherit = 'pos.order'

    @api.model
    def _get_account_move_line_group_data_type_key(self, data_type, values, options={}):
        """
        Return a tuple which will be used as a key for grouping account
        move lines in _create_account_move_line method.
        :param data_type: 'product', 'tax', ....
        :param values: account move line values
        :return: tuple() representing the data_type key
        """
        if data_type == 'product_debit':
            key = (
                'product_debit',
                values['partner_id'],
                (values['product_id'], tuple(values['tax_ids'][0][2]), values['name']),
                values['analytic_account_id'],
                values['debit'] > 0,
                values.get('currency_id'),
            )

            return key
        else:
            result = super()._get_account_move_line_group_data_type_key(data_type, values, options)
            return result
        # end if
    # end _get_account_move_line_group_data_type_key
# end PosOrder
