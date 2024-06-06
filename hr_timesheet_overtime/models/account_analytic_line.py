# Copyright 2020 Coop IT Easy SC
#   - Vincent Van Rossem <vincent@coopiteasy.be>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class AnalyticLine(models.Model):
    """
    Apply on account analytic lines the rate defined in resource.overtime.rate
    """

    _inherit = "account.analytic.line"

    def create(self, values):
        self._update_values(values)
        return super().create(values)

    def write(self, values):
        if not self.env.context.get("create"):  # sale module
            self._update_values(values)
        return super().write(values)

    def _update_values(self, values):
        """
        Update values if date or unit_amount fields have changed
        """
        if "date" in values or "unit_amount" in values:
            date = values.get("date", self.date)
            unit_amount = values.get("unit_amount", self.unit_amount)

            # rate management
            weekday = fields.Date.from_string(date).weekday()
            rate = (
                self.env["resource.overtime.rate"]
                .search([("dayofweek", "=", weekday)], limit=1)
                .rate
                or 1.0
            )

            # update
            values["unit_amount"] = unit_amount * rate
