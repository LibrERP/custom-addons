{
    'name': "Partner Origin",
    'summary': """
        Information about partner origin""",
    'author': "librERP enterprise network",
    'website': "https://github.com/LibrERP/custom-addons",
    'category': 'Sales',
    'version': '12.0.1.0.3',
    'depends': [
        'base',
        'contacts'
    ],
    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/res_partner_view.xml'
    ],
    # only loaded in demonstration mode
    'demo': [],
}
