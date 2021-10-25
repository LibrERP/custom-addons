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
    from git import (
        Repo,
        Git,
        cmd,
        GitError,
        NoSuchPathError,
        remote
    )

    from git.exc import (
        NoSuchPathError,
        InvalidGitRepositoryError,
        GitCommandError,
        UnmergedEntriesError,
        CheckoutError
    )



    from git.util import (
        Iterable,
        IterableList,
        RemoteProgress,
        CallableRemoteProgress
    )


except ImportError as err:
    _logger.debug(err)
    _logger.debug('!!! Please install gitpython module !!!')
    time.sleep(3)

import re
from os.path import isdir,dirname, join
from io import StringIO
import sys
from distutils.version import StrictVersion
from dateutil import parser



# logging.basicConfig(format='%(name)s: %(message)s')
# _logger.setLevel(logging.INFO)

regex = r"^([A-Za-z0-9]+@|http(|s)\:\/\/)([A-Za-z0-9.]+(:\d+)?)(?::|\/)([\d\/\w.-]+?)(\.git)?$"
clone_log = ''

class Progress(remote.RemoteProgress):
    def line_dropped(self, line):
        print(line)



class RedirectedStdout:
    def __init__(self):
        self._stdout = None
        self._string_io = None

    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._string_io = StringIO()
        return self

    def __exit__(self, type, value, traceback):
        sys.stdout = self._stdout

    def __str__(self):
        return self._string_io.getvalue()

