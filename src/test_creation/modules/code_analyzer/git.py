import re
from typing import Union, Optional
from pathlib import Path
from copy import copy

from git import Repo


class GitContext:
    def __init__(self, git_dir: Union[str, Path]):
        self.git_dir = Path(git_dir)
        self.git_repo = Repo(self.git_dir)

        self.head_commit_hash = self.git_repo.head.commit.hexsha
        self.branch = self._get_current_head()
        self.host, self.org, self.repo_name = self._get_remote_info()

        self.remote_link_format_map = {
            "github": "{host}/{org}/{repo}/blob/{branch}/{path}#L{line_num}",
            "gitlab": "{host}/{org}/{repo}/blob/{branch}/{path}#L{line_num}",
            "bitbucket": "{host}/{org}/{repo}/src/{branch}/{path}#lines-{"
                         "line_num}",
            "gitee": "{host}/{org}/{repo}/blob/{branch}{path}#L{line_num}"
        }
        self.remote_protocol = "https"
        self.remote_service_family = self.__get_remote_service_family()

    def __get_remote_service_family(self) -> str:
        """Determine the remote service family.

        This will do a keyword-based matching between the remote URL and the
        dictionary containing URL rules for different supported git hosting
        service families. For example, remotes pointing to "github.com",
        "github.example.com" will return "github", while "gitlab.example.com"
        will produce "gitlab".

        Returns
        -------
        str
            The key links to git hosting service family.
        """
        result = None
        if self.host:
            hits = [key for key in self.remote_link_format_map.keys() if
                    key in self.host]
            if hits:
                result = hits[0]
        return result

    def _get_current_head(self) -> str:
        """Getting the representation of current HEAD.

        This is to obtain branch name/commit hash for later use when
        constructing a URL to the git hosting service.

        Returns
        -------
        str
            The representation of current HEAD. This could be either the branch
            name or the commit hash.
        """
        if self.git_repo.head.is_detached:
            return self.head_commit_hash
        else:
            return self.git_repo.active_branch.name

    def _get_remote_info(self) -> tuple[Optional[str], Optional[str], str]:
        if self.git_repo.remotes:
            if 'origin' in [r.name for r in self.git_repo.remotes]:
                remote = self.git_repo.remote()
            else:
                remote = self.git_repo.remotes[0]
            remote_url = remote.url
            # git urls:
            # https://git-scm.com/docs/git-clone#URLS
            pattern = r"(?:\w+:\/\/)?(?:\w+@)?(.+)[\/:](.+)\/([^\.]+)(?:\.git)?"
            host, org, repo_name = re.search(pattern, remote_url).groups()
            return host, org, repo_name
        else:
            print("This git repository has no remote")
            return None, None, "."

    def construct_remote_link_to_file(self, file_path: Union[str, Path],
                                      line_num: Optional[int] = None) -> str:
        path = Path(file_path)
        if path.is_absolute():
            rel_path = path.relative_to(self.git_dir)
        else:
            rel_path = path
        if self.remote_service_family:
            f_str = copy(self.remote_link_format_map[self.remote_service_family])
            if line_num is None:
                f_str = f_str.split("#")[0]
            injected_str = f"{self.remote_protocol}://" + \
                f_str.format(host=self.host, org=self.org, repo=self.repo_name,
                             branch=self.branch, path=rel_path,
                             line_num=line_num)
            return injected_str
        else:
            print("No matching service. Using local link instead...")
            return f"file://{str(self.git_dir)}/{rel_path}"
