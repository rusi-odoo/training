from odoo import models, fields


class ProductCategory(models.Model):
    _inherit = 'product.category'

    description = fields.Char(string="Category Description")