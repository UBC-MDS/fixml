from pathlib import Path

import pytest
from test_creation.modules.utils import get_extension


@pytest.mark.parametrize(
    "path, expected",
    [
        ("checklist/checklist.csv", "csv"),
        (Path("checklist/checklist.csv"), "csv"),
        ("ALL/CAPITAL/PATH/TEST.ZIP", "zip"),
        ("test/multi_ext.tar.gz", "gz"),
        (Path("test/README"), ""),
        ("checklist/checklist.csv/dummy/..", "csv")
    ]
)
def test_extension_from_string_can_be_extracted_correctly(path, expected):
    assert get_extension(path) == expected


def test_extracted_extension_does_not_start_with_dot():
    path = "test_test_creation.py"
    assert not get_extension(path).startswith(".")
