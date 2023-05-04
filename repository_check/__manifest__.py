# © 2020-2023 Didotech srl (www.didotech.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'repository check',
    'summary': """Module executes "git pull" or "hg pull -u" command on repository path.""",
    'description': """A module permit to pull files from Git and Mercurial repositories
    
You should install GitPython and Mercurial python modules:
    
    pip install GitPython==3.1.2
    pip install mercurial==5.4.1
    
It can be necessary to set environment variable:

    GIT_PYTHON_REFRESH=quiet
    
And to verify 'git' executable is in the PATH
    
    """,

    "author": "Didotech SRL",
    'website': 'http://www.didotech.com',
    'category': 'Tools',
    'version': '1.12.9',

    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'mail'
    ],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/repository_view.xml'
    ],
    'demo': [],

    # "external_dependencies": {
    #     "python": [
    #         'GitPython',
    #          'mercurial'
    #     ],
    #     "bin": []
    # },

    # "application": False,
    'installable': True,
    'auto_install': False,
}
