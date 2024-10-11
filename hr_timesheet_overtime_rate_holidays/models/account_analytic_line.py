# SPDX-FileCopyrightText: 2024 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from odoo import models


class AnalyticLine(models.Model):
    _inherit = "account.analytic.line"

    def _update_values(self, values):
        if not values.get("holiday_id", self.holiday_id):
            return super()._update_values(values)
        return
