# Copyright 2020 Coop IT Easy SC
#   - Vincent Van Rossem <vincent@coopiteasy.be>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from datetime import date, datetime, timedelta

from pytz import timezone

from odoo import api, fields, models


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    # Numeric fields
    current_day_working_time = fields.Float(
        "Current Day Working Hours",
        compute="_compute_current_day_working_time",
        help="Hours to work for the current day",
    )
    initial_overtime = fields.Float(
        string="Initial Overtime",
        default=0.0,
        help="Initial Overtime to start Overtime Start Date with",
    )
    total_overtime = fields.Float(
        string="Total Overtime",
        compute="_compute_total_overtime",
        help="Total overtime since Overtime Start Date",
        store=True,
    )
    timesheet_sheet_ids = fields.One2many(
        comodel_name="hr_timesheet.sheet",
        inverse_name="employee_id",
        string="Timesheet sheets",
    )

    # Date fields
    overtime_start_date = fields.Date(
        string="Overtime Start Date",
        required=True,
        default=date.today().replace(month=1, day=1),
        help="Overtime Start Date to compute overtime",
    )

    @api.multi
    def get_working_time(self, start_date, end_date=None):
        """
        Get the working hours for a given date range according to the
        employee's contracts
        @param start_date: date
        @param end_date: date
        @return: total of working hours
        """
        self.ensure_one()
        if end_date is None:
            end_date = start_date
        tz = timezone(self.tz)
        start_dt = tz.localize(
            datetime(start_date.year, start_date.month, start_date.day)
        )
        end_dt = tz.localize(
            datetime(end_date.year, end_date.month, end_date.day)
        ) + timedelta(days=1)
        work_time_per_day = self.list_normal_work_time_per_day(start_dt, end_dt)
        # .list_normal_work_time_per_day() returns a list of tuples:
        # (date, work time)
        return sum(work_time[1] for work_time in work_time_per_day)

    @api.multi
    def _compute_current_day_working_time(self):
        """
        Computes working hours for the current day according to the employee's
        contracts.
        """
        current_day = date.today()
        for employee in self:
            employee.current_day_working_time = employee.get_working_time(current_day)

    @api.multi
    @api.depends(
        "initial_overtime",
        "overtime_start_date",
        "timesheet_sheet_ids.timesheet_overtime_trimmed",
    )
    def _compute_total_overtime(self):
        """
        Computes total overtime since employee's overtime start date
        """
        for employee in self:
            sheets = self.env["hr_timesheet.sheet"].search(
                [
                    ("employee_id", "=", employee.id),
                    ("date_end", ">=", employee.overtime_start_date),
                ]
            )
            overtime = sum(sheet.timesheet_overtime_trimmed for sheet in sheets)
            employee.total_overtime = employee.initial_overtime + overtime
