import psycopg2
import csv

save_csv_path = "/home/nebur/Desktop/poemautomator/data"


def check_if_db_exists(user, pwd, database_name):
    conn = None

    conn = psycopg2.connect(
        user=user,
        host="localhost",
        password=pwd,
        port="5432",
    )

    if conn is not None:

        conn.autocommit = True

        cur = conn.cursor()

        cur.execute("SELECT datname FROM pg_database;")

        list_database = cur.fetchall()
        list_database = [db[0] for db in list_database]

        if database_name in list_database:
            print("[+] '{}' database already exist".format(database_name))
            conn.close()
            return True

        else:
            print("[-] '{}' database not exist.".format(database_name))
            conn.close()
            return False


def create_db(user, pwd, database_name):
    print("[+] Creating the database...")

    conn = None

    conn = psycopg2.connect(
        user=user,
        host="localhost",
        password=pwd,
        port="5432",
    )

    conn.autocommit = True
    cur = conn.cursor()

    cur.execute("""CREATE DATABASE {};""".format(database_name))

    conn.close()

    print("[+] Database '{}' created".format(database_name))


def check_if_table_exists(user, pwd, database_name, tablename):
    conn = None

    conn = psycopg2.connect(
        user=user,
        host="localhost",
        password=pwd,
        database=database_name,
        port="5432",
    )

    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(
        """SELECT EXISTS (
                                   select from pg_tables
                                   where tablename = '{}');                  
    """.format(tablename)
    )

    exists = cur.fetchall()[0][0]

    if exists:
        print("[+] Table '{}' exist".format(tablename))
        return True

    else:
        print("[-] Table '{}' doesn't exist".format(tablename))
        return False


def create_db_table(user, pwd, database_name, tablename):
    print("[+] Creating the table {} in {}".format(tablename,
                                                   database_name))

    conn = None

    conn = psycopg2.connect(
        user=user,
        host="localhost",
        password=pwd,
        port="5432",
        database=database_name,
    )

    conn.autocommit = True

    cur = conn.cursor()

    cur.execute(
        f"""CREATE TABLE {tablename}(
                id integer,
                verse text,
                long integer,
                consonant_rhyme text,
                asonant_rhyme text,
                beg_verse bool,
                int_verse bool,
                fin_verse bool,
                UNIQUE(id, verse)
        );
        """
    )

    conn.close()

    print("[+] Table {} created in {}.".format(tablename,
                                               database_name))


def delete_rows_from_table(user, pwd, database, tablename):
    print("[+] Deleting all rows from {} in {}".format(tablename,
                                                       database))

    conn = None

    conn = psycopg2.connect(
        user=user,
        host="localhost",
        password=pwd,
        port="5432",
        database=database,
    )

    conn.autocommit = True

    cur = conn.cursor()

    cur.execute(f"DELETE FROM {tablename};")

    conn.close()

    print("[+] Table {} in {} is now clean for repopulating".format(tablename,
                                                                    database))


def csv_file_creator(verse):
    with open(f"{save_csv_path}/verse_list.csv", "a") as f:
        writer = csv.writer(f)
        writer.writerow(verse)
