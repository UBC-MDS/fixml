import os
import logging
from collections import defaultdict

from .analyzers.python import PythonNaiveCodeAnalyzer, PythonASTCodeAnalyzer

logger = logging.getLogger("test-creation.repo")


class Repository:
    def __init__(self, path: str):
        self.path = path
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

    def _get_language_file_map(self):
        file_language_map = defaultdict(list)
        files = self._get_all_files()
        for file in files:
            for k, v in self.fileext_language_map.items():
                if file.endswith(k):
                    file_language_map[v].append(file)
        return file_language_map

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

    def list_test_files(self):
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
