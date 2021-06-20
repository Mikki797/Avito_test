from pydantic import BaseModel
from typing import List


class PollType(BaseModel):
    name: str
    choices: List[str]


class VoteType(BaseModel):
    poll_id: int
    choice_id: int
