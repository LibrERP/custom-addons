# -*- encoding: utf-8 -*-

from .repo_base import RepoBase
import os
import logging
import time
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
logging.root.setLevel(logging.INFO)

try:
    from mercurial import(
        error,
        ui,
        hg,
        revlog,
        commands,
        cmdutil
    )

    from mercurial.node import hex

except ImportError as err:
    _logger.debug(err)
    _logger.debug('!!! Please install mercurial module !!!')
    time.sleep(3)


class RepoHg(RepoBase):

    def __init__(self, repo_path, user, passwd):
        """
        Initialize the class. This function from repo_path creates self._repo object (hg.repository).
        :param in: repo_path repository path to get data from
        :param in: user username in SSH private key to use for the session authentication to the desired ``hostname``.
        :param in: passwd password in SSH private key
        :raise UserError: if couldn't create self._repo object (hg.repository failed).
        """
        super().__init__(repo_path, user, passwd)

        self._myui = None
        self._repo = None

        if not os.path.exists(self._repo_path):
            _logger.error('No such path exists, path = {}'.format(self._repo_path))
            raise UserError('No such path exists, path = {}'.format(self._repo_path))

        try:
            self._myui = ui.ui()
            self._repo = hg.repository(self._myui, repo_path.encode('utf-8'))
        except error.Abort as exp:
            _logger.error('Invalid hg repository: {}, {} '.format(self._repo_path, (str(exp))))
            raise UserError("Invalid hg repository: {}, {} ".format(self._repo_path, (str(exp))))

    def print_check_status(self):
        """
        Check that all sources in repository path have been committed before calling 'hg pull -u'.
        Calls "hg status" and writes err_str if the changeset has been modified or if a file has
        been added, removed, or deleted. If finds non committed files pull command will not be started.
        :param in: self._repo (hg.mercurial): the repository to get data from
        Returns err_str: with details of the last non committed files in the repository if found, otherwise ''.
        """
        errstr = ''
        status = self._repo.status()
        changed_state = ['modified', 'added', 'removed', 'deleted']

        first_time_flag = True
        for state in changed_state:
            check = getattr(status, state, 0)
            if check:
                if first_time_flag:
                    first_time_flag = False
                    errstr = 'Changes have been made since the tip changeset.\n'
                    errstr += 'You need to either commit these changes or revert or rollback to the last changeset!\n'
                    errstr += 'Since the last changeset the following files have been\n'
                errstr += '{}:\n'.format(state)
                errors = [item.decode('utf-8') for item in check]
                errstr += '\n'.join(errors) + '\n'

        return errstr

    def print_repository(self):
        """
        Get the repository details.
        :param in: self._repo (hg.repository): the repository to get data from
        Returns str: with details of the active branch and remote url in the repository
        """
        details = ''
        ctx = self._repo[b'tip']
        remote_url = self._repo.ui.expandpath(b'default').decode('utf-8')  # hope this is the repo remote url!

        branch = ctx.branch().decode('utf-8')  # the branch of the changeset 'tip'
        description = ctx.description().decode('utf-8')  # the changeset log message
        details += 'Repo description: {}\n'.format(description)
        details += 'Repo active branch is: {}\n'.format(branch)
        details += 'Remote URL "{}"\n'.format(remote_url)
        details += 'Last changeset for repo is: {}:{} tip.\n'.format(ctx.rev(), ctx)

        return details

    def pull_repository(self):
        """
        Pull changes from a remote repository to a local one. This finds all changes from the repository at
        the specified pathor URL and adds them to a local repository (the current one specified in hg.repository()
        initialization). This also update the copy of the project in the working directory (used option update=True).
        The SOURCE is omitted, so the 'default' path will be used.
        (commands.pull returns 0 on success, 1 if an update had unresolved files.)
        :param in: self._repo (hg.mercurial): the repository to get data from
        Returns :ret_code: True on success, False otherwise.
                :output: if ret_code False
        """

        ret_code = True
        # here is wrong to use global ui (self._myui), ui must be self._repo.ui copy associat:ed to repository!
        self._repo.ui.pushbuffer(error=True, subproc=True)

        # it's important to use local repository copy of ui (self._repo.ui)
        ret = commands.pull(self._repo.ui, self._repo, update=True)
        if ret:
            ret_code = False

        output = self._repo.ui.popbuffer().decode('utf-8')

        return ret_code, output

    # def remote_ssh_url_has_pwd(self):
    #     """
    #     Control if remote url of repository starts with 'ssh://', in that case control if username and password are
    #     specified, otherwise will raise UseError.
    #     :param in: self._repo (hg.repository): the repository to get data from
    #     :raise UserError: if username and password are missing.
    #     Returns: True if no error message, otherwise False.
    #     """
    #
    #     # pull command doesn't specify source, it will be read from .hg/hgrc in [paths] as default=..(source=b'default')
    #     remote_url = self._repo.ui.expandpath(b'default').decode('utf-8')
    #     is_ssh_url = remote_url.startswith('ssh://')
    #     if not(self._user and self._passwd and is_ssh_url):
    #         _logger.error(
    #             'Can\'t launch pull command, please insert your username and password, necessary for ssh:// prefix !')
    #         raise UserError(
    #             'Can\'t launch pull command, please insert your username and password, necessary for ssh:// prefix!')
    #
    #     return True

    def pull_cmd(self):
        """
        Pull upstream commits from remote branch (default).
        :param in: self._repo (hg.mercurial): the repository to get data from
        :param out: self._output_list, list of info or error messages in append, to inform about events that happens
        during the execution of the same command or exceptions.
        Returns: True if received successfully the message returned from mercurial.commands.pull(),, False otherwise.
        """
        ret_flag = True

        self._output_list.append(str(time.ctime()) + ": Checking for updates")

        if self._user and self._passwd:
            project_dir = os.path.dirname(os.path.abspath(__file__))
            os.environ['SSH_ASKPASS'] = os.path.join(project_dir, 'askpass.py')
            os.environ['REPO_USERNAME'] = self._user
            os.environ['REPO_PASSWORD'] = self._passwd

        try:
            ret_flag, output = self.pull_repository()
            if output:
                self._output_list.append('{}'.format(output))
                _logger.info('output {}'.format(output))

            if self._user and self._passwd:
                # restore the environment back to its previous state after operation.
                del(os.environ['SSH_ASKPASS'])
                del(os.environ['REPO_USERNAME'])
                del(os.environ['REPO_PASSWORD'])

        except error.Abort as exc:
            ret_flag = False
            _logger.error("error.Abort exception occured: {}".format(str(exc)))  # to decode
        except error.FilteredRepoLookupError as exc:
            ret_flag = False
            _logger.error("error.FilteredRepoLookupError exception occured: {}".format(str(exc)))  # to decode
        except UserError as exc:
            # _logger.error('UserError exception occured, {}'.format(str(exc)))
            raise UserError(str(exc))
        except Exception as exc:
            ret_flag = False
            _logger.error('An exception occured, {}'.format(str(exc)))

        return ret_flag

    def pull(self):
        """
        This function makes some control to repo object and calls mercurial.commands.pull(update=True) and use
        configured username and password for authentication.
        All the warnings or info messagess will be returned in one list of strings to permit to send them in output
        to the web client windows.
        :param in: self._repo (hg.mercurial): the repository to get data from
        :param in: self._user: username in SSH private key to use for the session authentication to the desired ``hostname``.
        :param in: self._passwd: password in SSH private key
        Returns:  ret_flag: True if execution finish successfully, False otherwise.
                  self._output_list: list of all messages (also info) that accompany the execution of the same command.
                  In the case of mercurial.error.Abort exception generated mercurial.commands.pull(), its output
                  error will be also added to the output list.
        """

        ret_flag = True

        # return True if ok, otherwise raise, doesn't need to control
        # self.remote_ssh_url_has_pwd()

        ret_str = self.print_check_status()  # Check that all sources have been committed.
        if not ret_str:
            _logger.info('Repo at {} successfully loaded.'.format(self._repo_path))

            repo_details = self.print_repository()
            if repo_details:
                _logger.info(repo_details)
                self._output_list.append(repo_details)

            if not self.pull_cmd():
                ret_flag = False
        else:
            self._output_list.append('{}'.format(ret_str))
            _logger.info(ret_str)
            ret_flag = False

        if not ret_flag:
            self._output_list.append('Hg pull -u request failed. Check logs for details!')
            _logger.info('Hg pull -u request failed. Check logs for details!')

        return ret_flag, self._output_list
