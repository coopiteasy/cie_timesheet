# SPDX-FileCopyrightText: 2024 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from odoo import models


class AnalyticLine(models.Model):
    _inherit = "account.analytic.line"

    def get_overtime_rate(self):
        self.ensure_one()
        if self.holiday_id:
            return 1
        return super().get_overtime_rate()
