# SPDX-FileCopyrightText: 2024 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from odoo import api, models


class AnalyticLine(models.Model):
    _inherit = "account.analytic.line"

    # This is a bit of a hack. Normally in hr_timesheet_overtime, the value of
    # unit_amount is updated in this method as part of writing or creating a
    # record. However, in hr_timesheet_activity_begin_end, unit_amount is
    # adjusted during an onchange using unit_amount_from_start_stop.
    #
    # If BOTH the onchange and the write method adjust the value of unit_amount,
    # then the rate is applied twice, which is not good. Therefore, this method
    # is 'disabled', and we instead rely on onchange to correctly set the value
    # of unit_amount.
    #
    # The disadvantage is that programmatic usages of hr_timesheet_overtime no
    # longer work here. The advantage is that you can now manually override the
    # value of unit_amount without the rate being automatically applied.
    #
    # In version 16, this behaviour is a lot less messy, because it uses compute
    # functions instead of the aforementioned methods.
    @api.model
    def _update_values(self, values):
        time_start = values.get("time_start", self.time_start)
        time_stop = values.get("time_stop", self.time_stop)
        # Do not double-compute if we're using times.
        if time_start or time_stop:
            return
        return super()._update_values(values)

    def unit_amount_from_start_stop(self):
        result = super().unit_amount_from_start_stop()
        result *= self.rate_for_date(self.date)
        return result
