{
    'name': "Sale Order Logging",
    'summary': """
        More detailed logging of Sale Order changes""",
    'author': "powERP enterprise network",
    'website': "https://github.com/LibrERP/custom-addons",
    'category': 'Sales',
    'version': '12.0.0.2',
    'depends': [
        'base',
        'sale',
        'model_logging',
    ],
    # always loaded
    'data': [
        # 'security/training_security.xml',
        # 'security/ir.model.access.csv',
        # 'views/training_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [],
}
