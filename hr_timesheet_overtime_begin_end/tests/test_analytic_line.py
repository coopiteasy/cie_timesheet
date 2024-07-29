# SPDX-FileCopyrightText: 2024 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from odoo.tests.common import SavepointCase


class TestAnalyticLine(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.project = cls.env.ref("project.project_project_1")
        cls.employee = cls.env.ref("hr.employee_qdp")
        # I'm not sure what this record does in this context.
        cls.overtime = cls.env["resource.overtime"].create({"name": "test"})
        cls.rate = cls.env["resource.overtime.rate"].create(
            {
                "name": "test",
                "dayofweek": "0",  # Monday
                "rate": 2.0,
                "overtime_id": cls.overtime.id,
            }
        )

    def base_line(self):
        return {
            "name": "test",
            "date": "2024-01-01",  # Monday
            "time_start": 10.0,
            "time_stop": 12.0,
            "project_id": self.project.id,
            "employee_id": self.employee.id,
        }

    def test_rate_applied(self):
        line = self.base_line()
        line_record = self.env["account.analytic.line"].new(line)
        line_record.onchange_hours_start_stop()
        self.assertEqual(line_record.unit_amount, 4.0)

    def test_rate_not_double_applied(self):
        line = self.base_line()
        del line["time_start"]
        del line["time_stop"]

        # Emulating a transient record before it is actually created.
        line_new = self.env["account.analytic.line"].new(line)
        line_new.time_start = 10.0
        line_new.time_stop = 12.0
        line_new.onchange_hours_start_stop()
        self.assertEqual(line_new.unit_amount, 4.0)

        # Prepare the transient data for writing to a new record.
        #
        # Annoyingly, the value for unit_amount is not in _cache, so we have to
        # add it here.
        #
        # Ideally I would emulate this with a Form(), but the necessary fields
        # are not available in a form. This is the closest emulation.
        vals = line_new._convert_to_write(line_new._cache)
        vals.setdefault("unit_amount", line_new.unit_amount)
        line_record = self.env["account.analytic.line"].create(vals)

        # The rate was already applied on the transient record. Don't also apply
        # it on creation.
        self.assertEqual(line_record.unit_amount, 4.0)

    def test_rate_applied_if_no_times(self):
        line = self.base_line()
        del line["time_start"]
        del line["time_stop"]
        line["unit_amount"] = 1
        line_record = self.env["account.analytic.line"].create(line)
        self.assertEqual(line_record.unit_amount, 2)
