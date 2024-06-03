import pickle

from langchain_openai import ChatOpenAI

from ..modules.workflow.prompt_format import EvaluationPromptFormat
from ..modules.workflow.evaluator import PerFileTestEvaluator
from ..modules.code_analyzer.repo import Repository
from ..modules.workflow.parse import ResponseParser
from ..modules.checklist.checklist import Checklist


class RepositoryActions(object):
    def generate(self, repo_path: str,
                 checklist_path: str = "./checklist/checklist.csv/"):
        """Test spec generation.

        This is a more detailed description of what this command does.

        Parameters
        ----------
        repo_path
            The path of the git repository to be analyzed.
        checklist_path
            Optional flag to use non-default checklist during the operation.
        """
        pass

    @staticmethod
    def evaluate(repo_path: str, report_output_path: str = None,
                 response_output_path: str = None,
                 checklist_path: str = "./checklist/checklist.csv/",
                 model="gpt-3.5-turbo", verbose: bool = False,
                 overwrite: bool = False) -> None:
        """Evaluate a given repo based on the completeness of the test suites.

        This will evaluate the completeness of the test suites given a git
        repository, based on a checklist which consists of items relevant to
        various aspects related to Data Science/Machine Learning projects. A
        report will be generated according to the given format specified in

        Parameters
        ----------
        repo_path
            The path of the git repository to be analyzed.
        report_output_path
            Optional. If provided, the system will write the evaluation to
            the path. The format of the evaluation report will be based on
            the extension provided in this path. The extensions must be
            either one of `.html`, `.htm`, `.pdf`, or `.qmd`.
        response_output_path
            Optional. If provided, the system will write the response in
            PICKLE to the path.
        checklist_path
            Optional flag to use non-default checklist during the operation.
        model
            Optional flag to specify a specific model to be used. Default is
            `gpt-3.5-turbo`.
        verbose
            Optional. If provided, the system will print out evaluation
            results to standard output. Default is `False`.
        overwrite
            Optional. If provided, the system will not stop when
            attempting to overwrite an existing evaluation report.
        """
        llm = ChatOpenAI(model=model, temperature=0)
        checklist = Checklist(checklist_path)
        repo = Repository(repo_path)
        prompt_format = EvaluationPromptFormat()

        evaluator = PerFileTestEvaluator(llm, prompt_format=prompt_format,
                                         repository=repo, checklist=checklist)
        response = evaluator.run()
        if response_output_path:
            with open(response_output_path, 'wb') as file:
                pickle.dump(response, file)

        if report_output_path:
            parser = ResponseParser(response)
            parser.get_completeness_score(verbose=verbose)

            parser.export_evaluation_report(report_output_path, exist_ok=overwrite)
