# SPDX-FileCopyrightText: 2024 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

{
    "name": "Timesheet - Overtime and holidays compatibility",
    "summary": "Don't apply overtime rates on timesheet lines created from a holiday",
    "version": "16.0.1.0.0",
    "category": "Human Resources",
    "website": "https://github.com/coopiteasy/cie-timesheet",
    "author": "Coop IT Easy SC",
    "maintainers": ["carmenbianca"],
    "license": "AGPL-3",
    "depends": [
        "project_timesheet_holidays",
        "hr_timesheet_overtime_rate",
    ],
    "auto_install": True,
}
