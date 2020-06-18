# -*- encoding: utf-8 -*-

import os
import logging
import time

_logger = logging.getLogger(__name__)  # log
logging.basicConfig(level=logging.INFO)
logging.root.setLevel(logging.INFO)

try:
    from mercurial import (
        error,
        ui,
        hg,
        revlog,
        commands,
        cdmutil
    )
except ImportError as err:
    _logger.debug(err)
    _logger.debug('!!! Please install mercurial module !!!')
    time.sleep(3)

try:
    from mercurial.node import hex
except ImportError as err:
    _logger.debug(err)
    _logger.debug('!!! Please install mercurial module !!!')
    time.sleep(3)


# example raise error.Abort("The repository is not local")
# from mercurial.node import hex  # should I have used this?

# class HGStatusNotEmptyError(Exception):
#     """
#     Alert when a hg repository has a non-empty status, meaning that
#     there are modifications or changes to the repository from the stored
#     changeset.
#     """
#
#     def __init__(self, modified=[], added=[], removed=[], deleted=[]):
#         self.modified = modified
#         self.added = added
#         self.removed = removed
#         self.deleted = deleted
#
#     def __str__(self):
#         errstr = 'Changes have been made since the tip changeset.\n'
#         errstr += 'You need to either commit these changes or revert\n'
#         errstr += 'or rollback to the last changeset!'
#         if len(self.modified) > 0:
#             errstr += '\n  The following files have been modified since the \n'
#             errstr += '  last changeset:\n'
#             for item in self.modified:
#                 errstr += '    ' + item + '\n'
#         if len(self.added) > 0:
#             errstr += '\n  The following files have been added since the \n'
#             errstr += '  last changeset:\n'
#             for item in self.added:
#                 errstr += '    ' + item + '\n'
#         if len(self.removed) > 0:
#             errstr += '\n:  The following files have been removed since the \n'
#             errstr += '  last changeset:\n'
#             for item in self.removed:
#                 errstr += '    ' + item + '\n'
#         if len(self.deleted) > 0:
#             errstr += '\n  The following files have been deleted since the \n'
#             errstr += '  last changeset:\n'
#             for item in self.deleted:
#                 errstr += '    ' + item + '\n'
#
#         return errstr


def get_configured_ui():
    """Configure any desired ui settings."""
    u = ui.ui()
    # The following will suppress all messages. This is the same as adding the following setting to the repo
    # hgrc file' [ui] section: quiet = True
    # u.setconfig('ui', 'quiet', True)
    return u


# def get_repo_for_repository(app, repository=None, repo_path=None, create=False):
#     if repository is not None:
#         return hg.repository(get_configured_ui(), repository.repo_path(app), create=create)
#     if repo_path is not None:
#         return hg.repository(get_configured_ui(), repo_path, create=create)

def get_repo_from_path(u, repo_path):
    # for mercurial obj strings must be converted in bytes
    # The first parameter to encode defaults to 'utf-8' ever since Python 3.0.
    repo = None
    if repo_path is not None:
        repo = hg.repository(u, repo_path.encode())
    return repo


def get_repository_heads(repo):
    """Return current repository heads, which are changesets with no child changesets."""
    heads = [repo[h] for h in repo.heads(None)]
    return heads


# def get_repo_hex(reporoot):
#     # This gets the tip rev in hex as a string
#     repo = hg.repository(ui.ui(), reporoot)
#     revs = repo.revs('tip')
#     if len(revs) == 1:
#         return str(repo.changectx(revs[0]))
#     else:
#         raise Exception("Internal failure in get_repo_hex")

def print_check_status(repo):
    """
    Calls "hg status" and raises a
    :class: HGStatusNotEmptyError`, if the changeset
    has been modified, or if a file has been added, removed, or deleted.
    """
    errstr = ''
    modified, added, removed, deleted = repo.status()[:4]
    # if modified or added or removed or deleted:
    #    raise HGStatusNotEmptyError(modified, added, removed, deleted)

    if modified or added or removed or deleted:

        errstr = 'Changes have been made since the tip changeset.\n'
        errstr += 'You need to either commit these changes or revert\n'
        errstr += 'or rollback to the last changeset!'
        if len(modified) > 0:
            errstr += '\n  The following files have been modified since the \n'
            errstr += '  last changeset:\n'
            for item in modified:
                errstr += '    ' + item + '\n'
        if len(added) > 0:
            errstr += '\n  The following files have been added since the \n'
            errstr += '  last changeset:\n'
            for item in added:
                errstr += '    ' + item + '\n'
        if len(removed) > 0:
            errstr += '\n:  The following files have been removed since the \n'
            errstr += '  last changeset:\n'
            for item in removed:
                errstr += '    ' + item + '\n'
        if len(deleted) > 0:
            errstr += '\n  The following files have been deleted since the \n'
            errstr += '  last changeset:\n'
            for item in deleted:
                errstr += '    ' + item + '\n'

    return errstr


