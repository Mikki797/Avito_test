from pydantic import BaseModel, ValidationError, validator
from typing import List
from collections import Counter


class PollType(BaseModel):
    name: str
    choices: List[str]

    @validator('choices')
    def choices_validate(cls, choices: List[str]):
        if not choices:
            raise ValueError('Choices must contain at least one element')
        elif Counter(choices).most_common(1)[0][1] > 1:
            raise ValueError('Choices must not contain the same elements')
        return choices


class PollOutType(BaseModel):
    id: int


class VoteType(BaseModel):
    poll_id: int
    choice_id: int