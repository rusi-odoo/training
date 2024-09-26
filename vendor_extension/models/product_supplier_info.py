from odoo import fields, models,api

class ProductSupplierInfo(models.Model):
    _inherit = 'product.supplierinfo'
    
    qty_per_case = fields.Integer(string="Quantity per Case")
    cases_per_container = fields.Integer(string="Cases per Container")
    price_per_1000 = fields.Float(string="Cost per 1000")
    incoterm_id = fields.Many2one('account.incoterms', string="Incoterms")
    incoterm = fields.Integer(related='incoterm_id.id')
    