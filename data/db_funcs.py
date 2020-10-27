import psycopg2
import csv
import random
from typing import Tuple, List, Any

save_csv_path = "/home/nebur/Desktop/poemautomator/data"
Verse = List[Tuple[bool, bool, bool, str, str]]

user = "poemator_user"
pwd = "1234"
database = "poemator_db"
tablename = "verses_table"


def create_connection(username: str = user, password: str = pwd, database_name: Any = None) -> Any:
    if database_name:
        conn = psycopg2.connect(
            user=username,
            host="localhost",
            password=password,
            port="5432",
            database=database_name,
        )

    else:
        conn = psycopg2.connect(
            user=username,
            host="localhost",
            password=password,
            port="5432",
        )

    if conn is not None:
        conn.autocommit = True

        return conn


def cursor_execute(conn: Any, query: str) -> Any:
    cur = conn.cursor()

    cur.execute(query)

    return cur


def check_if_user_exists(username: str, password: str) -> bool:
    conn = create_connection(username, password)
    query = f"""SELECT usename
                FROM pg_catalog.pg_user;"""
    cur = cursor_execute(conn, query)

    users = cur.fetchall()
    users = [name_user[0] for name_user in users]  # From list of tuples to list of strings

    if user in users:
        conn.close()
        return True

    conn.close()
    return False


def create_user(username: str, password: str) -> None:
    conn = create_connection(username, password)
    query = f"""CREATE USER {user}
                WITH PASSWORD '{pwd}';
                """
    cursor_execute(conn, query)


def check_if_db_exists(username: str, password: str) -> bool:
    conn = create_connection(username, password)
    query = "SELECT datname FROM pg_database;"
    cur = cursor_execute(conn, query)

    list_database = cur.fetchall()
    list_database = [db[0] for db in list_database]

    if database in list_database:
        conn.close()
        return True

    conn.close()
    return False


def create_db(username: str, password: str) -> None:
    conn = create_connection(username, password)
    query = f"CREATE DATABASE {database};"
    cursor_execute(conn, query)
    conn.close()


def grant_access(username: str, password: str) -> None:
    conn = create_connection(username, password)
    query = f"grant all privileges on database {database} to {user};"
    cursor_execute(conn, query)
    conn.close()


def check_if_table_exists() -> bool:
    conn = create_connection(database_name=database)
    query = f"""SELECT EXISTS (
                             select from pg_tables
                             where tablename = '{tablename}'
                             );"""

    cur = cursor_execute(conn, query)
    exists = cur.fetchall()[0][0]

    if exists:
        return True

    return False


def create_db_table() -> None:
    conn = create_connection(database_name=database)
    query = f"""CREATE TABLE {tablename}(
                id integer,
                verse text,
                long integer,
                consonant_rhyme text,
                asonant_rhyme text,
                last_word text,
                beg_verse bool,
                int_verse bool,
                end_verse bool,
                UNIQUE(id, verse));"""
    cursor_execute(conn, query)
    conn.close()


def delete_rows_from_table() -> None:
    conn = create_connection(database_name=database)
    query = f"DELETE FROM {tablename};"
    cursor_execute(conn, query)
    conn.close()


def csv_file_appender(verse: List) -> None:
    with open(f"{save_csv_path}/verse_list.csv", "a") as f:
        writer = csv.writer(f)
        writer.writerow(verse)


def import_csv_to_db(username: str, password: str) -> None:
    conn = create_connection(username, password, database)
    query = f"""COPY {tablename} FROM '/home/nebur/Desktop/poemautomator/data/verse_list.csv' 
               WITH (FORMAT csv);"""
    cursor_execute(conn, query)
    conn.close()


def fetch_verses(long: Any, rhyme: str, cons: bool = True, unique: bool = False, type_verse="") -> List[Verse]:

    conn = create_connection(database_name=database)
    rhyme_type = "consonant_rhyme" if cons else "asonant_rhyme"
    type_verse = f"AND {type_verse}_verse is true" if type_verse else ""

    if type(long) == list:
        long_str = f"WHERE long >= {long[0]} AND long <= {long[1]}"
    else:
        long_str = f"WHERE long = {long}"

    query = f"""SELECT beg_verse, int_verse, end_verse, verse, last_word from {tablename} 
                {long_str}
                AND {rhyme_type} = '{rhyme}'
                {type_verse}
                ;
                """

    cur = cursor_execute(conn, query)

    fetched_verses = cur.fetchall()

    if unique:
        verses = []
        # Only unique last_words
        possible_last_words = set([verse[-1] for verse in fetched_verses])
        for word in possible_last_words:
            verse = random.choice([fetched for fetched in fetched_verses if fetched[-1] == word])
            verses.append(verse)

        return verses

    verses = fetched_verses
    return verses


def fetch_rhyme(long: Any, limit: int, cons: bool = True) -> str:
    conn = create_connection(database_name=database)
    rhyme_type = "consonant_rhyme" if cons else "asonant_rhyme"

    if type(long) == list:
        long_str = f"WHERE long >= {long[0]} AND long <= {long[1]}"
    else:
        long_str = f"WHERE long = {long}"

    query = f"""SELECT {rhyme_type}, count(*) FROM {tablename}
            {long_str}
            GROUP BY {rhyme_type}
            ORDER BY count(*) DESC;"""

    cur = cursor_execute(conn, query)

    rhymes = cur.fetchall()
    rhymes = [rhyme[0] for rhyme in rhymes if rhyme[1] > limit]

    rhyme = random.choice(rhymes)
    return rhyme


def is_subset_of(long: Any, assonant_rhyme: str, consonant_rhyme: str) -> bool:
    """Func to be sure that a given consonant_rhyme is a subset of a given assonant one"""
    conn = create_connection(database_name=database)

    if type(long) == list:
        long_str = f"WHERE long >= {long[0]} AND long <= {long[1]}"
    else:
        long_str = f"WHERE long = {long}"

    query = f"""SELECT consonant_rhyme, count(*) FROM {tablename}
            {long_str}
            AND asonant_rhyme = '{assonant_rhyme}'
            GROUP BY consonant_rhyme"""

    cur = cursor_execute(conn, query)

    rhymes = cur.fetchall()
    rhymes = [rhyme[0] for rhyme in rhymes]

    return True if consonant_rhyme in rhymes else False
