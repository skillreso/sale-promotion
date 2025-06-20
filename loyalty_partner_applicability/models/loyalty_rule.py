# Copyright 2023 Tecnativa - Pilar Vargas
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models


class LoyaltyRule(models.Model):
    _inherit = "loyalty.rule"
    _description = "Loyalty Rule"

    is_using_partner_list = fields.Boolean(
        string="Use Partner List",
        help="If checked, the loyalty program will only apply to the customers "
        "selected in the partner list.",
        default=True,
    )

    rule_partners_domain = fields.Char(
        string="Based on Customers",
        help="Loyalty program will work for selected customers only",
        default="[]",
    )

    rule_partner_ids = fields.Many2many(
        comodel_name="res.partner",
        string="Customers",
        help="Loyalty program will work for selected customers only",
    )

    @api.model_create_multi
    def create(self, vals_list):
        res = super().create(vals_list)
        for vals in vals_list:
            if not vals.get("rule_partners_domain", False):
                vals["rule_partners_domain"] = "[]"
        return res
