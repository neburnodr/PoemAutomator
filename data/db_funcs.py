import psycopg2
import csv
import getpass

save_csv_path = "/home/nebur/Desktop/poemautomator/data"


user = "poemator_user"
pwd = getpass.getpass()
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


def check_if_user_exists():
    conn = create_connection()

    query = f"""SELECT * FROM USER"""

    cur = cursor_execute(conn, query)

    users = cur.fetchall()

    if user in users:
        conn.close()
        return True

    conn.close()
    return False


def create_user():
    conn = create_connection()

    query = f"""CREATE USER {user}"""

    cursor_execute(conn, query)
    print("[+] Created user for DB")


def check_if_db_exists():
    conn = create_connection()

    query = "SELECT datname FROM pg_database;"

    cur = cursor_execute(conn, query)

    list_database = cur.fetchall()
    list_database = [db[0] for db in list_database]

    if database in list_database:
        conn.close()
        return True

    else:
        conn.close()
        return False


def create_db():
    print("[+] Creating the database...")

    conn = create_connection()
    query = f"CREATE DATABASE {database};"

    cursor_execute(conn, query)

    conn.close()
    print(f"[+] Database '{database}' created")


def check_if_table_exists():
    conn = create_connection(database_name=database)
    query = f"""SELECT EXISTS (
                             select from pg_tables
                             where tablename = '{tablename}'
                             );"""

    cur = cursor_execute(conn, query)
    exists = cur.fetchall()[0][0]

    if exists:
        print(f"[+] Table '{tablename}' exist")
        return True

    else:
        print(f"[-] Table '{tablename}' doesn't exist")
        return False


def create_db_table():
    print(f"[+] Creating the table {tablename} in {database}")

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
                UNIQUE(id, verse)
        );
        """

    cursor_execute(conn, query)

    conn.close()
    print("[+] Table '{}' created in '{}'.".format(tablename,
                                                   database))


def delete_rows_from_table():
    conn = create_connection(database_name=database)
    query = f"DELETE FROM {tablename};"

    cursor_execute(conn, query)
    conn.close()


def csv_file_appender(verse):
    with open(f"{save_csv_path}/verse_list.csv", "a") as f:
        writer = csv.writer(f)
        writer.writerow(verse)


def import_csv_to_db():
    print("[+] importing CSV file to '{}'".format(database))

    conn = create_connection(database_name=database)

    cur = conn.cursor()

    cur.execute(f"""COPY {tablename} FROM '/home/nebur/Desktop/poemautomator/data/verse_list.csv' 
                    WITH (FORMAT csv);
                    """
                )

    conn.close()

    print("[+] Done copying CSV file to database '{}'".format(database))


def fetch_verses(long, rhyme, cons=True):
    conn = create_connection(database_name=database)
    rhyme_type = "consonant_rhyme" if cons else "asonant_rhyme"
    query = f"""SELECT DISTINCT last_word, verse from public.verses 
                WHERE long = {long}
                AND {rhyme_type} = {rhyme}
                """

    cur = cursor_execute(conn, query)

    verses = cur.fetchall()
    # Only unique last_words
    verses = {verse[0]: verse[1] for verse in verses}

    return verses
