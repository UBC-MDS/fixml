import os
import logging
from functools import wraps
from pathlib import Path
from collections import defaultdict
from typing import Optional

from .analyzers.python import PythonNaiveCodeAnalyzer, PythonASTCodeAnalyzer
from .git import GitContext

logger = logging.getLogger("test-creation.repo")


def requires_git_context(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        """wrapper function to check if we have git context."""
        if self.git_context is None:
            raise RuntimeError("This repository has no git context.")
        return func(self, *args, **kwargs)

    return wrapper


class Repository:
    def __init__(self, path: str):

        if not os.path.exists(path):
            raise FileNotFoundError(f"Repository {path} does not exist.")
        elif os.path.isfile(path):
            raise NotADirectoryError("The path provided is not a directory.")
        self.path = Path(path)
        if not os.path.exists(self.path / ".git"):
            # TODO: to be converted to use logger
            print("Warning: The repository is not a git repository.")
            self.git_context = None
        else:
            self.git_context = GitContext(self.path)

        self.files = []
        self.fileext_language_map = {
            '.js': 'JavaScript',
            '.jsx': 'JavaScript',
            '.ts': 'TypeScript',
            '.java': 'Java',
            '.go': 'Go',
            '.rs': 'Rust',
            '.py': 'Python',
            '.ipynb': 'IPython Notebook',
            '.cpp': 'C++',
            '.c': 'C'
        }
        self.lf_map = self._get_language_file_map()
        self.ffl_map = self._get_file_function_lineno_map()

    @requires_git_context
    def get_git_direct_link(self, file: str,
                             lineno: Optional[int] = None) -> str:
        return self.git_context.construct_remote_link_to_file(file,
                                                              line_num=lineno)

    def _get_all_files(self, include_git_dir: bool = False):
        file_paths = []
        results = list(os.walk(self.path))
        for root, dirs, files in results:
            # Excluding files inside .git
            if '.git' in root and not include_git_dir:
                continue

            for file in files:
                file_paths.append(f'{root}/{file}')
        return file_paths

    def _get_language_file_map(self) -> dict[str, list[str]]:
        language_file_map = defaultdict(list)
        files = self._get_all_files()
        for file in files:
            for k, v in self.fileext_language_map.items():
                if file.endswith(k):
                    language_file_map[v].append(file)
        return language_file_map

    def _get_file_function_lineno_map(self) -> dict[str, dict[str, list[str]]]:
        file_function_lineno_map = defaultdict(lambda: defaultdict(int))
        for lang, files in self.lf_map.items():
            # TODO: only Python is supported now
            if lang == "Python":
                ast = PythonASTCodeAnalyzer()
                for file in files:
                    try:
                        ast.read(file)
                        file_function_lineno_map[lang][file] = ast._get_function_lineno_map()
                    except Exception as e:
                        logger.info("Exception occurred when parsing using ast (Python 2 code?) Using naive parser...")
        return file_function_lineno_map

    def list_languages(self):
        return list(self.lf_map.keys())

    def list_packages(self):
        packages = []
        for lang in self.lf_map.keys():
            if lang == "Python":
                analyzer = PythonNaiveCodeAnalyzer()
                files = self.lf_map[lang]
                for file in files:
                    analyzer.read(file)
                    packages += analyzer.list_imported_packages()
        packages = list(set(packages))
        return packages

    def list_test_files(self) -> dict[str, list[str]]:
        testfiles = defaultdict(list)
        # for now only Python is supported
        files = self.lf_map.get("Python", [])
        ast = PythonASTCodeAnalyzer()
        naive = PythonNaiveCodeAnalyzer()
        for file in files:
            try:
                ast.read(file)
                if ast.contains_test():
                    testfiles["Python"].append(file)
            except Exception as e:
                logger.info("Exception occurred when parsing using ast (Python 2 code?) Using naive parser...")
                naive.read(file)
                if naive.contains_test():
                    testfiles["Python"].append(file)
        return testfiles
