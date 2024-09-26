from odoo import models, api
from odoo.exceptions import AccessError, ValidationError


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    @api.constrains('partner_id')
    def _check_partner_status(self):
        partner = self.partner_id
        if partner.vendor_status_id.prevent_po == 'yes':
            raise ValidationError("You cannot create a PO for this vendor in its current status.")
            
        elif partner.vendor_status_id.prevent_po == 'no':
            partner.vendor_status_id = self.env.ref('vendor_extension.vendor_status_active').id

        if partner.vendor_status_id.prevent_po == 'alert':
            self.env['mail.activity'].create({
                'res_name': self.name,
                'automated': True,
                'activity_type_id': self.env.ref('mail.mail_activity_data_todo').id,
                'user_id': partner.vendor_status_id.notify_user_id.id,
                'res_id': self.id,
                'res_model_id': self.env.ref('vendor_extension.model_purchase_order').id,
            })