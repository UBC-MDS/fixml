import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Union

from pydantic import BaseModel, Field, ConfigDict

from ..code_analyzer.repo import Repository
from ..checklist.checklist import Checklist
from ..mixins import WriteableMixin


class LLMInfo(BaseModel):
    name: str = Field(description="Name of the LLM used")
    temperature: float = Field(description="Temperature of the LLM")


class RepositoryInfo(BaseModel):
    path: Union[str, Path] = Field(description="Path of the repository")
    git_commit: str = Field(description="Commit hash used during evaluation")
    object: Repository = Field(description="Repository object", exclude=True)

    model_config = ConfigDict(arbitrary_types_allowed=True)


class ChecklistInfo(BaseModel):
    path: Union[str, Path] = Field(description="Path of the checklist")
    object: Checklist = Field(description="Checklist object", exclude=True)

    model_config = ConfigDict(arbitrary_types_allowed=True)


class TokenInfo(BaseModel):
    input_count: int = Field(description="Number of tokens used in prompt")
    output_count: int = Field(description="Number of tokens used in the response generated")


class ErrorInfo(BaseModel):
    name: str = Field(description="Class name of the error")
    description: str = Field(description="Description of the error")


class CallResult(BaseModel):
    start_time: datetime = Field(description="Start time of the call")
    end_time: datetime = Field(description="End time of the call")
    tokens_used: TokenInfo = Field(description="Token related information")
    files_evaluated: List[str] = Field(description="List of files used in the call")
    context: Dict[str, str] = Field(description="Injected context as a dictionary")
    prompt: str = Field(description="Final constructed prompt sent to LLM")
    success: bool = Field(description="Whether the call is successful")
    parsed_response: Optional[Dict] = Field(description="Parsed response")
    error: Optional[ErrorInfo] = Field(description="List of errors (if any)", default=None)


class EvaluationResponse(BaseModel, WriteableMixin):
    """A data class to store all information from test evaluation runs.

    Here is the schema:
    {
        model {
            name
            temperature
        }
        repository {
            path
            git_commit
            object (excluded when exporting)
        }
        checklist {
            path
            object (excluded when exporting)
        }
        call_results [{
            start_time
            end_time
            tokens_used {
                input_count
                output_count
            }
            files_evaluated
            injected
            prompt
            success
            parsed_response
            errors [{
                name
                description
            }]
        }]
    }
    """
    model: LLMInfo = Field(description="LLM-related information")
    repository: RepositoryInfo = Field(description="Repository-related information")
    checklist: ChecklistInfo = Field(description="Checklist-related information")
    call_results: List[CallResult] = Field(description="List of call results", default=[])

    def __init__(self, **data):
        super().__init__(**data)

    def to_json(self, output_path: Union[str, Path], exist_ok=False):
        self._filedump_check(output_path, exist_ok=exist_ok)
        json_str = self.model_dump_json()
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(json_str)

    @classmethod
    def from_json(cls, json_path: Union[str, Path]):
        """Reconstruct an instance of EvaluationResponse from JSON file.

        Requires checklist path and repository path to actually exist in the
        system, otherwise an error will be thrown.
        """
        with open(json_path, "r", encoding="utf-8") as f:
            deserialized = json.load(f)
        repo_obj = Repository(deserialized["repository"]["path"])
        checklist_obj = Checklist(deserialized["checklist"]["path"])
        deserialized["repository"]["object"] = repo_obj
        deserialized["checklist"]["object"] = checklist_obj
        return cls(**deserialized)
