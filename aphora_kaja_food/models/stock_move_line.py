# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api


class StockMove(models.Model):
    _inherit = 'stock.move'

    aphora_batch_uom_qty = fields.Float(string="By Batch", digits='Product Unit of Measure')

    def _compute_aphora_batch_uom_qty(self):
        for move in self:
            if move.raw_material_production_id and move.raw_material_production_id.aphora_batch_size > 0:
                batch_count = move.raw_material_production_id.product_qty / move.raw_material_production_id.aphora_batch_size
                move.aphora_batch_uom_qty = move.product_uom_qty / batch_count
            else:
                move.aphora_batch_uom_qty = 0.0

    @api.onchange('product_uom_qty')
    def _onchange_product_uom_qty(self):
        super()._onchange_product_uom_qty()
        self._compute_aphora_batch_uom_qty()

class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    aphora_use_date = fields.Datetime(related='lot_id.use_date')
