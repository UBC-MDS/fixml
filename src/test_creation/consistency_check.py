import fire
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

from .modules.workflow.prompt_format import EvaluationPromptFormat
from .modules.workflow.runners.evaluator import PerFileTestEvaluator
from .modules.checklist.checklist import Checklist, ChecklistFormat
from .modules.code_analyzer.repo import Repository
from .modules.llm_eval.consistency_eval import ConsistencyEvaluator

load_dotenv()


if __name__ == '__main__':
    def main(checklist_path, repo_path):
        checklist = Checklist(checklist_path)
        repo = Repository(repo_path)
        prompt_format = EvaluationPromptFormat()

        gpt35 = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
        gpt4o = ChatOpenAI(model="gpt-4o", temperature=0)
        evaluator35 = PerFileTestEvaluator(gpt35, prompt_format=prompt_format, repository=repo, checklist=checklist)
        evaluator4o = PerFileTestEvaluator(gpt4o, prompt_format=prompt_format, repository=repo, checklist=checklist)

        consist_eval = ConsistencyEvaluator()
        consist_eval.evaluate(
            models=[
                {'name': 'gpt-3.5-turbo', 'model': evaluator35},
                {'name': 'gpt-4o', 'model': evaluator4o}
            ],
            verbose=True
        )


    fire.Fire(main)
