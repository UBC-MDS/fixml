import fire

import langchain
from langchain_openai import ChatOpenAI

from modules.workflow.prompt_format import EvaluationPromptFormat
from modules.workflow.evaluator import PerFileTestEvaluator
from modules.checklist.checklist import Checklist, ChecklistFormat
from modules.code_analyzer.repo import Repository
from modules.workflow.parse import ResponseParser

langchain.debug = True

if __name__ == '__main__':
    def main(checklist_path, repo_path):

        llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
        checklist = Checklist(checklist_path, checklist_format=ChecklistFormat.CSV)
        repo = Repository(repo_path)
        prompt_format = EvaluationPromptFormat()

        evaluator = PerFileTestEvaluator(llm, prompt_format=prompt_format, repository=repo, checklist=checklist)
        response = evaluator.evaluate()

        parser = ResponseParser(response)
        parser.get_completeness_score()

    fire.Fire(main)
