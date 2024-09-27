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
        self.ensure_one()
        # The only purpose of the below code is to sort the projects according
        # to the sequence of the prefill records. Instead of doing
        # `self.timesheet_prefill_ids.mapped("project_project_id")`, we
        # manually create the recordset. This is because the recordset MAY
        # contain duplicates, and `mapped()` removes duplicates.
        projects = self.env["project.project"].browse()
        for prefill in self.timesheet_prefill_ids:
            projects += prefill.project_project_id
        return projects
