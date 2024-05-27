import json

import fire
from dotenv import load_dotenv
from tqdm import tqdm
from pydantic import BaseModel, Field
from typing import List
from langchain_core.prompts.prompt import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_community.document_loaders import PythonLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter, Language
from langchain_openai import ChatOpenAI
from langchain_core.language_models import LanguageModelLike
from langchain_core.tools import ValidationError
from langchain_core.documents import Document

from modules.checklist.checklist import Checklist, ChecklistFormat
from modules.code_analyzer.repo import Repository
from modules.workflow.files import PythonTestFileExtractor, RepoFileExtractor
from modules.workflow.parse import ResponseParser

load_dotenv()


class TestEvaluator:
    def __init__(self, llm: LanguageModelLike, extractor: RepoFileExtractor, checklist: Checklist, retries: int = 3):
        self.llm = llm
        self.checklist = checklist
        self.file_extractor = extractor

        self.retries = retries

        self.files = self.file_extractor.extract()
        if not self.files:
            print("File loader returned no files!")

        self.test_items = self._load_tests_from_checklist()
        if not self.test_items:
            print("Loaded checklist successfully, but it contains no test items!")

        class TestItemEvaluation(BaseModel):
            ID: str = Field(description="The corresponding `ID` of the checklist item provided")
            Title: str = Field(description="The corresponding `Title` of the checklist item provided")
            Requirement: str = Field(description="The corresponding `Requirement` of the checklist item provided")
            Observation: str = Field(description="Your detailed observation of the code in accordance to the given checklist item")
            Functions: List[str] = Field(description="Test functions that satisfy the given requirement (if any)")
            Evaluation: str = Field(description="The summarized evaluation. Must be one of Satisfied/Partially Satisfied/Not Satisfied.")
            Score: int = Field(description="The score obtained from the given evaluation (1 for Satisfied / 0.5 for Partially Satisfied / 0 for Not Satisfied)")

        class EvalResult(BaseModel):
            results: List[TestItemEvaluation]

        self.parser = JsonOutputParser(pydantic_object=EvalResult)

        self.prompt = PromptTemplate(
            template="You are an expert Machine Learning Engineer.\n"
                     "Please help to evaluate the following code using the given checklist.\n"
                     "{format_instructions}\n"
                     "For a test item to be considered as `Satisfied` or `Partially Satisfied`, "
                     "the corresponding function(s) satisfying the item's requirement must be "
                     "provided in the `Functions` attribute.\n"
                     "Here is the checklist as a list of JSON objects:\n```{checklist}```\n"
                     "Here is the code to be analyzed:\n{context}",
            description="Code Review for Machine Learning Project",
            input_variables=["checklist", "context"],
            partial_variables={"format_instructions": self.parser.get_format_instructions()},
        )

        self.chain = self.prompt | self.llm | self.parser

    @staticmethod
    def _load_test_file_into_splits(file_path: str) -> List[Document]:
        loader = PythonLoader(file_path)
        py = loader.load()
        py_splits = RecursiveCharacterTextSplitter.from_language(language=Language.PYTHON, chunk_size=1000,
                                                                 chunk_overlap=0).split_documents(py)
        return py_splits

    def _load_tests_from_checklist(self) -> List[dict]:
        return self.checklist.get_all_tests(['ID', 'Title', 'Requirement'])

    def _validate_response(self, raw_response: dict) -> None:
        """Validation logics that are not covered by pydantic or langchain."""
        # ensures the number of items in the response is the same as provided checklists
        if len(raw_response['results']) != len(self.test_items):
            raise ValidationError("Number of items returned from LLM does not match that in checklist.")


    def evaluate(self, verbose: bool = False) -> List[dict]:
        result = []
        for fp in tqdm(self.files):
            if verbose:
                print(fp)
            splits = self._load_test_file_into_splits(fp)
            if verbose:
                print(f"# splits: {len(self.files)}")

            response = None
            retry_count = 0
            while not response and retry_count < self.retries:
                try:
                    response = self.chain.invoke({
                        "context": splits,
                        "checklist": json.dumps(self.test_items)
                    })
                    self._validate_response(response)
                except ValidationError as e:
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
        llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
        checklist = Checklist(checklist_path, checklist_format=ChecklistFormat.CSV)
        extractor = PythonTestFileExtractor(Repository(repo_path))

        evaluator = TestEvaluator(llm, extractor, checklist)
        response = evaluator.evaluate()

        parser = ResponseParser(response)
        parser.get_completeness_score()

    fire.Fire(main)
