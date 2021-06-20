from pydantic import BaseModel, ValidationError, validator
from typing import List


class PollType(BaseModel):
    name: str
    choices: List[str]

    @validator('choices')
    def choices_not_empty(cls, choices: List[str]):
        if not choices:
            raise ValueError('Choices must contain at least one element')
        return choices


class VoteType(BaseModel):
    poll_id: int
    choice_id: int
