from odoo import models, fields


class ProductStatus(models.Model):
    _name = 'product.status'
    _description = 'Product Status'

    name = fields.Char('Product Status', required=True)
    hierarchy = fields.Integer('Sequence', required=True)
    change_up_group_id = fields.Many2one(comodel_name='res.groups', string='Group Name - Status Change Up')
    change_down_group_id = fields.Many2one(comodel_name='res.groups', string='Group Name - Status Change Down')
