# SPDX-FileCopyrightText: 2024 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

{
    "name": "Timesheet - Overtime and begin/end hours compatibility",
    "summary": """
        Make the two modules compatible.""",
    "version": "12.0.1.0.0",
    "category": "Human Resources",
    "website": "https://coopiteasy.be",
    "author": "Coop IT Easy SC",
    "maintainers": ["carmenbianca"],
    "license": "AGPL-3",
    "application": False,
    "depends": [
        "hr_timesheet_overtime",
        "hr_timesheet_activity_begin_end",
    ],
    "auto_install": True,
}
