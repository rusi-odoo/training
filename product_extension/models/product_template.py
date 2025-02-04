from odoo import models, fields, api
from odoo.exceptions import AccessError, ValidationError


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    def _default_product_status(self):
        return self.env['product.status'].search([('change_up_group_id', '=', self.env.ref('base.group_user').id)], limit=1)

     # In excel sheet it was mention to keep product_status field Char but i think it would be M2O field
    product_status_id = fields.Many2one('product.status', required=True, default=_default_product_status)
    customer_product_code = fields.Char(string='Customer Reference')
    hs_code = fields.Char(string='HS Code', required=True)
    palletspec_ids = fields.One2many(
        'product.palletspec', 'product_tmpl_id', string="Pallet Specifications")
    landing_cost = fields.Float(string='Landing Cost')
    margin = fields.Float(string='Margin', compute='_compute_margin')
    is_archive = fields.Boolean(string='Archive')
    is_pricing = fields.Boolean(string='Pricing')
    is_active = fields.Boolean(string='Active')
    is_dormant = fields.Boolean(string='Dormant')
    is_npd = fields.Boolean(string='NPD')

    @api.constrains('product_status_id')
    def _check_product_status(self):
        if self.product_status_id.change_up_group_id.id not in self.env.user.groups_id.ids:
            raise ValidationError("You are not authorized to change the product status.")

    @api.depends('landing_cost', 'list_price', 'standard_price')
    def _compute_margin(self):
        for product in self:
            if product.list_price == 0:
                product.margin = 0
            else:
                product.margin = ((product.list_price - (product.standard_price + product.landing_cost)) / product.list_price)

    @api.model
    def write(self, vals):
        if 'product_status_id' in vals:
            new_status = self.product_status_id.browse(vals['product_status_id'])
            if self.is_archive is True:
                if ('is_pricing' not in vals and 'is_active' not in vals) or ('is_pricing' in vals and vals['is_pricing'] is False) or ('is_active' in vals and vals['is_active'] is False):
                    raise ValidationError(('Products in "Archived" status can only be moved to "Pricing" or "Active".'))

                elif self.product_status_id.change_down_group_id.id and self.product_status_id.change_down_group_id.id not in self.env.user.groups_id.ids:
                    raise ValidationError(('You are not authorized to change status to lower hierarchy'))

                else:
                    self.is_archive = False

            elif new_status.hierarchy <= self.product_status_id.hierarchy:
                raise ValidationError(('Status changes cannot be made to a lower hierarchy'))
            else:
                self.is_pricing = False
                self.is_active = False
        return super(ProductTemplate, self).write(vals)
