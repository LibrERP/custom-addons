"""
pip install odoo-client-lib

odoo_access = ('localhost', '8069', '<database>', 'admin', '*******')
"""

import odoolib
from collections import namedtuple
from rpc_config import odoo_access

OdooRPC = namedtuple('Odoo', ['host', 'port', 'database', 'user', 'password'])

rpc = OdooRPC(*odoo_access)

connection = odoolib.get_connection(
    hostname=rpc.host, database=rpc.database,
    login=rpc.user, password=rpc.password
)
bom_model = connection.get_model("mrp.bom")
product_model = connection.get_model("product.product")
x = 0

for count, bom_id in enumerate(bom_model.search([])):
    bom = bom_model.read(bom_id, ["product_id", 'product_tmpl_id'])
    if bom['product_id']:
        product = product_model.read(bom['product_id'][0], ['name', 'product_tmpl_id'])

        if bom['product_tmpl_id'][0] != product['product_tmpl_id'][0]:
            x += 1
            print(f'{x}: {count}')
            print(f'{bom["product_id"]}: {product["name"]}')

            bom_model.write(bom_id, {'product_tmpl_id': product['product_tmpl_id'][0]})
