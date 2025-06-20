# Copyright 2021 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import _, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _program_check_compute_points(self, programs):
        """Coupon incompatibility rules. Check the error strings for a detailed case
        detail."""
        self.ensure_one()
        result = super()._program_check_compute_points(programs)
        # already applied programs in the order
        order_programs = self.order_line.reward_id.program_id

        promo_programs = programs.filtered(lambda p: p.program_type == "promo_code")
        incompatible_programs = promo_programs.filtered(
            lambda p: p.is_incompatible_promotion_all == True
        )
        program_to_remove = None
        if promo_programs:
            print(
                f"Incompatible programs: {incompatible_programs.mapped('name')}"
            )
            if len(incompatible_programs) > 0 and len(promo_programs) > 1:
                program_to_remove = promo_programs[-1]

        for program in result:
            if any({x in order_programs for x in program.incompatible_promotion_ids}):
                result[program] = {
                    "error": _(
                        "This promotion is incompatible with other set already in the "
                        "order so it can't be applied."
                    )
                }
        if program_to_remove:
            result[program_to_remove] = {
                "error": _(
                    "This promotion is incompatible with other promotions already "
                    "applied in the order so it can't be applied."
                )
            }

        print(result)
        return result
