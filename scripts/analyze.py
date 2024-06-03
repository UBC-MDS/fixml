import fire
import pickle

from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

from test_creation.modules.workflow.prompt_format import EvaluationPromptFormat
from test_creation.modules.workflow.evaluator import PerFileTestEvaluator
from test_creation.modules.checklist.checklist import Checklist, ChecklistFormat
from test_creation.modules.code_analyzer.repo import Repository
from test_creation.modules.workflow.parse import ResponseParser

load_dotenv()


if __name__ == '__main__':
    def main(checklist_path, repo_path, report_output_path=None, report_output_format='html', response_output_path=None):
        """
        Example:
        ----------
        >>> python script/analyze.py --checklist_path='./checklist/checklist_demo.csv' --repo_path='../lightfm/' --report_output_path='./report/evaluation_report.html' --report_output_format='html'
        """
        llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
        checklist = Checklist(checklist_path, checklist_format=ChecklistFormat.CSV)
        repo = Repository(repo_path)
        prompt_format = EvaluationPromptFormat()

        evaluator = PerFileTestEvaluator(llm, prompt_format=prompt_format, repository=repo, checklist=checklist)
        response = evaluator.evaluate()
        if response_output_path:
            with open(response_output_path, 'wb') as file:
                pickle.dump(response, file)

        if report_output_path:
            parser = ResponseParser(response)
            parser.get_completeness_score(verbose=True)

            parser.export_evaluation_report(report_output_path, report_output_format, exist_ok=True)

    fire.Fire(main)
