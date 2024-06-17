from abc import ABC, abstractmethod
import codecs
import ast
from typing import Union
from pathlib import Path
from functools import wraps
from collections import defaultdict

from chardet import detect


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

    def _determine_encodings(self, file_path: Union[str, Path]) -> str:
        try:
            with open(file_path, 'rb') as f:
                result = detect(f.read())
            encoding = result['encoding']
            if not encoding:
                # chardet failed to detect encoding, returning `utf-8` as
                # fallback
                return 'utf-8'
            # make sure that python can read this codec, if not, a Lookup Error
            # will be raised
            codecs.lookup(encoding)
            return encoding
        except LookupError as e:
            print("failed to extract codec that is readable by Python, "
                  "cowardly returning None...")
            print("error:", e.__class__.__name__, str(e))
            return None


class PythonASTCodeAnalyzer(CodeAnalyzer):
    def __init__(self):
        super().__init__()
        self.content = None
        self._tree = None

    def read(self, file_path: Union[str, Path]):
        # TODO: duplicated code
        try:
            with open(file_path, 'r') as f:
                self.content = f.read()
        except Exception as e:
            print("exception occurred when reading the file. (Wrong encoding?)")
            print("trying to detect encoding and retry reading it...")
            try:
                encoding = self._determine_encodings(file_path)
                with open(file_path, 'r', encoding=encoding) as f:
                    self.content = f.read()
            except Exception as e:
                raise RuntimeError("Failed to read file.")
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
    def contains_test(self) -> bool:
        """Check if the loaded content contains tests.

        This assumes the file would be a Python file, and the tests are
        written using either pytest or unittest module.

        This will check the following conditions:
        1. If unittest or pytest modules is loaded, returns true.
        2. If unittest or pytest modules is *not* loaded, check if there is a
        function name that starts with `test` (case-insensitive). If found,
        further check if the content of this function contain assertions
        i.e. `assert` - returns true if found.
        """
        packages = self.list_imported_packages()
        if 'unittest' in packages or 'pytest' in packages:
            return True
        for node in ast.walk(self._tree):
            if isinstance(node, ast.FunctionDef) and node.name.lower().startswith('test'):
                for child_node in ast.walk(node):
                    if isinstance(child_node, ast.Assert):
                        return True
        return False


class PythonNaiveCodeAnalyzer(CodeAnalyzer):
    def __init__(self):
        super().__init__()
        self.content = None

    def read(self, file_path: Union[str, Path]):
        # TODO: duplicated code
        try:
            with open(file_path, 'r') as f:
                self.content = f.readlines()
        except Exception as e:
            print("exception occurred when reading the file. (Wrong encoding?)")
            print("trying to detect encoding and retry reading it...")
            try:
                encoding = self._determine_encodings(file_path)
                with open(file_path, 'r', encoding=encoding) as f:
                    self.content = f.readlines()
            except Exception as e:
                raise RuntimeError("Failed to read file.")

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
            # check if a function starts with test and contains asserts
            line_stripped = line.lstrip().lower()
            is_function = line_stripped.startswith('def ')
            if is_function:
                is_test_function = line_stripped.startswith('def test')
                continue
            if is_function and is_test_function:
                if line_stripped.startswith('assert'):
                    return True
            else:
                continue
        return False


