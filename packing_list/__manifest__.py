# -*- coding: utf-8 -*-
##############################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#    Copyright (C) 2017-TODAY Cybrosys Technologies(<http://www.cybrosys.com>).
#    Author: Ijaz Ahammed(<http://www.cybrosys.com>)
#    you can modify it under the terms of the GNU LESSER
#    GENERAL PUBLIC LICENSE (LGPL v3), Version 3.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU LESSER GENERAL PUBLIC LICENSE (LGPL v3) for more details.
#
#    You should have received a copy of the GNU LESSER GENERAL PUBLIC LICENSE
#    GENERAL PUBLIC LICENSE (LGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    'name': "Packing List",
    'version': '12.0.0.1.0',
    'summary': """Packing List""",
    'description': """ """,
    'author': "Cybrosys Technologies, Didotech srl", 
    'company': 'Cybrosys Techno Solutions, Didotech srl',
    'website': "https://www.cybrosys.com",
    'category': 'Accounting',
    'depends': [
        'base',
        'account',
        'stock',
        'sale'],
    'data': [
        'views/packing_list.xml',
        'report/packing_list_pdf_report.xml',
        'report/format_packing_list_pdf_report.xml',
    ],
    'images': ['static/description/banner.jpg'],
    'license': 'LGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
