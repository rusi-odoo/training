# -- coding: utf-8 --
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, Command, _
from odoo.exceptions import ValidationError


class AccountMove(models.Model):
    _inherit = 'account.move'

    total_external_commission = fields.Monetary(compute='_compute_total_commission', store=True)
    total_internal_commission = fields.Monetary(compute='_compute_total_commission', store=True, string="Total Internal Commission")
    total_account_owner_commission = fields.Monetary(compute='_compute_total_commission', store=True, string="Total Account Owner Commission")
    total_dsm_commission = fields.Monetary(compute='_compute_total_commission', store=True, string="Total DSM Commission")
    total_bdm_commission = fields.Monetary(compute='_compute_total_commission', store=True, string="Total BDM Commission")
    total_agent1_commission = fields.Monetary(compute='_compute_total_commission', store=True, string="Total Agent1 Commission")
    total_agent2_commission = fields.Monetary(compute='_compute_total_commission', store=True, string="Total Agent2 Commission")
    total_agent3_commission = fields.Monetary(compute='_compute_total_commission', store=True, string="Total Agent3 Commission")
    commission_external_move_id = fields.Many2one('account.move', copy=False)
    commission_internal_move_id = fields.Many2one('account.move', copy=False)

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
            if sale_order.partner_id.is_account_commission and sale_order.partner_id.account_owner_id:
                commission_value = sale_order.partner_id.account_owner_id.partner_id.commission
                move.total_account_owner_commission = total_quantity * commission_value
            if sale_order.partner_id.is_dsm_commission and sale_order.partner_id.dsm_id:
                commission_value = sale_order.partner_id.dsm_id.work_contact_id.commission
                move.total_dsm_commission = total_quantity * commission_value
            if sale_order.partner_id.is_bdm_commission and sale_order.bdm_id:
                commission_value = sale_order.bdm_id.work_contact_id.commission
                move.total_bdm_commission = total_quantity * commission_value
            if sale_order.agent_1_id.commission:
                commission_value = sale_order.agent_1_id.commission
                move.total_agent1_commission = commission_value * total_quantity
            if sale_order.agent_2_id.commission:
                commission_value = sale_order.agent_2_id.commission
                move.total_agent2_commission = commission_value * total_quantity
            if sale_order.agent_3_id.commission:
                commission_value = sale_order.agent_3_id.commission
                move.total_agent3_commission = commission_value * total_quantity

    def _prepare_commission_line_vals(self, move, partner_id):
        line_vals = []
        total_commission = 0.0
        for line in move.invoice_line_ids:
            commission_amount = partner_id.commission * line.quantity
            if move.move_type == 'out_invoice':
                debit = commission_amount
                credit = 0
            else:
                debit = 0
                credit = commission_amount
            line_vals.append({
                'name': _('Commission Charge for %s: %s') % (
                    line.move_id.name, line.product_id.display_name or line.name),
                'account_id': partner_id.commission_journal_id.id,
                'debit': debit,
                'credit': credit,
                'partner_id': partner_id.id,
                'mcxi_origin_invoice_line_id': line.id,
            })
            total_commission += commission_amount
        line_vals.append({
            'name': _('Amount Payable for %s') % move.name,
            'account_id': move.partner_id.property_account_payable_id.id,
            'debit': 0.0 if move.move_type == 'out_invoice' else total_commission,
            'credit': total_commission if move.move_type == 'out_invoice' else 0.0,
            'partner_id': partner_id.id,
        })
        return line_vals

    def _create_commission_journal_entry(self, move, partner_id):
        line_vals = self._prepare_commission_line_vals(move, partner_id)
        journal_entry_vals = {
            'date': move.invoice_date or move.date,
            'ref': move.payment_reference or _('Journal Entry'),
            'move_type': 'entry',
            'line_ids': [Command.create(line_val) for line_val in line_vals],
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

    def _reverse_moves(self, default_values_list=None, cancel=False):
        reverse_moves = super()._reverse_moves(default_values_list, cancel)
        commission_moves = self.filtered(
            lambda move: move.move_type == 'out_invoice').commission_external_move_id.filtered(
            lambda move: move.state == 'posted')
        if commission_moves:
            reverse_moves.with_context(is_external=True).action_create_commission()
        return reverse_moves


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    # To show commission in excel report
    mcxi_origin_invoice_line_id = fields.Many2one(
        'account.move.line', copy=False, readonly=True, string="Related Invoice Line")
    mcxi_commission_line_ids = fields.One2many('account.move.line', 'mcxi_origin_invoice_line_id')
