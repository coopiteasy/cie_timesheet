# Copyright 2020 Coop IT Easy SC
#   - Vincent Van Rossem <vincent@coopiteasy.be>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import logging
from datetime import date, timedelta

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class HrTimesheetSheet(models.Model):
    _inherit = "hr_timesheet.sheet"

    active = fields.Boolean(default=True)
    # Numeric fields
    daily_working_time = fields.Float(
        "Daily Working Hours",
        related="employee_id.current_day_working_time",
        help="Hours to work for the current day",
    )
    working_time = fields.Float(
        "Working Hours",
        compute="_compute_working_time",
        help="Hours to work for the timesheet period",
        store=True,
    )
    daily_overtime = fields.Float(
        compute="_compute_daily_overtime",
        help="Overtime for the current day",
    )
    timesheet_overtime = fields.Float(
        compute="_compute_timesheet_overtime",
        help="Overtime for this timesheet period",
        store=True,
    )
    timesheet_overtime_trimmed = fields.Float(
        compute="_compute_timesheet_overtime_trimmed",
        help="Overtime for this timesheet period, from the employee's start date until"
        " today",
        store=True,
    )
    total_overtime = fields.Float(
        related="employee_id.total_overtime",
        help="Overtime total since employee's overtime start date",
    )

    def get_worked_time(self, start_date, end_date=None):
        """
        Get total of worked hours from account analytic lines
        for a given date range
        @param start_date: date
        @param end_date: date
        @return: total of worked hours
        """
        self.ensure_one()
        if end_date is None:
            end_date = start_date
        aal = self.env["account.analytic.line"].search(
            [
                ("sheet_id", "=", self.id),
                ("date", ">=", start_date),
                ("date", "<=", end_date),
            ]
        )
        return sum(line.unit_amount for line in aal)

    @api.depends(
        "active",
        "date_start",
        "date_end",
        "employee_id",
        "employee_id.contract_ids",
        "employee_id.contract_ids.date_start",
        "employee_id.contract_ids.date_end",
        "employee_id.contract_ids.resource_calendar_id",
        "employee_id.contract_ids.resource_calendar_id.attendance_ids",
        "employee_id.contract_ids.resource_calendar_id.attendance_ids.dayofweek",
        "employee_id.contract_ids.resource_calendar_id.attendance_ids.hour_from",
        "employee_id.contract_ids.resource_calendar_id.attendance_ids.hour_to",
        "employee_id.resource_calendar_id",
        "employee_id.resource_calendar_id.attendance_ids",
        "employee_id.resource_calendar_id.attendance_ids.dayofweek",
        "employee_id.resource_calendar_id.attendance_ids.hour_from",
        "employee_id.resource_calendar_id.attendance_ids.hour_to",
    )
    def _compute_working_time(self):
        for sheet in self:
            sheet.working_time = sheet.employee_id.get_working_time(
                sheet.date_start, sheet.date_end
            )

    def _compute_daily_overtime(self):
        """
        Computes overtime for the current day
        """
        current_day = date.today()
        for sheet in self:
            working_time = sheet.employee_id.get_working_time(current_day)
            worked_time = sheet.get_worked_time(current_day)
            sheet.daily_overtime = worked_time - working_time

    @api.depends("total_time", "working_time")
    def _compute_timesheet_overtime(self):
        for sheet in self:
            sheet.timesheet_overtime = sheet.total_time - sheet.working_time

    @api.depends(
        "active",
        "date_start",
        "date_end",
        "company_id.today",
        "employee_id",
        "employee_id.contract_ids",
        "employee_id.contract_ids.date_end",
        "employee_id.contract_ids.date_start",
        "employee_id.contract_ids.resource_calendar_id",
        "employee_id.contract_ids.resource_calendar_id.attendance_ids",
        "employee_id.contract_ids.resource_calendar_id.attendance_ids.dayofweek",
        "employee_id.contract_ids.resource_calendar_id.attendance_ids.hour_from",
        "employee_id.contract_ids.resource_calendar_id.attendance_ids.hour_to",
        "employee_id.overtime_start_date",
        "employee_id.resource_calendar_id",
        "employee_id.resource_calendar_id.attendance_ids",
        "employee_id.resource_calendar_id.attendance_ids.dayofweek",
        "employee_id.resource_calendar_id.attendance_ids.hour_from",
        "employee_id.resource_calendar_id.attendance_ids.hour_to",
        "timesheet_ids.unit_amount",
    )
    def _compute_timesheet_overtime_trimmed(self):
        """
        Computes overtime for the timesheet period
        (from the start date (included) to the current date (not included))
        """
        current_day = date.today()
        for sheet in self:
            employee = sheet.employee_id
            start_date = sheet.date_start
            end_date = sheet.date_end
            if current_day < start_date or employee.overtime_start_date > end_date:
                sheet.timesheet_overtime_trimmed = 0.0
                continue
            if employee.overtime_start_date > start_date:
                start_date = employee.overtime_start_date
            if current_day <= end_date:
                end_date = current_day - timedelta(days=1)

            working_time = employee.get_working_time(start_date, end_date)
            worked_time = sheet.get_worked_time(start_date, end_date)
            sheet.timesheet_overtime_trimmed = worked_time - working_time
