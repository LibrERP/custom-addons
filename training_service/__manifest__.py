{
    'name': "Training Service",
    'summary': """
        Manage Training""",
    'author': "powERP enterprise network",
    'website': "https://github.com/LibrERP/custom-addons",
    'category': 'Training',
    'version': '12.0.0.2',
    'depends': [
        'base',
        'sale'
    ],
    # always loaded
    'data': [
        'security/training_security.xml',
        'security/ir.model.access.csv',
        'views/training_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [],
}
