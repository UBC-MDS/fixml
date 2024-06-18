from pathlib import Path

import pytest
from fixml.modules.checklist import checklist as c


@pytest.fixture()
def test_git_repo(git_repo):
    # The fixture derives from `workspace` in `pytest-shutil`, so they contain
    # a handle to the path `path` object (see https://path.readthedocs.io/)
    path = git_repo.workspace
    txt_file = path / 'hello.txt'
    txt_file.write_text('hello world!')

    py_file = Path(path / 'src/python/main.py')
    py_file.parent.mkdir(parents=True, exist_ok=True)
    py_file.write_text('print("hello world!")')

    # We can run commands relative to the working directory
    git_repo.run('git add .')

    # It's better to use the GitPython api directly - the 'api' attribute is
    # a handle to the repository object.
    git_repo.api.index.commit("Initial commit")

    # The fixture has a URI property you can use in downstream systems
    assert git_repo.uri.startswith('file://')

    return git_repo


@pytest.fixture(scope="module")
def loaded_checklist():
    return c.Checklist()


@pytest.fixture()
def export_html_path(tmp_path):
    return tmp_path / "checklist.html"


@pytest.fixture()
def write_yaml_path(tmp_path):
    return tmp_path / "checklist.yaml"


@pytest.fixture()
def write_csv_path(tmp_path):
    return tmp_path / "checklist.csv/"


@pytest.fixture()
def csv_file_paths(write_csv_path):
    return [write_csv_path / x for x in ["tests.csv", "topics.csv", "overview.csv"]]


