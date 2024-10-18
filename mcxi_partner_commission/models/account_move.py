# -- coding: utf-8 --
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, Command, _
from odoo.exceptions import ValidationError


class AccountMove(models.Model):
    _inherit = 'account.move'

    total_external_commission = fields.Monetary(compute='_compute_total_commission',store=True)
    total_internal_commission = fields.Monetary(compute='_compute_total_commission',store=True)
    commission_external_move_id = fields.Many2one('account.move')
    commission_internal_move_id = fields.Many2one('account.move')

    @api.depends('line_ids','line_ids.quantity')
    def _compute_total_commission(self):
        for move in self:
            total_quantity = sum(line.quantity for line in move.line_ids if line.quantity)
            sale_order = self.env['sale.order'].search([('name', '=', move.invoice_origin)], limit=1)
            if sale_order and sale_order.mcxi_referrer_id:
                commission_value = sale_order.mcxi_referrer_id.commission
                move.total_external_commission = total_quantity * commission_value
            if sale_order and sale_order.user_id.partner_id:
                commission_value = sale_order.user_id.partner_id.commission
                move.total_internal_commission = total_quantity * commission_value

    def _create_commission_journal_entry(self, move, partner_id):
        total_quantity = sum(line.quantity for line in move.line_ids if line.quantity)  
        journal_entry_vals = {
            'date': move.invoice_date,
            'ref': move.payment_reference or _('Journal Entry'),
            'move_type': 'entry',
            'line_ids': [
                Command.create({
                    'name': _('Amount Payable for %s') % move.name,
                    'account_id': move.partner_id.property_account_payable_id.id,
                    'debit': 0.0,
                    'credit': (partner_id.commission * total_quantity) or 0.0,
                    'partner_id': partner_id.id,
                }),
                Command.create({
                    'name': _('Commission Charge for %s') % move.name,
                    'account_id': partner_id.commission_journal_id.id,
                    'debit': (partner_id.commission * total_quantity) or 0.0,
                    'credit': 0.0,
                    'partner_id': partner_id.id,
                })
            ],
        }
        return self.env['account.move'].create(journal_entry_vals)

    def _check_commission_journal(self, partner_id):
        if not partner_id.commission_journal_id:
            raise ValidationError(_("The partner '%s' does not have a commission journal defined.") % partner_id.name)

    def action_create_commission(self):
        for move in self:
            context = self.env.context
            sale_order = self.env['sale.order'].search([
            ('order_line.invoice_lines.move_id', '=', move.id)
            ])

            if not sale_order:
                raise ValidationError(_("No related Sale Order found."))
            if context.get('is_internal'):
                partner_id = sale_order.user_id.partner_id
                self._check_commission_journal(partner_id)
                journal_entry = self._create_commission_journal_entry(move, partner_id)
                journal_entry.state = 'draft'
                move.commission_internal_move_id = journal_entry.id
                if partner_id.commission_rate != 'fixed':
                    raise ValidationError(_("Kindly use Fixed Commission for '%s' and Add Commission") % (partner_id.name))
            elif context.get('is_external'):
                if sale_order.mcxi_referrer_id:
                    partner_id = sale_order.mcxi_referrer_id
                    self._check_commission_journal(partner_id)
                    journal_entry = self._create_commission_journal_entry(move, partner_id)
                    journal_entry.state = 'draft'
                    move.commission_external_move_id = journal_entry.id
                else:
                    raise ValidationError(_("No referrer found for the sale order '%s'.") % (sale_order.name))

        return {
            'name': _('Journal Entry'),
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'view_mode': 'form',
            'res_id': journal_entry.id,
            'target': 'current',
        }

    def action_view_commission(self):
        self.ensure_one()
        context = self.env.context
        if context.get('is_external'):
            journal_entries = self.commission_external_move_id
        if context.get('is_internal'):
            journal_entries = self.commission_internal_move_id
        action = self.env.ref('account.action_move_journal_line').read()[0]
        if len(journal_entries) == 1:
            action['views'] = [(self.env.ref('account.view_move_form').id, 'form')]
            action['res_id'] = journal_entries.id
        else:
            action['domain'] = [('id', 'in', journal_entries.ids)]
        return action

    def _update_commission_state(self):
        for move in self:
            if move.commission_external_move_id:
                move.commission_external_move_id.state = move.state
            if move.commission_internal_move_id:
                move.commission_internal_move_id.state = move.state

    def _update_commission_journal_entry(self, move):
        if move.commission_external_move_id:
            journal_entry = move.commission_external_move_id
            line_vals = [
                Command.update(journal_entry.line_ids.filtered(lambda l: l.credit > 0).id, { 
                    'credit': move.total_external_commission or 0.0,
                }),
                Command.update(journal_entry.line_ids.filtered(lambda l: l.debit > 0).id, {
                    'debit': move.total_external_commission or 0.0,
                })
            ]
            journal_entry.write({
                'line_ids': line_vals,
            })
        if move.commission_internal_move_id:
            journal_entry = move.commission_external_move_id
            line_vals = [
                Command.update(journal_entry.line_ids.filtered(lambda l: l.credit > 0).id, { 
                    'credit': move.total_internal_commission or 0.0,
                }),
                Command.update(journal_entry.line_ids.filtered(lambda l: l.debit > 0).id, {
                    'debit': move.total_internal_commission or 0.0,
                })
            ]
            journal_entry.write({
                'line_ids': line_vals,
            })

    def write(self, vals):
        res = super().write(vals) 
        if 'invoice_line_ids' in vals:
            if (line[0] == 1 and 'quantity' in line[2] for line in vals['invoice_line_ids']):
                for move in self.filtered(lambda m: m.commission_external_move_id or m.commission_internal_move_id):
                    self._update_commission_journal_entry(move)

        if 'state' in vals:
            self._update_commission_state()
        return res
