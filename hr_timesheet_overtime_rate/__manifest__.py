# SPDX-FileCopyrightText: 2024 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

{
    "name": "Overtime Rate",
    "summary": """
        Define an extra rate for working certain days.""",
    "version": "16.0.1.0.0",
    "category": "Human Resources",
    "website": "https://github.com/coopiteasy/cie-timesheet",
    "author": "Coop IT Easy SC",
    "maintainers": ["carmenbianca"],
    "license": "AGPL-3",
    "application": False,
    "depends": [
        "hr_timesheet_sheet",
    ],
    "excludes": [],
    "data": [
        "security/ir.model.access.csv",
        "data/data.xml",
        "views/resource_views.xml",
        "views/account_analytic_line_views.xml",
        "views/hr_timesheet_sheet_views.xml",
    ],
    "demo": [],
    "qweb": [],
}
