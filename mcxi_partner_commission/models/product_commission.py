# -- coding: utf-8 --
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields

class PartnerProductCommission(models.Model):
    _name = 'partner.product.commission'
    _description = 'Partner Product Commission'

    partner_id = fields.Many2one('res.partner',string="Partner")
    product_template_id = fields.Many2one('product.template', string="Product")
    commission = fields.Float(string="Commission")
