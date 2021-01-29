#!/usr/bin/env python
# -*- coding: utf-8 -*-
# #############################################################################
#
#    Copyright © 2016-2019 Didotech srl (<http://www.didotech.com>)
#    All Rights Reserved
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# #############################################################################

"""
odoo_access = {
    '<name>': ['url', 'database', 'user', 'password'],
}


"""

import xmlrpc.client
from collections import namedtuple
from update_config import odoo_access
import getopt
import sys


OdooRPC = namedtuple('Odoo', ['url', 'database', 'user', 'password'])


def update_odoo(odoo_access):
    for name, access_data in odoo_access.items():
        rpc = OdooRPC(*access_data)

        common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(rpc.url))

        if not common.version():
            raise Warning("Cant't connect to remote database")

        uid = common.authenticate(rpc.database, rpc.user, rpc.password, {})
        models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(rpc.url))

        result = models.execute_kw(
            rpc.database,
            uid,
            rpc.password,
            'ir.module.module',
            'set_modules_to_upgrade',
            {}
        )

        if result:
            print('Upgrading modules for {}'.format(rpc.database))

            return models.execute_kw(
                rpc.database,
                uid,
                rpc.password,
                'base.module.upgrade',
                'upgrade_module',
                [[]],
                {}
            )


def update_module(odoo_data, name):
    for _name, access_data in odoo_data.items():
        rpc = OdooRPC(*access_data)

        common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(rpc.url))

        if not common.version():
            raise Warning("Cant't connect to remote database")

        uid = common.authenticate(rpc.database, rpc.user, rpc.password, {})
        models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(rpc.url))

        module_ids = models.execute_kw(
            rpc.database,
            uid,
            rpc.password,
            'ir.module.module',
            'search',
            [[['name', '=', name]]]
        )
        print(module_ids)

        return models.execute_kw(
            rpc.database,
            uid,
            rpc.password,
            'ir.module.module',
            'write',
            [module_ids, {'state': 'to upgrade'}]
        )


def list():
    for name in odoo_access.keys():
        print(name)


def usage():
    print('''Usage: {name} [--help] [--all] [--list] [--odoo=]

        --all (-q): upgrade all databases

        --odoo=<database> (-o): upgrade <database>

        --help (-h): show this message

        --list (-l): list databases

        --update (-u): update module

        '''.format(name=sys.argv[0]))


if __name__ == '__main__':
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'alho:u:', ['all', 'list', 'help', 'odoo=', 'update='])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    if len(opts) in (1, 2):
        odoo = False
        module = False
        for opt, arg in opts:
            if opt in ('-h', '--help'):
                usage()
                sys.exit(2)
            elif opt in ('-a', '--all'):
                update_odoo(odoo_access)
            elif opt in ('-o', '--odoo'):
                odoo = arg
            elif opt in ('-l', '--list'):
                list()
            elif opt in ('-u', '--update'):
                module = arg
            else:
                usage()
                sys.exit(2)

        if module and odoo:
            if update_module({odoo: odoo_access[odoo]}, module):
                if odoo_access.get(odoo, False):
                    update_odoo({odoo: odoo_access[odoo]})
                else:
                    usage()
            else:
                usage()
        elif odoo:
            if odoo_access.get(odoo, False):
                update_odoo({odoo: odoo_access[odoo]})
            else:
                usage()

    else:
        usage()
        sys.exit(2)