class RepoGit(RepoBase):

    def __init__(self, repo_path, user, passwd, repo_name):
        """
        Initialize the class. This function from repo_path creates self._repo object (git.Repo). If the repository is
        bare repository (does not have a default remote origin repository or a working_tree') raise an error.
        :param in: repo_path repository path to get data from
        :param in: user username in SSH private key to use for the session authentication to the desired ``hostname``.
        :param in: passwd password in SSH private key
        :raise UserError: if couldn't create self._repo object (git.Repo failed) or the repository is a bare repository.
        """
        super().__init__(repo_path, user, passwd)

        # if re.search(regex, self._repo_path) or repo_name:
        #     return

        self._repo = None
        # if not os.path.exists(self._repo_path) and not re.search(regex, self._repo_path):
        #     _logger.error('No such path exists, path = {}'.format(self._repo_path))
        #     raise UserError('No such path exists, path = {}'.format(self._repo_path))

        try:
            self._repo = Repo(self._repo_path)
        except InvalidGitRepositoryError as exp:
            _logger.error('Invalid git repository: {}, {} '.format(self._repo_path, exp))
            raise UserError("Invalid git repository: {}, {} ".format(self._repo_path, exp))
        except NoSuchPathError as exp:
            _logger.error('Invalid git repository: {}, {} '.format(self._repo_path, exp))
            return
            #raise UserError("Invalid git repository: {}, {} ".format(self._repo_path, exp))

        if not self._repo.bare:
            type(self._repo.git).GIT_PYTHON_TRACE = "full"  # this works, writes log!
        # else:
        #     _logger.error('Repository {} is a bare repository! Can\'t launch pull command.'.format(self._repo_path))
        #     raise UserError("Repository {} is a bare repository! Can\'t launch pull command.".format(self._repo_path))

    # def remote_ssh_url_has_pwd(self):
    #     """
    #     Control if remote url of repository starts with 'ssh://', in that case control if username and password are
    #     specified, otherwise will raise UseError.
    #     :param in:   self._repo (git.Repo): the repository to get data from
    #     :raise UserError: if username and password are missing.
    #     Returns: True if no error message, otherwise False.
    #     """
    #
    #     remote_origin = self._repo.remotes.origin
    #     if remote_origin.url.startswith('ssh://'):
    #         if not (self._user and self._passwd):
    #             _logger.error(
    #                 'Can\'t launch pull command, please insert your username and password, necessary for ssh:// prefix !')
    #             _logger.error('repo_path={}, remote_url={}'.format(self._repo_path, remote_origin.url))
    #             raise UserError(
    #                 'Can\'t launch pull command, please insert your username and password, necessary for ssh:// prefix!')
    #
    #     return True


    @property
    def check_repo_state(self):
        """
        Check up self._repo object, control  if repository is unstaged (without 'git add') or detached (without branch)
        (commented if it has untracked files), (commented if the active branch is not a 'master').
        :param in:   self._repo (git.Repo): the repository to get data from
        :param out:  self._output_list, list of output/error message in append, to inform about 'unexpected conditions'.
        Returns: True if no error message, otherwise False.
        """
        ret_code = True

        # if 'master' not in self._repo.heads:
        #     ret_code = False
        #     _logger.info('Repository does not have a master branch.')
        #     self._output_list.append('Repository does not have a master branch.')
        # else:
        #     if self._repo.head.ref != self._repo.heads.master:
        #         ret_code = False
        #         _logger.info('Branch {} is not master'.format(self._repo.head.ref))
        #         self._output_list.append('Branch {} is not master'.format(self._repo.head.ref))


        if self._repo.is_dirty():
            ret_code = False
            _logger.info('Repository has unstaged changes.')
            self._output_list.append('Repository has unstaged changes.')
        if self._repo.head.is_detached:
            ret_code = False
            _logger.info('Repository has detached changes.')
            self._output_list.append('Repository has detached changes.')

        # if len(self._repo.untracked_files) > 0:
        #     ret_code = False
        #     _logger.info('Repository has untracked files.')
        #     self._output_list.append('Repository has untracked files.')

        # if 'origin' in self._repo.remotes:
        #     if self._repo.remotes.origin.refs.master.commit != self_repo.head.ref.commit:
        #         ret_code = False
        #         _logger.info('Branch has unsynced changes, different commit.')
        #         self._output_list.append('Branch has unsynced changes, different commit.')

        return ret_code

    def print_repository(self):
        """
        Get the repository details.
        :param in: self._repo (git.Repo): the repository to get data from
        Returns str: with details of the active branch and remote urls in the repository
        """
        details = ''
        try:
            # details += 'Repo description: {}\n'.format(repo.description)
            details += 'Repo active branch is: {}\n'.format(self._repo.active_branch)
            for remote in self._repo.remotes:
                details += 'Remote named "{}" with URL "{}"\n'.format(remote, remote.url)
            details += 'Last commit for repo is {}.\n'.format(str(self._repo.head.commit.hexsha))
        except:
            import traceback
            _logger.error(traceback.format_exc())

        return details

    def pull_cmd(self):
        """
        Pull upstream commits from remote branch 'master' or current and remote repository 'origin'.
        :param in: self._repo (git.Repo): the repository to get data from
        :param out: self._output_list, list of error message in append, to inform about exceptions of GitCmd in GitPython.
        Returns: True if received successfully the message returned from git.cmd.Git().pull(), False otherwise.
        """
        msg = ''
        old_env = {}
        ret_flag = True

        self._output_list.append(str(time.ctime()) + ": Checking for updates")

        # pulls = repo.remote('origin').pull('master')
        remote_origin = self._repo.remotes.origin
        if remote_origin.exists():
            try:
                self._repo.remote()
                # os.environ['SSH_ASKPASS'] = os.path.join(project_dir, 'askpass.py') # NO GIT_SSH
                # os.environ['REPO_USERNAME'] = 'user'
                # os.environ['REPO_PASSWORD'] = '...'
                git_cmd = cmd.Git(self._repo_path)

                # if self._user and self._passwd and remote_origin.url.startswith('ssh://'):
                if self._user and self._passwd:
                    project_dir = os.path.dirname(os.path.abspath(__file__))
                    # old_env = git_cmd.update_environment(SSH_ASKPASS=os.path.join(project_dir, 'askpass.py'),
                    #                                      REPO_USERNAME=self._user, GIT_PASSWORD=self._passwd)
                    old_env = git_cmd.update_environment(SSH_ASKPASS=os.path.join(project_dir, 'askpass.py'),
                                                          REPO_USERNAME=self._user, REPO_PASSWORD=self._passwd)
                msg = git_cmd.pull()
                # restore the environment back to its previous state after operation.
                if old_env:
                    git_cmd.update_environment(**old_env)

                # msg is '' or 'Updating ...' or 'Already up-to-date.' if you pulled successfully
                if msg:  # encoding = 'utf-8', msg1 = msg.decode(encoding) to see if use here instead of msg!
                    _logger.info(str(msg))
                    self._output_list.append(str(msg))
                else:
                    ret_flag = False

            except GitCommandError as exc:
                # after some tests we can cancel _logger.error of exc.stdout e exc.stdin because with
                # GIT_PYTHON_TRACE set to "full" the same output is written to logger.
                ret_flag = False
                if exc.stderr:
                    self._output_list.append(exc.stderr.lstrip())
                    _logger.error('GitCommandError exception occured: {}'.format(exc.stderr.lstrip()))
                elif exc.stdout:
                    self._output_list.append(exc.stdout.lstrip())
                    _logger.error('GitCommandError exception occured: {}'.format(exc.stdout.lstrip()))
            except InvalidGitRepositoryError as exc:
                ret_flag = False
                _logger.error('Invalid git repository: {}, {} '.format(self._repo_path, exc))
            except CheckoutError as exc:
                ret_flag = False
                _logger.error("CheckoutError exception occured: {}".format(exc))
            except UnmergedEntriesError as exc:
                ret_flag = False
                _logger.error("CheckouUnmergedEntriesError exception occured: {}".format(exc))
            # except AssertionError as exc:
            #     ret_flag = False
            #     _logger.error("AssertionError exception occured: {}".format(exc))

        else:
            ret_flag = False
            _logger.info('Remote repository \'origin\' doesn\'t exsist!')
            self._output_list.append('Remote repository \'origin\' doesn\'t exsist!')

        return ret_flag



    def pull(self):
        """
        Tis function makes some control to repo object and executes 'git pull' command. All the warnings or
        info messagess will be returned in one list of strings to permit to send them in output to the web client
        windows. Pull command is called from remote repository 'origin' configured in the git config file and local
        branch is not specified, so as default value will be taken the local/remote branch 'master' or current.
        :param in: self._repo (git.Repo): the repository to get data from
        :param in: self._user: username in SSH private key to use for the session authentication to the desired ``hostname``.
        :param in: self._passwd: password in SSH private key
        Returns:  ret_flag: True if git.cmd.Git().pull() finish successfully, False otherwise.
                  self._output_list: list of all messages (also info) that accompany the execution of the same command.
                  In the case of GitCommandError exception generated from cmd.Git.pull(), its exc.stdout or exc.stdout
                  error will be also added to the output list.
        """

        ret_flag = True

        # return True if ok, otherwise raise, doesn't need to control
        # self.remote_ssh_url_has_pwd()

        # if check_repo_state fails can't continue execution! See if do raise!
        if self.check_repo_state:

            _logger.info('Repo at {} successfully loaded.'.format(self._repo_path))
            repo_details = self.print_repository()
            if repo_details:
                _logger.info(repo_details)
                self._output_list.append(repo_details)

            if not self.pull_cmd():
                ret_flag = False
        else:
            ret_flag = False

        if not ret_flag:
            self._output_list.append('Git pull request failed. Check logs for details!')
            _logger.info('Git pull request failed. Check logs for details!')

        # Get the tags
        tags_unformatted = self._repo.git.tag()
        tags = tags_unformatted.split('\n')
        tags = [tag.replace('r', '').replace('a', '').replace('b', '') for tag in tags if tag[0] == 'r']
        tags.sort(key=StrictVersion)
        last_version = int(tags[-1].split('.')[1]) - 2
        tags.reverse()
        for idx, tag in  enumerate(tags):
            if last_version == int(tag.split('.')[1]):
                tag_to_start = tags[idx-1]
                break
        logs = self._repo.git.log(f"r{tag_to_start}..HEAD", '--tags', '--oneline', '--pretty=format:"%d%ad%x09%s"')

        collective_text = ""
        tag_name = {}
        for idx, log in enumerate(logs.split('\n')):
            if idx == 0:
                tag = log.split(': ')[1].split(',')[0]
                date, message = log.split(')')[1].split('\t')
                date = parser.parse(date).strftime("%d-%m-%Y %H:%M:%S")
                message = message.replace('"', '')
                collective_text += tag + '\n'
                collective_text += date + message + '\n'
                tag_name[tag] = [{'date': date, 'message': message}]
            else:
                if "tag:" in log:
                    tag = log.split(': ')[1].split(')')[0]
                    collective_text += tag + '\n'
                    tag_name[tag] = []
                else:
                    date, message = log.split('\t')
                    if 'Merge' in message:
                        continue
                    message = message.replace('"', '')
                    date = date.replace('"', '')
                    if ')' in date:
                        date = date.split(')')[1]
                    date = parser.parse(date).strftime("%d-%m-%Y %H:%M:%S")
                    dict_copy = tag_name.copy()
                    tag_list = dict_copy[tag]
                    tag_list.append({'date': date, 'message': message})

        return ret_flag, self._output_list, tag_name

    def clone_cmd(self, repo_name):
        """
        Clones repositories either from a local source or from a remote origin
        :param in: self._repo (git.Repo): the repository to get data from
        :param out: self._output_list, list of error message in append, to inform about exceptions of GitCmd in GitPython.
        Returns: True if the process of cloning the repo executes without errors, False if the directory already exists or
        the repo link is incorrect
        """
        cloned_log=''

        #Build Github url
        github_url = f'https://github.com/OCA/{repo_name}'

        #Check if target directory already contains the repo
        if isdir(self._repo_path):
            raise UserError(f'Module already exists in: {self._repo_path}')

        #Clone the repository using a remote url
        if re.search(regex, self._repo_path) or repo_name:
            try:
                with RedirectedStdout() as out:
                    cloned_log = Repo.clone_from(url=github_url, to_path=self._repo_path, progress=Progress(), branch='12.0')

                #_logger.info('Git clone request failed. Check logs for details!')
            except GitCommandError:
                _logger.info('Git clone request failed. Check logs for details!')
                return False
        # else:
        #     # Clone the repository using a local directory as source
        #     try:
        #         self._repo.clone(path=target_dir)
        #     except GitCommandError:
        #         _logger.info('Git clone request failed. Check logs for details!')
        #         return False

        return True, out




    # end RepoGit
    # the next functions can be used forward

    def print_commit(self, commit):
        details = ''
        try:
            details += '----\n'
            details += str(commit.hexsha)
            details += "\"{}\" by {} ({})\n".format(commit.summary, commit.author.name, commit.author.email)
            details += '{}\n'.format(str(commit.authored_datetime))
            details += str("count: {} and size: {}\n".format(commit.count(), commit.size))
        except:
            import traceback
            _logger.error(traceback.format_exc())

        return details

    def get_last_commit_details(self):
        """
        Get the HEAD details for a given repository (similar to git logger).
        :param in: self._repo (git.Repo): the repository to get data from
        Returns str: with details of the last commit in the repository
        """
        details = ''

        try:
            details += 'commit {}'.format(self._repo.active_branch.commit.hexsha) + '\n'
            details += 'Author: {} <{}>'.format(
                self._repo.active_branch.commit.author.name,
                self._repo.active_branch.commit.author.email
            ) + '\n'
            details += 'Date: {}'.format(self._repo.active_branch.commit.authored_datetime) + '\n'
            details += self._repo.active_branch.commit.message.strip().split('\n', 1)[0]
        except:
            import traceback
            _logger.error(traceback.format_exc())
        return details
