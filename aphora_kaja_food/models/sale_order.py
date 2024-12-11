# -*- coding: utf-8 -*-

import json

from odoo import api, models, fields, _
from odoo.tools import format_date

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    aphora_commitment_date_confirmed = fields.Boolean('Delivery Date Confirmed')
    json_popover = fields.Char('JSON data for the popover widget', compute='_compute_json_popover', store=True)
    show_json_popover = fields.Boolean('Has late picking', compute='_compute_json_popover', store=True)

    @api.depends('picking_ids.delay_alert_date')
    def _compute_json_popover(self):
        for order in self:
            late_stock_picking = order.picking_ids.filtered(lambda p: p.delay_alert_date)
            order.json_popover = json.dumps({
                'popoverTemplate': 'sale_stock.DelayAlertWidget',
                'late_elements': [{
                        'id': late_move.id,
                        'name': late_move.display_name,
                        'model': 'stock.picking',
                    } for late_move in late_stock_picking
                ]
            })
            order.show_json_popover = bool(late_stock_picking)

    def _compute_l10n_din5008_template_data(self):
        super()._compute_l10n_din5008_template_data()
        for record in self:
            order_date_index = 0
            if record.state not in ('draft', 'sent') and record.commitment_date and record.aphora_commitment_date_confirmed:
                for index, item in enumerate(record.l10n_din5008_template_data):
                    if item[0] == 'Order Date' or item[0] == _('Order Date'):
                        order_date_index = index
                        break
                if order_date_index:
                    record.l10n_din5008_template_data.insert(order_date_index + 1, (_("Delivery Date"), format_date(self.env, record.commitment_date)))
