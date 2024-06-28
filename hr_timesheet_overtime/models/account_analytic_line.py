# Copyright 2020 Coop IT Easy SC
#   - Vincent Van Rossem <vincent@coopiteasy.be>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class AnalyticLine(models.Model):
    """
    Apply on account analytic lines the rate defined in resource.overtime.rate
    """

    _inherit = "account.analytic.line"

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            self._update_values(vals)
        return super().create(vals_list)

    def write(self, values):
        if not self.env.context.get("create"):  # sale module
            self._update_values(values)
        return super().write(values)

    def _update_values(self, values):
        """
        Update values if date or unit_amount fields have changed
        """
        if "date" in values or "unit_amount" in values:
            # TODO: self.date and self.unit_amount do not exist when called from
            # create().
            date = values.get("date", self.date)
            unit_amount = values.get("unit_amount", self.unit_amount)
            values["unit_amount"] = unit_amount * self.rate_for_date(date)

    @api.model
    def rate_for_date(self, date):
        # n.b. from_string also works on date objects, returning itself.
        weekday = fields.Date.from_string(date).weekday()
        return (
            self.env["resource.overtime.rate"]
            .search([("dayofweek", "=", weekday)], limit=1)
            .rate
            or 1.0
        )
