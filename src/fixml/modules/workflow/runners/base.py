from abc import ABC, abstractmethod

from langchain_core.language_models import LanguageModelLike

from ..prompt_format import PromptFormat
from ...checklist.checklist import Checklist
from ...code_analyzer.repo import Repository


class PipelineRunner(ABC):
    """Abstract base class for running langchain pipelines.

    This class object assembles prompt and to obtain response from LLMs.
    """
    @abstractmethod
    def run(self):
        pass


class PromptInjectionRunner(PipelineRunner, ABC):
    """Abstract base class for runners which will involve prompt injections
    from checklists and files from a repository.
    i.e. class object to use a prompt template, constructing a complete
    prompt by injecting context such as checklist items and test files,
    then pass the prompt to LLM.
    """

    def __init__(self, llm: LanguageModelLike, prompt_format: PromptFormat,
                 repository: Repository, checklist: Checklist):
        self.llm = llm

        self.checklist = checklist
        self.repository = repository
        self.prompt_format = prompt_format

        self.chain = self.prompt_format.prompt | self.llm | self.prompt_format.parser
