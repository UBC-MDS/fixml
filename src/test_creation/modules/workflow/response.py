from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional, Union

from pydantic import BaseModel, Field


class LLM(BaseModel):
    name: str = Field(description="Name of the LLM used")
    temperature: float = Field(description="Temperature of the LLM")


class Error(BaseModel):
    name: str = Field(description="Class name of the error")
    description: str = Field(description="Description of the error")


class CallResult(BaseModel):
    start_time: datetime = Field(description="Start time of the call")
    end_time: datetime = Field(description="End time of the call")
    files_evaluated: List[str] = Field(description="List of files used in the call")
    injected: Dict[str, Any] = Field(description="Injected context as a dictionary")
    prompt: str = Field(description="Final constructed prompt sent to LLM")
    success: bool = Field(description="Whether the call is successful")
    parsed_response: Optional[Dict] = Field(description="Parsed response")
    errors: List[Error] = Field(description="List of errors (if any)", default=[])


class EvaluationResponse(BaseModel):
    """A data class to store all information from test evaluation runs.

    Here is the schema:
    {
        model {
            name
            temperature
        }
        repository_path
        checklist_path
        call_results [{
            start_time
            end_time
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
    model: LLM = Field(description="LLM-related information")
    repository_path: Union[str, Path] = Field(description="Repository path")
    checklist_path: Union[str, Path] = Field(description="Checklist path")
    call_results: List[CallResult] = Field(description="List of call results", default=[])
