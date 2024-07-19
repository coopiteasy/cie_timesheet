# Copyright 2019 Coop IT Easy SC
#   - Vincent Van Rossem <vincent@coopiteasy.be>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import timedelta

from odoo import api, models


class Sheet(models.Model):
    _inherit = "hr_timesheet.sheet"

    @api.model
    def create(self, vals):
        ts = super().create(vals)

        date_start = ts.date_start
        date_end = ts.date_end
        employee_id = ts.employee_id
        sheet_id = ts.id

        days = self.get_number_days_between_dates(date_start, date_end)
        for day in range(days):
            date_current = date_start + timedelta(days=day)
            for project in employee_id.project_ids:
                aal_dict = self._prepare_analytic_line(
                    date_current, project, sheet_id, employee_id.user_id
                )
                ts.write({"timesheet_ids": [(0, 0, aal_dict)]})
        return ts

    @api.model
    def get_number_days_between_dates(self, date_start, date_end):
        """
        Return the number of days between two dates, including both of them.

        Arguments:
            date_start (date): start date
            date_end (date): end date

        Returns:
            int: the number of days between the provided dates
        """
        difference = date_end - date_start
        # return result and add a day
        return difference.days + 1

    @api.model
    def _prepare_analytic_line(self, date, project, sheet_id, user_id):
        return {
            "project_id": project.id,
            "amount": 0.0,
            "date": date,
            # this used to be "/", but this is now a special string considered
            # by the hr_timesheet_sheet module as an empty line. when a
            # timesheet is saved, any line with "/" as description and 0 time
            # is removed.
            "name": "-",
            "sheet_id": sheet_id,
            "unit_amount": 0,
            "user_id": user_id.id,
        }
