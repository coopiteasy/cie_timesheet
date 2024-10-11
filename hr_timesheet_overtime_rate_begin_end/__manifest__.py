# SPDX-FileCopyrightText: 2024 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

{
    "name": "Timesheet - Overtime rate and begin/end hours compatibility",
    "summary": "Make ``hr_timesheet_overtime_rate`` and ``hr_timesheet_begin_end`` compatible.",
    "version": "16.0.1.0.0",
    "category": "Human Resources",
    "website": "https://github.com/coopiteasy/cie-timesheet",
    "author": "Coop IT Easy SC",
    "maintainers": ["carmenbianca"],
    "license": "AGPL-3",
    "application": False,
    "depends": [
        "hr_timesheet_overtime_rate",
        "hr_timesheet_begin_end",
    ],
    "auto_install": True,
}
