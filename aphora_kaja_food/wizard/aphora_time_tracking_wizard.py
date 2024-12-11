# -*- coding: utf-8 -*-

from odoo import models, fields


class AphoraTimeTrackingWizard(models.TransientModel):
    _name = 'aphora.time.tracking.wizard'
    _description = 'Time Tracking Wizard'

    aphora_employee_id = fields.Many2one('hr.employee', string="Employee", default=lambda self: self.env.user.employee_id)
    aphora_quantity = fields.Float(string='Quantity')
    aphora_worker = fields.Float(string='Workers')

    def action_confirm(self):
        active_wo_id = self.env.context.get('active_id')
        if active_wo_id:
            # TODO: UTAG need to fix here
            current_wo_time_tracking = self.env['mrp.workorder'].browse(active_wo_id).time_ids.sorted('id')[-1]
            current_wo_time_tracking.update({'aphora_quantity_count': self.aphora_quantity,
                                             'aphora_worker_count': self.aphora_worker,
                                             'employee_id': self.aphora_employee_id.id
                                             })
