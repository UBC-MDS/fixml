from abc import ABC
from typing import List


from pydantic import BaseModel, Field
from langchain_core.prompts.prompt import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser


class PromptFormat(ABC):
    """A formatter to define how the prompt should be constructed and parsed."""
    def __init__(self):
        self.parser = None
        self.prompt = None


class EvaluationPromptFormat(PromptFormat):
    """Formatter for the initial call of the test evaluation pipeline.
     Injects checklist and codebase into prompt and expect JSON in return."""
    def __init__(self):
        super().__init__()

        class TestItemEvaluation(BaseModel):
            ID: str = Field(description="The corresponding `ID` of the checklist item provided. Make sure the ID is quoted in output as this ID is a string, not a number.")
            Title: str = Field(description="The corresponding `Title` of the checklist item provided")
            Requirement: str = Field(description="The corresponding `Requirement` of the checklist item provided")
            Observation: str = Field(description="Your detailed observation of the code in accordance to the given checklist item")
            Functions: List[str] = Field(description="Test functions that satisfy the given requirement. If no function satisfies, an empty list i.e. [] should be returned.")
            Evaluation: str = Field(description="The summarized evaluation. Must be one of Satisfied/Partially Satisfied/Not Satisfied.")
            Score: float = Field(description="The score obtained from the given evaluation (1 for Satisfied / 0.5 for Partially Satisfied / 0 for Not Satisfied)")

        class EvalResult(BaseModel):
            results: List[TestItemEvaluation]

        self.parser = JsonOutputParser(pydantic_object=EvalResult)

        self.prompt = PromptTemplate(
            template="You are an expert Machine Learning Engineer.\n"
                     "Please help to evaluate the following code using the given checklist.\n"
                     "{format_instructions}\n"
                     "For a test item to be considered as `Satisfied` or `Partially Satisfied`, "
                     "the corresponding function(s) satisfying the item's requirement must be "
                     "provided in the `Functions` attribute.\n"
                     "Here is the checklist as a list of JSON objects:\n```{checklist}```\n"
                     "Here is the code to be analyzed:\n```{codebase}```",
            description="Code Review for Machine Learning Project",
            input_variables=["checklist", "codebase"],
            partial_variables={"format_instructions": self.parser.get_format_instructions()},
        )
