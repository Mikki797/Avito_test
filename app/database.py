"""
Provide access to database
"""

import os
from typing import List, Dict

import psycopg2
from psycopg2 import sql
from psycopg2.extras import execute_values

DB_NAME = 'avito_api_db'
DB_TEST_NAME = 'avito_api_db_test'
DB_USER = 'postgres'
DB_PASSWORD = 'admin'
DB_HOST = os.environ.get('DB_HOST')
DB_PORT = '5432'

POLL_TABLE_NAME = 'polls'
CHOICE_TABLE_NAME = 'choices'


class Database:
    """
    Provides access to database on PostgreSQL.

    Attributes
    ----------
    con : psycopg2.connection
        Handles the connection to PostgreSQL database instance with received name,
        user, password, host and port.
    cursor: psycopg2 cursor class
        Allows to execute PostgreSQL command in a database session.
    """
    def __init__(self):
        self.con = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD,
                                    host=DB_HOST, port=DB_PORT)
        self.cursor = self.con.cursor()

    def add_poll(self, poll_name: str, choices: List[str]) -> int:
        """
        Add to database poll with given name and choices. Name must
        not be an empty string. Choices must have at least one element
        and can't contain duplicates.

        Parameters
        ----------
        poll_name : str
            Name of poll
        choices : List[str]
            List of choices names.

        Returns
        -------
        poll_id : int
            Id of added poll.
        """
        cursor = self.cursor

        query = sql.SQL("INSERT INTO {table} (id, name) VALUES "
                        "(DEFAULT, %(name)s) "
                        "RETURNING id;").format(table=sql.Identifier(POLL_TABLE_NAME))
        cursor.execute(query, {'name': poll_name})

        result = cursor.fetchone()
        poll_id = result[0]

        values = [(choice_id, poll_id, choice_name, 0) for choice_id, choice_name in enumerate(choices)]
        query = sql.SQL("INSERT INTO {table} (id, poll_id, name, vote_count) VALUES %s")\
            .format(table=sql.Identifier(CHOICE_TABLE_NAME))
        execute_values(cursor, query.as_string(cursor), values, template='(%s, %s, %s, %s)')
        self.con.commit()

        return poll_id

    def vote(self, poll_id: int, choice_id: int) -> bool:
        """
        Add one vote to choice in poll.

        Parameters
        ----------
        poll_id : int
        choice_id : int

        Returns
        -------
        result : bool
            True if vote was added, otherwise False. Vote can't be added
            if missed poll with poll_id or poll doesn't have choice with choice_id.
        """
        query = sql.SQL("UPDATE {table} SET vote_count = vote_count + 1 "
                        "WHERE poll_id = %(poll_id)s AND id = %(choice_id)s")\
            .format(table=sql.Identifier(CHOICE_TABLE_NAME))
        self.cursor.execute(query, {'poll_id': poll_id, 'choice_id': choice_id})
        self.con.commit()

        result = bool(self.cursor.rowcount)
        return result

    def get_result(self, poll_id: int) -> Dict[int, int]:
        """
        Return result of poll.

        Parameters
        ----------
        poll_id : int

        Returns
        -------
        result_map : Dict[int, int]
            Return map choice_id -> vote_count.
        """
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
