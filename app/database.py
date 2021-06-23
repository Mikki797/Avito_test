import psycopg2
from psycopg2 import sql
from psycopg2.extras import execute_values

import os
from typing import Dict

from app.api_types import PollCreateType, VoteType

DB_NAME = 'avito_api_db'
DB_TEST_NAME = 'avito_api_db_test'
DB_USER = 'postgres'
DB_PASSWORD = 'admin'
DB_HOST = 'avito_test_db'
DB_PORT = '5432'

POLL_TABLE_NAME = 'polls'
CHOICE_TABLE_NAME = 'choices'


class Database:
    def __init__(self):
        db_name = DB_NAME if not os.environ.get('TESTING') else DB_TEST_NAME
        self.con = psycopg2.connect(dbname=db_name, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
        self.cursor = self.con.cursor()

    def add_poll(self, poll: PollCreateType) -> int:
        cursor = self.cursor

        query = sql.SQL("INSERT INTO {table} (id, name) VALUES "
                        "(DEFAULT, %(name)s) "
                        "RETURNING id;").format(table=sql.Identifier(POLL_TABLE_NAME))
        cursor.execute(query, {'name': poll.name})

        result = cursor.fetchone()
        poll_id = result[0]

        choices = {}
        values = []
        for choice_id, choice_name in enumerate(poll.choices):
            choices[choice_name] = poll_id
            values.append((choice_id, poll_id, choice_name, 0))
        query = sql.SQL("INSERT INTO {table} (id, poll_id, name, vote_count) VALUES %s")\
            .format(table=sql.Identifier(CHOICE_TABLE_NAME))
        execute_values(cursor, query.as_string(cursor), values, template='(%s, %s, %s, %s)')
        self.con.commit()

        return poll_id

    def vote(self, vote: VoteType) -> bool:
        query = sql.SQL("UPDATE {table} SET vote_count = vote_count + 1 "
                        "WHERE poll_id = %(poll_id)s AND id = %(choice_id)s")\
            .format(table=sql.Identifier(CHOICE_TABLE_NAME))
        self.cursor.execute(query, {'poll_id': vote.poll_id, 'choice_id': vote.choice_id})
        self.con.commit()

        result = bool(self.cursor.rowcount)
        return result

    def get_result(self, poll_id: int) -> Dict[int, int]:
        self.con.autocommit = True

        query = sql.SQL("SELECT (id, vote_count) FROM {table} WHERE poll_id = %s;")\
            .format(table=sql.Identifier(CHOICE_TABLE_NAME))
        self.cursor.execute(query, (poll_id,))
        self.con.commit()

        result = self.cursor.fetchall()

        result_map = {}
        for choice in result:
            choice_tuple = eval(*choice)
            result_map[choice_tuple[0]] = choice_tuple[1]
        return result_map