# © 2026 Andrei Levin <andrei.levin@didotech.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)
"""
set_region.py:

    -d <database>
    -U <user>
    -W <password>
    -H <host:port>, default: localhost:8069
    -P <protocol>, jsonrpc / jsonrpcs / xmlrpc / xmlrpcs. Default: jsonrpc
    -h - help
    -t - Test connection and exit

Ex:

    set_region.py -d <database> -U admin -W <password>
    set_region.py -d <database> -H <host:port> -P <protocol> -U admin -W <password>

Installation:
    pip install odoo-client-lib

"""

import odoolib
import getopt
import sys


def get_category_code(model, name):
    print(f'{name}')
    record_ids = model.search([
        ('complete_name', '=', name)
    ], context={'active_test': False})

    if len(record_ids) == 1:
        return record_ids[0]
    elif len(record_ids) > 1:
        print(f'Too many records of Category found')
        return record_ids[0]
    return False


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
    user_model = odoo.get_model("res.users")
    user_ids = user_model.search([("login", "=", "admin")])
    user_info = user_model.read(user_ids[0], ["name"])
    print(user_info["name"])

    partner_model = odoo.get_model('res.partner')
    region_model = odoo.get_model('res.country.region')

    if test:
        sys.exit()

    errors = []

    start = 0
    # end = 400

    partners = partner_model.search_read([
        ('parent_id', '=', False),
        ('region_id', '=', False),
        ('state_id', '!=', False),
        ('country_id.code', '=', 'IT')
    ], ('id', 'name', 'state_id'))

    state2region = {}

    for counter, partner in enumerate(partners, start=1):
        if counter > start:
            print(f"{counter}: {partner['name']} - {partner['state_id'][1]}")

            if partner['state_id'][0] in state2region:
                region_id = state2region[partner['state_id'][0]]
            else:
                regions = region_model.search_read([
                    ('state_ids', 'in', partner['state_id'][0])
                ], ('id', 'name'))

                if len(regions) == 1:
                    region_id = state2region[partner['state_id'][0]] = regions[0]['id']

                    print(f"Region: {regions[0]['name']}")
                else:
                    print(f"Region not found for {partner['state_id'][1]}")
                    continue

            partner_model.write(partner['id'], {'region_id': region_id})