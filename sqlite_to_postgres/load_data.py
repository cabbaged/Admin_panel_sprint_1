import datetime
import psycopg2
import sqlite3
import uuid

from dataclasses import dataclass, field, asdict, astuple
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor, execute_batch


@dataclass(frozen=True)
class Person:
    full_name: str
    birth_date: datetime.datetime
    created_at: datetime.datetime
    updated_at: datetime.datetime
    id: uuid.UUID = field(default_factory=uuid.uuid4)


@dataclass(frozen=True)
class GenreFilmWork:
    created_at: datetime.datetime
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    genre_id: uuid.UUID = field(default_factory=uuid.uuid4)
    film_work_id: uuid.UUID = field(default_factory=uuid.uuid4)


@dataclass(frozen=True)
class Genre:
    name: str
    description: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    id: uuid.UUID = field(default_factory=uuid.uuid4)


@dataclass(frozen=True)
class PersonFilmWork:
    role: str
    created_at: datetime.datetime
    film_work_id: uuid.UUID = field(default_factory=uuid.uuid4)
    person_id: uuid.UUID = field(default_factory=uuid.uuid4)
    id: uuid.UUID = field(default_factory=uuid.uuid4)


@dataclass(frozen=True)
class FilmWork:
    title: str
    description: str
    creation_date: datetime.datetime
    certificate: str
    file_path: str
    rating: float
    type: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    id: uuid.UUID = field(default_factory=uuid.uuid4)


class SQLiteLoader:
    def __init__(self, connection):
        connection.row_factory = sqlite3.Row
        self.connection = connection
        self.data = {}
        self.table_handlers = {
            "film_work": FilmWork,
            "genre_film_work": GenreFilmWork,
            "person_film_work": PersonFilmWork,
            "genre": Genre,
            "person": Person
        }

    def load_movies(self):
        for table_name in tuple(self.table_handlers):
            self.data[table_name] = self.get_table_content(table_name)
        return self.data

    def get_table_content(self, table_name):
        result = self.connection.execute(f"SELECT * FROM {table_name}")
        handler = self.table_handlers[table_name]
        return [handler(**row) for row in result]


class PostgresSaver:
    def __init__(self, pg_conn):
        self.connection = pg_conn

    def save_all_data(self, data):
        self.data = data
        for table_name in tuple(data):
            self.insert_data(table_name)

    def make_insert_statement(self, table_name):
        row = self.data[table_name][0]
        field_names = asdict(row).keys()
        columns = ",".join(field_names)
        columns = columns.replace("created_at", "created").replace("updated_at", "modified")
        values = ",".join(["%s" for _ in field_names])
        insert_statement = f"insert into {table_name} ({columns}) values ({values})"
        return insert_statement

    def insert_data(self, table_name):
        insert_statement = self.make_insert_statement(table_name)
        execute_batch(
            self.connection.cursor(),
            insert_statement,
            [astuple(x) for x in self.data[table_name]],
            page_size=5000,
        )


def load_from_sqlite(connection: sqlite3.Connection, pg_conn: _connection):
    """Основной метод загрузки данных из SQLite в Postgres"""
    postgres_saver = PostgresSaver(pg_conn)
    sqlite_loader = SQLiteLoader(connection)

    data = sqlite_loader.load_movies()
    postgres_saver.save_all_data(data)


if __name__ == "__main__":
    dsl = {"dbname": "movies_database",
           "user": "postgres",
           "password": 1234,
           "host": "127.0.0.1",
           "port": 5432,
           "options": "-c search_path=content"}
    with sqlite3.connect("db.sqlite") as sqlite_conn, psycopg2.connect(**dsl, cursor_factory=DictCursor) as pg_conn:
        load_from_sqlite(sqlite_conn, pg_conn)
