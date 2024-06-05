from abc import ABC, abstractmethod
import ast
from typing import Union
from pathlib import Path
from functools import wraps
from collections import defaultdict


def assert_have_read_content(f):
    @wraps(f)
    def decorator(self, *args, **kwargs):
        if self.content is None:
            raise RuntimeError("No content has been read yet.")
        return f(self, *args, **kwargs)

    return decorator


class CodeAnalyzer(ABC):

    @abstractmethod
    def read(self, file_path: Union[str, Path]) -> None:
        pass

    @abstractmethod
    def list_imported_packages(self):
        pass

    @abstractmethod
    def list_all_functions(self):
        pass

    @abstractmethod
    def contains_test(self):
        pass


class PythonASTCodeAnalyzer(CodeAnalyzer):
    def __init__(self):
        super().__init__()
        self.content = None
        self._tree = None

    def read(self, file_path: str):
        with open(file_path, 'r') as f:
            self.content = f.read()
            self._tree = ast.parse(self.content)

    @assert_have_read_content
    def _get_function_lineno_map(self):
        function_lineno_map = defaultdict(int)
        for node in ast.walk(self._tree):
            if isinstance(node, ast.FunctionDef):
                function_lineno_map[node.name] = node.lineno
        return function_lineno_map

    @assert_have_read_content
    def list_imported_packages(self):
        packages = set()
        for node in ast.walk(self._tree):
            if isinstance(node, ast.Import):
                packages.update(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom):
                packages.add(node.module)
        return packages

    @assert_have_read_content
    def list_all_functions(self):
        return self._get_function_lineno_map().keys()

    @assert_have_read_content
    def contains_test(self):
        packages = self.list_imported_packages()
        if 'unittest' in packages or 'pytest' in packages:
            return True
        for node in ast.walk(self._tree):
            if isinstance(node, ast.FunctionDef) and node.name.startswith('test_'):
                return True
            elif isinstance(node, ast.ClassDef) and ("TestCase" in node.bases or node.name.startswith('Test')):
                return True
        return False


class PythonNaiveCodeAnalyzer(CodeAnalyzer):
    def __init__(self):
        super().__init__()
        self.content = None

    def read(self, file_path: str):
        with open(file_path, 'r') as f:
            self.content = f.readlines()

    @assert_have_read_content
    def _get_function_lineno_map(self):
        function_lineno_map = defaultdict(int)
        for line_num, line in enumerate(self.content):
            if line.lstrip().startswith('def '):
                func_name = line.lstrip().split('(')[0].split(' ')[1]
                function_lineno_map[func_name] = line_num + 1 # line starts with 1
        return function_lineno_map

    @assert_have_read_content
    def list_imported_packages(self):
        packages = set()
        for line in self.content:
            if line.startswith('from ') or line.startswith('import '):
                packages.add(line.split()[1].split(".")[0])
            else:
                continue
        return list(packages)

    @assert_have_read_content
    def list_all_functions(self):
        raise NotImplementedError()

    @assert_have_read_content
    def contains_test(self):
        packages = self.list_imported_packages()
        if 'unittest' in packages or 'pytest' in packages:
            return True
        for line in self.content:
            # pytest
            if "def test_" in line or "TestCase" in line:
                return True
        return False


