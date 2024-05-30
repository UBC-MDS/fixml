import fire

from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

from modules.workflow.prompt_format import EvaluationPromptFormat
from modules.workflow.evaluator import PerFileTestEvaluator
from modules.checklist.checklist import Checklist, ChecklistFormat
from modules.code_analyzer.repo import Repository
from modules.workflow.parse import ResponseParser

load_dotenv()


if __name__ == '__main__':
    def main(checklist_path, repo_path, report_output_path, report_output_format='html'):
        """
        Example:
        ----------
        >>> python src/test_creation/evaluate.py --checklist_path='./checklist/checklist.csv' --repo_path='../lightfm/' --report_output_path='./report/evaluation_report.html' --report_output_format='html'
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
