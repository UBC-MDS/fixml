from contextlib import nullcontext as does_not_raise

import pytest
from fixml.modules.code_analyzer import repo as r
from fixml.modules.code_analyzer.git import GitContext


################################################################################
# Repository                                                                   #
################################################################################
def test_repository_should_be_able_to_read_git_repo(test_git_repo):
    path = test_git_repo.workspace
    repo = r.Repository(path)
    assert any(['src/python/main.py' in file for file in repo._get_all_files()])


@pytest.mark.parametrize(
    "dirs_input, expected_result, expectation",
    [
        (["src", "./src/python"], ["src"], does_not_raise()),
        (["~/.vimrc"], [], pytest.raises(FileNotFoundError)),
        (["./src/python/main.py"], [], pytest.raises(NotADirectoryError)),
        (["..", "../.."], [], pytest.raises(ValueError)),
        (["/non/existent/path"], [], pytest.raises(FileNotFoundError)),
    ],
)
def test_repository_normalize_dirs_works_as_expected(test_git_repo, dirs_input,
                                                     expected_result,
                                                     expectation):
    path = test_git_repo.workspace
    repo = r.Repository(path)
    with expectation:
        assert repo.normalize_dirs(dirs_input) == [repo.root / dir for dir in expected_result]


################################################################################
# GitContext                                                                   #
################################################################################
@pytest.mark.parametrize(
    "fixture_name, remote_name, remote_url, expected",
    [
        (
                "test_git_repo",
                "origin",
                "git@github.internal.com:UBC-MDS/testing-repo_1234.git",
                ("github.internal.com", "UBC-MDS", "testing-repo_1234")
        ),
        (
                "test_git_repo",
                "export",
                "ssh://git@github.internal.com:UBC-MDS/testing-repo_1234.git",
                ("github.internal.com", "UBC-MDS", "testing-repo_1234")
        ),
        (
                "test_git_repo",
                "internal",
                "https://github.com:8080/UBC-MDS/fixml.git",
                ("github.com:8080", "UBC-MDS", "fixml")
        ),
        (
                "test_git_repo",
                "origin",
                "http://gitlab.example.com:8080/UBC-MDS/fixml.git",
                ("gitlab.example.com:8080", "UBC-MDS", "fixml")
        ),
        (
                "test_git_repo",
                "a",
                "ftp://github.com/SoloSynth1/Solosynth1",
                ("github.com", "SoloSynth1", "Solosynth1")
        ),
    ]
)
def test_git_context_can_extract_remote_git_urls(fixture_name, remote_name,
                                                 remote_url, expected, request):
    repo = request.getfixturevalue(fixture_name)
    repo.api.create_remote(remote_name, remote_url)
    gc = GitContext(repo.workspace)
    assert (gc.host, gc.org, gc.repo_name) == expected


def test_git_context_gives_out_local_link_when_no_remote(test_git_repo):
    context = GitContext(test_git_repo.workspace)
    link = context.construct_remote_link_to_file("src/python/main.py")
    assert link == f"file://{test_git_repo.workspace}/src/python/main.py"
