from odoo import api, fields, models


class AccountMove(models.Model):
    _inherit = 'account.move'

    falak_rate = fields.Float(string='Current Rate', default=0.0,
                              states={'posted': [('readonly', True)], 'cancel': [('readonly', True)]})
    is_diff_currency = fields.Boolean(compute="_compute_is_diff_currency")

    @api.onchange('currency_id', 'date', 'invoice_date', 'company_id')
    def _onchange_falak_rate(self):
        to_currency = self.currency_id or \
            self.journal_id.currency_id or \
            self.journal_id.company_id.currency_id
        self.falak_rate = self.env["res.currency"]._get_conversion_rate(
            from_currency=self.company_currency_id,
            to_currency=to_currency,
            company=self.company_id,
            date=(self.invoice_date or self.date or fields.Date.context_today(self)),
        )

    @api.depends('currency_id', 'company_id')
    def _compute_is_diff_currency(self):
        for move in self:
            move.is_diff_currency = move. move.move_type in ['out_invoice', 'out_refund'] and \
                move.company_currency_id != move.currency_id
