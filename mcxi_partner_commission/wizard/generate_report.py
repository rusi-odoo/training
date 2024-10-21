import io
import xlsxwriter
import base64
import datetime
from odoo import models, fields
from odoo.tools import date_utils
from odoo.http import content_disposition, request


class ExternalReport(models.TransientModel):

    _name = 'external.report'
    _description = 'external report'

    start_date = fields.Date(string='Start Date', required=True)
    end_date = fields.Date(string='End Date', required=True)
    file = fields.Binary(readonly=True)
    filename = fields.Char(string='Filename', size=256, readonly=True)

    def action_generate_external_report(self):
        sale_orders = self.env['sale.order'].search([
            ('date_order', '>=', self.start_date),
            ('date_order', '<=', self.end_date),
            ('partner_id.sales_channel', '=', 'agent')
        ])

        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet()

        bold = workbook.add_format({'bold': True})
        money_format = workbook.add_format({'num_format': '$#,##0.00'})

        worksheet.write('A1', 'Date From:', bold)
        worksheet.write('B1', str(self.start_date))
        worksheet.write('D1', 'Date To:', bold)
        worksheet.write('E1', str(self.end_date))
        worksheet.write('J1', 'Total Commission:', bold)

        headers = ['Customer', 'Dealer Code', 'SO #', 'Product', 'Quantity', 'Price',
                   'Amount', 'Invoice #', 'Invoice date', 'Invoice status', 'Commission']
        for col_num, header in enumerate(headers):
            worksheet.write(2, col_num, header, bold)

        row = 3
        total_commission = 0

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
        self.write({
            'file': base64.encodebytes(output.getvalue()),
            'filename': str(datetime.date.today())+'_External_report',
        })
        return {
            "type": "ir.actions.act_url",
            'url': "web/content/?model=external.report&id=" + str(self.id) + "&filename_field=filename&field=file&download=true&filename=" + self.filename,
            "target": "download",
        }


class InternalReport(models.TransientModel):

    _name = 'internal.report'
    _description = 'internal report'

    start_date = fields.Date(string='Start Date', required=True)
    end_date = fields.Date(string='End Date', required=True)
    dsm_id = fields.Many2one(
        string='DSM', comodel_name="hr.employee", required=True)
    file = fields.Binary(readonly=True)
    filename = fields.Char(string='Filename', size=256, readonly=True)

    def action_generate_internal_report(self):
        sale_orders = self.env['sale.order'].search([
            ('date_order', '>=', self.start_date),
            ('date_order', '<=', self.end_date),
            ('partner_id.dsm_id', '=', self.dsm_id.id)
        ])

        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet()

        bold = workbook.add_format({'bold': True})
        money_format = workbook.add_format({'num_format': '$#,##0.00'})

        # Write the header information
        worksheet.write('A1', 'Date From:', bold)
        worksheet.write('B1', str(self.start_date))
        worksheet.write('D1', 'Date To:', bold)
        worksheet.write('E1', str(self.end_date))
        worksheet.write('G1', 'DSM:', bold)
        worksheet.write('H1', str(self.dsm_id.name))

        # Total commissions will be calculated at the end of the report
        worksheet.write('J1', 'Total Commission:', bold)

        # Define the table headers starting from row 6 (row 5 in zero-index)
        headers = ['Customer', 'Dealer Code', 'SO #', 'Product', 'Quantity', 'Price',
                   'Amount', 'Invoice #', 'Invoice date', 'Invoice status', 'Commission']
        for col_num, header in enumerate(headers):
            worksheet.write(2, col_num, header, bold)

        # Populate the data in the table
        row = 3  # Start data from row 6 (row 5 in zero-index)
        total_commission = 0

        for order in sale_orders:
            for line in order.order_line:
                invoice = line.invoice_lines.mapped(
                    'move_id')[0] if line.invoice_lines else None
                # Write the data per order line
                worksheet.write(row, 0, order.partner_id.name)  # Customer
                # Dealer Code
                worksheet.write(row, 1, order.partner_id.dealer_code)
                worksheet.write(row, 2, order.name)  # Sales Order
                worksheet.write(row, 3, line.product_id.name)  # Product
                worksheet.write(row, 4, line.product_uom_qty)  # Quantity
                worksheet.write(row, 5, line.price_unit, money_format)  # Price
                worksheet.write(row, 6, line.price_subtotal, money_format)  # Amount
                worksheet.write(row, 7, invoice.name if invoice else '')  # Invoice #
                worksheet.write(row, 8, str(invoice.invoice_date)if invoice else '')  # Invoice Date
                worksheet.write(row, 9, invoice.state if invoice else 'N/A') # Invoice Status
                worksheet.write(row, 10, line.commission, money_format)  # Commission

                total_commission += line.commission
                row += 1

        # Write the total commission in the header
        worksheet.write('K1', total_commission, money_format)

        workbook.close()
        self.write({
            'file': base64.encodebytes(output.getvalue()),
            'filename': str(datetime.date.today())+'_Internal_report',
        })
        return {
            "type": "ir.actions.act_url",
            'url': "web/content/?model=internal.report&id=" + str(self.id) + "&filename_field=filename&field=file&download=true&filename=" + self.filename,
            "target": "download",
        }
