import json
from abc import ABC, abstractmethod
from datetime import datetime

from tqdm import tqdm
from typing import List
from langchain_community.document_loaders import PythonLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter, Language
from langchain_core.language_models import LanguageModelLike
from langchain_core.documents import Document

from ..checklist.checklist import Checklist
from ..code_analyzer.repo import Repository
from .prompt_format import PromptFormat
from .response import EvaluationResponse, CallResult


class PipelineRunner(ABC):
    """Abstract base class for running langchain pipelines.

    This class object assembles prompt and to obtain response from LLMs.
    """
    @abstractmethod
    def run(self):
        pass


class TestEvaluator(PipelineRunner, ABC):
    """Abstract base class for test evaluators
    i.e. class object to run evaluation of test files from a given repository.
    """

    def __init__(self, llm: LanguageModelLike, prompt_format: PromptFormat,
                 repository: Repository, checklist: Checklist):
        self.llm = llm

        self.checklist = checklist
        self.repository = repository
        self.prompt_format = prompt_format
        self._test_items = None

        self.chain = self.prompt_format.prompt | self.llm | self.prompt_format.parser


class PerFileTestEvaluator(TestEvaluator):
    """Concrete test evaluator that performs per-file evaluation."""

    def __init__(self, llm: LanguageModelLike, prompt_format: PromptFormat,
                 repository: Repository, checklist: Checklist, retries: int = 3):
        super().__init__(llm, prompt_format, repository, checklist)
        self.retries = retries

        self._files = self.repository.list_test_files()['Python']
        if not self._files:
            print("File loader returned no files!")

        self._test_items = self.checklist.get_all_tests(['ID', 'Title',
                                                         'Requirement'])
        if not self._test_items:
            print("Loaded checklist successfully, but it contains no test items!")

    @staticmethod
    def _load_test_file_into_splits(file_path: str) -> List[Document]:
        loader = PythonLoader(file_path)
        py = loader.load()
        py_splits = RecursiveCharacterTextSplitter.from_language(language=Language.PYTHON, chunk_size=1000,
                                                                 chunk_overlap=0).split_documents(py)
        return py_splits

    def _validate_response(self, raw_response: dict) -> None:
        """Validation logics that are not covered by pydantic or langchain."""
        # ensures the number of items in the response is the same as provided
        # checklists
        if len(raw_response['results']) != len(self._test_items):
            raise AssertionError("Number of items returned from LLM does not match that in checklist.")
        if not all(['Functions' in item for item in raw_response['results']]):
            raise AssertionError("Not all items returned contain the attribute `Functions`.")

    def run(self, verbose: bool = False) -> EvaluationResponse:
        eval_response = EvaluationResponse(
            model={'name': self.llm.model_name, 'temperature': self.llm.temperature},
            repository={'path': self.repository.path, 'object': self.repository},
            checklist={'path': self.checklist.path, 'object': self.checklist}
        )

        for fp in tqdm(self._files):
            if verbose:
                print(fp)
            splits = self._load_test_file_into_splits(fp)
            if verbose:
                print(f"# splits: {len(self._files)}")

            response = None
            retry_count = 0
            errors = []
            start_time = datetime.now()

            context = {"codebase": splits, "checklist": json.dumps(self._test_items)}

            while not response and retry_count < self.retries:
                try:
                    response = self.chain.invoke(context)

                    # inconsistent behaviour across langchains' parsers!
                    # some will return dictionary while some will return pydantic model.
                    # for now, we coerce all responses to dictionary, but later on it might be preferable to coerce all
                    # into pydantic model for easier validation instead.
                    if not isinstance(response, dict):
                        response = response.dict()

                    self._validate_response(response)

                except Exception as e:
                    if verbose:
                        print(f"error occurred: {e.__class__.__name__} - {str(e)}")
                    errors.append({'name': e.__class__.__name__, 'description': str(e)})
                    retry_count += 1
                    response = None
                    continue

            if not response:
                print(f"Unable to obtain valid response from LLM within {self.retries} attempts")
                print("continuing...")

            end_time = datetime.now()

            call_result = CallResult(
                start_time=start_time,
                end_time=end_time,
                files_evaluated=[fp],
                context={k: str(v) for k, v in context.items()},
                prompt=self.prompt_format.prompt.format(**context),
                success=bool(response),
                parsed_response=response,
                errors=errors
            )

            eval_response.call_results.append(call_result)

        return eval_response
