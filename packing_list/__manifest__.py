# -*- coding: utf-8 -*-
##############################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#    Copyright (C) 2017-TODAY Cybrosys Technologies(<http://www.cybrosys.com>).
#    Author: Ijaz Ahammed(<http://www.cybrosys.com>)
#    you can modify it under the terms of the GNU LESSER
#    GENERAL PUBLIC LICENSE (LGPL v3), Version 3.
{
    'name': 'Packing List',
    'version': '12.0.0.1.2',
    'category': 'Accounting',
    'summary': 'Packing List',
    'author': 'powERP enterprise network',
    'website': 'https://www.powerp.it',
    'development_status': 'Alpha',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'account',
        'stock',
        'sale',
    ],
    'data': [
        'views/packing_list.xml',
        'report/packing_list_pdf_report.xml',
        'report/format_packing_list_pdf_report.xml',
    ],
    'installable': True,
    'company': 'Cybrosys Techno Solutions, Didotech srl',
    'application': False,
    'auto_install': False,
    'images': ['static/description/banner.jpg'],
}
