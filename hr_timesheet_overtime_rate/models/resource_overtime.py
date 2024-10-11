# Copyright 2020 Coop IT Easy SC
#   - Vincent Van Rossem <vincent@coopiteasy.be>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import fields, models


class ResourceOvertime(models.Model):
    _name = "resource.overtime"
    _description = "Resource Overtime"

    # String fields
    name = fields.Char(required=True)

    # Relational fields
    rate_ids = fields.One2many(
        string="Overtime Rate",
        comodel_name="resource.overtime.rate",
        inverse_name="overtime_id",
        copy=True,
    )
    company_id = fields.Many2one(
        string="Company",
        comodel_name="res.company",
        default=lambda self: self.env.company,
    )
    manager = fields.Many2one(
        string="Workgroup Manager",
        comodel_name="res.users",
        default=lambda self: self.env.uid,
    )
