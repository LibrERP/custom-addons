# -*- encoding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2020-2023 Didotech srl
#    (<http://www.didotech.com/>).
#
#    Created on : 2023-04-1
#    Author : Fabio Colognesi
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
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

from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    show_timesheet_name = fields.Boolean(
        'Show timesheet names',
        default=False,
        config_parameter='enhance_maintenance.show_timesheet_name',
    )
    show_expense_name = fields.Boolean(
        'Show expense names',
        default=False,
        config_parameter='enhance_maintenance.show_expense_name',
    )
    show_away_name = fields.Boolean(
        'Show away names',
        default=False,
        config_parameter='enhance_maintenance.show_away_name',
    )
