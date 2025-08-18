# -*- encoding: utf-8 -*-
##############################################################################
#
#    Oddo Addons Module, Open Source   
#    Copyright (C) 2024-2025 Codebeex srl (<http://www.codebeex.com>). All Rights Reserved
#
#    Created on: 2025-08-14
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

from odoo import api, models, fields, _
from odoo.exceptions import UserError


class Partner(models.Model):
    _inherit = "res.partner"

    @api.model
    def get_calendar(self, year=None):
        """
            Gets work calendar for this partner using country (and year or current).
        """
        if self and not self.country_id:
            raise UserError(_('Please, set country for partner "%s".') % type(self.name))
        calendar = self.env['res.calendar'].getcalendar(self, year=year)
        return calendar
    
    @api.model
    def is_working_day(self, this_date):
        """
            Checks if this_date is a working day for this partner. 
        """
        ret = False
        calendar = self.get_calendar()
        if calendar:
            ret = calendar.is_working_day(this_date)
        return ret

    @api.model
    def next_working_day(self, this_date, add_days=0):
        """
            Returns next working day this_date adding it add_days, for this partner. 
        """
        ret = this_date
        calendar = self.get_calendar()
        if calendar:
            ret = calendar.add_working_days(this_date, add_days, keep_datetime=True)
        return ret
