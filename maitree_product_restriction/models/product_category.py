from odoo import models, fields


class ProductCategory(models.Model):
    _inherit = 'product.category'

    maitree_allowed_users = fields.Many2many('res.users', string="Allowed Users", help="Users allowed to access products in this category.")
