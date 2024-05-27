import json
from abc import ABC, abstractmethod

import fire
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

from modules.checklist.checklist import Checklist, ChecklistFormat
from modules.code_analyzer.repo import Repository
from modules.workflow.parse import ResponseParser
from modules.workflow.prompt_format import PromptFormat

load_dotenv()


class TestEvaluator(ABC):
    def __init__(self, llm: LanguageModelLike, prompt_format: PromptFormat, repository: Repository,
                 checklist: Checklist):
        self.llm = llm
        self.checklist = checklist
        self.repository = repository
        self.prompt_format = prompt_format

        self.chain = self.prompt_format.prompt | self.llm | self.prompt_format.parser

    @abstractmethod
    def evaluate(self):
        pass


class PerFileTestEvaluator(TestEvaluator):
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

    def evaluate(self, verbose: bool = False) -> List[dict]:
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
        return result


if __name__ == '__main__':
    def main(checklist_path, repo_path):
        import langchain
        langchain.debug = True
        from langchain_openai import ChatOpenAI

        from modules.workflow.prompt_format import EvaluationPromptFormat

        llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
        checklist = Checklist(checklist_path, checklist_format=ChecklistFormat.CSV)
        repo = Repository(repo_path)

        prompt_format = EvaluationPromptFormat()
        evaluator = PerFileTestEvaluator(llm, prompt_format=prompt_format, repository=repo, checklist=checklist)
        response = evaluator.evaluate()

        parser = ResponseParser(response)
        parser.get_completeness_score()

    fire.Fire(main)
