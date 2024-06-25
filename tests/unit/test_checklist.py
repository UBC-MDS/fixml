import os

import pytest
from fixml.modules.checklist import checklist as c


################################################################################
# Checklist loading
################################################################################
def test_loaded_checklist_is_indeed_a_checklist(loaded_checklist):
    assert loaded_checklist is not None and isinstance(loaded_checklist, c.Checklist)


def test_error_when_checklist_file_does_not_exist(loaded_checklist):
    with pytest.raises(FileNotFoundError):
        c.Checklist("checklist/this_checklist_does_not_exist.csv/")


def test_checklist_content_is_a_dictionary(loaded_checklist):
    assert isinstance(loaded_checklist.content, dict)


################################################################################
# Checklist exporting to HTML
################################################################################
def test_checklist_can_be_exported_successfully(loaded_checklist, export_html_path):
    loaded_checklist.export_html(export_html_path)
    assert os.path.exists(export_html_path)


def test_checklist_will_not_overwrite_existing_html_by_default(loaded_checklist, export_html_path):
    loaded_checklist.export_html(export_html_path)
    with pytest.raises(FileExistsError):
        loaded_checklist.export_html(export_html_path)


def test_checklist_will_overwrite_existing_file_without_error_when_arg_is_provided(loaded_checklist, export_html_path):
    loaded_checklist.export_html(export_html_path)
    loaded_checklist.export_html(export_html_path, exist_ok=True)


################################################################################
# Checklist writing to YAML
################################################################################
def test_checklist_will_not_write_yaml_by_default(loaded_checklist, write_yaml_path):
    with pytest.raises(NotImplementedError):
        loaded_checklist.to_yaml(write_yaml_path)


def test_checklist_will_write_yaml_successfully_with_no_preserve_format(loaded_checklist, write_yaml_path):
    loaded_checklist.to_yaml(write_yaml_path, no_preserve_format=True)
    assert os.path.exists(write_yaml_path)


def test_checklist_will_not_overwrite_existing_yaml_by_default(loaded_checklist, write_yaml_path):
    loaded_checklist.to_yaml(write_yaml_path, no_preserve_format=True)
    with pytest.raises(FileExistsError):
        loaded_checklist.to_yaml(write_yaml_path, no_preserve_format=True)


def test_checklist_will_overwrite_when_exist_ok_is_provided(loaded_checklist, write_yaml_path):
    loaded_checklist.to_yaml(write_yaml_path, no_preserve_format=True)
    loaded_checklist.to_yaml(write_yaml_path, no_preserve_format=True, exist_ok=True)
    assert os.path.exists(write_yaml_path)


################################################################################
# Checklist writing to CSV
################################################################################
def test_checklist_will_write_csv_successfully_with_no_preserve_format(loaded_checklist, write_csv_path):
    loaded_checklist.to_csv(write_csv_path)
    assert os.path.exists(write_csv_path)


def test_checklist_will_not_overwrite_existing_csv_by_default(loaded_checklist, write_csv_path):
    loaded_checklist.to_csv(write_csv_path)
    with pytest.raises(FileExistsError):
        loaded_checklist.to_csv(write_csv_path)


def test_checklist_will_overwrite_existing_csv_when_exist_ok_is_provided(loaded_checklist, write_csv_path):
    loaded_checklist.to_csv(write_csv_path)
    loaded_checklist.to_csv(write_csv_path, exist_ok=True)
    assert os.path.exists(write_csv_path)


def test_written_csv_path_contains_expected_files(loaded_checklist, write_csv_path, csv_file_paths):
    loaded_checklist.to_csv(write_csv_path)
    assert os.path.isdir(write_csv_path)
    for path in csv_file_paths:
        assert os.path.exists(path)
