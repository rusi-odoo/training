# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import io
import xlsxwriter
import base64
from pytz import timezone

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools.misc import formatLang


class CommissionReport(models.TransientModel):
    _name = 'commission.report'
    _rec_name = 'filename'
    _description = 'commission report'

    start_date = fields.Date(string='Start Date', required=True)
    end_date = fields.Date(string='End Date', required=True)
    dsm_id = fields.Many2one(string='DSM', comodel_name="hr.employee")
    bdm_id = fields.Many2one(comodel_name="hr.employee", string='BDM')
    account_owner_id = fields.Many2one(comodel_name="res.users", string='Account Owner')
    file = fields.Binary(readonly=True)
    filename = fields.Char(string='Filename', size=256, readonly=True)

    @api.constrains('start_date', 'end_date')
    def _check_dates(self):
        start_date, end_date = self.convert_dates_to_utc(self.start_date, self.end_date)
        if start_date.date() > fields.Date.today() or end_date.date() > fields.Date.today():
            raise ValidationError(_("Start date and End date cannot be in the future."))
        if start_date > end_date:
            raise ValidationError(_("Start date must be earlier than or equal to the end date."))

    def convert_dates_to_utc(self, start_date, end_date):
        """Convert start and end date from client timezone to UTC datetime."""
        client_timezone = timezone(self.env.user.tz or 'UTC')
        start_datetime_utc = self._convert_to_utc(start_date, client_timezone, "00:00:00")
        end_datetime_utc = self._convert_to_utc(end_date, client_timezone, "23:59:59")
        return start_datetime_utc, end_datetime_utc

    def _convert_to_utc(self, date_str, client_timezone, time_str):
        """Helper method to convert date with time to UTC."""
        client_time = fields.Datetime.from_string(f"{date_str} {time_str}")
        localized_time = client_timezone.localize(client_time)
        return localized_time.astimezone(timezone('UTC'))

    def action_generate_commission_report(self):
        """Generate the commission report in Excel format."""
        start_date, end_date = self.convert_dates_to_utc(self.start_date, self.end_date)
        domain = self._get_domain(start_date, end_date)

        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet()

        self._write_header(workbook, worksheet)
        self._write_filters(workbook, worksheet)
        headers = self._get_headers()
        self._write_table_headers(workbook, worksheet, headers)

        sale_orders = self.env['sale.order'].search(domain)
        if not sale_orders:
            raise UserError(_('There are no open orders with commission in this period.'))

        total_commission = 0
        row = 3
        for order in sale_orders:
            for order_line in order.order_line:
                quantity, price, amount = self._get_line_amounts(order_line, order)
                self._write_order_line(workbook, worksheet, row, order, order_line, quantity, price, amount)

                invoice_data = self._get_invoice_details(order_line)
                for invoice in invoice_data:
                    self._write_invoice_line(workbook, worksheet, row, invoice)
                    total_commission += float(invoice['commission_amount'])
                    row += 1

                if not invoice_data:
                    row += 1

        self._write_total_commission(workbook, worksheet, row, total_commission)
        self._set_column_widths(worksheet, headers)

        workbook.close()
        self.file = base64.encodebytes(output.getvalue())
        self.filename = f"{fields.Date.context_today(self)}_commission_report.xlsx"
        return {
            "type": "ir.actions.act_url",
            'url': "web/content/?model=commission.report&id=" + str(self.id) + "&filename_field=filename&field=file&download=true&filename=" + self.filename,
            "target": "download",
        }

    def _get_domain(self, start_date, end_date):
        """Define domain filters for searching sale orders."""
        domain = [
            ('company_id', '=', self.env.company.id),
            ('date_order', '>=', start_date),
            ('date_order', '<=', end_date),
            ('state', '=', 'sale'),
        ]
        if self.dsm_id:
            domain.append(('user_id.partner_id.dsm_id', '=', self.dsm_id.id))
        else:
            domain.append(('mcxi_referrer_id.sales_channel', '=', 'agent'))
        return domain

    def _get_headers(self):
        """Define headers for the report table."""
        return [
            _('Customer'), _('Dealer Code'), _('SO #'), _('Product'), _('Quantity'), _('Price'),
            _('Amount (Tax excl.)'), _('Invoice #'), _('Invoice Date'), _('Invoiced Qty'), _('Unit Price'),
            _('Invoice Total'), _('Invoice status'), _('Invoice Payment Status'), _('Commission')
        ]

    def _write_header(self, workbook, worksheet):
        """Write the report header with the date range."""
        bold = workbook.add_format({'bold': True})
        worksheet.write('A1', _('Date From:'), bold)
        worksheet.write('B1', str(self.start_date))
        worksheet.write('D1', _('Date To:'), bold)
        worksheet.write('E1', str(self.end_date))

    def _write_filters(self, workbook, worksheet):
        """Write filters for DSM or Agent and set file name accordingly."""
        bold = workbook.add_format({'bold': True})
        if self.dsm_id:
            worksheet.write('G1', _('DSM:'), bold)
            worksheet.write('H1', self.dsm_id.name)
        else:
            worksheet.write('G1', _('Agent:'), bold)
            worksheet.write('H1', _('Yes'))

    def _write_table_headers(self, workbook, worksheet, headers):
        """Write table headers."""
        bold = workbook.add_format({'bold': True})
        for col_num, header in enumerate(headers):
            worksheet.write(2, col_num, header, bold)

    def _get_line_amounts(self, order_line, order):
        """Retrieve quantity, price, and subtotal for an order line."""
        quantity = str(order_line.product_uom_qty)
        price = formatLang(self.env, order_line.price_unit, currency_obj=order.currency_id or order.company_id.currency_id)
        amount = formatLang(self.env, order_line.price_subtotal, currency_obj=order.currency_id or order.company_id.currency_id)
        return quantity, price, amount

    def _get_invoice_details(self, order_line):
        """Retrieve invoice details for an order line."""
        invoices_data = []
        invoices = order_line.invoice_lines.mapped('move_id').filtered(
            lambda inv: inv.move_type in ('out_invoice', 'out_refund')
        )
        payment_states_dict = dict(self.env['account.move']._fields['payment_state']._description_selection(self.env))

        for invoice in invoices:
            sign = -1 if invoice.move_type == 'out_refund' else 1
            invoice_name = invoice.display_name or ''
            invoice_date = str(invoice.invoice_date) if invoice.invoice_date else ''
            invoice_state = invoice.state
            if invoice.reversal_move_id:
                payment_state = payment_states_dict.get('reversed')
            else:
                payment_state = payment_states_dict.get(invoice.payment_state, _('Unpaid'))

            for invoice_line in invoice.invoice_line_ids.filtered(lambda line: line.product_id == order_line.product_id):
                invoiced_qty = str(invoice_line.quantity)
                unit_price = formatLang(self.env, invoice_line.price_unit, currency_obj=invoice.currency_id)
                total_amount = formatLang(self.env, invoice_line.price_subtotal, currency_obj=invoice.currency_id)
                
                commission = (order_line.order_id.user_id.partner_id.commission * invoice_line.quantity if self.dsm_id
                              else sum(invoice_line.mcxi_commission_line_ids.filtered(
                                  lambda line: line.parent_state == 'posted'
                              ).mapped('credit')) or sum(invoice_line.mcxi_commission_line_ids.mapped('debit')))
                
                invoices_data.append({
                    'currency_id': invoice.currency_id,
                    'invoice_name': invoice_name,
                    'invoice_date': invoice_date,
                    'invoiced_qty': invoiced_qty,
                    'unit_price': unit_price,
                    'total_amount': total_amount,
                    'invoice_state': invoice_state,
                    'commission_amount': commission * sign,
                    'commission': formatLang(self.env, commission * sign, currency_obj=invoice.currency_id),
                    'payment_state': payment_state,
                })
        return invoices_data

    def _write_order_line(self, workbook, worksheet, row, order, order_line, quantity, price, amount):
        """Write the sale order line details."""
        numeric = workbook.add_format({'align': 'right'})
        worksheet.write(row, 0, order.partner_id.display_name or '')
        worksheet.write(row, 1, order.partner_id.dealer_code or '')
        worksheet.write(row, 2, order.display_name or '')
        worksheet.write(row, 3, order_line.product_id.display_name or '')
        worksheet.write(row, 4, quantity, numeric)
        worksheet.write(row, 5, price, numeric)
        worksheet.write(row, 6, amount, numeric)

    def _write_invoice_line(self, workbook, worksheet, row, invoice):
        """Write the invoice details."""
        numeric = workbook.add_format({'align': 'right'})
        worksheet.write(row, 7, invoice['invoice_name'])
        worksheet.write(row, 8, invoice['invoice_date'])
        worksheet.write(row, 9, invoice['invoiced_qty'], numeric)
        worksheet.write(row, 10, invoice['unit_price'], numeric)
        worksheet.write(row, 11, invoice['total_amount'], numeric)
        worksheet.write(row, 12, invoice['invoice_state'])
        worksheet.write(row, 13, invoice['payment_state'])
        if invoice['commission_amount'] < 0:
            numeric = workbook.add_format({'align': 'right', 'font_color': 'red'})
        worksheet.write(row, 14, invoice['commission'], numeric)

    def _write_total_commission(self, workbook, worksheet, row, total_commission):
        """Write the total commission at the end of the report."""
        bold = workbook.add_format({'bold': True})
        bold_numeric = workbook.add_format({'bold': True, 'align': 'right'})
        worksheet.write(row + 1, 13, _('Total Commission:'), bold)
        worksheet.write(row + 1, 14, total_commission, bold_numeric)

    def _set_column_widths(self, worksheet, headers):
        """Set the width of columns based on headers."""
        for col_num, header in enumerate(headers):
            worksheet.set_column(col_num, col_num, len(header) + 2)
