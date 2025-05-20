# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 DevIntelle Consulting Service Pvt.Ltd (<http://www.devintellecs.com>).
#
#    For Module Support : devintelle@gmail.com  or Skype : devintelle
#
##############################################################################

{
    'name': 'Import Sales Lines | Import Sale Order Lines | CSV | Excel',
    'version': '18.0.2.0',
    'sequence': 1,
    'category': 'Sales',
    'description':
        """
Import Sale Order Line Odoo app allows businesses to streamline their sales order management by importing sale order lines in bulk using CSV or Excel files. This app supports importing lines based on product name, internal reference, or barcode, making it highly flexible and efficient for data entry.

With a simple interface, users can upload their files, and the app validates the file type to ensure compatibility with the selected format (CSV or Excel). If the uploaded file does not match the selected type, a validation message is displayed, ensuring accuracy. After successful import, the sale order lines are displayed for review, and the uploaded file can be downloaded for record-keeping.

 Import sale order lines using CSV or Excel files.
 Supports importing sale order lines by product name, internal reference, or barcode.
 Validates file type to ensure it matches the selected format (CSV or Excel).
 Displays imported sale order lines for review after upload.
 Eliminates the need for manual entry by enabling bulk imports of sale order lines.
 Simplifies the sales order creation process, saving time and effort for sales teams.
    """,
    'summary': 'Import sale order lines import sale lines import sale order import sale order lines csv import csv import excel import so import lines csv import lines excel excel all in one import lines all in one import csv all in one import excel',
    'depends': ['base', 'sale_management'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/import_sale_lines_view.xml',
        'views/sale_view.xml',
    ],
	'demo': [],
    'test': [],
    'css': [],
    'qweb': [],
    'js': [],
    'images': ['images/main_screenshot.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
    
    #author and support Details
    'author': 'DevIntelle Consulting Service Pvt.Ltd',
    'website': 'http://www.devintellecs.com',    
    'maintainer': 'DevIntelle Consulting Service Pvt.Ltd', 
    'support': 'devintelle@gmail.com',
    'price':11.0,
    'currency':'EUR',
    #'live_test_url':'https://youtu.be/A5kEBboAh_k',
    'pre_init_hook' :'pre_init_check',
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
