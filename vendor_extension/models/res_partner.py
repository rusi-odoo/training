from odoo import models, fields, api
from odoo.exceptions import AccessError, ValidationError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    vendor_status_id=fields.Many2one('vendor.status')
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

    certification_ids = fields.Many2many('certification', string="Certifications")

    gfsi_scheme_id = fields.Many2one('gfsi.scheme', string="GFSI Scheme")

    gfsi_grade_id = fields.Many2one('gfsi.grade', string="GFSI Grade")
    

    def write(self, values):
        if 'vendor_status_id' in values:
            new_status = self.env['vendor.status'].browse(values['vendor_status_id'])
            if new_status.name != 'Active':
                current_user = self.env.user
                if new_status.hierarchy < self.vendor_status_id.hierarchy:
                    raise ValidationError("You cannot change the status to a lower hierarchy level.")
                    
                if current_user not in new_status.change_user_ids:
                    raise ValidationError("You are not authorized to change the vendor status.")
               
        return super(ResPartner, self).write(values)
    