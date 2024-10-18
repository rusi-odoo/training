# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    mcxi_referrer_id = fields.Many2one('res.partner', string='Referrer (Fixed)', inverse='_inverse_mcxi_referrer_id')
    referrer_id = fields.Many2one('res.partner', 'Referrer', domain=[('grade_id', '!=', False)], tracking=True, inverse='_inverse_referrer_id')


    def _inverse_mcxi_referrer_id(self):
        for record in self:
            if record.referrer_id:
                record.mcxi_referrer_id = False

    def _inverse_referrer_id(self):
        for record in self:
            if record.mcxi_referrer_id:
                record.referrer_id = False
