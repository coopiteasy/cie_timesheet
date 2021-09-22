# Copyright 2019 Coop IT Easy SCRLfs
#   - Vincent Van Rossem <vincent@coopiteasy.be>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.exceptions import UserError
from odoo.tests.common import TransactionCase


class TestHrTimesheetSheetPrefill(TransactionCase):
    def setUp(self):
        super().setUp()

        # projects
        self.project_01 = self.env["project.project"].create(
            {"name": "Project 01"}
        )
        self.project_02 = self.env["project.project"].create(
            {"name": "Project 02"}
        )

    def test_timesheet_creation_fail_linked_employee(self):
        # unlinked employee
        unlinked_employee_dict = {"name": "Unlinked Employee"}
        unlinked_employee = self.env["hr.employee"].create(
            unlinked_employee_dict
        )

        ts_unlinked_employee_dict = {
            "employee_id": unlinked_employee.id,
            "date_start": "2019-12-09",
            "date_end": "2019-12-15",
        }
        with self.assertRaises(UserError):
            self.env["hr_timesheet.sheet"].create(ts_unlinked_employee_dict)

    def test_timesheet_creation_01(self):
        # user
        user_01_dict = {
            "name": "User 1",
            "login": "user1",
            "password": "password",
        }
        user_01 = self.env["res.users"].create(user_01_dict)

        # employee
        employee_01_dict = {
            "name": "Employee 1",
            "user_id": user_01.id,
            "address_id": user_01.partner_id.id,
        }
        employee_01 = (
            self.env["hr.employee"]
            .with_context(mail_create_nosubscribe=True)
            .create(employee_01_dict)
        )

        # timesheet
        ts_01_dict = {
            "employee_id": employee_01.id,
            "date_start": "2019-12-09",
            "date_end": "2019-12-15",
        }
        ts_01 = self.env["hr_timesheet.sheet"].create(ts_01_dict)

        self.assertEqual(len(ts_01.timesheet_ids), 0)

    def test_timesheet_creation_02(self):
        # user
        user_02_dict = {
            "name": "User 2",
            "login": "user2",
            "password": "password",
        }
        user_02 = self.env["res.users"].create(user_02_dict)

        # employee
        employee_02_dict = {
            "name": "Employee 2",
            "user_id": user_02.id,
            "address_id": user_02.partner_id.id,
            "project_ids": [
                (
                    6,
                    0,
                    [self.project_01.id, self.project_02.id],
                )
            ],
        }
        employee_02 = (
            self.env["hr.employee"]
            .with_context(mail_create_nosubscribe=True)
            .create(employee_02_dict)
        )

        # timesheet
        ts_02_dict = {
            "employee_id": employee_02.id,
            "date_start": "2019-12-09",
            "date_end": "2019-12-15",
        }
        ts_02 = self.env["hr_timesheet.sheet"].create(ts_02_dict)

        self.assertEqual(len(ts_02.timesheet_ids), 14)
