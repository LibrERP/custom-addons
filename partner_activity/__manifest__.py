# © 2023 Andrei Levin - Didotech srl (www.didotech.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Partner Activity',
    'version': '15.0.0.0',
    'category': 'Customer Relationship Management',
    'summary': "Show all scheduled activities of the Partner",
    "author": "Didotech srl",
    'website': 'http://www.didotech.com',
    'depends': [
        'base',
        'mail'
    ],
    'data': [
        "views/partner_view.xml"
    ],
    'test': [],
    'installable': True,
    'auto_install': True,
    'application': True,
}
