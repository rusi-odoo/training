# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Document(models.Model):
    _inherit = "documents.document"

    aphora_validity_date = fields.Date("Expiration")
