# © 2023 Fabio Giovannelli <fabio.giovannelli@didotech.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)
"""
update_order_lines_sequence.py:

    -d <database>
    -U <user>
    -W <password>
    -H <host:port>, default: localhost:8069
    -P <protocol>, jsonrpc / jsonrpcs / xmlrpc / xmlrpcs. Default: jsonrpc
    -h - help
    -t - Test connection and exit

Ex:

    update_order_lines_sequence.py -d <database> -U admin -W <password>
    update_order_lines_sequence.py -d <database> -H <host:port> -P <protocol> -U admin -W <password>

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
        elif opt in ('-W', '--password'):
            password = arg
        elif opt in ('-H', '--host'):
            if ':' in arg:
                host, port = arg.split(':')
                port = int(port)
            else:
                host = arg
        elif opt in ('-P', '--protocol'):
            protocol = arg
        elif opt in ('-t', '--test'):
            test = True
        elif opt in ('-h', '--help'):
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
    user_model = odoo.get_model("res.users")
    user_ids = user_model.search([("login", "=", "admin")])
    user_info = user_model.read(user_ids[0], ["name"])
    print(user_info["name"])

    sale_order_model = odoo.get_model('sale.order')

    if test:
        sys.exit()

    orders = sale_order_model.search_read([
        ('invoice_ids', '=', False),
    ], ['id'])

    orders_count = len(orders)
    # print('orders_count', orders_count)
    for count, order in enumerate(orders, start=1):
        sale_order_model.update_sequence(order['id'])
        print('aggiornato ordine: ', order['id'])

