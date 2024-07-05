# SPDX-FileCopyrightText: 2024 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from odoo import models


class HrTimesheetSheet(models.Model):
    _inherit = "hr_timesheet.sheet"

    def _get_default_sheet_line(self, matrix, key):
        result = super()._get_default_sheet_line(matrix, key)
        result["hours_worked"] = sum(t.hours_worked for t in matrix[key])
        return result
