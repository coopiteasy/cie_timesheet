# SPDX-FileCopyrightText: 2024 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from odoo import models


class AnalyticLine(models.Model):
    _inherit = "account.analytic.line"

    def unit_amount_from_start_stop(self):
        result = super().unit_amount_from_start_stop()
        result *= self.rate_for_date(self.date)
        return result
