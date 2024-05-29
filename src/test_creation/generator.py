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


class TestGenerator:
    def __init__(self, llm: LanguageModelLike, extractor: RepoFileExtractor = None, checklist: Checklist = None, retries: int = 3):
        self.llm = llm
        self.checklist = checklist
        self.file_extractor = extractor

        self.retries = retries

        # self.files = self.file_extractor.extract()
        # if not self.files:
        #     print("File loader returned no files!")

        self.test_items = self._load_tests_from_checklist()
        if not self.test_items:
            print("Loaded checklist successfully, but it contains no test items!")

        class TestSpecGeneration(BaseModel):
            ID: str = Field(description="The corresponding `ID` of the checklist item provided")
            Title: str = Field(description="The corresponding `Title` of the checklist item provided")
            Function: str = Field(description="A test function with the docstring of numpy format") # FIXME: define python function format

        class SpecGenResult(BaseModel):
            results: List[TestSpecGeneration]

        self.parser = JsonOutputParser(pydantic_object=SpecGenResult)
        
        self.prompt = PromptTemplate(
            template="You are an expert Machine Learning Engineer.\n"
                     "Please generate Python test functions based on corresponding requirement of given checklist, with docstring of numpy format.\n"
                     "{format_instructions}\n" 
                     "Here is the checklist as a list of JSON objects:\n```{checklist}```\n",
                     #"Here is the code to be analyzed:\n{context}",
            description="Test Generation for Machine Learning Project",
            #input_variables=["checklist", "context"],
            input_variables=["checklist"],
            partial_variables={"format_instructions": self.parser.get_format_instructions()},
        )

        self.chain = self.prompt | self.llm | self.parser

        self.spec = []

    @staticmethod
    def _load_test_file_into_splits(file_path: str) -> List[Document]:
        # FIXME: to examine whether this is still needed
        loader = PythonLoader(file_path)
        py = loader.load()
        py_splits = RecursiveCharacterTextSplitter.from_language(language=Language.PYTHON, chunk_size=1000,
                                                                 chunk_overlap=0).split_documents(py)
        return py_splits

    def _load_tests_from_checklist(self) -> str:
        checklist = self.checklist.get_all_tests(['ID', 'Title', 'Requirement'])
        return json.dumps(checklist)

    def generate_spec(self) -> List[dict]:
        response = None
        retry_count = 0
        while not response and retry_count < self.retries:
            try:
                response = self.chain.invoke({"checklist": self.test_items})
            except ValidationError as e:
                retry_count += 1
                continue

        if not response:
            raise RuntimeError(f"Unable to obtain valid response from LLM within {self.retries} attempts")

        result = response['results']
        self.spec = result
            
        return result

    def fill_functions_body(self) -> List[dict]:
        prompt = PromptTemplate(
            template="You are an expert Machine Learning Engineer.\n"
                     "Please fill the Python test functions' body with docstring of numpy format.\n"
                     "{format_instructions}\n" 
                     "Here is a list of JSON objects, in which the 'Function's are the functions to be filled:\n```{functions}```\n",
                     #"Here is the code to be analyzed:\n{context}",
            description="Filling Test Functions for Machine Learning Project",
            #input_variables=["checklist", "context"],
            input_variables=["functions"],
            partial_variables={"format_instructions": self.parser.get_format_instructions()},
        )

        chain = prompt | self.llm | self.parser

        response = chain.invoke({"functions": json.dumps(self.spec)})
        #result = response['results']

        return response


if __name__ == '__main__':
    # FIXME: to be updated
    def main(checklist_path, repo_path, report_output_path, report_output_format='html'):
        """
        Example:
        ----------
        >>> python src/test_creation/analyze.py --checklist_path='./checklist/checklist_demo.csv' --repo_path='../lightfm/' --report_output_path='./report/evaluation_report.html' --report_output_format='html'
        """
        llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
        checklist = Checklist(checklist_path, checklist_format=ChecklistFormat.CSV)
        extractor = PythonTestFileExtractor(Repository(repo_path))

        evaluator = TestEvaluator(llm, extractor, checklist)
        response = evaluator.evaluate()

        parser = ResponseParser(response)
        parser.get_completeness_score(verbose=True)
        parser.export_evaluation_report(report_output_path, report_output_format, exist_ok=True)

    fire.Fire(main)
