# -*- coding: utf-8 -*-

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    aphora_is_approved = fields.Boolean("Approved")
    aphora_is_bio = fields.Boolean("Bio")
    aphora_is_consignment = fields.Boolean("Consignment")
    aphora_has_coating = fields.Boolean("Coating")
    aphora_gmo = fields.Char("GMO")
    aphora_gmo_2 = fields.Selection(selection=[
        ('none','Complies with EU Regulation 1829/2003 and 1830/2003')
    ], string="GMO")
    aphora_ionizing_radiation = fields.Char("Ionizing Radiation")
    aphora_ionizing_radiation_2 = fields.Selection(selection=[
        ('none','The product or its ingredients have not been treated with ionizing radiation.')
    ], string="Ionizing Radiation")
    aphora_additives = fields.Char("Additives")
    aphora_additives_2 = fields.Selection(selection=[('none','The product contains no additives (antioxidants, preservatives or other chemical additives)')],string="Additives")
    aphora_needs_quality_check = fields.Boolean("Quality Check")
    aphora_needs_certificate = fields.Boolean("Certificate")
    aphora_lot_nomenclature = fields.Char("Nomenclature")
    aphora_best_before_date_production = fields.Char("Best Before Date (Production)")
    aphora_retention_sample = fields.Char("Retention Sample")
    aphora_coating_note = fields.Char("Coating Note")
    aphora_weight_check = fields.Char("Weight Control")
    aphora_nutritional_values_source = fields.Char("Source (Nutrition)")
    aphora_raw_materials_info_source = fields.Char("Source (Raw Materials)")
    aphora_creator = fields.Char("Creator")
    aphora_approver = fields.Char("Approver")
    aphora_actitivity_of_water = fields.Char("Activity of Water")
    aphora_residual_term_customer = fields.Char("Remaining Term (Customer)")
    aphora_best_before_date_customer = fields.Char("Best Before Date (Customer)")
    aphora_best_before_date_sheet = fields.Char("Best Before Date (Product Sheet)")
    aphora_product_ean = fields.Char("Product EAN")
    aphora_tray_ean = fields.Char("Tray EAN")
    aphora_package_ean = fields.Char("Package EAN")
    aphora_customer_code = fields.Char("Customer Reference")
    aphora_customer_tray_code = fields.Char("Customer Tray Reference")
    aphora_approver_development = fields.Char("Approver (Development)")
    aphora_appearance = fields.Char("Appearance")
    aphora_taste = fields.Char("Taste")
    aphora_consistency = fields.Char("Consistency")
    aphora_color = fields.Char("Color")
    aphora_smell = fields.Char("Smell")
    aphora_size_shape = fields.Char("Size/Shape")
    aphora_storage_info = fields.Char(string="Storage Information")
    aphora_description_production = fields.Html("Production Description", translate=True)
    aphora_ccp = fields.Selection([
        ('magnet', 'Magnet'),
        ('metal', 'Metal Detector'),
        ('magnet_metal', 'Magnet, Metal Detector'),
    ], string="CCP")
    aphora_billing_dual_system = fields.Selection([
        ('customer', 'Customer'),
        ('company', 'Kaja Food')], string="Billing Dual System")
    aphora_warning_note = fields.Html("Warnings")
    aphora_warning_note_2 = fields.Selection(selection=[
        ('residue', 'May contain shells and core residues'),
        ('laxative', 'May have a laxative effect if consumed in excess'),
        ('caffeine', 'Increased caffeine content. Not recommended for children and pregnant or breastfeeding women'),
        ('glucose', 'Source of glucose'),
        ('hemp', 'Contains hemp'),
        ('no_child', 'Keep out of reach of children')
    ], string="Warnings")
    aphora_shipping_note = fields.Html("Shipping Note")
    aphora_description_extra = fields.Html("Extra Note")
    aphora_description_mibi = fields.Html("Mibi Instructions")
    aphora_description_quality = fields.Html("Quality Control")
    aphora_description_internal = fields.Html("Internal Description")
    aphora_description_long = fields.Html("Long Description")
    aphora_tray_label = fields.Html("Tray Label")
    aphora_lmiv_name = fields.Html("Description (LMIV)")
    aphora_ingredients = fields.Html("Ingredients")
    aphora_units_per_tray = fields.Char("Units/Tray")
    aphora_trays_per_layer = fields.Char("Trays/Layer")
    aphora_layers_per_pallet = fields.Char("Layers/Pallet")
    aphora_group_id = fields.Many2one("aphora.product.group", string="Product Group")
    aphora_owner = fields.Many2one("res.partner", string="Owner")
    aphora_property_ids = fields.Many2many("aphora.product.property", string="Properties")
    aphora_allergen_ids = fields.Many2many("aphora.product.allergen", string="Allergenes")
    aphora_trace_ids = fields.Many2many("aphora.product.trace", string="Traces of")
    aphora_pack_type_1_id = fields.Many2one("aphora.product.pack_type", string="Primary Packaging Type")
    aphora_pack_type_2_id = fields.Many2one("aphora.product.pack_type", string="Secondary Packaging Type")
    aphora_pack_type_3_id = fields.Many2one("aphora.product.pack_type", string="Tertiary Packaging Type")
    aphora_energy_kj = fields.Float("Energy (kJ)")
    aphora_energy_kcal = fields.Float("Energy (kcal)")
    aphora_fat_level = fields.Float("Fat")
    aphora_fat_level_satured = fields.Float("Saturated Fat")
    aphora_carbohydrates_level = fields.Float("Carbohydrates")
    aphora_sugar_level = fields.Float("Sugar")
    aphora_protein_level = fields.Float("Protein")
    aphora_salt_level = fields.Float("Salt")
    aphora_surplus_quantity = fields.Float("Surplus Quantity (%)")
    aphora_filling_weight = fields.Float("Filling Weight")
    aphora_fiber_level = fields.Float("Fiber")
    aphora_poly_alc = fields.Float("Polyhydric Alcohols")
    aphora_poly_alc_erithritol = fields.Float("Polyhydric Alcohols (Erithritol)")
    aphora_weight_adjusted = fields.Float("Adjusted Weight")
