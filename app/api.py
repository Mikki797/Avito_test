"""
JSON API Service
"""

import json

from datetime import datetime
from fastapi import FastAPI, HTTPException
from typing import Dict, Any, Optional

from app.api_types import PollType, VoteType
from app.database import Database


app = FastAPI(title='avito-test')
db = Database()

@app.post('/api/createPoll',
          response_description="Id добавленного голосования")
async def create_poll(poll: PollType) -> Dict[str, Any]:
    poll_id = db.add_poll(poll)
    return {'status': 'ok', 'id': poll_id}


@app.post('/api/poll',
          response_description="Результат голосования за конкретный вариант"
                               "(False при отсутствии такого голосования или варианта, иначе True")
async def poll(id: int, date1: Optional[int] = None, date2: Optional[int] = None) -> Dict[str, Any]:
    return {'status': 'ok', 'result': ''}
