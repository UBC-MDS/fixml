import ast
import os
from pathlib import Path
import json

import pytest
from fixml.cli.repository import RepositoryActions
from fixml.modules.workflow.response import EvaluationResponse


@pytest.mark.integration
@pytest.mark.parametrize(
    "fixture_name",
    [
        ("lightfm_repo"),
        ("group8_repo"),
        ("group21_repo")
    ],
)
def test_evaluation_will_output_response_json_and_qmd_report(fixture_name,
                                                             request,
                                                             git_clone_root_dir,
                                                             monkeypatch):
    """Equivalent to `fixml evaluate {repo-name}`."""
    fixture = request.getfixturevalue(fixture_name)

    repo_path = Path(fixture.working_tree_dir)
    working_dir = git_clone_root_dir / f"{fixture_name}_output"
    working_dir.mkdir()
    monkeypatch.chdir(working_dir)

    # checks the new working directory does not have any JSON file
    assert not any(['json' in working_dir.iterdir()])

    RepositoryActions().evaluate(repo_path, export_report_to="report.qmd")

    # check the assumption only one file is dumped
    jsons = list(working_dir.glob('*.json'))
    assert len(jsons) == 1
    response_json = jsons[0]

    # checks it is not empty
    assert os.path.getsize(response_json) != 0

    # checks the file content can be parsed as JSON
    with open(response_json, 'r') as f:
        loaded_response = json.load(f)

    # checks the loaded JSON has same top-level fields as EvaluationResponse's
    assert loaded_response.keys() == EvaluationResponse.model_fields.keys()


@pytest.mark.integration
def test_generation_will_create_python_file(git_clone_root_dir):
    """Equivalent to `fixml generate test.py`."""
    output_path = git_clone_root_dir / 'generate' / 'test.py'
    output_path.parent.mkdir(exist_ok=True)

    RepositoryActions().generate(output_path)
    assert output_path.is_file()

    # checks the python code generated is parse-able
    with open(output_path, 'r') as f:
        ast.parse(f.read())
