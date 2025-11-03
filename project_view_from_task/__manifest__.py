# © 2025 Andrei Levin - Codebeex srl (www.codebeex.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# noinspection PyStatementEffect
{
    'name': 'Open Project from Tasks',
    'version': '18.0.0.0',
    'category': 'Project',
    'summary': 'Open Project from Tasks Kanban',
    'author': 'Codebeex srl',
    'website': 'https://www.codebeex.com',
    'license': 'AGPL-3',
    'depends': [
        'base',
        'project'
    ],
    'data': [
        'views/project_task_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'project_view_from_task/static/src/js/project_task_kanban_custom.js',
            "project_view_from_task/static/src/xml/project_task_kanban_button.xml",
        ],
    },
}
