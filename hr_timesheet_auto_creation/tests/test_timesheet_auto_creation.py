# © 2016-2017 Elico Corp (https://www.elico-corp.com)
# Copyright 2019 Coop IT Easy SCRLfs
#   - Vincent Van Rossem <vincent@coopiteasy.be>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from datetime import date, timedelta

from odoo.tests import common


class TestHrTimesheetSheet(common.TransactionCase):
    def setUp(self):
        super().setUp()
        self.env["hr.employee"].search([]).write({"user_id": False})
        self.tms_obj = self.env["hr_timesheet.sheet"]
        today = date.today()
        self.monday = today + timedelta(days=-today.weekday())
        self.sunday = self.monday + timedelta(days=6)

        self.user1 = self.env.ref("base.user_root").copy({"login": "test1"})
        self.employee1 = self.env.ref("hr.employee_ngh")
        self.employee1.user_id = self.user1.id

        self.user2 = self.user1.copy({"login": "test2"})
        self.employee2 = self.env.ref("hr.employee_vad").copy(
            {"user_id": self.user2.id}
        )

    def test_create_employee_timesheet(self):
        """Check timesheet has been created automatically for the week."""
        conditions = [
            ("employee_id", "in", (self.employee1.id, self.employee2.id)),
            ("date_start", "=", self.monday),
            ("date_end", "=", self.sunday),
        ]
        # test that no matching timesheets exist yet.
        tms = self.tms_obj.search(conditions)
        self.assertEqual(len(tms), 0)
        self.tms_obj.create_employee_timesheet()
        # test that the timesheets have correctly been created.
        tms = self.tms_obj.search(conditions)
        self.assertEqual(len(tms), 2)
        self.tms_obj.create_employee_timesheet()
        # test that no extra timesheets have been created, because they
        # already exist.
        tms = self.tms_obj.search(conditions)
        self.assertEqual(len(tms), 2)
