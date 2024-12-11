# -*- coding: utf-8 -*-

from odoo import fields, models


class ProductGroup(models.Model):
    _name = "aphora.product.group"
    _description = "Product Group"

    name = fields.Char()


class ProductProperty(models.Model):
    _name = "aphora.product.property"
    _description = "Product Property"

    name = fields.Char()


class ProductAllergen(models.Model):
    _name = "aphora.product.allergen"
    _description = "Product Allergen"

    name = fields.Char()


class ProductTrace(models.Model):
    _name = "aphora.product.trace"
    _description = "Product Trace"

    name = fields.Char()


class PackagingType(models.Model):
    _name = "aphora.product.pack_type"
    _description = "Packaging Type"

    name = fields.Char()
