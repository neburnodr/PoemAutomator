import psycopg2
import csv
import random

save_csv_path = "/home/nebur/Desktop/poemautomator/data"


user = "poemator_user"
pwd = "1234"
database = "poemator_db"
tablename = "verses_table"


def create_connection(username=user, password=pwd, database_name=None):
    conn = None

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


def cursor_execute(conn, query):
    cur = conn.cursor()

    cur.execute(query)

    return cur


def check_if_user_exists(username, password):
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


def create_user(username, password):
    conn = create_connection(username, password)
    query = f"""CREATE USER {user}
                WITH PASSWORD '{pwd}';
                """
    cursor_execute(conn, query)


def check_if_db_exists(username, password):
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


def create_db(username, password):
    conn = create_connection(username, password)
    query = f"CREATE DATABASE {database};"
    cursor_execute(conn, query)
    conn.close()


def grant_access(username, password):
    conn = create_connection(username, password)
    query = f"grant all privileges on database {database} to {user};"
    cursor_execute(conn, query)
    conn.close()


def check_if_table_exists():
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


def create_db_table():
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
                fin_verse bool,
                UNIQUE(id, verse));"""
    cursor_execute(conn, query)
    conn.close()


def delete_rows_from_table():
    conn = create_connection(database_name=database)
    query = f"DELETE FROM {tablename};"
    cursor_execute(conn, query)
    conn.close()


def csv_file_appender(verse):
    with open(f"{save_csv_path}/verse_list.csv", "a") as f:
        writer = csv.writer(f)
        writer.writerow(verse)


def import_csv_to_db(username, password):
    conn = create_connection(username, password, database)
    query = f"""COPY {tablename} FROM '/home/nebur/Desktop/poemautomator/data/verse_list.csv' 
               WITH (FORMAT csv);"""
    cursor_execute(conn, query)
    conn.close()


def fetch_verses(long, rhyme, cons=True, unique=False):
    conn = create_connection(database_name=database)
    rhyme_type = "consonant_rhyme" if cons else "asonant_rhyme"
    query = f"""SELECT verse, last_word, beg, int, end from public.verses 
                WHERE long = {long}
                AND {rhyme_type} = {rhyme};
                """

    cur = cursor_execute(conn, query)

    fetched_verses = cur.fetchall()

    if unique:
        verses = []
        # Only unique last_words
        possible_last_words = set([verse[1] for verse in fetched_verses])
        for word in possible_last_words:
            verse = random.choice([fetched for fetched in fetched_verses if fetched[1] == word])
            verses.append(verse)

    verses = fetched_verses

    return verses


def fetch_rhyme(long, cons=True):
    conn = create_connection(database_name=database)
    rhyme_type = "consonant_rhyme" if cons else "asonant_rhyme"
    query = f"""select {rhyme_type}, count(*) from {tablename}
            where long = {long}
            group by {rhyme_type}
            order by count(*) DESC;"""

    cur = cursor_execute(conn, query)

    rhymes = cur.fetchall()
    rhymes = [rhyme[0] for rhyme in rhymes if rhyme[1] > 5]

    rhyme = random.choice(rhymes)

    return rhyme
