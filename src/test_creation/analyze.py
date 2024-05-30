import fire

from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

from modules.workflow.prompt_format import EvaluationPromptFormat
from modules.workflow.evaluator import PerFileTestEvaluator
from modules.checklist.checklist import Checklist, ChecklistFormat
from modules.code_analyzer.repo import Repository
from modules.workflow.parse import ResponseParser

load_dotenv()


<<<<<<< HEAD
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

    def _load_tests_from_checklist(self) -> str:
        checklist = self.checklist.get_all_tests(['ID', 'Title', 'Requirement'])
        return json.dumps(checklist)

    def evaluate(self, verbose: bool = False) -> List[dict]:
        result = []
        for fp in tqdm(self.files):
            if verbose:
                print(fp)
            splits = self._load_test_file_into_splits(fp)
            if verbose:
                print(f"# splits: {len(self.files)}")
            # FIXME: it sometimes tests only part of the checklist items

            response = None
            retry_count = 0
            while not response and retry_count < self.retries:
                try:
                    response = self.chain.invoke({"context": splits, "checklist": self.test_items})
                except ValidationError as e:
                    retry_count += 1
                    continue

            if not response:
                raise RuntimeError(f"Unable to obtain valid response from LLM within {self.retries} attempts")

            report = response['results']
            repo = self.file_extractor._repo
            for item in report:
                item['file'] = fp
                item['lineno'] = [repo.ffl_map[fp][func] for func in item['Functions']]
                item['lineno_href'] = [
                    f"[{lineno}]({repo._get_git_direct_link(repo._get_relative_path(fp), lineno)})"
                    for lineno in item['lineno']
                ]
            result += [{
                'file': fp,
                'report': report,
            }]
        return result


=======
>>>>>>> main
if __name__ == '__main__':
    def main(checklist_path, repo_path, report_output_path, report_output_format='html'):
        """
        Example:
        ----------
        >>> python src/test_creation/analyze.py --checklist_path='./checklist/checklist_demo.csv' --repo_path='../lightfm/' --report_output_path='./report/evaluation_report.html' --report_output_format='html'
        """
        llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
        checklist = Checklist(checklist_path, checklist_format=ChecklistFormat.CSV)
        repo = Repository(repo_path)
        prompt_format = EvaluationPromptFormat()

        evaluator = PerFileTestEvaluator(llm, prompt_format=prompt_format, repository=repo, checklist=checklist)
        response = evaluator.evaluate()

        parser = ResponseParser(response)
        parser.get_completeness_score(verbose=True)

        parser.export_evaluation_report(report_output_path, report_output_format, exist_ok=True)

    fire.Fire(main)
