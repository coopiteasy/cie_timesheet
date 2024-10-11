# SPDX-FileCopyrightText: 2024 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from odoo.tests.common import TransactionCase


class TestPrefillMulti(TransactionCase):
    def setUp(self):
        super().setUp()

        self.project_01 = self.env["project.project"].create({"name": "Project 01"})
        self.project_02 = self.env["project.project"].create({"name": "Project 02"})

        self.user = self.env["res.users"].create(
            {
                "name": "Test",
                "login": "test",
                "password": "test",
            }
        )
        self.employee = self.env["hr.employee"].create(
            {
                "name": "Test",
                "user_id": self.user.id,
                "address_id": self.user.partner_id.id,
            }
        )

    def test_all_prefill_projects_filtered_sorted(self):
        """Prefill projects are sorted and filtered."""
        project_03 = self.env["project.project"].create({"name": "Project 03"})
        self.project_02.active = False

        self.employee.timesheet_prefill_ids = [
            (0, False, {"project_project_id": self.project_01.id, "sequence": 1}),
            (0, False, {"project_project_id": self.project_02.id, "sequence": 2}),
            (0, False, {"project_project_id": project_03.id, "sequence": 3}),
        ]
        sheet = self.env["hr_timesheet.sheet"].create(
            {
                "employee_id": self.employee.id,
                "date_start": "2024-01-01",
                "date_end": "2024-01-01",
            }
        )
        self.assertEqual(len(sheet.timesheet_ids), 2)
        used_projects = sheet.timesheet_ids.mapped("project_id")
        self.assertIn(self.project_01, used_projects)
        self.assertNotIn(self.project_02, used_projects)
        self.assertIn(project_03, used_projects)

    def test_project_ids_still_works(self):
        """You can still use project_ids on hr.employee as normally. It will
        create prefill records.
        """
        projects = self.project_01 | self.project_02
        self.employee.project_ids = projects

        self.assertEqual(len(self.employee.timesheet_prefill_ids), 2)
        prefill_01 = self.employee.timesheet_prefill_ids[0]
        prefill_02 = self.employee.timesheet_prefill_ids[1]
        # We can't know for sure which project was sorted first, so we do the
        # below to make sure they are both given a timesheet.
        self.assertNotEqual(
            prefill_01.project_project_id, prefill_02.project_project_id
        )
        self.assertIn(prefill_01.project_project_id, projects)
        self.assertIn(prefill_02.project_project_id, projects)

        sheet = self.env["hr_timesheet.sheet"].create(
            {
                "employee_id": self.employee.id,
                "date_start": "2024-01-01",
                "date_end": "2024-01-01",
            }
        )
        self.assertEqual(len(sheet.timesheet_ids), 2)
        self.assertNotEqual(
            sheet.timesheet_ids[0].project_id, sheet.timesheet_ids[1].project_id
        )
        self.assertIn(sheet.timesheet_ids[0].project_id, projects)
        self.assertIn(sheet.timesheet_ids[1].project_id, projects)

    def test_sequenced_repeated_prefills(self):
        """You can repeat and sequence prefills."""
        self.employee.timesheet_prefill_ids = [
            (0, False, {"project_project_id": self.project_01.id, "sequence": 1}),
            (0, False, {"project_project_id": self.project_02.id, "sequence": 2}),
            (0, False, {"project_project_id": self.project_01.id, "sequence": 3}),
        ]

        # Sanity check.
        self.assertEqual(len(self.employee.project_ids), 3)

        sheet = self.env["hr_timesheet.sheet"].create(
            {
                "employee_id": self.employee.id,
                "date_start": "2024-01-01",
                "date_end": "2024-01-01",
            }
        )
        self.assertEqual(len(sheet.timesheet_ids), 3)
        self.assertEqual(sheet.timesheet_ids[0].project_id, self.project_01)
        self.assertEqual(sheet.timesheet_ids[1].project_id, self.project_02)
        self.assertEqual(sheet.timesheet_ids[2].project_id, self.project_01)
