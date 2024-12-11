# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


from odoo import _, models
from odoo.addons.product.report.product_label_report import _prepare_data


class ReportProductTemplateLabel8x8NoPrice(models.AbstractModel):
    _name = 'report.aphora_kaja_food.aphora_report_producttemplatelabel8x8noprice'
    _table = 'aphora_report_producttemplatelabel8x8_no_price'
    _description = 'Aphora Product Label Report 8x8 No Price'

    def _get_report_values(self, docids, data):
        return _prepare_data(self.env, docids, data)

class ReportProductTemplateLabel8x8(models.AbstractModel):
    _name = 'report.aphora_kaja_food.aphora_report_producttemplatelabel8x8'
    _table = "aphora_report_producttemplatelabel8x8"
    _description = 'Aphora Product Label Report 8x8'

    def _get_report_values(self, docids, data):
        return _prepare_data(self.env, docids, data)
