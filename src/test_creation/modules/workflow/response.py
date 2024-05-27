"""
Response object. Here is the JSON representation:
{
    model
    repo_path
    checklist [{
        ID
        Title
        Requirement
    }]
    prompt_format
    evaluator
    calls [{
        start_time
        end_time
        injected
        prompt
        parsed_response
        errors [{
            exception_name
            description
        }]

    }]
}

This can be obtained by calling `Response.__repr__()`.
"""
from abc import ABC

from langchain_core.language_models import LanguageModelLike


from .evaluator import Evaluator, TestEvaluator
from .prompt_format import PromptFormat
from ..checklist.checklist import Checklist
from ..code_analyzer.repo import Repository


class Response(ABC):
    """Abstract class object obtained from running evaluation from evaluators."""
    def __init__(self, evaluator: Evaluator):
        self.evaluator = evaluator


class EvaluationResponse(Response):
    """Class object to store all information from test evaluation runs."""

    def __init__(self, model: LanguageModelLike, repo_path: str, checklist_path: str, prompt_format: PromptFormat,
                 evaluator: TestEvaluator):
        super().__init__(evaluator)
        self.model = model
        self.repo_path = repo_path
        self.checklist_path = checklist_path
        self.prompt = prompt_format
        self.evaluator = evaluator

    def __repr__(self):
        # TODO
        return self

    def add_call_result(self, start_time, end_time, files_injected, prompt_injected, parsed_response, errors):
        # TODO
        pass
