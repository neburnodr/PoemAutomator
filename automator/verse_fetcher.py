import psycopg2
from data.analyse_verses import Syllabifier
from random import randint
from getpass import getpass


class Buscador:
    def __init__(self, sentence):
        self.syll = Syllabifier(sentence)


    def get_verses(self):
        conn = None

        try:
            conn = psycopg2.connect(user=user,
                                    password=pwd,
                                    database=database,
                                    host="localhost",
                                    port="5432")

        except:
            print("Connection could no be established.")

        cur = conn.cursor()

        cur.execute(f"""SELECT verse FROM {tablename}
                        WHERE consonant_rhyme = {self.syll.consonant_rhyme}
                        AND long = {self.syll.syllables}
                        LIMIT 50;""")

        verses = cur.fetchall()

        return verses

user = "postgres"
pwd = getpass()
database = "verses_db"
tablename = "verses"


buscador = Buscador(input("Verso para el que buscar rimas: "))
verses = buscador.get_verses()

for verse in verses:
    print("\t\t" + verse + "\n")
