# SPDX-FileCopyrightText: 2024 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from odoo import fields, models


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    timesheet_prefill_ids = fields.One2many(
        comodel_name="hr_timesheet.sheet.prefill",
        inverse_name="hr_employee_id",
        string="Prefill Projects",
        copy=False,
    )

    def all_prefill_projects(self):
        projects = super().all_prefill_projects()
        # By searching, we get prefills sorted by sequence.
        prefills = self.env["hr_timesheet.sheet.prefill"].search(
            [
                ("project_project_id", "in", projects.ids),
                ("hr_employee_id", "=", self.id),
            ]
        )
        # Instead of doing `prefills.mapped("project_project_id")`, we manually
        # create the recordset. This is because the recordset MAY contain
        # duplicates, and `mapped()` removes duplicates.
        result = self.env["project.project"]
        for prefill in prefills:
            result += prefill.project_project_id
        return result
