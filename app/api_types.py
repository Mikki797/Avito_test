"""
Types for API service.
"""

from typing import List
from collections import Counter

from pydantic import BaseModel, validator


class PollCreateType(BaseModel):
    """
    Type to create poll.

    Attributes
    ----------
    name : str
    choices: List[str]
    """
    name: str
    choices: List[str]

    @validator('name')
    def name_not_empty(cls, name: str):
        if not name:
            raise ValueError('Name cannot be empty string')
        return name

    @validator('choices')
    def choices_not_empty_no_duplicates(cls, choices: List[str]) -> List[str]:
        if not choices:
            raise ValueError('Choices must contain at least one element')
        if Counter(choices).most_common(1)[0][1] > 1:
            raise ValueError('Choices must not contain the same elements')
        return choices


class PollType(PollCreateType):
    """
    Poll type.

    Attributes
    ----------
    id : int
    name : str
    choices: List[str]
    """
    id: int


class VoteType(BaseModel):
    """
    Vote type.

    Attributes
    ----------
    poll_id : int
    choice_id : int
    """
    poll_id: int
    choice_id: int


class ChoiceResultType(BaseModel):
    """
    Type to return result of poll.

    Attributes
    ----------
    choice_id : int
    vote_count : int
    """
    choice_id: int
    vote_count: int


class ResultType(BaseModel):
    """
    Result of poll type.

    Attributes
    ----------
    poll_id : int
    result : List[ChoiceResultType]
        ChoiceResultType from api_types.
    """
    poll_id: int
    result: List[ChoiceResultType]
