# SPDX-FileCopyrightText: 2024 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

{
    "name": "Timesheet Sheet prefill with duplicates",
    "summary": """
        Allow duplicates in prefill templates.""",
    "version": "12.0.1.0.0",
    "category": "Human Resources",
    "website": "https://coopiteasy.be",
    "author": "Coop IT Easy SC, Odoo Community Association (OCA)",
    "maintainers": ["carmenbianca"],
    "license": "AGPL-3",
    "application": False,
    "depends": [
        "hr_timesheet_sheet_prefill",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/hr_employee_views.xml",
    ],
}
