# -*- encoding: utf-8 -*-


class RepoBase:

    def __init__(self, repo_path, user, passwd):
        self._repo_path = repo_path
        self._user = user
        self._passwd = passwd
        self._output_list = []
    # end init

    def pull(self):
        assert False
    # end pull
# end RepoBase
