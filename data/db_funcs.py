import psycopg2
import csv
import getpass
from os import path
import sys
save_csv_path = "/data"


def check_if_db_exists():
    conn = None

    conn = psycopg2.connect(user="postgres",
                            host="localhost",
                            password=getpass.getpass(),
                            port="5432",
    )

    if conn is not None:

        conn.autocommit = True

        cur = conn.cursor()

        cur.execute("SELECT datname FROM pg_database;")

        list_database = cur.fetchall()
        list_database = [db[0] for db in list_database]

        database_name = "verses_db"

        if database_name in list_database:
            print("[+] '{}' database already exist".format(database_name))
            conn.close()
            return True

        else:
            print("[-] '{}' database not exist.".format(database_name))
            conn.close()
            return False


def create_db():
    print("[+] Creating the database...")

    conn = None

    conn = psycopg2.connect(user="postgres",
                            host="localhost",
                            password=getpass.getpass(),
                            port="5432",
                            )

    conn.autocommit = True
    cur = conn.cursor()

    cur.execute("""CREATE DATABASE verses_db;""")

    conn.close()

    print("[+] Database 'verses_db' created")


def check_if_table_exists():
    conn = None

    conn = psycopg2.connect(user="postgres",
                            host="localhost",
                            password=getpass.getpass(),
                            database="verses_db",
                            port="5432",
                            )

    conn.autocommit = True
    cur = conn.cursor()

    tablename = "verses"

    cur.execute("""SELECT EXISTS (
                                   select from pg_tables
                                   where tablename = '{}');                  
    """.format(tablename))

    exists = cur.fetchall()[0][0]

    if exists:
        print("[+] Table '{}' exist".format(tablename))
        return True

    else:
        print("[-] Table '{}' doesn't exist".format(tablename))
        return False


def create_db_table():
    print("[+] Creating the table...")

    conn = None

    conn = psycopg2.connect(user="postgres",
                            host="localhost",
                            password=getpass.getpass(),
                            port="5432",
                            database="verses_db",
                            )

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

    print("[+] Table created.")


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
