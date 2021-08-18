# © 2016-2017 Elico Corp (https://www.elico-corp.com)
# Copyright 2019 Coop IT Easy SCRLfs
#   - Vincent Van Rossem <vincent@coopiteasy.be>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging
from datetime import date, timedelta

from odoo import api, models

_logger = logging.getLogger(__name__)


class HrTimesheetSheet(models.Model):
    _inherit = "hr_timesheet.sheet"

    @api.model
    def create_employee_timesheet(self):
        _logger.info("[hr_timesheet_auto_creation][create_employee_timesheet]")
        employee_obj = self.env["hr.employee"]
        employee_ids = employee_obj.search(
            [("active", "=", True), ("user_id", "!=", False)]
        ).ids
        today = date.today()
        # FIXME: this assumes weekly time sheets with weeks starting on
        # monday. the hr_timesheet_sheet module allows to configure the
        # default sheet range and the week start day (sheet_range and
        # timesheet_week_start company properties). this should be used
        # instead.
        monday = today + timedelta(days=-today.weekday())
        sunday = monday + timedelta(days=6)
        # Search for existing timesheet
        exists_timesheet_records = self.search([("date_end", ">=", monday)])
        ignore_employee_ids = map(
            lambda x: x.employee_id.id, exists_timesheet_records
        )
        employee_ids = list(set(employee_ids) - set(ignore_employee_ids))
        for employee_id in employee_ids:
            self.sudo().create(
                {
                    "employee_id": employee_id,
                    "date_start": monday,
                    "date_end": sunday,
                }
            )
            _logger.info(
                "[hr_timesheet_auto_creation] hr_timesheet.sheet "
                "created for employee %s " % employee_id
            )

        return True
