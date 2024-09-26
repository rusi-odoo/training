from odoo import models, fields
from odoo.exceptions import AccessError, ValidationError


class VendorStatus(models.Model):
    _name = 'vendor.status'
    _description = 'Vendor Status'
    _inherit = 'mail.thread'

    name = fields.Char('Vendor Status', required=True)
    hierarchy = fields.Integer('Sequence', required=True)
    change_user_ids = fields.Many2many(comodel_name='res.users', string='Status Change')
    prevent_po = fields.Selection(string="Prevent PO", selection=[('yes', 'Yes'), ('no', 'No'), ('alert', 'Alert')])
    notify_user_id = fields.Many2one('res.users', string="Notify Users", help="Users who will be notified for manual PO approval.")
