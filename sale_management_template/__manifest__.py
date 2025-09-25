# © 2025 Andrei Levin - Codebeex srl (www.codebeex.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# noinspection PyStatementEffect
{
    'name': 'Sale Management Template',
    'version': '12.0.0.3',
    'category': 'Customer Relationship Management',
    'summary': 'Module enhance Sale Management Template related functionality',
    'author': 'Codebeex srl',
    'website': 'https://www.codebeex.com',
    'license': 'AGPL-3',
    'depends': [
        'base',
        'sale_management',
        'web_onchange_wizard',
        'web_widget_many2many_tags_multi_selection',
    ],
    'data': [
        # 'views/assets.xml',
        'views/product_views.xml',
        'views/sale_views.xml'
    ],
}
