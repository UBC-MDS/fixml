import json

from typing import List
from langchain_core.language_models import LanguageModelLike

from .base import PromptInjectionRunner
from ..prompt_format import PromptFormat
from ...checklist.checklist import Checklist
from ...code_analyzer.repo import Repository


# NOTE: only support Python
class NaiveTestGenerator(PromptInjectionRunner):
    """Generate test specs using checklist items only.

    This runner will not refer to files in the repository - hence the name
    "naive".
    """
    def __init__(self, llm: LanguageModelLike, prompt_format: PromptFormat,
                 repository: Repository = None, checklist: Checklist = None,
                 retries: int = 3):
        super().__init__(llm, prompt_format, repository, checklist)
        self.retries = retries

        self.result = []

        self._test_items = self.checklist.get_all_tests(['ID', 'Title',
                                                         'Requirement'])
        if not self._test_items:
            print("Loaded checklist successfully, but it contains no test items!")

    def _validate_response(self, raw_response: dict) -> None:
        """Validation logics that are not covered by pydantic or langchain."""
        # ensures the number of items in the response is the same as provided
        # checklists
        if len(raw_response['results']) != len(self._test_items):
            raise AssertionError("Number of items returned from LLM does not match that in checklist.")
        if not all(['Function' in item for item in raw_response['results']]):
            raise AssertionError("Not all items returned contain the attribute `Functions`.")

    def run(self, verbose: bool = False) -> List[dict]:
        response = None
        retry_count = 0
        context= {"checklist": json.dumps(self._test_items)}
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
                retry_count += 1
                response = None
                continue

        if not response:
            raise RuntimeError(f"Unable to obtain valid response from LLM within {self.retries} attempts")

        result = response['results']
        self.result = result

        return result

    def export_py(self, output_path: str, exist_ok: bool = False):
        # TODO
        raise NotImplementedError()
