from odoo import models, fields, api
from odoo.exceptions import AccessError, ValidationError


class ProductTemplate(models.Model):
    _inherit = 'product.template'
    
    # In excel sheet it was mention to keep product_status field Char but i think it would be M2O field
    product_status_id = fields.Many2one('product.status', required=True)
    customer_product_code = fields.Char(string='Customer Reference')
    hs_code = fields.Char(string='HS Code', required=True)
    palletspec_ids = fields.One2many('product.palletspec', 'product_tmpl_id', string="Pallet Specifications")
    landing_cost = fields.Float(string='Landing Cost', required=True)
    margin = fields.Float(string='Margin', compute='_compute_margin')

    @api.depends('landing_cost', 'list_price', 'standard_price')
    def _compute_margin(self):
        for product in self:
            product.margin = (
                (product.list_price - (product.standard_price + product.landing_cost)) / product.list_price)


    @api.model
    def write(self, vals):
        if 'product_status_id' in vals:
            new_status = self.product_status_id.browse(vals['product_status_id'])
            current_status = self.product_status_id

            # archived_status = self.env.ref('product_extension.product_status_archived')
            # pricing_status = self.env.ref('product_extension.product_status_pricing')
            # active_status = self.env.ref('product_extension.product_status_active')
            archived_status = self.product_status_id.search([('name','=','Archived')])
            pricing_status = self.product_status_id.search([('name','=','Pricing')])
            active_status = self.product_status_id.search([('name','=','Active')])

            if current_status == archived_status:
                 if new_status not in (pricing_status, active_status):
                     raise ValidationError(('Products in "Archived" status can only be moved to "Pricing" or "Active".'))

            elif new_status.hierarchy <= current_status.hierarchy:
                raise ValidationError(('Status changes cannot be made to a lower hierarchy'))

            if new_status.change_up_group_id and new_status.change_up_group_id not in self.env.user.groups_id:
                raise AccessError((f'You do not have the necessary permissions to change product status to {new_status.name}'))

        return super(ProductTemplate, self).write(vals)
