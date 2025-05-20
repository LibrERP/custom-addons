# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 DevIntelle Consulting Service Pvt.Ltd (<http://www.devintellecs.com>).
#
#    For Module Support : devintelle@gmail.com  or Skype : devintelle
#
##############################################################################
from odoo import api, fields, models, _
import base64
import xlrd
from io import BytesIO
from xlwt import easyxf
from io import StringIO
import xlwt
import csv
from odoo.exceptions import ValidationError

class import_inventory_lines(models.TransientModel):
    _name = "import.sale.lines"

    file_type = fields.Selection([ ('csv', 'CSV'),('excel', 'Excel')],
                                 string='File Type', default='csv')
    select_file = fields.Binary(string='File')
    excel_file = fields.Binary(string='Download Sample file', readonly=True)
    file_name = fields.Char('Excel Name', size=64)
    csv_file_name = fields.Char(string='File Name')
    import_by = fields.Selection(selection=[('name', 'Name'),('internal_ref', 'Internal ref'),('barcode','Barcode')], default='name', required=True,
                                   string='Product Import by')
    def print_report(self):
        if self.file_type == 'csv':
            return self._generate_csv_report()
        elif self.file_type == 'excel':
            return self.generate_excel_report()

    def _generate_csv_report(self):
        filename = 'Sample_SaleOrder.csv'
        csv_content = [
            ['Name', 'Internal ref', 'Barcode', 'Description', 'Qty', 'Price'],
            ['Storage Box', 'E-COM08', '5675', 'black-brown: Box', '1', '200'],
            ['Office Design Software', 'FURN_9999', '1234', 'white Down', '2', '100']
        ]

        output = StringIO()
        writer = csv.writer(output)
        writer.writerows(csv_content)
        csv_string = output.getvalue()
        output.close()

        csv_file_data = csv_string.encode('utf-8')
        self.write({
            'excel_file': base64.encodebytes(csv_file_data),
            'file_name': filename
        })

        active_id = self.ids[0]
        return {
            'type': 'ir.actions.act_url',
            'url': f'web/content/?model=import.sale.lines&download=true&field=excel_file&id={active_id}&filename={filename}',
            'target': 'new',
        }


    def generate_excel_report(self):
        filename = 'Sample SaleOrder.xls'
        workbook = xlwt.Workbook()
        worksheet = workbook.add_sheet('Line')
        worksheet.col(0).width = 4500
        worksheet.col(1).width = 4000
        worksheet.col(2).width = 4000
        worksheet.col(3).width = 4500
        font_style = easyxf(
            'font:height 215;pattern: pattern solid, fore_color gray25; font:bold True;align: vert center, horiz left;')

        worksheet.write(0, 0, 'Product Name',font_style)
        worksheet.write(0, 1, 'Internal ref',font_style)
        worksheet.write(0, 2, 'Barcode',font_style)
        worksheet.write(0, 3, 'Description',font_style)
        worksheet.write(0, 4, 'Qty',font_style)
        worksheet.write(0, 5, 'Price',font_style)

        counter = 1
        worksheet.write(1, 0, 'Storage Box')
        worksheet.write(1,  1, 'E-COM08')
        worksheet.write(1, 2, '5675')
        worksheet.write(1, 3, 'black-brown: Box')
        worksheet.write(1,  4, '1')
        worksheet.write(1, 5, '200')

        counter = 1
        worksheet.write(2, 0, 'Office Design Software')
        worksheet.write(2, 1, 'FURN_9999')
        worksheet.write(2, 2, '1234')
        worksheet.write(2, 3, 'white Down')
        worksheet.write(2, 4, '2')
        worksheet.write(2, 5, '100')

        fp = BytesIO()
        workbook.save(fp)
        fp.seek(0)
        excel_file = base64.encodebytes(fp.read())
        fp.close()
        self.write({'excel_file': excel_file})
        active_id = self.ids[0]
        url = ('web/content/?model=import.sale.lines&download=true&field=excel_file&id=%s&filename=%s' % (active_id, filename))
        if self.excel_file:
            return {'type': 'ir.actions.act_url',
                    'url': url,
                    'target': 'new'
                    }



    def import_line(self):
        active_id = self._context.get('active_id')
        sale_id = self.env['sale.order'].browse(active_id)
        if not self.select_file:
            raise ValidationError(_('No file uploaded!'))
        data = []
        file_data = base64.b64decode(self.select_file)

        if self.file_type == 'excel':
            try:
                workbook = xlrd.open_workbook(file_contents=file_data)
                sheet = workbook.sheet_by_index(0)
                data = [[sheet.cell_value(r, c) for c in range(sheet.ncols)] for r in range(sheet.nrows)]
                data.pop(0)
            except Exception:
                raise ValidationError(_('The uploaded file is not a valid Excel file.'))

        else:
            try:
                s_data = file_data.decode("utf-8").splitlines()
                data = [line.split(',') for line in s_data if line]
                data.pop(0)
            except Exception:
                raise ValidationError(_('The uploaded file is not a valid CSV file.'))
        count = 0
        note = ''
        for line in data:
            count += 1

            if self.import_by == 'name':
                domain = [('name', '=', line[0])]
            elif self.import_by == 'internal_ref':
                domain = [('default_code', '=', line[1])]
            else :
                domain = [('barcode', '=', str(line[2]))]
            product_id = self.env['product.product'].search(domain)

            if product_id:
                existing_line_ids = self.env['sale.order.line'].search(
                    [('order_id', '=', sale_id.id), ('product_id', '=', product_id.id)]
                )
                existing_line_ids._compute_price_unit()
                existing_line_ids._compute_tax_id()
                if existing_line_ids:
                    for existing_line_id in existing_line_ids:
                        existing_line_id.product_uom_qty += float(line[4])
                        existing_line_id.price_unit = float(line[5])
                else:
                    vals = {
                        'product_id': product_id.id or False,
                        'name': line[3] or '',
                        'product_uom_qty': float(line[4]) or 0.0,
                        'price_unit': float(line[5]) or 0.0,
                        'order_id': sale_id.id or False,
                        'product_uom': product_id and product_id.uom_id and product_id.uom_id.id,
                    }
                    self.env['sale.order.line'].create(vals)
               
            else:
                if not note:
                    note = "Product Not found in uploaded File.\n"
                note += "Line no :" + str(count) + " Product :" + str(
                    line[0]) + "\n"
        if note:
            log_id = self.env['sale.log'].create({'name': note})
            return {
                'view_mode': 'form',
                'res_id': log_id.id,
                'res_model': 'sale.log',
                'view_type': 'form',
                'type': 'ir.actions.act_window',
                'target': 'new',
            }

class sale_log(models.TransientModel):
    _name = "sale.log"

    name = fields.Text(string='Logs',readonly=True)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
