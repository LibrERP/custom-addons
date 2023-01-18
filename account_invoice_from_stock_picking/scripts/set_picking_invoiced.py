# © 2023 Andrei Levin <andrei.levin@didotech.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)
"""
set_picking_invoiced.py:

    -d <database>
    -U <user>
    -W <password>
    -H <host:port>, default: localhost:8069
    -P <protocol>, jsonrpc / jsonrpcs / xmlrpc / xmlrpcs. Default: jsonrpc
    -h - help
    -t - Test connection and exit

Ex:

    set_picking_invoiced.py -d <database> -U admin -W <password>
    rset_picking_invoiced.py -d <database> -H <host:port> -P <protocol> -U admin -W <password>

Installation:
    pip install odoo-client-lib

"""

import odoolib
import getopt
import sys


def script_help():
    import __main__
    return __main__.__doc__


if __name__ == '__main__':
    # LOCAL VERSION
    host = 'localhost'
    port = 8069  # default value, can be changed with -P
    protocol = 'jsonrpc'
    database = ''
    user = ''
    password = ''
    test = False
    invoice_id: int = False

    options, remainder = getopt.getopt(sys.argv[1:], 'd:U:W:H:P:i:ht',
                                       [
                                           'database=',
                                           'user=',
                                           'password=',
                                           'host=',
                                           'protocol=',
                                           'invoice=',
                                           'help',
                                           'test'
                                       ])

    print(options)
    for opt, arg in options:
        if opt in ('-d', '--database'):
            database = arg
        elif opt in ('-U', '--user'):
            user = arg
        elif opt in ('-W', '--password'):
            password = arg
        elif opt in ('-H', '--host'):
            if ':' in arg:
                host, s_port = arg.split(':')
                port = int(s_port)
            else:
                host = arg
        elif opt in ('-P', '--protocol'):
            protocol = arg
        elif opt in ('-t', '--test'):
            test = True
        elif opt in ('-h', '--help'):
            print(script_help())
            sys.exit()
        elif opt in ('-i', '--invoice'):
            invoice_id = int(arg)
        else:
            print(script_help())
            sys.exit()

    if not all([database, user, password, host]):
        print(script_help())
        sys.exit()

    odoo = odoolib.get_connection(
        hostname=host, database=database, login=user, password=password, protocol=protocol, port=port)
    user_model = odoo.get_model("res.users")
    user_ids = user_model.search([("login", "=", "admin")])
    user_info = user_model.read(user_ids[0], ["name"])
    print(user_info["name"])

    invoice_model = odoo.get_model('account.invoice.line')
    picking_model = odoo.get_model('stock.picking')
    package_model = odoo.get_model('stock.picking.package.preparation')

    if test:
        sys.exit()

    operation = 'invoiced'
    # operation = '2binvoiced'
    # operation = 'internal'

    processed: list = []

    if operation == 'invoiced':
        domain: list = []
        invoices = invoice_model.search_read(domain, ('id', 'ddt_id'))

        line_count = len(invoices)

        for count, invoice_line in enumerate(invoices, start=1):
            print(f"{count} / {line_count} - {invoice_line['id']}")

            if invoice_line['ddt_id']:
                package = package_model.read(invoice_line['ddt_id'][0], ('id', 'picking_ids'))

                for picking_id in package['picking_ids']:
                    if picking_id not in processed:
                        picking_model.write(picking_id, {'invoice_state': 'invoiced'})
                        processed.append(picking_id)

    elif operation == '2binvoiced':
        domain = [
            ('state', '=', 'done'),
            ('invoice_state', '!=', 'invoiced'),
            ('picking_type_id.code', '!=', 'internal')
        ]

        pickings = picking_model.search_read(domain, ('id', 'invoice_state'))
        picking_count = len(pickings)

        for count, picking in enumerate(pickings, start=1):
            print(f"{count} / {picking_count} - {picking['id']}")

            if picking['invoice_state'] != 'invoiced' and picking['id'] not in processed:
                picking_model.write(picking['id'], {'invoice_state': '2binvoiced'})
                processed.append(picking['id'])

    elif operation == 'internal':
        domain = [
            ('state', '=', 'done'),
            ('invoice_state', '=', '2binvoiced'),
            ('picking_type_id.code', '=', 'internal')
        ]

        pickings = picking_model.search_read(domain, ('id', 'invoice_state'))
        picking_count = len(pickings)

        for count, picking in enumerate(pickings, start=1):
            print(f"{count} / {picking_count} - {picking['id']}")

            if picking['invoice_state'] != 'invoiced' and picking['id'] not in processed:
                picking_model.write(picking['id'], {'invoice_state': 'none'})
                processed.append(picking['id'])
