# SPDX-FileCopyrightText: 2024 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from odoo import api, fields, models


class AnalyticLine(models.Model):
    _inherit = "account.analytic.line"

    hours_worked = fields.Float(
        store=True,
        readonly=True,
        compute="_compute_hours_worked",
    )
    unit_amount = fields.Float(
        # Make sure unit_amount is computed from hours worked, NOT directly from
        # time_start and time_stop.
        compute="_compute_unit_amount_from_hours",
    )

    @api.depends("time_start", "time_stop")
    def _compute_hours_worked(self):
        for line in self:
            line.hours_worked = self._hours_from_start_stop(
                line.time_start, line.time_stop
            )

    # Add date to constrains.
    @api.constrains("time_start", "time_stop", "unit_amount", "date")
    def _check_time_start_stop(self):
        return super()._check_time_start_stop()

    def unit_amount_from_start_stop(self):
        result = super().unit_amount_from_start_stop()
        result *= self.get_overtime_rate()
        return result
