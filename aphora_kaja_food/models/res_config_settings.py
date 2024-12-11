# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    aphora_delivery_note = fields.Html(related="company_id.aphora_delivery_note", string="Default Delivery Note", readonly=False)
