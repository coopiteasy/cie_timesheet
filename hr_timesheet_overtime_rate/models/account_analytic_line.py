# SPDX-FileCopyrightText: 2024 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from odoo import api, fields, models


class AnalyticLine(models.Model):
    """
    Apply on account analytic lines the rate defined in resource.overtime.rate
    """

    _inherit = "account.analytic.line"

    hours_worked = fields.Float(
        default=0.0,
    )
    # Override to be a computed field.
    unit_amount = fields.Float(
        # We use a kind of custom name here because `hr_timesheet_begin_end`
        # also overrides this, and the two compute methods are not necessarily
        # compatible.
        compute="_compute_unit_amount_from_hours",
        store=True,
        readonly=False,
        # This triggers computation on creation. default=False and default=0 do
        # not trigger computation.
        default=None,
    )

    # TODO: should this also depend on resource.overtime.rate, somehow?
    @api.depends("hours_worked", "date")
    def _compute_unit_amount_from_hours(self):
        # Do not compute/adjust the unit_amount of non-timesheets.
        lines = self.filtered(lambda line: line.project_id)
        for line in lines:
            line.unit_amount = line.hours_worked * line.rate_for_date(line.date)

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

    def _init_hours_worked(self):
        """Upon module installation (or manually any other time, if you really
        want), this method is called to populate hours_worked with something
        sensible, derived from unit_amount and the rate for that day.
        """
        # We use an SQL query because we do not want to trigger computation upon
        # writing to hours_worked.
        query = """
            UPDATE account_analytic_line
            SET hours_worked=CASE
            """
        params = []

        for line in self.filtered(lambda item: item.project_id):
            rate = self.rate_for_date(line.date)
            hours_worked = line.unit_amount / rate
            query += "WHEN id=%s THEN %s "
            params.extend([line.id, hours_worked])
        query += "END WHERE id IN %s"

        if params:
            self.env.cr.execute(query, (*params, tuple(line.id for line in self)))
