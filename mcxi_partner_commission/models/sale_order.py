# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, Command


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    mcxi_referrer_id = fields.Many2one('res.partner', string='Referrer (Fixed)', inverse='_inverse_mcxi_referrer_id')
    referrer_id = fields.Many2one('res.partner', 'Referrer', domain=[('grade_id', '!=', False)], tracking=True, inverse='_inverse_referrer_id')
    # agent_ids = fields.Many2many('res.partner', string='Agent Ids', compute='_compute_agent_ids')
    agent_domain = fields.Binary("Agent Domain",compute = '_compute_agent_domain')
    agent_1_id = fields.Many2one('res.partner', string='Agent 1')
    agent_2_id = fields.Many2one('res.partner', string='Agent 2')
    agent_3_id = fields.Many2one('res.partner', string='Agent 3')

    def _inverse_mcxi_referrer_id(self):
        for record in self:
            if record.referrer_id:
                record.mcxi_referrer_id = False

    def _inverse_referrer_id(self):
        for record in self:
            if record.mcxi_referrer_id:
                record.referrer_id = False

    @api.depends('partner_id', 'agent_1_id', 'agent_2_id', 'agent_3_id')
    def _compute_agent_domain(self):
        for order in self:
            selected_agents = []
            if order.agent_1_id:
                selected_agents.append(order.agent_1_id.id)
            if order.agent_2_id:
                selected_agents.append(order.agent_2_id.id)
            if order.agent_3_id:
                selected_agents.append(order.agent_3_id.id)
            partner_agent_ids = order.partner_id.agent_ids.ids
            order.agent_domain = [('id', 'in', partner_agent_ids), ('id', 'not in', selected_agents)]    
