from dateutil.relativedelta import relativedelta
from dateutil.rrule import DAILY, MONTHLY, WEEKLY, YEARLY, rrule

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class DateRangeGenerator(models.TransientModel):
    _name = 'res.calendar.date.interval.generator'
    _description = 'Date Interval Generator'

    name_prefix = fields.Char('Range name prefix', required=True)
    date_start = fields.Date(strint='Start date', required=True)
    type_id = fields.Many2one(
        comodel_name='res.calendar.date.interval.type', string='Type', required=True,
        ondelete='cascade')
    company_id = fields.Many2one(
        comodel_name='res.company', string='Company')
    unit_of_time = fields.Selection([
        (YEARLY, 'years'),
        (MONTHLY, 'months'),
        (WEEKLY, 'weeks'),
        (DAILY, 'days')], required=True)
    duration_count = fields.Integer('Duration', required=True)
    count = fields.Integer(
        string="Number of ranges to generate", required=True)

    @api.multi
    def _compute_date_ranges(self):
        self.ensure_one()
        vals = rrule(freq=self.unit_of_time, interval=self.duration_count,
                     dtstart=self.date_start,
                     count=self.count + 1)
        vals = list(vals)
        count_digits = len(str(self.count))
        date_intervals = [{"name": '%s%0*d' % (self.name_prefix, count_digits, idx + 1),
                "date_start": dates.date(),
                "date_end": vals[idx + 1].date() - relativedelta(days=1),
                "type_id": self.type_id.id,
                "company_id": self.company_id.id
                } for idx, dates in enumerate(vals[:-1])]
        return date_intervals

    @api.multi
    def action_apply(self):
        date_ranges = self._compute_date_ranges()
        if date_ranges:
            for dr in date_ranges:
                self.env['res.calendar.date.interval'].create(dr)
        return self.env['ir.actions.act_window'].for_xml_id(
            module='extend_calendar', xml_id='res_calendar_date_interval_action')
