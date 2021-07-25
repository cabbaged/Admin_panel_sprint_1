CREATE DATABASE movies_database;
\connect movies_database;

CREATE SCHEMA IF NOT EXISTS content;

CREATE TABLE content.genre (
    id uuid PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    created timestamp with time zone,
    modified timestamp with time zone
);

CREATE TABLE content.film_work (
    id uuid PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    creation_date DATE,
    certificate TEXT,
    file_path TEXT,
    rating FLOAT,
    type TEXT not null,
    created timestamp with time zone,
    modified timestamp with time zone
);

CREATE TABLE content.person (
    id uuid PRIMARY KEY,
    full_name TEXT NOT NULL,
    birth_date DATE,
    created timestamp with time zone,
    modified timestamp with time zone
);

CREATE TABLE content.genre_film_work (
    id uuid PRIMARY KEY,
    film_work_id uuid NOT NULL,
    genre_id uuid NOT NULL,
    created timestamp with time zone,
    CONSTRAINT fk_film_work
      FOREIGN KEY(film_work_id)
      REFERENCES content.film_work(id)
      ON DELETE CASCADE,
    CONSTRAINT fk_genre
      FOREIGN KEY(genre_id)
      REFERENCES content.genre(id)
      ON DELETE CASCADE
);

CREATE UNIQUE INDEX film_work_genre ON content.genre_film_work (film_work_id, genre_id);

CREATE TABLE content.person_film_work (
    id uuid PRIMARY KEY,
    film_work_id uuid NOT NULL,
    person_id uuid NOT NULL,
    role TEXT NOT NULL,
    created timestamp with time zone,
    CONSTRAINT fk_film_work
      FOREIGN KEY(film_work_id)
      REFERENCES content.film_work(id)
      ON DELETE CASCADE,
    CONSTRAINT fk_person
      FOREIGN KEY(person_id)
      REFERENCES content.person(id)
      ON DELETE CASCADE
);

CREATE UNIQUE INDEX film_work_person_role ON content.person_film_work (film_work_id, person_id, role);
