CREATE TABLE polls (
        choice_id serial PRIMARY KEY,
        name text NOT NULL CHECK (name <> '')
);

CREATE TABLE choices (
        choice_id integer NOT NULL,
        poll_id integer REFERENCES polls,
        name text NOT NULL CHECK (name <> ''),
        vote_count integer NOT NULL,
        PRIMARY KEY (id, poll_id),
        UNIQUE (poll_id, name)
)
WITH (fillfactor=70);