def get_tip(repo):
    """
    Get the changeset id of the hg tip as a hex number.
    """
    return hex(repo.changelog.tip())


def get_changeset_dict(repo, id=None):
    """
    Return a dictionary of a given changeset given by a changeset id
    where the keys are the values as returned by the `Mercurial API
    <http://mercurial.selenic.com/wiki/MercurialApi>_`.

    :param id: The changeset ID in hexadecimal format as a string.
    Default is ``None``, which defaults to ``'tip'``.
    """
    if id is None:
        id = 'tip'
    ctx = repo[id]

    return dict( \
        rev=ctx.rev(),  # the revision number \
        node=hex(ctx.node()),  # the revision ID, in hexadecimal \
        user=ctx.user(),  # the user who created the changeset \
        date=ctx.date(),  # the date of the changeset \
        files=ctx.files(),  # the files changed in the changeset \
        description=ctx.description(),  # the changeset log message \
        branch=ctx.branch(),  # the branch of the changeset \
        tags=ctx.tags(),  # a list of the tags applied to the changeset \
        parents=repr(ctx.parents()),  # a list of the change context objects  \
        # for the changeset's parents \
        children=ctx.children()  # a list of the change context \
        # objects for the changeset's children
    )


# def pull_repository(u, repo, repository_clone_url, ctx_rev):
#     """Pull changes from a remote repository to a local one."""
#     commands.pull(u, repo, source=repository_clone_url, rev=[ctx_rev])

# u = ui.ui()
# repo = hg.repository(u, "/path/to/repo")
# u.pushbuffer()
# # command / function to call, for example:
# commands.log(u, repo)
# output = u.popbuffer()
# assert type(output) == str


def update_repository(u, repo):
    """
    Update the cloned repository to changeset_revision.  It is critical that the installed repository is updated to the desired
    changeset_revision before metadata is set because the process for setting metadata uses the repository files on disk.

    # update working directory (or switch revisions)
    # Update the repository's working directory to the specified
    # changeset. If no changeset is specified, update to the tip of the
    # current named branch and move the active bookmark (see :hg:`help
    # bookmarks`).

    update working directory
    Update the repository's working directory to the tip of the
    current named branch and move the active bookmark (see :hg:`help
    bookmarks`).
    Update sets the working directory's parent revision to the specified
    changeset (see :hg:`help parents`).
    If the changeset is not a descendant or ancestor of the working
    directory's parent and there are uncommitted changes, the update is
    aborted. With the -c/--check option, the working directory is checked
    for uncommitted changes; if none are found, the working directory is
    updated to the specified changeset.
    .. container:: verbose
      The -C/--clean, -c/--check, and -m/--merge options control what
      happens if the working directory contains uncommitted changes.
      At most of one of them can be specified.
      1. If no option is specified, and if
         the requested changeset is an ancestor or descendant of
         the working directory's parent, the uncommitted changes
         are merged into the requested changeset and the merged
         result is left uncommitted. If the requested changeset is
         not an ancestor or descendant (that is, it is on another
         branch), the update is aborted and the uncommitted changes
         are preserved.
      2. With the -m/--merge option, the update is allowed even if the
         requested changeset is not an ancestor or descendant of
         the working directory's parent.
      3. With the -c/--check option, the update is aborted and the
         uncommitted changes are preserved.
      4. With the -C/--clean option, uncommitted changes are discarded and
         the working directory is updated to the requested changeset.
    To cancel an uncommitted merge (and lose your changes), use
    :hg:`merge --abort`.
    Use null as the changeset to remove the working directory (like
    :hg:`clone -U`).
    If you want to revert just one file to an older revision, use
    :hg:`revert [-r REV] NAME`.
    See :hg:`help dates` for a list of formats valid for -d/--date.
    commands.update returns 0 on success, 1 if there are unresolved files.
    Returns :ret_code: True on success, False otherwise.
                :output: if ret_code False
    """
    # TODO: We may have files on disk in the repo directory that aren't being tracked, so they must be removed.
    # The codes used to show the status of files are as follows.
    # M = modified
    # A = added
    # R = removed
    # C = clean
    # ! = deleted, but still tracked
    # ? = not tracked
    # I = ignored
    # It would be nice if we could use mercurial's purge extension to remove untracked files.  The problem is that
    # purging is not supported by the mercurial API.
    ret_code = True
    u.pushbuffer(error=True, subproc=True)

    if commands.update(u, repo) == 1:
        ret_code = False

    output = u.popbuffer()

    return ret_code, output


