# © 2026 Andrei Levin <andrei.levin@codebeex.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class HrHolidaysPublic(models.Model):
    _inherit = "hr.holidays.public"

    @api.model
    @api.returns('hr.holidays.public.line')
    def get_holidays_list(self, year, employee_id=None):
        holiday_lines = super().get_holidays_list(year, employee_id=employee_id)

        if holiday_lines:
            # Delete holidays connected to cities
            holiday_lines = holiday_lines.filtered(lambda row: not row.city_id)

            if employee_id:
                employee = self.env['hr.employee'].browse(employee_id)

                if employee.address_id and employee.address_id.city_holiday_id:
                    holiday_date = employee.address_id.city_holiday_id.date.replace(year=year)

                    city_holiday_lines = self.env['hr.holidays.public.line'].search([
                        ('year_id.year', '=', year),
                        ('date', '=', holiday_date),
                        ('city_id', '=', employee.address_id.city_holiday_id.city_id.id)
                    ])
                    if city_holiday_lines:
                        city_holiday_line = city_holiday_lines[0]
                    else:
                        city_holiday_line = employee.address_id.city_holiday_id.copy(
                            default={
                                'year_id': holiday_lines[0].year_id.id,
                                'date': holiday_date
                            })

                    holiday_lines |= city_holiday_line
        else:
            # raise ValidationError(_("There is no calendar for year {year}").format(year=year))
            pass

        return holiday_lines


class HrHolidaysPublicLine(models.Model):
    _inherit = "hr.holidays.public.line"

    city_id = fields.Many2one(comodel_name='res.city', string='City')
