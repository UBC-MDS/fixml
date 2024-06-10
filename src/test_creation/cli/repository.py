from langchain_openai import ChatOpenAI
from langchain.globals import set_debug

from ..modules.workflow.prompt_format import EvaluationPromptFormat, \
    GenerationPromptFormat
from ..modules.workflow.runners.evaluator import PerFileTestEvaluator
from ..modules.workflow.runners.generator import NaiveTestGenerator
from ..modules.code_analyzer.repo import Repository
from ..modules.workflow.parse import ResponseParser
from ..modules.checklist.checklist import Checklist


class RepositoryActions(object):
    @staticmethod
    def generate(test_output_path: str,
                 checklist_path: str = "./checklist/checklist.csv/",
                 model="gpt-3.5-turbo", verbose: bool = False,
                 debug: bool = False):
        """Test spec generation.

        This will generate function specifications for each item in the
        checklist. Currently, it will not be referencing existing codebase and
        thus the specifications created will not be aware of the existing
        codes or the requirements.

        Parameters
        ----------
        test_output_path
            Test file path that the system will write the test functions to.
        checklist_path
            Optional flag to use non-default checklist during the operation.
        model
            Optional flag to specify a specific model to be used. Default is
            `gpt-3.5-turbo`.
        verbose
            Optional. If provided, the system will print out evaluation
            results to standard output. Default is `False`.
        debug
            Optional. If provided, the system will enable langchain's debug
            mode to expose all debug messages to the standard output.
        """
        set_debug(debug)
        llm = ChatOpenAI(model=model, temperature=0)
        checklist = Checklist(checklist_path)
        prompt_format = GenerationPromptFormat()

        generator = NaiveTestGenerator(llm, prompt_format, checklist=checklist)
        result = generator.run(verbose=verbose)

        # FIXME: assume overwrite
        with open(test_output_path, "w") as file:
            for res in result:
                file.write(f"# {res['ID']} {res['Title']}\n")
                file.write(res['Function'])
                file.write("\n\n")


    @staticmethod
    def evaluate(repo_path: str, report_output_path: str,
                 checklist_path: str = "./checklist/checklist.csv/",
                 model="gpt-3.5-turbo", verbose: bool = False,
                 overwrite: bool = False, debug: bool = False) -> None:
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
            The path which the evaluation will be written to. The format of
            the evaluation report will be based on the extension provided in
            this path. The extensions must be either one of `.html`, `.htm`,
            `.pdf`, or `.qmd`.
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
        debug
            Optional. If provided, the system will enable langchain's debug
            mode to expose all debug messages to the standard output.
        """
        set_debug(debug)
        llm = ChatOpenAI(model=model, temperature=0)
        checklist = Checklist(checklist_path)
        repo = Repository(repo_path)
        prompt_format = EvaluationPromptFormat()

        evaluator = PerFileTestEvaluator(llm, prompt_format=prompt_format,
                                         repository=repo, checklist=checklist)
        response = evaluator.run()

        parser = ResponseParser(response)
        parser.get_completeness_score(verbose=verbose)

        parser.export_evaluation_report(report_output_path, exist_ok=overwrite)
