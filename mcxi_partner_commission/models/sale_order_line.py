# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    commission = fields.Monetary(string='Commission', compute='_compute_commission')
    product_ids = fields.Many2many('product.template', compute='_compute_product_ids', string="Products")
    agent_1_commission = fields.Monetary(string='Agent1 Commission', compute='_compute_agent_commission')
    agent_2_commission = fields.Monetary(string='Agent2 Commission', compute='_compute_agent_commission')
    agent_3_commission = fields.Monetary(string='Agent3 Commission', compute='_compute_agent_commission')

    @api.depends('order_id.mcxi_referrer_id', 'product_uom_qty', 'order_id.partner_id')
    def _compute_commission(self):
        for line in self:
            line.commission = 0.0
            commission_line = line.order_id.partner_id.product_commission_ids.filtered(
                lambda c: c.product_template_id == line.product_id.product_tmpl_id)
            if commission_line and commission_line.commission:
                line.commission = commission_line.commission * line.product_uom_qty
            elif line.order_id.mcxi_referrer_id and line.order_id.mcxi_referrer_id.commission:
                line.commission = line.order_id.mcxi_referrer_id.commission * line.product_uom_qty

    @api.depends('order_id.partner_id')
    def _compute_product_ids(self):
        for line in self:
            if line.order_id.partner_id:
                line.product_ids = line.order_id.partner_id.product_commission_ids.mapped('product_template_id')
            else:
                line.product_ids = []

    @api.depends('order_id.agent_1_id', 'order_id.agent_2_id', 'order_id.agent_3_id', 'product_uom_qty')
    def _compute_agent_commission(self):
        for line in self:
            line.agent_1_commission = 0.0
            line.agent_2_commission = 0.0
            line.agent_3_commission = 0.0
            if line.order_id.agent_1_id and line.order_id.agent_1_id.commission:
                line.agent_1_commission = line.order_id.agent_1_id.commission * line.product_uom_qty
            if line.order_id.agent_2_id and line.order_id.agent_2_id.commission:
                line.agent_2_commission = line.order_id.agent_2_id.commission * line.product_uom_qty
            if line.order_id.agent_3_id and line.order_id.agent_3_id.commission:
                line.agent_3_commission = line.order_id.agent_3_id.commission * line.product_uom_qty
