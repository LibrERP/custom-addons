# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#
#    Copyright (C) 2016 Didotech srl (<http://www.didotech.com>).
#
#                       All Rights Reserved
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

"""

$ ./openerp-server -c etc/openerp-server.conf -d <database> -i data_migration --test-enable --stop-after-init

"""


from odoo.tests import common
from odoo.addons.data_migration.utils.utils import BaseImport


class TestToString(common.TransactionCase):
    def test_simple(self):
        self.assertEqual(BaseImport.to_string(34), u'34')

    def test_float(self):
        self.assertEqual(BaseImport.to_string(34.0), u'34')

    def test_float_with_decimal(self):
        self.assertEqual(BaseImport.to_string(34.2), u'34.2')

    def test_string_with_decimal(self):
        self.assertEqual(BaseImport.to_string('1.394,20'), u'1394.2')

    def test_string_with_zero(self):
        self.assertEqual(BaseImport.to_string('0270'), u'0270')
