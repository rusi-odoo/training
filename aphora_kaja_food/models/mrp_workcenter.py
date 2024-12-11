# -*- coding: utf-8 -*-


from odoo import models, fields, _


class WorkCenterProductivity(models.Model):
    _inherit = 'mrp.workcenter.productivity'

    aphora_quantity_count = fields.Float(string='Quantity')
    aphora_worker_count = fields.Float(string='Workers')


class MrpWorkorder(models.Model):
    _inherit = 'mrp.workorder'

    def button_start(self):
        super(MrpWorkorder, self).button_start()
        return {
            'name': _('Time Tracking'),
            'view_mode': 'form',
            'res_model': 'aphora.time.tracking.wizard',
            'views': [[self.env.ref('aphora_kaja_food.aphora_time_tracking_wizard_form').id, 'form']],
            'type': 'ir.actions.act_window',
            'target': 'new',
        }
