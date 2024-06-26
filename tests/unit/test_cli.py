from types import NoneType

import pytest
from fixml.cli.repository import RepositoryActions
from fixml.cli.utils import parse_list


def test_cli_should_stop_if_file_exists_but_no_overwrite_flag_is_given(tmp_path, test_git_repo):
    report_path = tmp_path / 'report.html'
    report_path.touch()
    with pytest.raises(FileExistsError):
        RepositoryActions().evaluate(
            test_git_repo.workspace,
            export_report_to=str(report_path)
        )


@pytest.mark.parametrize(
    "raw_input, expected_type",
    [
        (None, NoneType),
        (['a', 'b', 3124], type(tuple)),
        (1234.05, type(tuple)),
        ('test', type(tuple))
    ]
)
def test_parse_list_should_be_returning_tuples(raw_input, expected_type):
    result = parse_list(raw_input)
    assert (result, expected_type)
