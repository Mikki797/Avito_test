CREATE TABLE polls (
        id serial PRIMARY KEY,
        name text NOT NULL
    );

CREATE TABLE choices (
        id integer NOT NULL,
        poll_id integer REFERENCES polls,
        name text NOT NULL,
        votes_number integer NOT NULL,
        PRIMARY KEY (id, poll_id)
    );