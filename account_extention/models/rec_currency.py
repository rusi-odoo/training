from odoo import models, api, fields


class Currency(models.Model):
    _inherit = "res.currency"

    def _get_conversion_rate(self, from_currency, to_currency, company, date):
        if self.env.context.get('specific_rate') and self.env.context.get('specific_rate') > 0:
            return self.env.context['specific_rate']
        else:
            return super()._get_conversion_rate(from_currency, to_currency, company, date)
