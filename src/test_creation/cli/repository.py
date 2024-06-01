from langchain_openai import ChatOpenAI

from ..modules.workflow.prompt_format import EvaluationPromptFormat
from ..modules.workflow.evaluator import PerFileTestEvaluator
from ..modules.code_analyzer.repo import Repository
from ..modules.workflow.parse import ResponseParser
from ..modules.checklist.checklist import Checklist, ChecklistFormat


class RepositoryActions(object):
    def generate(self, checklist_path, repo_path):
        """Test spec generation.

        This is a more detailed description of what this command does.

        Parameters
        ----------
        checklist_path
        repo_path

        Returns
        -------

        """
        pass

    def evaluate(self, checklist_path, repo_path, report_output_path, report_output_format='html'):
        """Evaluate a given repo based on the completeness of the test suites."""
        llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
        checklist = Checklist(checklist_path, checklist_format=ChecklistFormat.CSV)
        repo = Repository(repo_path)
        prompt_format = EvaluationPromptFormat()

        evaluator = PerFileTestEvaluator(llm, prompt_format=prompt_format, repository=repo, checklist=checklist)
        response = evaluator.evaluate()

        parser = ResponseParser(response)
        parser.get_completeness_score(verbose=True)

        parser.export_evaluation_report(report_output_path, report_output_format, exist_ok=True)

