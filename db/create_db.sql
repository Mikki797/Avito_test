CREATE TABLE polls (
        id serial PRIMARY KEY,
        name text NOT NULL CHECK (name <> '')
);

CREATE TABLE choices (
        id integer NOT NULL,
        poll_id integer REFERENCES polls,
        name text NOT NULL CHECK (name <> ''),
        vote_count integer NOT NULL,
        PRIMARY KEY (id, poll_id),
        UNIQUE (poll_id, name)
)
WITH (fillfactor=50);
