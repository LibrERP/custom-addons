"""
pip install odoo_rpc_client

odoo = client('localhost', 'database', 'user', 'password')
"""

from odoo_rpc_client import Client

# assume that odoo server is listening localhost on standard 8069 port and
# have database 'my_db'.
odoo = Client('localhost', 'db_name', 'admin', '******')

# get current user
odoo.user
print(odoo.user.name)

partner_model = odoo['res.partner']

partner_ids = partner_model.search([])

total_count = len(partner_ids)
doubles = 0

for count, partner_id in enumerate(partner_ids):
    # simple rpc calls
    partner = partner_model.read(partner_id)
    if partner['vat']:
        doubled_partners = partner_model.search([
            ('sanitized_vat', '=', partner['vat']),
            '|',
            ('company_id', 'child_of', 1),
            ('company_id', '=', False)
        ])
        if len(doubled_partners) > 1:
            commercial_partner_id = partner['commercial_partner_id'][0]
            for dpartner_id in doubled_partners:
                if dpartner_id == partner_id:
                    continue
                else:
                    dpartner = partner_model.read(dpartner_id)
                    if dpartner['commercial_partner_id'][0] != commercial_partner_id:
                        doubles += 1
                        print(f"{count}/{total_count}  {doubles}")
                        print(f"{commercial_partner_id}/{dpartner['commercial_partner_id'][0]}: {partner['name']}: {partner['vat']}")
