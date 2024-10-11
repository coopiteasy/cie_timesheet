# SPDX-FileCopyrightText: 2024 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from odoo import api, fields, models


class HrTimesheetSheetPrefill(models.Model):
    _name = "hr_timesheet.sheet.prefill"
    _description = "Timesheet prefill line"
    _order = "sequence, id"
    # This is a weird hack, inspired by what is done in the `mail` module for
    # the `mail.notification` model. That model, like this one, is a model
    # doubling as a Many2many table. In `hr_timesheet_sheet_prefill`, the below
    # Many2many relation table is created. Here, we claim that table for
    # ourselves to add the functionality we want, while still preserving the
    # original Many2many functionality without any changes upstream.
    _table = "hr_employee_project_project_rel"
    _rec_name = "project_project_id"

    hr_employee_id = fields.Many2one(
        string="Employee",
        comodel_name="hr.employee",
        ondelete="cascade",
        required=True,
    )
    project_project_id = fields.Many2one(
        string="Project",
        comodel_name="project.project",
        ondelete="cascade",
        required=True,
    )
    sequence = fields.Integer(string="Sequence", default=10)
    active = fields.Boolean(related="project_project_id.active")

    @api.model_cr
    def init(self):
        # Add id column if it doesn't exist yet.
        self.env.cr.execute(
            """
            DO $$
            BEGIN
                IF NOT EXISTS (SELECT 1 FROM information_schema.columns
                               WHERE table_name='hr_employee_project_project_rel'
                               AND column_name='id') THEN
                    ALTER TABLE hr_employee_project_project_rel
                    ADD COLUMN id SERIAL NOT NULL PRIMARY KEY;
                END IF;
            END $$;
            """
        )
        # Get rid of the unique constraint from the Many2many relationship.
        self.env.cr.execute(
            """
            ALTER TABLE hr_employee_project_project_rel
            DROP CONSTRAINT IF EXISTS
            hr_employee_project_project_r_hr_employee_id_project_projec_key;
            """
        )
