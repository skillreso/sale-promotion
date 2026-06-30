# Copyright 2021 Tecnativa - David Vidal
# Copyright 2023 Tecnativa - Stefan Ungureanu
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import fields, models

class LoyaltyProgram(models.Model):
    _inherit = "loyalty.program"

    incompatible_promotion_ids = fields.Many2many(
        comodel_name="loyalty.program",
        relation="sale_loyalty_program_incompatibility_rel",
        column1="program_id",
        column2="incompatible_program_id",
        inverse="_inverse_incompatible_promotion_ids",
        string="Incompatible Promotions",
        domain="[('id', '!=', id)]",
    )

    is_incompatible_promotion_all = fields.Boolean(
        string="Incompatible with all promotions",
        help="If checked, this program is incompatible with all other promotions.",
        default=False,
    )

    def _inverse_incompatible_promotion_ids(self):
        """We'll be ensuring that any program that could have been removed from the
        field will be compatible again and that any new program in the field will
        be incompatible with this one. So we will ensure that A ⊥ B as B ⊥ A"""
        for program in self:
            incompatible_programs = self.search(
                [
                    ("incompatible_promotion_ids", "in", program.ids),
                    ("id", "!=", program.id),
                ]
            )
            to_remove_programs = (
                incompatible_programs - program.incompatible_promotion_ids
            )
            # The line below does not work if there are more than one entry in program.incompatible_promotion_ids
            # Because all entries would then have their incompatible_promotion_ids set to the same value, containing all incompatible_promotion_ids of every entry
            # That's why we replace this line with a for loop that updates the incompatible_promotion_ids separately for each entry
            # program.incompatible_promotion_ids.incompatible_promotion_ids |= program
            for incompatible_program in program.incompatible_promotion_ids:
                incompatible_program.incompatible_promotion_ids |= program
            # to_remove_programs.incompatible_promotion_ids -= program
            for to_remove_program in to_remove_programs:
                to_remove_program.incompatible_promotion_ids -= program
