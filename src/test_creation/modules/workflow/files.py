from abc import ABC, abstractmethod
from ..code_analyzer.repo import Repository


class RepoFileExtractor(ABC):
    def __init__(self, repo: Repository):
        self._repo = repo

    @abstractmethod
    def extract(self) -> list:
        pass


class PythonTestFileExtractor(RepoFileExtractor):
    def __init__(self, repository: Repository):
        super().__init__(repository)

    def extract(self) -> list:
        return self._repo.list_test_files()['Python']
