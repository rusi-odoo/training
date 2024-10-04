from odoo import models, fields, api
from odoo.exceptions import AccessError, ValidationError


class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    def _default_vendor_status(self):
        user = self.env['res.users'].search([('active', '=', True)]).ids
        return self.env['vendor.status'].search([('change_user_ids', '=', user)])

    vendor_status_id = fields.Many2one('vendor.status', default=_default_vendor_status)
    sedex_registered = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No')
    ], string="Sedex Registered?")

    sedex_no = fields.Char(string="Sedex Number")

    ethical_audit = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No')
    ], string="Ethical Audit Conducted?")

    gfsi_certification = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No')
    ], string="GFSI Certification")

    fsc_certified = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No')
    ], string="FSC Certified?")

    pefc_certified = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No')
    ], string="PEFC Certified?")

    certification_ids = fields.Many2many(
        'certification', string="Certifications")

    gfsi_scheme_id = fields.Many2one('gfsi.scheme', string="GFSI Scheme")

    gfsi_grade_id = fields.Many2one('gfsi.grade', string="GFSI Grade")
    
    @api.model
    def write(self, values):
        current_hierarchy=self.vendor_status_id.hierarchy
        if 'vendor_status_id' in values:
            new_status = self.env['vendor.status'].browse(values['vendor_status_id'])
            if len(new_status.change_user_ids) > 0:
                if new_status.hierarchy < current_hierarchy:
                    raise ValidationError("You cannot change the status to a lower hierarchy level.")
            else:
                raise ValidationError("You cannot change the status to Active manually")
        return super(ResPartner, self).write(values)
    
    @api.constrains('vendor_status_id')
    def _check_vendor_status(self):
        if self.env.user.id not in self.vendor_status_id.change_user_ids.ids:
            raise ValidationError("You are not authorized to change the vendor status.")
