import pytest

from test_creation.cli.repository import RepositoryActions


def test_cli_should_stop_if_file_exists_but_no_overwrite_flag_is_given(tmp_path, test_git_repo):
    report_path = tmp_path / 'report.html'
    report_path.touch()
    with pytest.raises(FileExistsError):
        RepositoryActions().evaluate(
            test_git_repo.workspace,
            export_report_to=str(report_path)
        )