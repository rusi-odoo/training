# -*- coding: utf-8 -*-
from odoo import models


class StockRule(models.Model):
    _inherit = "stock.rule"

    def _should_auto_confirm_procurement_mo(self, p):
        """
        Updates custom fields taken in the legacy tab by calling the onchange method
        when a manufacturing order (MO) is created from MTO (Make to Order) or a reordering rule.
        This method is called only from the _run_manufacture method.
        """
        res = super()._should_auto_confirm_procurement_mo(p)
        p._onchange_product_id()
        return res
