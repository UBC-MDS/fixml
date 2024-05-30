import os
import re
import logging
from collections import defaultdict
from configparser import ConfigParser
from typing import Dict, List

from .analyzers.python import PythonNaiveCodeAnalyzer, PythonASTCodeAnalyzer

logger = logging.getLogger("test-creation.repo")


class Repository:
    def __init__(self, path: str):
        self.path = path

        # git metadata
        self.url = ''
        self.mode = ''
        self.service = ''
        self.user = ''
        self.name = ''
        self.main_branch = ''
        
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
        try:
            self._get_git_metadata()
        except Exception as e:
            logger.info(e)

    def _get_git_metadata(self):
        config = ConfigParser()
        if os.path.exists(self.path + '/.git/config'):
            config.read(self.path + '/.git/config')
        else:
            raise FileNotFoundError('/.git/config does not exist')

        self.url = config['remote "origin"']['url']
        
        if 'git@' in self.url:
            self.mode = 'ssh'
            pattern = 'git@(.*?):(.*?)/(.*?).git'
        elif 'https' in self.url:
            self.mode = 'https'
            pattern = 'https://(.*?)/(.*?)/(.*?).git'
            
        self.service, self.user, self.name = re.search(pattern, self.url).group(1,2,3)

        if 'branch "master"' in list(config):
            self.main_branch = 'master'
        elif 'branch "main"' in list(config):
            self.main_branch = 'main'

        return {
            'mode': self.mode,
            'service': self.service,
            'user': self.user,
            'name': self.name,
            'main_branch': self.main_branch
        }

    def _get_git_direct_link(self, file: str, lineno: int = None):
        link = f'https://{self.service}/{self.user}/{self.name}/blob/{self.main_branch}/{file}'
        if lineno:
            link += f'#L{lineno}'
        return link

    def _get_relative_path(self, file: str):
        path = file.replace(self.path, '', 1)
        if path[0] == '/':
            return path
        else:
            return '/' + path
    
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
        return file_language_map # FIXME: why is it called file_language_map instead of language_file_map?

    def _get_file_function_lineno_map(self):
        file_function_lineno_map = defaultdict(lambda: defaultdict(int))
        files = self.lf_map.get("Python", [])
        ast = PythonASTCodeAnalyzer() # FIXME: only support Python ATS, what's the implication?
        for file in files:
            try:
                ast.read(file)
                file_function_lineno_map[file] = ast._get_function_lineno_map()
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

    def list_test_files(self) -> Dict[str, List[str]]:
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

