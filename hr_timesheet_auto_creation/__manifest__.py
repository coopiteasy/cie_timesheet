# © 2016-2017 Elico Corp (https://www.elico-corp.com)
# Copyright 2019 Coop IT Easy SCRLfs
#   - Vincent Van Rossem <vincent@coopiteasy.be>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "HR TimeSheet Auto Creation",
    "summary": "Create weekly timesheets for employees automatically",
    "version": "12.0.1.0.0",
    "category": "Human Resources",
    "author": (
        "Coop IT Easy SCRLfs, Elico Corp, Odoo Community Association (OCA)"
    ),
    "license": "AGPL-3",
    "website": "https://coopiteasy.be",
    "depends": [
        "hr_timesheet_sheet",
    ],
    "data": [
        "data/hr_timesheet_sheet_cron_job.xml",
    ],
}
