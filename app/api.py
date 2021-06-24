"""
JSON API Service
"""
from typing import Dict

import uvicorn
from fastapi import FastAPI, HTTPException

from app.api_types import PollCreateType, PollType, VoteType, ResultType, ChoiceResultType
from app.database import Database


app = FastAPI(title='avito-test')
db = Database()


@app.post('/api/createPoll',
          response_description="Id добавленного голосования",
          response_model=PollType)
async def create_poll(poll: PollCreateType):
    """
    Create poll with given name and choices. Name must not be an
    empty string. Choices must have at least one element and can't
    contain duplicates.

    Parameters
    ----------
    poll : PollCreateType from api_types
        Contains poll name and list of choices.

    Returns
    -------
    PollType from api_types
        Contains poll id, poll name and list of choices.
    """
    poll_id = db.add_poll(poll.name, poll.choices)
    return PollType(id=poll_id, **poll.dict())


@app.post('/api/poll',
          response_description="Проголосовать за вариант в голосовании",
          response_model=Dict[str, str])
async def poll(vote: VoteType):
    """
    Add vote to choice in poll. Poll with received poll_id must be and
    have choice with received choice_id.

    Parameters
    ----------
    vote : VoteType from api_types
        Contains poll_id and choice_id. For choice with choice_id in poll
        with poll_id one vote will be added.

    Returns
    -------
    Dict[str, str] like {'status': 'ok'}
    """
    if not db.vote(vote.poll_id, vote.choice_id):
        raise HTTPException(status_code=404, detail='Poll or choice not found')
    return {'status': 'ok'}


@app.post('/api/getResult/{poll_id}',
          response_description="Получить результаты голосования",
          response_model=ResultType)
async def get_result(poll_id: int):
    """
    Get result poll. Poll with received poll_id must be.

    Parameters
    ----------
    poll_id : int
        For poll with poll_id result will be received.

    Returns
    -------
    ResultType from api_types
        Contains poll_id and list of pair of choice_id and number of votes.
    """
    results = db.get_result(poll_id)
    if not results:
        raise HTTPException(status_code=404, detail='Poll not found')
    return ResultType(poll_id=poll_id,
                      result=[ChoiceResultType(choice_id=choice_id, vote_count=vote_count)
                              for choice_id, vote_count in results.items()])


"""
Start uvicorn server
"""
if __name__ == "__main__":
    uvicorn.run('api:app', host='0.0.0.0', port=8000)
