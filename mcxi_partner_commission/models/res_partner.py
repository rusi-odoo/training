# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = "res.partner"

    commission_rate = fields.Selection([
        ('percentage', 'Percentage'),
        ('fixed', 'Fixed Amount'),
    ], default='percentage', string='Commission Rate', required=True, inverse="_inverse_commission_rate")
    commission = fields.Float(string='Commission')
    commission_journal_id = fields.Many2one('account.account', string='Commission GL Account')
    account_owner_id = fields.Many2one('res.users', string="Account Owner")
    dsm_id = fields.Many2one('hr.employee', string="DSM")
    bdm_id = fields.Many2one('hr.employee', string="BDM")
    is_account_commission = fields.Boolean(string="Account Commission")
    is_dsm_commission = fields.Boolean(string="DSM Commission")
    is_bdm_commission = fields.Boolean(string="BDM Commission")
    account_type = fields.Selection([
        ('aerospace','Aerospace'),
        ('agent','Agent'),
        ('agent_tpa','Agent - TPA'),
        ('auto_dealer_independent','Auto Dealer - Independent'),
        ('auto_dealer','Auto Dealer'),
        ('rv_dealer','RV Dealer'),
        ('motorcycle_dealer','Motorcycle Dealer'),
        ('marine_dealer','Marine Dealer'),
        ('distributor','Distributor'),
        ('end_user','End User'),
        ('n/a','N/A'),
        ('vendor','Vendor'),
        ('rv_marine_dealer','RV/Marine Dealer'),
        ('tpa','TPA')
    ], string ="Account Type")
    agent_ids = fields.Many2many('res.partner', 'partner_agent_rel','partner_id', 
        'agent_id', string='Agent',
        domain=[
            '|', 
            ('account_type', '=', 'agent'), 
            ('account_type', '=', 'agent_tpa')
        ])
    sales_channel = fields.Selection([
        ('direct', 'Direct'),
        ('tpa', 'TPA'),
        ('distributor', 'Distributor'),
        ('agent', 'Agent (External)'),
        ('sales', 'Sales (Internal)')
    ], string='Dealer Category', default="sales")
    product_commission_ids = fields.One2many('partner.product.commission', 'partner_id', string="Product Commissions")

    @api.constrains('is_account_commission', 'is_dsm_commission', 'is_bdm_commission')
    def _check_valid_char_value(self):
        for record in self:
            if record.is_account_commission and not record.account_owner_id.partner_id.commission:
                raise ValidationError(_('Can not find Commission for Acctount Owner. Kindly fill commission for the partner %s.', record.account_owner_id.partner_id.name))
            if record.is_dsm_commission and not record.dsm_id.work_contact_id.commission:
                raise ValidationError(_('Can not find Commission for DSM. Kindly fill commission for the partner %s.', record.dsm_id.work_contact_id.name))
            if record.is_bdm_commission and not record.bdm_id.work_contact_id.commission:
                raise ValidationError(_('Can not find Commission for BDM. Kindly fill commission for the partner %s.', record.bdm_id.work_contact_id.name))

    def _inverse_commission_rate(self):
        for record in self:
            if record.commission_rate == 'percentage':
                record.commission = 0.0
