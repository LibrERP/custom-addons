# -*- encoding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2020-2020 Didotech srl
#    (<http://www.didotech.com/>).
#
#    Created on : 2020-09-04
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

from workalendar.registry import registry
from datetime import date, datetime, timedelta

from odoo import api, models, fields, _
from odoo.exceptions import ValidationError


def check_in_range(this_value=0, minimum=0, maximum=0):
    """
        Checks if value is on given range
    """
    ret = this_value
    if this_value < minimum:
        ret = minimum
    elif this_value > maximum:
        ret = maximum
    return ret


def check_hour(this_hour=0):
    """
        Checks if if hour is valid value
    """
    return check_in_range(this_hour, maximum=23)


def check_minute(this_minute=0):
    """
        Checks if if minute is valid value
    """
    return check_in_range(this_minute, maximum=59)


class WorkCal(object):
    calendar = None

    def __init__(self, iso_country="", year=0):
        calendar = None
        today = date.today()
        year = year or today.year
        if iso_country:
            CalendarClass = registry.get(iso_country)
            calendar = CalendarClass()
        if calendar and year:
            self.calendar = calendar
            self.calendar.holidays(year)


class Hours(models.Model):
    _name = "res.calendar.intervals"
    _description = "Calendar Time Intervals"
    _order = 'name'

    name = fields.Char(
        string='Time Interval Name', required=True, translate=True,
        help='The full name of the time interval.')
    hour_code = fields.Char(
        string='Time Interval Code',
        help='The day code in two chars. \nYou can use this field for quick search.')
    start_hour = fields.Integer('Starting Hour')
    start_minute = fields.Integer('Starting Minutes')
    end_hour = fields.Integer('Ending Hour')
    end_minute = fields.Integer('Ending Minutes')
    duration = fields.Float(compute='_compute_duration',
                            string='Interval Duration',
                            help='The interval duration expressed in hours.')
    starting = fields.Char('Starting Hour', compute='_compute_duration')
    ending = fields.Char('Ending Hour', compute='_compute_duration')

    @api.multi
    @api.depends('start_hour', 'start_minute', 'end_hour', 'end_minute')
    def _compute_multi_duration(self):
        """
            Evaluation on multiple values
        """
        for interval in self:
            interval._compute_duration()

    @api.onchange('start_hour', 'start_minute', 'end_hour', 'end_minute')
    def _compute_duration(self):
        """
            Computes duration time, starting, ending values
        """
        for interval in self:
            start_hour = check_hour(interval.start_hour)
            end_hour = check_hour(interval.end_hour)
            start_minute = check_minute(interval.start_minute)
            end_minute = check_minute(interval.end_minute)

            h1 = "{:02d}:{:02d}".format(start_hour, start_minute or 0)
            h2 = "{:02d}:{:02d}".format(end_hour, end_minute or 0)
            ending = datetime.strptime(h2, "%H:%M")
            starting = datetime.strptime(h1, "%H:%M")

            if end_hour < start_hour:
                ending += timedelta(days=1)  # Manages ranges ending on next day

            interval.duration = ((ending - starting).total_seconds()) / 3600
            interval.ending = h2
            interval.starting = h1


class Days(models.Model):
    _name = "res.calendar.day"
    _description = "Calendar Days"
    _order = 'day_number'

    name = fields.Char(
        string='Day Name', required=True, translate=True, help='The full name of the day.')
    day_code = fields.Char(
        string='Day Code',
        help='The day code in two chars. \nYou can use this field for quick search.')
    day_number = fields.Integer(
        string='Day Number',
        help='The day number, in the week. \nYou can use this field for quick search.')
    interval_ids = fields.Many2many('res.calendar.intervals', string='Time Intervals')


class Calendar(models.Model):
    _name = "res.calendar"
    _description = "Calendar"

    @api.model
    def GetWorkCalendar(self, partner_id, year=None):
        """
            Gets work calendar for partner country (and year or current)
        """
        calendar = None
        if partner_id and partner_id.country_id:
            iso_country = partner_id.country_id.code
            calendar = WorkCal(iso_country=iso_country, year=year)
        return calendar


class DateInterval(models.Model):
    _name = "res.calendar.date.interval"

    name = fields.Char(required=True, translate=True)
    date_start = fields.Date(string='Start date', required=True)
    date_end = fields.Date(string='End date', required=True)
    type_id = fields.Many2one(
        comodel_name='res.calendar.date.interval.type', string='Type', index=1, required=True,
        ondelete='restrict')
    company_id = fields.Many2one(
        comodel_name='res.company', string='Company', index=1,
    )
    type_name = fields.Char(
        related='type_id.name', readonly=True, store=True, string="Type Name")
    active = fields.Boolean(
        help="The active field allows you to hide the date range without "
             "removing it.", default=True)

    @api.constrains('type_id', 'date_start', 'date_end')
    def _validate_range(self):
        for range in self:
            if range.date_start > range.date_end:
                raise ValidationError(
                    _("%s is not a valid range (%s > %s)") % (
                        range.name, range.date_start, range.date_end))
            if range.type_id.allow_overlap:
                continue
            res = self.env['res.calendar.date.interval'].search(
                [('id', '!=', range.id), ('type_id.id', '=', range.type_id.id), ('date_end', '>=', range.date_start),
                 ('date_start', '<=', range.date_end)])
            if res:
                name = res[0].name
                raise ValidationError(
                    _("%s overlaps %s") % (range.name, name))


class DateIntervalType(models.Model):
    _name = "res.calendar.date.interval.type"

    name = fields.Char(required=True, translate=True)
    allow_overlap = fields.Boolean(
        help="If sets date range of same type must not overlap.",
        default=False)
    active = fields.Boolean(
        help="The active field allows you to hide the date range type "
             "without removing it.", default=True)
    company_id = fields.Many2one(
        comodel_name='res.company', string='Company', index=1,
    )
    date_range_ids = fields.One2many('res.calendar.date.interval', 'type_id', string='Ranges')
    parent_type_id = fields.Many2one(
        comodel_name='res.calendar.date.interval.type',
        index=1)
