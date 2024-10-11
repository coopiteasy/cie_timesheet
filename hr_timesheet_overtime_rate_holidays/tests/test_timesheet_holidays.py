# SPDX-FileCopyrightText: 2024 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later


from datetime import datetime

from dateutil.relativedelta import relativedelta

from odoo.addons.hr_timesheet.tests.test_timesheet import TestCommonTimesheet


class TestTimesheetHolidays(TestCommonTimesheet):
    def setUp(self):
        super().setUp()

        self.leave_start_datetime = datetime(2018, 2, 5, 7, 0, 0, 0)  # this is monday
        self.leave_end_datetime = self.leave_start_datetime + relativedelta(days=3)

        self.internal_project = self.env.user.company_id.leave_timesheet_project_id
        self.internal_task_leaves = self.env.user.company_id.leave_timesheet_task_id

        self.hr_leave_type = self.env["hr.leave.type"].create(
            {
                "name": "Leave Type",
                "allocation_type": "no",
                "validity_start": self.leave_start_datetime,
                "timesheet_generate": True,
                "timesheet_project_id": self.internal_project.id,
                "timesheet_task_id": self.internal_task_leaves.id,
            }
        )

        # I'm not sure what this record does in this context.
        self.overtime = self.env["resource.overtime"].create({"name": "test"})
        self.rate = self.env["resource.overtime.rate"].create(
            {
                "name": "test",
                "dayofweek": "0",  # Monday
                "rate": 2.0,
                "overtime_id": self.overtime.id,
            }
        )

        # This is necessary because hr_timesheet_overtime depends on
        # resource_work_time_from_contracts.
        self.env["hr.contract"].create(
            {
                "name": "test",
                "employee_id": self.empl_employee.id,
                "wage": 0.0,
                "resource_calendar_id": self.empl_employee.resource_calendar_id.id,
                "date_start": "2017-01-01",
            }
        )

    def test_unit_amount(self):
        number_of_days = (self.leave_end_datetime - self.leave_start_datetime).days
        holiday = (
            self.env["hr.leave"]
            .sudo(self.user_employee.id)
            .create(
                {
                    "name": "Leave 1",
                    "employee_id": self.empl_employee.id,
                    "holiday_type": "employee",
                    "holiday_status_id": self.hr_leave_type.id,
                    "date_from": self.leave_start_datetime,
                    "date_to": self.leave_end_datetime,
                    "number_of_days": number_of_days,
                }
            )
        )
        holiday.sudo().action_validate()

        # This is the important bit. All the above is really annoying Odoo
        # testing scaffolding.
        analytic_lines = self.env["account.analytic.line"].search(
            [
                ("date", ">=", self.leave_start_datetime.date()),
                ("date", "<=", self.leave_end_datetime.date()),
            ]
        )
        self.assertEqual(len(analytic_lines), 3)
        for line in analytic_lines:
            self.assertAlmostEqual(line.unit_amount, 8.0)
