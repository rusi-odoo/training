from odoo import api, fields, models


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    @api.depends('move_id.falak_rate')
    def _compute_currency_rate(self):
        super()._compute_currency_rate()
        for line in self.filtered(lambda l: l.currency_id and
                                  l.move_id.falak_rate):
            line.currency_rate = line.move_id.falak_rate

    def _compute_price_unit(self):
        lines_to_recompute = self.filtered(lambda l: l.currency_id and
                                           l.move_id.falak_rate and not self._context.get('skip'))
        lines_to_not_compute = self - lines_to_recompute
        super(
            AccountMoveLine, lines_to_not_compute
        )._compute_price_unit()
        for line in lines_to_recompute:
            super(AccountMoveLine, lines_to_recompute).with_context(
                specific_rate=line.move_id.falak_rate, skip=True)._compute_price_unit()
