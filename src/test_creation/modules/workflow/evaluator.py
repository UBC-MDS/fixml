import json
from abc import ABC, abstractmethod

from dotenv import load_dotenv
from tqdm import tqdm
from typing import List
from pydantic_core._pydantic_core import ValidationError as PydanticValidationError
from langchain_core.tools import ValidationError as LangchainValidationError
from langchain_core.exceptions import OutputParserException
from langchain_community.document_loaders import PythonLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter, Language
from langchain_core.language_models import LanguageModelLike
from langchain_core.documents import Document

from ..checklist.checklist import Checklist
from ..code_analyzer.repo import Repository
from .prompt_format import PromptFormat
from .response import Response

load_dotenv()


class Evaluator(ABC):
    """Abstract base class for evaluators i.e. class object to assemble prompt and to obtain response from LLMs."""
    @abstractmethod
    def evaluate(self) -> Response:
        pass


class TestEvaluator(Evaluator, ABC):
    """Abstract base class for test evaluators
    i.e. class object to run evaluation of test files from a given repository.
    """
    def __init__(self, llm: LanguageModelLike, prompt_format: PromptFormat, repository: Repository,
                 checklist: Checklist):
        self.llm = llm
        self.checklist = checklist
        self.repository = repository
        self.prompt_format = prompt_format
        self.test_items = None

        self.chain = self.prompt_format.prompt | self.llm | self.prompt_format.parser


class PerFileTestEvaluator(TestEvaluator):
    """Concrete test evaluator that performs per-file evaluation."""
    def __init__(self, llm: LanguageModelLike, prompt_format: PromptFormat, repository: Repository,
                 checklist: Checklist, retries: int = 3):
        super().__init__(llm, prompt_format, repository, checklist)
        self.retries = retries

        self._files = self.repository.list_test_files()['Python']
        if not self._files:
            print("File loader returned no files!")

        self._test_items = self.checklist.get_all_tests(['ID', 'Title', 'Requirement'])
        if not self._test_items:
            print("Loaded checklist successfully, but it contains no test items!")

    @staticmethod
    def _load_test_file_into_splits(file_path: str) -> List[Document]:
        loader = PythonLoader(file_path)
        py = loader.load()
        py_splits = RecursiveCharacterTextSplitter.from_language(language=Language.PYTHON, chunk_size=1000,
                                                                 chunk_overlap=0).split_documents(py)
        return py_splits

    def evaluate(self, verbose: bool = False) -> Response:
        response = Response()
        result = []
        for fp in tqdm(self._files):
            if verbose:
                print(fp)
            splits = self._load_test_file_into_splits(fp)
            if verbose:
                print(f"# splits: {len(self._files)}")
            # FIXME: it sometimes tests only part of the checklist items

            response = None
            retry_count = 0
            while not response and retry_count < self.retries:
                try:
                    response = self.chain.invoke({"codebase": splits, "checklist": json.dumps(self._test_items)})

                    # TODO: to be moved in PR for #103
                    # inconsistent behaviour across langchains' parsers!
                    # some will return dictionary while some will return pydantic model
                    if not isinstance(response, dict):
                        print(response.results)
                        response = response.dict()
                        print(response)

                except (PydanticValidationError, LangchainValidationError, OutputParserException) as e:
                    retry_count += 1
                    continue

            if not response:
                raise RuntimeError(f"Unable to obtain valid response from LLM within {self.retries} attempts")

            report = response['results']
            for item in report:
                item['file'] = fp
            result += [{
                'file': fp,
                'report': report,
            }]
        return response
