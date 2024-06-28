# Copyright 2020 Coop IT Easy SC
#   - Vincent Van Rossem <vincent@coopiteasy.be>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Timesheet/Contract - Overtime",
    "version": "16.0.2.1.0",
    "category": "Human Resources",
    "summary": "Overtime Calculation",
    "author": "Coop IT Easy SC, Odoo Community Association (OCA)",
    "website": "https://github.com/coopiteasy/cie-timesheet",
    "license": "AGPL-3",
    "depends": [
        "company_today",
        "hr_timesheet_sheet",
        "resource_work_time_from_contracts",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/hr_employee_view.xml",
        "views/resource_view.xml",
        "views/hr_timesheet_sheet_view.xml",
    ],
    "demo": [
        "demo/hr_contract_demo.xml",
    ],
}
