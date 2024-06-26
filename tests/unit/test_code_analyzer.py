import pytest
from fixml.modules.code_analyzer.analyzers.python import (
    PythonNaiveCodeAnalyzer, PythonASTCodeAnalyzer)


################################################################################
# Code Analyzers                                                               #
################################################################################
@pytest.mark.parametrize(
    "analyzer_class",
    [PythonNaiveCodeAnalyzer, PythonASTCodeAnalyzer]
)
def test_code_analyzer_can_read_repo(test_git_repo, analyzer_class):
    python_file_path = test_git_repo.workspace / "src/python/main.py"
    analyzer = analyzer_class()
    analyzer.read(python_file_path)
    assert not analyzer.contains_test()
