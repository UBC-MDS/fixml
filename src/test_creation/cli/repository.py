from pathlib import Path
from typing import Union, Optional
from pprint import pprint

from langchain_openai import ChatOpenAI
from langchain.globals import set_debug

from .utils import parse_list
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
                 checklist_path: str = None,
                 model="gpt-3.5-turbo", verbose: bool = False,
                 debug: bool = False):
        """Test spec generation.

        This will generate function specifications for each item in the
        checklist. Currently, it will not be referencing existing codebase and
        thus the specifications created will not be aware of the existing
        codes or the requirements.

        Parameters
        ----------
        test_output_path : str
            Test file path that the system will write the test functions to.
        checklist_path : Optional[str]
            Optional flag to use non-default checklist during the operation.
        model : Optional[str]
            Optional flag to specify a specific model to be used. Default is
            `gpt-3.5-turbo`.
        verbose : Optional[bool]
            Optional. If provided, the system will print out evaluation
            results to standard output. Default is `False`.
        debug : Optional[bool]
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
    def evaluate(repo_path: str, save_response_to: str = None,
                 export_report_to: str = None,
                 checklist_path: str = None,
                 model="gpt-3.5-turbo", verbose: bool = False,
                 overwrite: bool = False, debug: bool = False,
                 test_dirs: list[Union[str, Path]] = None) -> None:
        """Evaluate a given repo based on the completeness of the test suites.

        This will evaluate the completeness of the test suites given a git
        repository, based on a checklist which consists of items relevant to
        various aspects related to Data Science/Machine Learning projects. A
        JSON file containing the evaluation results would be saved. Optionally,
        you can provide the `export_report_to` flag to use the content of the
        JSON file to render a human-readable report in HTML or PDF format.

        Parameters
        ----------
        repo_path
            The path of the git repository to be analyzed.
        save_response_to
            Optional. If provided, the JSON file saved would be in the specified
            path instead of the default location.
        export_report_to
            Optional. If provided, the system will render the evaluation report
            to the specified path. The format of the evaluation report will be
            based on the extension provided in this path. The extensions must be
            either one of `.html`, `.htm`, `.pdf`, or `.qmd`.
        checklist_path
            Optional flag to use non-default checklist during the operation.
        test_dirs
            Optional list of directories to indicate where the test files are
            located. If provided, only files inside these directories will be
            scanned. Otherwise, all files in the repository will be scanned,
            which is the default behaviour.
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
        parsed_test_dirs = parse_list(test_dirs)
        llm = ChatOpenAI(model=model, temperature=0)
        checklist = Checklist(checklist_path)
        repo = Repository(repo_path)
        prompt_format = EvaluationPromptFormat()

        evaluator = PerFileTestEvaluator(llm, prompt_format=prompt_format,
                                         repository=repo, checklist=checklist,
                                         test_dirs=parsed_test_dirs)
        response = evaluator.run(verbose=verbose)

        if not save_response_to:
            repo_name = response.repository.object.root.stem
            commit_hash = response.repository.git_commit
            eval_time = response.call_results[0].start_time.timestamp()
            response_output_path = Path(
                f"./evaluation_{repo_name}_{commit_hash}_{eval_time:0.0f}.json"
            ).resolve()
        else:
            response_output_path = Path(save_response_to).resolve()

        response.to_json(output_path=response_output_path, exist_ok=overwrite)
        print(f"Evaluation response saved to {response_output_path}.")

        if export_report_to:
            parser = ResponseParser(response)
            parser.get_completeness_score(verbose=verbose)
            parser.export_evaluation_report(export_report_to,
                                            exist_ok=overwrite)
            print(f"Evaluation report exported to {export_report_to}.")

    @staticmethod
    def quarto_test(repo_path: str, report_output_path: str = None,
                 response_output_path: str = None,
                 checklist_path: str = None,
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
        json_str = response.model_dump_json()
        with open("test-response.json", 'w') as f:
            f.write(json_str)

        # quarto-python does not support providing params by -P flag so a
        # YAML file has to be created in order to pass the parameters
        # with open("params.yml", 'w') as f:
        #     f.write("json_file: ./test-response.json")

        from quarto import render


        render("quarto-test.qmd",
               execute_params={"json_file": "./test-response.json"})
        # if report_output_path:
        #     parser = ResponseParser(response)
        #     parser.get_completeness_score(verbose=verbose)
        #
        #     parser.export_evaluation_report(report_output_path, exist_ok=overwrite)

    @staticmethod
    def list_tests(repo_path: str, test_dirs: list[Union[str, Path]] = None):
        """List out all tests found in this repository.

        Parameters
        ----------
        repo_path
            The path of the git repository to be analyzed.
        test_dirs
            Optional list of directories to indicate where the test files are
            located. If provided, only files inside these directories will be
            scanned. Otherwise, all files in the repository will be scanned,
            which is the default behaviour.
        """

        dirs = parse_list(test_dirs)
        repo = Repository(repo_path)
        test_lang_file_map = repo.list_test_files(test_dirs=dirs)
        print("Test files found:")
        for lang, files in test_lang_file_map.items():
            print(f"{lang}: ", end='')
            pprint(files)
