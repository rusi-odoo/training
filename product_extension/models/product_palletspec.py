from odoo import models, fields, api


class ProductPalletSpec(models.Model):
    _name = 'product.palletspec'
    _description = 'Product Pallet Specification'

    product_tmpl_id = fields.Many2one('product.template', string="Product")

    name = fields.Char(string="Pallet Type", required=True)
    cases_per_layer = fields.Float(string="Cases/Layer")
    layers_per_pallet = fields.Float(string="Layers/Pallet")
    pallet_quantity = fields.Float(string="Pallet Quantity",compute="_compute_pallet_quantity")
    product_uom_id = fields.Many2one('uom.uom', string="Unit of Measure")
    pallet_width = fields.Integer(string="Pallet Width (m)")
    pallet_length = fields.Integer(string="Pallet Length (m)")
    pallet_height = fields.Integer(string="Pallet Height (m)")
    pallet_weight = fields.Float(string="Pallet Weight (kg)")

    pallet_volume = fields.Float(string="Pallet Volume (m³)",compute="_compute_pallet_volume")

    pcs_per_pallet = fields.Integer(string="Pcs/Pallet",compute="_compute_pcs_per_pallet")

    @api.depends('cases_per_layer', 'layers_per_pallet')
    def _compute_pallet_quantity(self):
        for pallet in self:
            pallet.pallet_quantity = pallet.cases_per_layer * pallet.layers_per_pallet

    @api.depends('pallet_width', 'pallet_length', 'pallet_height')
    def _compute_pallet_volume(self):
        for pallet in self:
            pallet.pallet_volume = pallet.pallet_width * pallet.pallet_length * pallet.pallet_height

    @api.depends('cases_per_layer', 'layers_per_pallet', 'product_tmpl_id')
    def _compute_pcs_per_pallet(self):
        for pallet in self:
            if pallet.product_tmpl_id:
                package_qty=sum(pallet.product_tmpl_id.packaging_ids.mapped('qty'))
                pallet.pcs_per_pallet = (pallet.cases_per_layer * pallet.layers_per_pallet) * package_qty
            else:
                pallet.pcs_per_pallet = 0
