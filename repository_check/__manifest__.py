# -*- encoding: utf-8 -*-
##############################################################################
#
# Copyright (c) 20120 Didotech SRL (info at didotech.com)
#                          All Rights Reserved.
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsability of assessing all potential
# consequences resulting from its eventual inadequacies and bugs
# End users who are looking for a ready-to-use solution with commercial
# garantees and support are strongly adviced to contract a Free Software
# Service Company
#
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
##############################################################################

{
    'name': 'repository check',
    'summary': """Module executes "git pull" or "hg pull -u" command on repository path.""",
    'description': """A module for repository check files from Git and Mercurial repositories
    
    You should install GitPython and Mercurial python modules:
    
    pip install GitPython==3.1.2
    pip install mercurial==5.4.1
    
    """,

    "author": "Didotech SRL",
    'website': 'http://www.didotech.com',
    'category': 'Customer Relationship Management',
    'version': '0.2.4',

    # any module necessary for this one to work correctly
    'depends': [
        'base'
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
