import io
import xlsxwriter
import base64
import datetime
from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo.tools import date_utils
from odoo.http import content_disposition, request


class CommissionReport(models.TransientModel):

    _name = 'commission.report'
    _description = 'commission report'

    start_date = fields.Date(string='Start Date', required=True)
    end_date = fields.Date(string='End Date', required=True)
    dsm_id = fields.Many2one(string='DSM', comodel_name="hr.employee")
    file = fields.Binary(readonly=True)
    filename = fields.Char(string='Filename', size=256, readonly=True)

    @api.constrains('start_date', 'end_date')
    def _check_dates(self):
        if self.start_date > fields.Date.today() or self.end_date > fields.Date.today():
            raise ValidationError("Start date and End date cannot be in the future.")

        if self.start_date > self.end_date:
            raise ValidationError("Start date must be earlier than or equal to the end date.")

    def action_generate_commission_report(self):
        file_name = ""
        domain = [('date_order', '>=', self.start_date),
                  ('date_order', '<=', self.end_date)]

        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet()
        bold = workbook.add_format({'bold': True})
        money_format = workbook.add_format({'num_format': '$#,##0.00'})
        worksheet.write('A1', 'Date From:', bold)
        worksheet.write('B1', str(self.start_date))
        worksheet.write('D1', 'Date To:', bold)
        worksheet.write('E1', str(self.end_date))
        if self.dsm_id:
            domain.append(('partner_id.dsm_id', '=', self.dsm_id.id))
            file_name = str(datetime.date.today())+'_Internal_report'
            worksheet.write('G1', 'DSM:', bold)
            worksheet.write('H1', str(self.dsm_id.name))
        else:
            domain.append(('partner_id.sales_channel', '=', 'agent'))
            file_name = str(datetime.date.today())+'_External_report'
            worksheet.write('G1', 'Agent:', bold)
            # worksheet.write('H1', str(self.dsm_id.name))
        worksheet.write('J1', 'Total Commission:', bold)

        headers = ['Customer', 'Dealer Code', 'SO #', 'Product', 'Quantity', 'Price',
                   'Amount', 'Invoice #', 'Invoice date', 'Invoice status', 'Commission']

        for col_num, header in enumerate(headers):
            worksheet.write(2, col_num, header, bold)

        row = 3
        total_commission = 0
        sale_orders = self.env['sale.order'].search(domain)
        for order in sale_orders:
            for line in order.order_line:
                invoice = line.invoice_lines.mapped('move_id')[0] if line.invoice_lines else None
                worksheet.write(row, 0, order.partner_id.name)
                worksheet.write(row, 1, order.partner_id.dealer_code)
                worksheet.write(row, 2, order.name)
                worksheet.write(row, 3, line.product_id.name)
                worksheet.write(row, 4, line.product_uom_qty)
                worksheet.write(row, 5, line.price_unit, money_format)
                worksheet.write(row, 6, line.price_subtotal, money_format)
                worksheet.write(row, 7, invoice.name if invoice else '')
                worksheet.write(row, 8, str(invoice.invoice_date) if invoice else '')
                worksheet.write(row, 9, invoice.state if invoice else 'N/A')
                worksheet.write(row, 10, line.commission, money_format)

                total_commission += line.commission
                row += 1

        worksheet.write('K1', total_commission, money_format)

        workbook.close()
        self.file = base64.encodebytes(output.getvalue())
        self.filename = file_name
        return {
            "type": "ir.actions.act_url",
            'url': "web/content/?model=commission.report&id=" + str(self.id) + "&filename_field=filename&field=file&download=true&filename=" + self.filename,
            "target": "download",
        }
