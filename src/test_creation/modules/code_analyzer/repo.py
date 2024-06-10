import os
import logging
from functools import wraps
from pathlib import Path
from collections import defaultdict
from typing import Optional, Union, Iterable

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
    def __init__(self, path: str, ):
        if not os.path.exists(path):
            raise FileNotFoundError(f"Repository {path} does not exist.")
        elif os.path.isfile(path):
            raise NotADirectoryError("The path provided is not a directory.")
        self.root = Path(path).resolve()
        if not os.path.exists(self.root / ".git"):
            # TODO: to be converted to use logger
            print("Warning: The repository is not a git repository.")
            self.git_context = None
        else:
            self.git_context = GitContext(self.root)

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

    def normalize_dirs(self, dirs: Iterable[Union[str, Path]]) -> list[Path]:
        """Validate and normalize directories in relation to repo's root path.

        This would first convert all relative paths in relation to the repo's
        root path, then to validate if the provided list contains valid
        subdirectories of this repository, meaning that every item:
        1. is a directory.
        2. does exist.
        3. is a subdirectory of the repo's root (relative transversal beyond
            root is not allowed)


        Items with overlapping paths e.g. `./src` and `/src/modules` would be
        reduced to the largest path i.e. `./src` which can encompass all
        overlaps.

        Parameters
        ----------
        dirs : list[Union[str, Path]]
            A list of directories to normalize. Must be inside the repo's root
            directory. An error would be raised if any directory provided does
            not exist, or if it is not a directory, or if it is not under the root
            directory.

        Returns
        -------
        list[Path]
            A list of normalized paths in relation to the root directory.
        """
        # convert all paths in test_dirs to Paths relative to the root
        path_dirs = [(self.root / Path(x)).resolve() for x in dirs]

        for path in path_dirs:
            # ensures all paths exist
            if not path.exists():
                raise FileNotFoundError("One or more directories does not exist.")

            # ensures the paths are in fact directories
            if not path.is_dir():
                raise NotADirectoryError("One or more items provided is not "
                                         "a directory.")

            if not path.is_relative_to(self.root):
                raise ValueError("One or more items exists outside the"
                                 "repository.")

        path_dirs = sorted(path_dirs, key=lambda x: len(str(x)))

        normalized_dirs = []
        while path_dirs:
            popped_item = path_dirs.pop()
            is_relative = False
            for path in path_dirs:
                if popped_item.is_relative_to(path):
                    is_relative = True
                    break
            if not is_relative:
                normalized_dirs.append(popped_item)

        return normalized_dirs

    @requires_git_context
    def get_git_direct_link(self, file: str,
                             lineno: Optional[int] = None) -> str:
        return self.git_context.construct_remote_link_to_file(file,
                                                              line_num=lineno)

    def _get_all_files(self, include_git_dir: bool = False):
        file_paths = []
        results = list(os.walk(self.root))
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
                naive = PythonNaiveCodeAnalyzer()
                for file in files:
                    try:
                        ast.read(file)
                        file_function_lineno_map[lang][file] = ast._get_function_lineno_map()
                    except Exception as e:
                        logger.info("Exception occurred when parsing using ast (Python 2 code?) Using naive parser...")
                        naive.read(file)
                        file_function_lineno_map[lang][file] = naive._get_function_lineno_map()
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

    def list_test_files(self, test_dirs: Optional[
            Iterable[Union[str, Path]]] = None) -> dict[str, list[str]]:
        """List files containing tests in the repository.

        Parameters
        ----------
        test_dirs : Optional[list[Union[str, Path]]]
            Optional argument to limit the directories to be searched. If not
            provided, all directories under this repository will be searched.
        """
        testfiles = defaultdict(list)
        # for now only Python is supported
        files_map = self.lf_map
        if test_dirs:
            test_dirs = self.normalize_dirs(test_dirs)
            files_map = {lang: [file for file in files if
                                any([Path(file).is_relative_to(dir) for dir in
                                     test_dirs])] for lang, files in
                         files_map.items()}

        files = files_map.get("Python", [])
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
