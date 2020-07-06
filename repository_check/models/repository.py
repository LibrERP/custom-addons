# -*- encoding: utf-8 -*-

from odoo import models, fields, api
from .repo_git import RepoGit
from .repo_hg import RepoHg

import time
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT
from os.path import isdir, join
import logging
from odoo.exceptions import AccessError, UserError, ValidationError


_logger = logging.getLogger(__name__)
_logger.setLevel(logging.INFO)

try:
    from git.exc import InvalidGitRepositoryError
except ImportError as err:
    _logger.debug(err)
    _logger.debug('!!! Please install gitpython module !!!')
    time.sleep(3)


GIT_TYPE = 'git'
MERCURIAL_TYPE = 'hg'
NO_TYPE = 'disable'


class RepositoryCheck(models.Model):
    _name = 'repository.check'
    _rec_name = 'repository_path'
    _description = 'Check Repository'

    repository_path = fields.Char('Repository Path', size=200, help="Repository path in local filesystem.", required=True,
                                  default='')
    repository_type = fields.Selection([
        ('git', 'Git'),
        ('hg', 'Mercurial'),
        ('disable', 'Disable')
    ], string='Type', readonly=True, default='disable')

    username = fields.Char('Username', required=False, default='')
    password = fields.Char('Password', required=False, default='')
    last_check_state = fields.Selection([
        ('new', ''),
        ('done', 'Success'),
        ('failed', 'Failed')
    ], string='Last Check State', readonly=True, default='new')
    last_check = fields.Date('Last Check', readonly=True)
    log = fields.Text('Logging', readonly=True, default='')

    _sql_constraints = [
        ('unique_repository_path', 'UNIQUE(repository_path)', 'Repository path must be unique !')
    ]

    def exec_git_pull_cmd(self, repo_path, user, passwd):
        """This function calls git.cmd.Git().pull() command only for 'git' type
        and use configured username and password"""

        ret_str = ''
        ret_flag = False
        try:
            # to decide if send msg or err_msg to client window
            git_repo = RepoGit(repo_path, user, passwd)
            ret_flag, err_msgs = git_repo.pull()
            if len(err_msgs) > 0:
                ret_str = '\n'.join(str(x) for x in err_msgs)

        except UserError as e:
            # _logger.error('UserError exception occured, {}'.format(e))
            self.last_check_state = 'failed'
            raise UserError(str(e))

        except InvalidGitRepositoryError as e:
            self.last_check_state = 'failed'
            _logger.error('Invalid git repository: {}, {} '.format(repo_path, e))
            raise UserError("Invalid git repository: {}, {} ".format(repo_path, e))

        except Exception as e:
            self.last_check_state = 'failed'
            _logger.error('An exception occured, {}'.format(e))
            ret_str += 'Git pull request failed. Check logs for details!\n'

        # except:
        #     import traceback
        #     _logger.error(traceback.format_exc())

        return ret_flag, ret_str

    def exec_hg_pull_cmd(self, repo_path, user, passwd):

        ret_str = ''
        err_msg = ''
        ret_flag = False
        try:
            # to decide if send msg or err_msg to client window
            hg_repo = RepoHg(repo_path, user, passwd)
            ret_flag, err_msgs = hg_repo.pull()
            if len(err_msgs) > 0:
                ret_str = '\n'.join(str(x) for x in err_msgs)

        # except error.Abort as e:
        #     _logger.error('Mercurial Abort error {}'.format(e.decode())))

        except UserError as e:
            # _logger.error('UserError exception occured, {}'.format(e))
            self.last_check_state = 'failed'
            raise UserError(str(e))

        except Exception as e:
            _logger.error('An exception occured, {}'.format(e))
            self.last_check_state = 'failed'
            ret_str += 'Hg pull -u request failed. Check logs for details!\n'
        return ret_flag, ret_str

    @api.multi
    def action_pull_repository(self):
        if self.env.context.get('active_ids'):
            for repository in self.browse(self.env.context['active_ids']):
                # print(repository.repository_path)
                repository.action_pull()

    @api.multi
    def action_pull(self):
        values = {}

        ret_str = ''
        ret_code = False
        current_date = time.strftime(DEFAULT_SERVER_DATE_FORMAT)

        self.ensure_one()

        repository_path = self.repository_path
        repository_type = self.repository_type
        password = self.password
        user = self.username

        if repository_type == NO_TYPE:
            _logger.error('Can\'t launch pull command, the specified path isn\'t configured to allow it (path={})!'.format(repository_path))
            raise UserError('Can\'t launch pull command, path={} isn\'t configured to allow it!'.format(repository_path))

        if (password and not user) or (not password and user):
            if password:
                _logger.error('Can\'t launch pull command, please insert also your username!')
                raise UserError('Can\'t launch pull command, please insert also your username!')
            if user:
                _logger.error('Can\'t launch pull command, please insert also your password (user={})!'.format(user))
                raise UserError('Can\'t launch pull command, please insert also your password!')

        if repository_type == GIT_TYPE:
            ret_code, ret_str = self.exec_git_pull_cmd(repository_path, user, password)
        elif repository_type == MERCURIAL_TYPE:
            ret_code, ret_str = self.exec_hg_pull_cmd(repository_path, user, password)

        if ret_code:
            self.last_check_state = 'done'
            # write current date of last pull command
            values['last_check'] = current_date
        else:
            self.last_check_state = 'failed'

        values['last_check_state'] = self.last_check_state
        if ret_str != '':
            values['log'] = '{}'.format(ret_str)

        if values:
            self.write(values)

        return True

    def set_default_type(self, path):
        path = path.rstrip('/')

        if isdir(join(path, '.git')):
            ret_type = GIT_TYPE
        elif isdir(join(path, '.hg')):
            ret_type = MERCURIAL_TYPE
        else:
            ret_type = NO_TYPE

        return ret_type

    @api.model
    def create(self, values):
        # check if repository_path is directory and if inside has .git or .hg directory
        view_path = values.get('repository_path', '')
        if not view_path:
            _logger.error('You have not defined the \'Repository Path\'')
            raise UserError('You have not defined the \'Repository Path\'')

        if not isdir(view_path):
            _logger.error('{} is not a valid repository.'.format(view_path))
            raise UserError('{} is not a valid repository.'.format(view_path))

        # TODO test if last_check_state and log should be set as default, add here to be sure
        values['log'] = ''
        values['last_check_state'] = 'new'
        view_type = self.set_default_type(view_path)
        values['repository_type'] = view_type

        return super(RepositoryCheck, self).create(values)

    @api.multi
    def write(self, values):

        # if there is no values to write return
        if not values:
            return True

        self.ensure_one()
        # recordset = self.browse(self.ids[0])

        if 'repository_path' in values:
            # if changed path, can change also type
            view_path = values['repository_path']
            view_type = self.set_default_type(view_path)  # every time check type, maybe is wrong latest in db!
            values['repository_type'] = view_type
            # onchange doesn't work for readonly fields (last_check_state, log), they will not be passed to write!
            # think that every time when repository_path is changed(in values) need to reset last_check_state and log
            # if view_type == 'disable':
            values['last_check_state'] = 'new'
            values['last_check'] = None
            values['log'] = ''
        else:
            view_path = self.repository_path
            view_type = self.repository_type

        # TODO to control ...
        # values['last_check_state'] = self.last_check_state

        if not isdir(view_path):
            _logger.error('{} is not a valid repository.'.format(view_path))
            raise UserError('{} is not a valid repository.'.format(view_path))

        # if 'log' not in values: # to see if do this: clear log text field !
        #     values['log'] = ''
        #     self.log.default = ''

        return super(RepositoryCheck, self).write(values)

    @api.onchange('repository_path')
    def onchange_repository_path(self):

        # ids is set only if path field is changed on already created record (not if it's new to be create)
        if self.repository_path:
            if isdir(self.repository_path):
                view_type = self.set_default_type(self.repository_path)
                # try to set repository_type here...to be tested
                self.repository_type = view_type
                self.log = ''
                self.last_check_state = 'new'
            else:
                return {
                    # 'value': {},
                    'warning': {
                        'title': 'Warning!',
                        'message': '"{}" is not a valid repository'.format(self.repository_path)
                    }
                }
        else:
            self.repository_type = 'disable'
            self.log = ''
            self.last_check_state = 'new'
