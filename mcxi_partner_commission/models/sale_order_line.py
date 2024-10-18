# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    commission = fields.Monetary(string='Commission', compute='_compute_commission')


    @api.depends('order_id.mcxi_referrer_id.commission', 'product_uom_qty')
    def _compute_commission(self):
        for record in self:
            record.commission = record.order_id.mcxi_referrer_id.commission * record.product_uom_qty
