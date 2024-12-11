# -*- coding: utf-8 -*-

from odoo import api, fields, models


class MrpProduction(models.Model):
    _inherit = "mrp.production"

    aphora_date_finished_confirmed = fields.Boolean("End Date Confirmed")
    aphora_partner_id = fields.Many2one(
        "res.partner",
        string="Customer",
        compute="_compute_aphora_partner_id",
        store=True,
    )
    aphora_note = fields.Html("Note", translate=True)
    aphora_batch_size = fields.Float(
        string="Batch Size", digits="Product Unit of Measure"
    )
    aphora_allergen_ids = fields.Many2many(
        "aphora.product.allergen", string="Allergenes"
    )
    aphora_description_production = fields.Html(string="Production Description")
    aphora_coating_note = fields.Char(string="Coating Note")
    aphora_shipping_note = fields.Html(string="Shipping Note")
    aphora_tray_label = fields.Html(string="Tray Label")
    aphora_lot_nomenclature = fields.Char(string="Nomenclature")
    aphora_retention_sample = fields.Char(string="Retention Sample")
    aphora_best_before_date_production = fields.Char(
        string="Best Before Date (Production)",
    )
    aphora_best_before_date_customer = fields.Char(
        string="Best Before Date (Customer)",
    )
    aphora_best_before_date_sheet = fields.Char(
        string="Best Before Date (Product Sheet)",
    )
    aphora_residual_term_customer = fields.Char(
        string="Remaining Term (Customer)",
    )
    aphora_actitivity_of_water = fields.Char(string="Activity of Water")
    aphora_description_quality = fields.Html(string="Quality Control")
    aphora_weight_check = fields.Char(string="Weight Control")
    aphora_units_per_tray = fields.Char(string="Units/Tray")
    aphora_trays_per_layer = fields.Char(string="Trays/Layer")
    aphora_layers_per_pallet = fields.Char(string="Layers/Pallet")
    aphora_has_kits = fields.Boolean(
        string="Has Kits", compute="_compute_aphora_has_kits"
    )
    aphora_has_kits = fields.Boolean(string='Has Kits', compute='_compute_aphora_has_kits')
    aphora_weight_adjusted = fields.Float(string='Adjusted Weight')

    @api.depends("move_raw_ids")
    def _compute_aphora_has_kits(self):
        for production in self:
            production.aphora_has_kits = (
                "phantom" in production.move_raw_ids.bom_line_id.bom_id.mapped("type")
            )

    @api.depends("move_raw_ids")
    def _compute_aphora_has_kits(self):
        for production in self:
            production.aphora_has_kits = (
                "phantom" in production.move_raw_ids.bom_line_id.bom_id.mapped("type")
            )

    @api.depends(
        "procurement_group_id.mrp_production_ids.move_dest_ids.group_id.sale_id",
        "aphora_partner_id",
    )
    def _compute_aphora_partner_id(self):
        for record in self:
            partner = False
            if (
                record.procurement_group_id.mrp_production_ids.move_dest_ids.group_id.sale_id
            ):
                partner = (
                    record.procurement_group_id.mrp_production_ids.move_dest_ids.group_id.sale_id.partner_id
                )
            if record._get_sources().ids:
                partner = record._get_sources()[0].aphora_partner_id
            record.aphora_partner_id = partner

    def copy(self, default=None):
        """When a Manufacturing Order creates a backorder, it should inherit the aphora_partner_id
        field from the original order. Ensure that the copy method is overridden to handle this
        """
        default = dict(default or {})
        default["aphora_partner_id"] = self.aphora_partner_id.id
        return super(MrpProduction, self).copy(default)

    @api.onchange("product_qty", "aphora_batch_size")
    def _onchange_product_qty(self):
        self.move_raw_ids._compute_aphora_batch_uom_qty()

    @api.depends(
        "company_id",
        "bom_id",
        "product_id",
        "product_qty",
        "product_uom_id",
        "location_src_id",
    )
    def _compute_move_raw_ids(self):
        self = self.with_context(manage_sequence=True)
        super()._compute_move_raw_ids()
        for production in self:
            production.move_raw_ids._compute_aphora_batch_uom_qty()

    def _split_productions(self, amounts=False, cancel_remaining_qty=False, set_consumed_qty=False):
        productions = super()._split_productions(amounts=amounts, cancel_remaining_qty=cancel_remaining_qty, set_consumed_qty=set_consumed_qty)
        for production in productions:
            production.move_raw_ids._compute_aphora_batch_uom_qty()
        return productions

    @api.onchange("product_id")
    def _onchange_product_id(self):
        super()._onchange_product_id()
        self.aphora_allergen_ids = self.product_id.aphora_allergen_ids
        self.aphora_description_production = (
            self.product_id.aphora_description_production
        )
        self.aphora_coating_note = self.product_id.aphora_coating_note
        self.aphora_shipping_note = self.product_id.aphora_shipping_note
        self.aphora_tray_label = self.product_id.aphora_tray_label
        self.aphora_lot_nomenclature = self.product_id.aphora_lot_nomenclature
        self.aphora_retention_sample = self.product_id.aphora_retention_sample
        self.aphora_best_before_date_production = (
            self.product_id.aphora_best_before_date_production
        )
        self.aphora_best_before_date_customer = (
            self.product_id.aphora_best_before_date_customer
        )
        self.aphora_best_before_date_sheet = (
            self.product_id.aphora_best_before_date_sheet
        )
        self.aphora_residual_term_customer = (
            self.product_id.aphora_residual_term_customer
        )
        self.aphora_actitivity_of_water = self.product_id.aphora_actitivity_of_water
        self.aphora_description_quality = self.product_id.aphora_description_quality
        self.aphora_weight_check = self.product_id.aphora_weight_check
        self.aphora_units_per_tray = self.product_id.aphora_units_per_tray
        self.aphora_trays_per_layer = self.product_id.aphora_trays_per_layer
        self.aphora_layers_per_pallet = self.product_id.aphora_layers_per_pallet
        self.aphora_weight_adjusted = self.product_id.aphora_weight_adjusted

    def _get_moves_raw_values(self):
        moves = super()._get_moves_raw_values()
        if self.env.context.get('manage_sequence'):
            count = 1
            for move in moves:
                move['sequence'] = count
                count += 1
        return moves
