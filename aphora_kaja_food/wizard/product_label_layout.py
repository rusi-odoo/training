# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields

class ProductLabelLayout(models.TransientModel):
    _inherit = "product.label.layout"

    print_format = fields.Selection(selection_add=[
        ('aphora_8x8_no_price', '8 x 8'),
        ('aphora_8x8', '8 x 8 with price'),
    ], default='aphora_8x8_no_price', ondelete={'aphora_8x8': 'cascade', 'aphora_8x8_no_price': 'cascade'})

    def _prepare_report_data(self):
        xml_id, data = super()._prepare_report_data()
        if self.print_format == 'aphora_8x8_no_price':
            xml_id = 'aphora_kaja_food.aphora_report_product_template_label_8x8_no_price'
        elif self.print_format == 'aphora_8x8':
            xml_id = 'aphora_kaja_food.aphora_report_product_template_label_8x8'
        return xml_id, data
