# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = "res.partner"

    commission_rate = fields.Selection([
        ('percentage', 'Percentage'),
        ('fixed', 'Fixed Amount'),
    ], default='percentage', string='Commission Rate', required=True, inverse="_inverse_commission_rate")
    commission = fields.Float(string='Commission')
    commission_journal_id = fields.Many2one('account.account', string='Commission GL Account')
    contact_type = fields.Selection([
        ('customer','Customer'),
        ('vendor','Vendor'),
        ('employee','Employee'),
        ],default='customer',required=True)
    dealer_code = fields.Char(string='Dealer Code')
    dsm_id = fields.Many2one(string='DSM',comodel_name="hr.employee")
    sales_channel = fields.Selection(string='Dealer Category' ,selection=[
        ('direct','Direct'),
        ('tpa','TPA'),
        ('agent','Agent'),
        ('distributor','Distributor'),
        ])

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('contact_type') == 'customer' and not vals.get('dealer_code'):
                vals['dealer_code'] = self.env['ir.sequence'].next_by_code('res.partner.dealer') or _('New')
        return super(ResPartner, self).create(vals_list)

    def _inverse_commission_rate(self):
        for record in self:
            if record.commission_rate == 'percentage':
                record.commission = 0.0
