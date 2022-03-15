# © 2022 Andrei Levin <andrei.levin@didotech.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)
"""
sort_picking_lines.py:

    -d <database>
    -U <user>
    -W <password>
    -H <host:port>, default: localhost:8069
    -P <protocol>, jsonrpc / jsonrpcs / xmlrpc / xmlrpcs. Default: jsonrpc
    -h - help
    -t - Test connection and exit

Ex:
    Test connection:
    ./sort_picking_lines.py -d <database> -U admin -W <password> --test
    ./sort_picking_lines.py -d <database> -U admin -W <password>

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

    options, remainder = getopt.getopt(sys.argv[1:], 'd:U:W:H:P:h:t',
                                       [
                                           'database=',
                                           'user=',
                                           'password=',
                                           'host=',
                                           'protocol=',
                                           'help',
                                           'test'
                                       ])

    print(options)
    for opt, arg in options:
        if opt in ('-d', '--database'):
            database = arg
        elif opt in ('-U', '--user'):
            user = arg
        elif opt in ('-W, --password'):
            password = arg
        elif opt in ('-H, --host'):
            if ':' in arg:
                host, port = arg.split(':')
                port = int(port)
            else:
                host = arg
        elif opt in ('-P, --protocol'):
            protocol = arg
        elif opt in ('-t, --test'):
            test = True
        elif opt in ('-h, --help'):
            print(script_help())
            sys.exit()
        else:
            print(script_help())
            sys.exit()

    if not all([database, user, password, host]):
        print(script_help())
        sys.exit()

    odoo = odoolib.get_connection(
        hostname=host, database=database, login=user, password=password, protocol=protocol, port=port)

    # Test connection
    user_model = odoo.get_model("res.users")
    user_ids = user_model.search([("login", "=", "admin")])
    user_info = user_model.read(user_ids[0], ["name"])
    print(user_info["name"])

    if test:
        sys.exit()

    preparation_line_model = odoo.get_model('stock.picking.package.preparation.line')
    sale_order_model = odoo.get_model('sale.order')
    sale_line_model = odoo.get_model('sale.order.line')
    lines = preparation_line_model.search_read([], ('id', 'sale_line_id'))
    length = len(lines)
    errors = {}
    for counter, line in enumerate(lines, start=1):
        print(f"Setting name and sequence for line {line['id']}: {counter} / {length}")
        if line['sale_line_id']:
            sale_line = sale_line_model.read(line['sale_line_id'][0], ('order_id', 'sequence'))

            try:
                preparation_line_model.write(line['id'], {
                    'sale_order_name': sale_line['order_id'][1],
                    'sale_order_line_sequence': sale_line['sequence']
                })
            except Exception as e:
                errors[line['id']] = {
                    line['id']: e.error['data']['message'],
                    'name': line['name']
                }
                print(f"    Error: {e.error['data']['message']}")

    for key, value in errors.items():
        print(key, '->', value)
