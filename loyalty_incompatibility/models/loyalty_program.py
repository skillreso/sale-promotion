# Copyright 2021 Tecnativa - David Vidal
# Copyright 2023 Tecnativa - Stefan Ungureanu
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import fields, models
import logging
_logger = logging.getLogger("Skillreso")

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
        _logger.info("_inverse_incompatible_promotion_ids")
        for program in self:
            _logger.info("program : %s" % program)
            _logger.info("incompatible_promotion_ids : %s" % program.incompatible_promotion_ids)
            incompatible_programs = self.search(
                [
                    ("incompatible_promotion_ids", "in", program.ids),
                    ("id", "!=", program.id),
                ]
            )
            _logger.info("incompatible_programs : %s" % incompatible_programs)
            to_remove_programs = (
                incompatible_programs - program.incompatible_promotion_ids
            )
            _logger.info("to_remove_programs : %s" % to_remove_programs)
            _logger.info("before : %s" % program.incompatible_promotion_ids.incompatible_promotion_ids)
            program.incompatible_promotion_ids.incompatible_promotion_ids |= program
            _logger.info("after : %s" % program.incompatible_promotion_ids.incompatible_promotion_ids)
            _logger.info("before2 : %s" % to_remove_programs.incompatible_promotion_ids)
            to_remove_programs.incompatible_promotion_ids -= program
            _logger.info("after2 : %s" % to_remove_programs.incompatible_promotion_ids)
