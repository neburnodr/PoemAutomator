import psycopg2
import csv
from os import path
save_csv_path = "/home/nebur/Desktop/poemautomator/files"


def check_if_db_exists():
    conn = None

    try:
        conn = psycopg2.connect("user=postgres host=localhost password=|>ediatraTROMPET4 port=5432")
        print('Database connected.')
    except:
        print('Database not connected.')

    if conn is not None:

        conn.autocommit = True

        cur = conn.cursor()

        cur.execute("SELECT datname FROM pg_database;")

        list_database = cur.fetchall()

        database_name = "verses_db"

        if database_name in list_database:
            print("'{}' Database already exist".format(database_name))
            conn.close()
            return True
        else:
            print("'{}' Database not exist.".format(database_name))
            conn.close()
            return False


def create_db():
    conn = None

    try:
        conn = psycopg2.connect("user=postgres host=localhost password=|>ediatraTROMPET4 port=5432")
        print('Database connected.')
    except:
        print('Database not connected.')

    if conn is not None:
        conn.autocommit = True
        cur = conn.cursor()

        cur.execute("""CREATE DATABASE verses_db;""")
        conn.close()


def create_db_table():
    conn = None

    try:
        conn = psycopg2.connect("user=postgres  host=localhost db=verses_db password=|>ediatraTROMPET4 port=5432")
        print('Database connected.')
    except:
        print('Database not connected.')

    if conn is not None:
        conn.autocommit = True
        cur = conn.cursor()

        cur.execute("""CREATE TABLE verses(
                    id integer,
                    verse text,
                    long integer,
                    consonant_rhyme text,
                    asonant_rhyme text,
                    beg_verse bool,
                    int_verse bool,
                    fin_verse bool);
                    """)
        conn.close()


def csv_file_creator(verse):
    if not path.exists(f"{save_csv_path}/verse_list.csv"):
        f = open(f"{save_csv_path}/verse_list.csv", "w")
        writer = csv.writer(f)
        writer.writerow(verse)
        f.close()

    else:
        with open(f"{save_csv_path}/verse_list.csv", "a") as f:
            writer = csv.writer(f)
            writer.writerow(verse)
