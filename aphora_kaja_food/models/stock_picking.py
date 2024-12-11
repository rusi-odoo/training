# -*- coding: utf-8 -*-


from odoo import models, fields

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    aphora_shipping_weight_adjusted = fields.Float("Adjusted Shipping Weight")
    aphora_delivery_note = fields.Html(string='Delivery Note', default=lambda self: self.env.company.aphora_delivery_note)
