from odoo import models, fields, api


class ProductPackaging(models.Model):
    _inherit = 'product.packaging'

    case_width = fields.Integer(string="Case Width (mm)")
    case_length = fields.Integer(string="Case Length (mm)")
    case_height = fields.Integer(string="Case Height (mm)")
    case_net_weight = fields.Float(string="Case Net Weight")
    case_gross_weight = fields.Float(string="Case Gross Weight (Kg)")
    case_volume = fields.Float(string="Case Volume (m³)", compute="_compute_case_volume")

    @api.depends('case_width', 'case_length', 'case_height')
    def _compute_case_volume(self):
        for product in self:
            # Convert mm³ to m³ by dividing by 1,000,000,000 (mm³ to m³)
            product.case_volume = (product.case_width * product.case_length * product.case_height) / 1e9
           