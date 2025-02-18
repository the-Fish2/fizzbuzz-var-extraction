import together
from pydantic import BaseModel, Field
from typing import Dict, List

"""
These are the JSON schema that specify the format of output for the variable state extraction.
"""


class StateExtraction(BaseModel):
    line_number: int = Field(description="Line number of state extracted")
    variables: Dict[str, str] = Field(
        description="Dictionary of variable names and their values"
    )
    file: str = Field(description="Name of the file that the code is currently in")


class StateExtractionFormat(BaseModel):
    state_extractions: List[StateExtraction] = Field(
        description="List of intermediate variable state extractions",
        default_factory=list,
    )
