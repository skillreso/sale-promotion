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

        existing_promo_programs = order_programs.filtered(
            lambda p: p.program_type == "promo_code"
        )
        promo_programs = programs.filtered(lambda p: p.program_type == "promo_code")

        print('AAAAAAAAAAAAAAAAAAA  ',existing_promo_programs, promo_programs)
        if not existing_promo_programs:
            print('C VIDEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE')
        if not promo_programs:
            print('C VIDEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE 2')

        to_remove: bool = False
        program_to_remove = None

        if existing_promo_programs and promo_programs:
            # Comparer uniquement les programmes ayant des IDs différents
            for existing_program in existing_promo_programs:
                for new_program in promo_programs:
                    if existing_program.id != new_program.id:
                        # Si l'un des deux est incompatible avec d'autres promotions
                        if existing_program.is_incompatible_promotion_all or new_program.is_incompatible_promotion_all:
                            to_remove = True
                            if existing_program.is_incompatible_promotion_all:
                                program_to_remove = existing_program
                            elif new_program.is_incompatible_promotion_all:
                                program_to_remove = new_program
                            break
                if to_remove:
                    break


        for program in result:
            if to_remove and program_to_remove and program_to_remove == program:
                result[program] = {
                    "error": _(
                        "This promotion is incompatible with other promotions already "
                        "applied in the order so it can't be applied."
                    )
                }
            # If program is incompatible with specific programs
            if any({x in order_programs for x in program.incompatible_promotion_ids}):
                result[program] = {
                    "error": _(
                        "This promotion is incompatible with other set already in the "
                        "order so it can't be applied."
                    )
                }

        print(result)
        return result