# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Fast API Demo',
    'version': '0.1.0',
    'category': 'API',
    'website': 'https://www.codebeex.com',
    'summary': 'FastAPI Demo',
    'description': """
        Module adds endpoint and creates one get route.
        To make it work an endpoint should be created in Odoo
    """,
    'depends': [
        'fastapi',
    ],
    'data': [
        # 'data/demo_user_data.xml'
    ],
    'demo': [],

    'installable': True,
    'application': False,
    'assets': {},
    'license': 'LGPL-3',
}
