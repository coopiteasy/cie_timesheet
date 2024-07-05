# SPDX-FileCopyrightText: 2024 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from datetime import date

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
        }
        cls.employee1 = cls.env["hr.employee"].create(employee1_dict)
        # projects
        cls.project_01 = cls.env["project.project"].create({"name": "Project 01"})

    def test_write_multiple_lines(self):
        """When writing multiple analytic lines, overtime rates are applied
        separately to each record.
        """
        overtime = self.env["resource.overtime"].create({"name": "test"})
        self.env["resource.overtime.rate"].create(
            {
                "name": "test",
                "dayofweek": "0",  # Monday
                "rate": 2.0,
                "overtime_id": overtime.id,
            }
        )

        lines = self.env["account.analytic.line"].browse()
        # monday and tuesday
        for day in range(9, 11):
            lines += self.env["account.analytic.line"].create(
                {
                    "project_id": self.project_01.id,
                    "amount": 0.0,
                    "date": date(2019, 12, day),
                    "name": "-",
                    "employee_id": self.employee1.id,
                }
            )
        lines.write({"hours_worked": 1})

        self.assertEqual(lines[0].unit_amount, 2)
        self.assertEqual(lines[0].hours_worked, 1)
        self.assertEqual(lines[1].unit_amount, 1)
        self.assertEqual(lines[1].hours_worked, 1)
