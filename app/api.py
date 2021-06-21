"""
JSON API Service
"""

import json

from datetime import datetime
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional

from app.api_types import PollType, VoteType, PollOutType, ResultType, ChoiceResultType
from app.database import Database


app = FastAPI(title='avito-test')
db = Database()


@app.post('/api/createPoll',
          response_description="Id добавленного голосования",
          response_model=PollOutType)
async def create_poll(poll: PollType):
    poll_id = db.add_poll(poll)
    return PollOutType(id=poll_id)


# TODO добавить голосование за несколько вариантов
@app.post('/api/poll',
          response_description="Проголосовать за вариант в голосовании")
async def vote(vote: VoteType):
    if not db.vote(vote):
        raise HTTPException(status_code=404, detail='Poll or choice not found')
    return {'status': 'ok'}


@app.post('/api/getResult/{poll_id}',
          response_description="Получить результаты голосования",
          response_model=ResultType)
async def get_result(poll_id: int):
    results = db.get_result(poll_id)
    if not results:
        raise HTTPException(status_code=404, detail='Poll not found')
    return ResultType(poll_id=poll_id,
                      result=[ChoiceResultType(choice_id=choice_id, vote_count=vote_count)
                              for choice_id, vote_count in results.items()])
