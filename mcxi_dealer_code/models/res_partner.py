# -- coding: utf-8 --
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import _, fields, models, api


class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    contact_type = fields.Selection([
        ('customer','Customer'),
        ('vendor','Vendor'),
        ('employee','Employee'),
        ('1099', '1099'),
        ],default='customer',required=True)
    dealer_code = fields.Char(string='Dealer Code')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('contact_type') == 'customer' and not vals.get('dealer_code'):
                vals['dealer_code'] = self.env['ir.sequence'].next_by_code('res.partner.dealer') or _('New')
        return super(ResPartner, self).create(vals_list)
