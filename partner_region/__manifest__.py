# © 2020-2023 Fabio Colognesi - Didotech srl
# © 2024-2026 Fabio Colognesi - Codebeex srl (www.codebeex.com)
#
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# noinspection PyStatementEffect
{
    'name': 'Partner Region',
    'version': '18.0.1.0.1',
    'category': 'Contacts',
    'summary': 'Adds region (sub-country / supra-state) hierarchy on partners',
    'author': 'Didotech srl',
    'website': 'https://www.codebeex.com',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'contacts',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/res_country_data.xml',
        'data/res.country.region.csv',
        'data/res.country.state.csv',
        'views/partner_view.xml',
    ],
    'installable': True,
    'auto_install': False,
}
