# Copyright 2019 Coop IT Easy SC
#   - Vincent Van Rossem <vincent@coopiteasy.be>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class Employee(models.Model):
    _inherit = "hr.employee"

    project_ids = fields.Many2many(
        comodel_name="project.project",
        relation="hr_employee_project_project_rel",
        string="Projects",
    )

    # This exists solely for extension in hr_timesheet_sheet_prefill_multi.
    def all_prefill_projects(self):
        self.ensure_one()
        return self.project_ids
