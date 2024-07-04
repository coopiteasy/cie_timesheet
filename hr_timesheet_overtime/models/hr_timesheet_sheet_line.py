# SPDX-FileCopyrightText: 2024 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from odoo import api, fields, models


class HrTimesheetSheetLineAbstract(models.AbstractModel):
    _inherit = "hr_timesheet.sheet.line.abstract"

    hours_worked = fields.Float(default=0.0)
    unit_amount = fields.Float(
        compute="_compute_unit_amount_from_hours", readonly=False
    )

    # TODO: this is basically identical to account.analytic.line. it's probably
    # fine?
    @api.depends("hours_worked", "date")
    def _compute_unit_amount_from_hours(self):
        for line in self:
            line.unit_amount = line.hours_worked * self.env[
                "account.analytic.line"
            ].rate_for_date(line.date)


class HrTimesheetSheetLine(models.TransientModel):
    _inherit = "hr_timesheet.sheet.line"

    @api.onchange("unit_amount", "hours_worked")
    def onchange_unit_amount(self):
        return super().onchange_unit_amount()
