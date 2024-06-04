from pathlib import Path

from test_creation.modules.utils import get_extension


def test_extension_from_string_can_be_extracted_correctly():
    correct_path = "checklist/checklist.csv"
    assert get_extension(correct_path) == "csv"


def test_extension_from_path_can_be_extracted_correctly():
    correct_path = Path("checklist/checklist.csv")
    assert get_extension(correct_path) == "csv"


def test_extension_extracted_is_all_lower_cased():
    path = "ALL/CAPITAL/PATH/TEST.ZIP"
    assert get_extension(path) == "zip"


def test_only_last_extension_will_be_extracted():
    path = "test/multi_ext.tar.gz"
    assert get_extension(path) == "gz"


def test_file_with_no_extension_will_produce_empty_string():
    path = "test/README"
    assert get_extension(path) == ""


def test_extracted_extension_does_not_start_with_dot():
    path = "test_test_creation.py"
    assert not get_extension(path).startswith(".")