def getrepohex(reporoot):
    # from mercurial.node import hex  # should I have used this?

    repo = hg.repository(ui.ui(), reporoot)
    revs = repo.revs('tip')
    if len(revs)==1:
      return str(repo.changectx(revs[0]))
    else:
      raise Exception("Internal failure in getrepohex")


def pull_repository(u, repo):
    """Pull changes from a remote repository to a local one.
    This finds all changes from the repository at the specified path
    or URL and adds them to a local repository (the current one unless
    -R is specified). By default, this does not update the copy of the
    project in the working directory.

    When cloning from servers that support it, Mercurial may fetch
    pre-generated data. When this is done, hooks operating on incoming
    changesets and changegroups may fire more than once, once for each
    pre-generated bundle and as well as for any additional remaining
    data. See :hg:`help -e clonebundles` for more.

    Use :hg:`incoming` if you want to see what would have been added
    by a pull at the time you issued this command. If you then decide
    to add those changes to the repository, you should use :hg:`pull
    -r X` where ``X`` is the last changeset listed by :hg:`incoming`.

    If SOURCE is omitted, the 'default' path will be used.
    See :hg:`help urls` for more information.

    Specifying bookmark as ``.`` is equivalent to specifying the active
    bookmark's name.

    commands.pull returns 0 on success, 1 if an update had unresolved files.
    Returns :ret_code: True on success, False otherwise.
            :output: if ret_code False
    """
    ret_code = True
    # def pushbuffer(self, error=False, subproc=False, labeled=False):

    ret_code = True
    u.pushbuffer(error=True, subproc=True)

    if commands.pull(u, repo):
        ret_code = False

    output = u.popbuffer()

    return ret_code, output


def validate_hg_url(url):
    error = "Invalid Hg URL: {}".format(url)
    source, branches = hg.parseurl(url)
    try:
        hg.repository(ui.ui(), source)
    except error.Abort as exc:
        raise Exception('Invalid Hg URL {}, {}'.format(url, exc))

    # myui=ui.ui()
    # myui.setconfig('ui', 'interactive', 'off')
    # repo=hg.repository(myui,'<path-to-hg-repo>')
    # [repo.changelog.rev(h) for h in repo.heads()]


def hg_pull_request(repo_path, user, passwd):
    """This function calls mercurial.commands.pull() and mercurial.commands.update() commands
        only for 'hg' type and use configured username and password"""

    # Authentication credentials:
    #
    # >>> url(b'ssh://joe:xyz@x/repo')
    # scheme: 'ssh', user: 'joe', passwd: 'xyz', host: 'x', path: 'repo' >
    # >>> url(b'ssh://joe@x/repo')
    # scheme: 'ssh', user: 'joe', host: 'x', path: 'repo' >

    ret_flag = False
    failures = []
    if os.path.exists(repo_path):
        try:
            # u = ui.ui()
            u = get_configured_ui()
            repo = get_repo_from_path(u, repo_path)
            if repo:
                ret_str = print_check_status(repo)  # Check that all sources have been committed.
                if ret_str:
                    failures.append('{}'.format(ret_str))
                    _logger.info('{}'.format(ret_str))

                tip = get_tip()  # Get the last changeset

                # if user and passwd:
                #     project_dir = os.path.dirname(os.path.abspath(__file__))
                #     old_env = git_cmd.update_environment(SSH_ASKPASS=os.path.join(project_dir, 'askpass.py'),
                #                                          GIT_USERNAME=user, GIT_PASSWORD=passwd)

                ret_flag, output = pull_repository(u, repo)
                if output:
                    failures.append('{}'.format(output))
                    _logger.info('{}'.format(output))

                ret_flag, output = update_repository(u, repo)
                if output:
                    failures.append('{}'.format(output))
                    _logger.info('{}'.format(output))
            else:
                failures.append("Get hg repository failed: {}".format(repo_path))
                _logger.info("Get hg repository failed: {}".format(repo_path))

        except error.Abort as exp:
            failures.append("Abort: invalid git repository: {}, {} ".format(repo_path, str(exp)))
            _logger.info("Abort: invalid git repository: {}, {} ".format(repo_path, str(exp)))
        # except HGStatusNotEmptyError as exp:
        #     failures.append("{}".format(exp))
        #     _logger.info('{}'.format(exp))
        except Exception as exp:
            _logger.error('Exception {}'.format(str(exp)))
        # except:
        #     import traceback
        #     _logger.error(traceback.format_exc())

    else:
        failures.append('No such path exists, path = {}'.format(repo_path))
        _logger.info('No such path exists, path = {}'.format(repo_path))

    if not ret_flag:
        failures.append('Hg pull request failed. Check logs for details!')
        _logger.info('Hg pull request failed. Check logs for details!')

    return ret_flag, failures

    #_logger.exception(odoo.tools.exception_to_unicode(e))