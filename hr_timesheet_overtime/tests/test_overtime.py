# Copyright 2020 Coop IT Easy SC
#   - Vincent Van Rossem <vincent@coopiteasy.be>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from datetime import date

from freezegun import freeze_time

from odoo.tests.common import TransactionCase


class TestOvertime(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # users
        user1_dict = {"name": "User 1", "login": "user1", "password": "user1"}
        cls.user1 = cls.env["res.users"].create(user1_dict)

        # employees
        employee1_dict = {
            "name": "Employee 1",
            "user_id": cls.user1.id,
            "address_id": cls.user1.partner_id.id,
            "overtime_start_date": "2019-01-01",
        }
        cls.employee1 = cls.env["hr.employee"].create(employee1_dict)

        # working hours
        # calendar have default attendance_ids, force it to have none.
        calendar = cls.env["resource.calendar"].create(
            {"name": "Calendar", "attendance_ids": False}
        )
        for day in range(5):
            cls.env["resource.calendar.attendance"].create(
                {
                    "name": "Attendance",
                    "dayofweek": str(day),
                    "hour_from": 9.0,
                    "hour_to": 18.0,
                    "calendar_id": calendar[0].id,
                }
            )

        # contracts
        contract_dict = {
            "name": "Contract 1",
            "employee_id": cls.employee1.id,
            "wage": 0.0,
            "resource_calendar_id": calendar.id,
            "date_start": "2019-01-01",
        }

        cls.contract1 = cls.env["hr.contract"].create(contract_dict)

        # projects
        cls.project_01 = cls.env["project.project"].create({"name": "Project 01"})

        # create ts
        ts1_dict = {
            "employee_id": cls.employee1.id,
            "date_start": "2019-12-02",
            "date_end": "2019-12-08",
        }
        cls.ts1 = cls.env["hr_timesheet.sheet"].create(ts1_dict)

        # create and link aal
        # monday 02/12/2019
        cls.env["account.analytic.line"].create(
            {
                "project_id": cls.project_01.id,
                "amount": 0.0,
                "date": "2019-12-02",
                "name": "-",
                "sheet_id": cls.ts1.id,
                "unit_amount": 10.0,  # 1 hour overtime
                "user_id": cls.employee1.user_id.id,
            }
        )
        # tuesday 03/12/2019 -> friday 06/12/2019
        for day in range(3, 7):
            cls.env["account.analytic.line"].create(
                {
                    "project_id": cls.project_01.id,
                    "amount": 0.0,
                    "date": date(2019, 12, day),
                    "name": "-",
                    "sheet_id": cls.ts1.id,
                    "unit_amount": 9.0,  # expected time
                    "user_id": cls.employee1.user_id.id,
                }
            )

    def test_overtime_01(self):
        """
        A timesheet and its analytic line with one hour extra time
        """

        self.assertEqual(self.ts1.timesheet_overtime_trimmed, 1)
        self.assertEqual(self.ts1.timesheet_overtime, 1)
        self.assertEqual(self.ts1.total_overtime, 1)

    def test_overtime_02(self):
        """
        Change overtime start date
        """
        ts2 = self.env["hr_timesheet.sheet"].create(
            {
                "employee_id": self.employee1.id,
                "date_start": "2019-12-09",
                "date_end": "2019-12-15",
            }
        )

        # create and link aal
        # monday and tuesday
        for day in range(9, 11):
            self.env["account.analytic.line"].create(
                {
                    "project_id": self.project_01.id,
                    "amount": 0.0,
                    "date": date(2019, 12, day),
                    "name": "-",
                    "sheet_id": ts2.id,
                    "unit_amount": 10.0,  # 1 hour overtime
                    "user_id": self.employee1.user_id.id,
                }
            )
        # wednesday -> thursday
        for day in range(10, 13):
            self.env["account.analytic.line"].create(
                {
                    "project_id": self.project_01.id,
                    "amount": 0.0,
                    "date": date(2019, 12, day),
                    "name": "-",
                    "sheet_id": ts2.id,
                    "unit_amount": 9.0,  # expected time
                    "user_id": self.employee1.user_id.id,
                }
            )

        self.employee1.write({"overtime_start_date": "2019-12-10"})

        # overtime for any timesheet takes overtime_start_date into account
        self.assertEqual(self.ts1.timesheet_overtime_trimmed, 0)
        self.assertEqual(self.ts1.timesheet_overtime, 1)
        # it should start computing on tuesday
        self.assertEqual(ts2.timesheet_overtime_trimmed, 1)
        self.assertEqual(ts2.timesheet_overtime, 2)
        self.assertEqual(ts2.total_overtime, 1)
        # total_overtime is just a link to the employee's total overtime
        self.assertEqual(self.ts1.total_overtime, 1)

    def test_overtime_03(self):
        """
        Change initial overtime
        """
        self.employee1.write({"initial_overtime": 10})

        self.assertEqual(self.ts1.timesheet_overtime_trimmed, 1)
        self.assertEqual(self.ts1.timesheet_overtime, 1)
        self.assertEqual(self.ts1.total_overtime, 11)

    def test_overtime_04(self):
        """
        Worker did not work on a day he was expected to work on.
        """
        ts2 = self.env["hr_timesheet.sheet"].create(
            {
                "employee_id": self.employee1.id,
                "date_start": "2019-12-09",
                "date_end": "2019-12-15",
            }
        )

        # create and link aal
        # monday
        self.env["account.analytic.line"].create(
            {
                "project_id": self.project_01.id,
                "amount": 0.0,
                "date": "2019-12-09",
                "name": "-",
                "sheet_id": ts2.id,
                "unit_amount": 10.0,  # 1 hour overtime
                "user_id": self.employee1.user_id.id,
            }
        )
        # tuesday -> thursday
        for day in range(10, 13):
            self.env["account.analytic.line"].create(
                {
                    "project_id": self.project_01.id,
                    "amount": 0.0,
                    "date": date(2019, 12, day),
                    "name": "-",
                    "sheet_id": ts2.id,
                    "unit_amount": 9.0,  # expected time
                    "user_id": self.employee1.user_id.id,
                }
            )

        self.assertEqual(ts2.timesheet_overtime_trimmed, -8)
        self.assertEqual(ts2.timesheet_overtime, -8)
        self.assertEqual(ts2.total_overtime, -7)

    def test_overtime_05(self):
        """
        Multiple contracts
        """

        # end previous contract
        self.contract1.date_end = "2020-01-06"

        # create new contract
        # working hours : half-time
        calendar = self.env["resource.calendar"].create(
            {"name": "Calendar", "attendance_ids": False}
        )
        for day in range(5):  # from monday to friday
            self.env["resource.calendar.attendance"].create(
                {
                    "name": "Attendance",
                    "dayofweek": str(day),
                    "hour_from": 9.0,
                    "hour_to": 13.0,
                    "calendar_id": calendar[0].id,
                }
            )

        # contracts
        contract_dict = {
            "name": "Contract 2",
            "employee_id": self.employee1.id,
            "wage": 0.0,
            "resource_calendar_id": calendar.id,
            "date_start": "2020-01-07",
        }

        self.contract2 = self.env["hr.contract"].create(contract_dict)

        # create ts
        ts2_dict = {
            "employee_id": self.employee1.id,
            "date_start": "2020-01-06",
            "date_end": "2020-01-12",
        }
        self.ts2 = self.env["hr_timesheet.sheet"].create(ts2_dict)

        # create and link aal
        # monday
        self.env["account.analytic.line"].create(
            {
                "project_id": self.project_01.id,
                "amount": 0.0,
                "date": "2020-01-06",
                "name": "-",
                "sheet_id": self.ts2.id,
                "unit_amount": 9.0,  # expected time from previous contract
                "user_id": self.employee1.user_id.id,
            }
        )

        # tuesday 07/01/2020 -> friday 10/01/2020
        for day in range(7, 11):
            self.env["account.analytic.line"].create(
                {
                    "project_id": self.project_01.id,
                    "amount": 0.0,
                    "date": date(2020, 1, day),
                    "name": "-",
                    "sheet_id": self.ts2.id,
                    "unit_amount": 4.0,  # expected time from new contract
                    "user_id": self.employee1.user_id.id,
                }
            )

        self.assertEqual(self.ts2.timesheet_overtime_trimmed, 0)
        self.assertEqual(self.ts2.timesheet_overtime, 0)
        self.assertEqual(self.ts2.total_overtime, 1)  # 1 hour overtime from ts1

    def test_overtime_archived_timesheet(self):
        """
        Archived timesheets
        """
        ts2 = self.env["hr_timesheet.sheet"].create(
            {
                "employee_id": self.employee1.id,
                "date_start": "2019-12-09",
                "date_end": "2019-12-15",
            }
        )

        # create and link aal
        # monday -> friday
        for day in range(9, 14):
            self.env["account.analytic.line"].create(
                {
                    "project_id": self.project_01.id,
                    "amount": 0.0,
                    "date": date(2019, 12, day),
                    "name": "-",
                    "sheet_id": ts2.id,
                    "unit_amount": 10.0,  # 1 hour overtime
                    "user_id": self.employee1.user_id.id,
                }
            )

        self.assertEqual(self.ts1.timesheet_overtime_trimmed, 1)
        self.assertEqual(self.ts1.timesheet_overtime, 1)
        self.assertEqual(self.ts1.total_overtime, 6)
        self.assertEqual(ts2.timesheet_overtime_trimmed, 5)
        self.assertEqual(ts2.timesheet_overtime, 5)
        self.assertEqual(ts2.total_overtime, 6)
        self.assertEqual(self.employee1.total_overtime, 6)

        self.ts1.write({"active": False})
        # an inactive timesheet still has the same overtime
        self.assertEqual(self.ts1.timesheet_overtime_trimmed, 1)
        self.assertEqual(self.ts1.timesheet_overtime, 1)
        self.assertEqual(self.ts1.total_overtime, 5)
        self.assertEqual(ts2.timesheet_overtime_trimmed, 5)
        self.assertEqual(ts2.timesheet_overtime, 5)
        self.assertEqual(ts2.total_overtime, 5)
        self.assertEqual(self.employee1.total_overtime, 5)

        ts2.write({"active": False})
        self.assertEqual(self.ts1.timesheet_overtime_trimmed, 1)
        self.assertEqual(self.ts1.timesheet_overtime, 1)
        self.assertEqual(self.ts1.total_overtime, 0)
        self.assertEqual(ts2.timesheet_overtime_trimmed, 5)
        self.assertEqual(ts2.timesheet_overtime, 5)
        self.assertEqual(ts2.total_overtime, 0)
        self.assertEqual(self.employee1.total_overtime, 0)

        self.ts1.write({"active": True})
        self.assertEqual(self.ts1.timesheet_overtime_trimmed, 1)
        self.assertEqual(self.ts1.timesheet_overtime, 1)
        self.assertEqual(self.ts1.total_overtime, 1)
        self.assertEqual(ts2.timesheet_overtime_trimmed, 5)
        self.assertEqual(ts2.timesheet_overtime, 5)
        self.assertEqual(ts2.total_overtime, 1)
        self.assertEqual(self.employee1.total_overtime, 1)

    # The subsequent tests verify whether the stored fields respond correctly to
    # changing variables.

    def test_stored_change_contract_date_start(self):
        """When contract_id.date_start is changed, adjust correctly."""
        # These initial assertions are not repeated in subsequent tests.
        self.assertEqual(self.ts1.timesheet_overtime_trimmed, 1)
        self.assertEqual(self.ts1.timesheet_overtime, 1)
        self.assertEqual(self.ts1.total_overtime, 1)
        self.assertEqual(self.ts1.working_time, 9 * 5)
        self.contract1.date_start = date(2019, 12, 3)
        self.assertEqual(self.ts1.timesheet_overtime_trimmed, 10)
        self.assertEqual(self.ts1.timesheet_overtime, 10)
        self.assertEqual(self.ts1.total_overtime, 10)
        self.assertEqual(self.ts1.working_time, 9 * 4)

    def test_stored_change_contract_date_end(self):
        """When contract_id.date_end is changed, adjust correctly."""
        self.contract1.date_end = date(2019, 12, 5)
        self.assertEqual(self.ts1.timesheet_overtime_trimmed, 10)
        self.assertEqual(self.ts1.timesheet_overtime, 10)
        self.assertEqual(self.ts1.total_overtime, 10)
        self.assertEqual(self.ts1.working_time, 9 * 4)

    def test_stored_change_attendance_hour_to(self):
        """When contract_id.resource_calendar_id.attendance_ids.hour_to is changed,
        adjust correctly.
        """
        self.contract1.resource_calendar_id.attendance_ids[0].hour_to = 17
        self.assertEqual(self.ts1.timesheet_overtime_trimmed, 2)
        self.assertEqual(self.ts1.timesheet_overtime, 2)
        self.assertEqual(self.ts1.total_overtime, 2)
        self.assertEqual(self.ts1.working_time, 9 * 5 - 1)

    def test_stored_change_attendance_hour_from(self):
        """When contract_id.resource_calendar_id.attendance_ids.hour_from is changed,
        adjust correctly.
        """
        self.contract1.resource_calendar_id.attendance_ids[0].hour_from = 10
        self.assertEqual(self.ts1.timesheet_overtime_trimmed, 2)
        self.assertEqual(self.ts1.timesheet_overtime, 2)
        self.assertEqual(self.ts1.total_overtime, 2)
        self.assertEqual(self.ts1.working_time, 9 * 5 - 1)

    def test_stored_change_initial_overtime(self):
        """When employee_id.initial_overtime is changed, adjust accordingly."""
        self.employee1.initial_overtime = 1
        self.assertEqual(self.ts1.total_overtime, 2)

    def test_stored_change_overtime_start_date(self):
        """When employee_id.overtime_start_date is changed, adjust accordingly."""
        self.employee1.overtime_start_date = date(2020, 1, 1)
        # No matching records.
        self.assertEqual(self.ts1.total_overtime, 0)

    def test_stored_change_today(self):
        """When today is changed, adjust accordingly."""
        # More hours of work in the week
        line = self.env["account.analytic.line"].search(
            [
                ("date", "=", "2019-12-4"),
                ("sheet_id", "=", self.ts1.id),
            ]
        )
        line.unit_amount = 10
        self.assertEqual(self.ts1.timesheet_overtime_trimmed, 2)
        self.assertEqual(self.ts1.timesheet_overtime, 2)
        self.assertEqual(self.ts1.total_overtime, 2)
        self.assertEqual(self.ts1.working_time, 9 * 5)

        # Time travel into the past before the overtime.
        with freeze_time("2019-12-3"):
            self.ts1.company_id.cron_update_today()
            # Not affected by the extra overtime
            self.assertEqual(self.ts1.timesheet_overtime_trimmed, 1)
            self.assertEqual(self.ts1.total_overtime, 1)
            self.assertEqual(self.ts1.working_time, 9 * 5)
            # Affected by the extra overtime
            self.assertEqual(self.ts1.timesheet_overtime, 2)
