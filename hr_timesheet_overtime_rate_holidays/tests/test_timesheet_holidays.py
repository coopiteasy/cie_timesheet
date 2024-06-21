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

        self.internal_project = self.env.company.internal_project_id
        self.internal_task_leaves = self.env.company.leave_timesheet_task_id

        self.hr_leave_type = self.env["hr.leave.type"].create(
            {
                "name": "Leave Type",
                "requires_allocation": "no",
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

    def test_unit_amount(self):
        number_of_days = (self.leave_end_datetime - self.leave_start_datetime).days
        holiday = (
            self.env["hr.leave"]
            .with_user(self.user_employee)
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
