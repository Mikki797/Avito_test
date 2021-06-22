from pydantic import BaseModel, ValidationError, validator
from typing import List
from collections import Counter


class PollCreateType(BaseModel):
    name: str
    choices: List[str]

    @validator('name')
    def name_not_empty(cls, name: str):
        if not len(name):
            raise ValueError('Name cannot be empty string')
        return name

    @validator('choices')
    def choices_not_empty_no_duplicates(cls, choices: List[str]) -> List[str]:
        if not choices:
            raise ValueError('Choices must contain at least one element')
        elif Counter(choices).most_common(1)[0][1] > 1:
            raise ValueError('Choices must not contain the same elements')
        return choices


class PollType(PollCreateType):
    id: int


class VoteType(BaseModel):
    poll_id: int
    choice_id: int


class ChoiceResultType(BaseModel):
    choice_id: int
    vote_count: int


class ResultType(BaseModel):
    poll_id: int
    result: List[ChoiceResultType]