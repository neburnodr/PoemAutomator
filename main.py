from data import scraping_amediavoz, scraping_buscapoemas, db_funcs
from data.processing_verses import clean_verses
from data.analyse_verses import Syllabifier
from automator import poem_creator
from typing import List
from os import path
import getpass

urls = [
    "http://amediavoz.com/indice-A-K.htm",
    "http://amediavoz.com/indice-L-Z.htm",
    "https://www.buscapoemas.net/poetas.html",
]


def fetch_data() -> None:
    if not path.exists("data/raw_verses.txt"):

        print("[+] Starting the webscraping process to create a database of verses...")
        verses = scrape_verses()

        print("[+] Saving the raw verses in 'raw_verses.txt'")
        with open("data/raw_verses.txt", "w") as f:
            f.write("\n".join(verses))

    if not path.exists("data/verses.txt"):
        print("[+] Retrieving the verses from 'raw_verses.txt")
        with open("data/raw_verses.txt") as f:
            verses = f.read().split("\n")

        cleaned_verses = clean_verses(verses)

        print("[+] Saving the cleaned verses in 'verses.txt'")
        with open("data/verses.txt", "w") as f:
            f.write("\n".join(cleaned_verses))

    else:
        with open("data/verses.txt") as f:
            cleaned_verses = f.read().split("\n")

    with open("data/verse_list.csv", "w") as f:
        f.close()

    print("[+] Analysing the verses and creating the CSV File.")
    for i, verse in enumerate(cleaned_verses):

        analysed_verse = Syllabifier(verse)

        ready_verse = [
            i,
            verse,
            analysed_verse.syllables,
            analysed_verse.consonant_rhyme,
            analysed_verse.asonant_rhyme,
            analysed_verse.last_word,
            analysed_verse.beg,
            analysed_verse.end,
            analysed_verse.int,

        ]

        db_funcs.csv_file_creator(ready_verse)

    print("[+] Done analysing the verses. CSV File ready to use.")


def scrape_verses() -> List[str]:
    """Scraping Amediavoz and Buscapoemas"""
    urls_poets_amediavoz = scraping_amediavoz.getting_amediavoz_links(urls[:2])
    verses = scraping_amediavoz.getting_the_verses(urls_poets_amediavoz)

    # Scraping Buscapoemas
    urls_poets = scraping_buscapoemas.getting_poets(urls[2])

    counter = 0
    for poet_url in urls_poets:
        if poet_url in scraping_buscapoemas.exclude_poets:
            continue

        poet_path = poet_url[34:-4]
        counter += 1
        urls_poems = scraping_buscapoemas.getting_poems(poet_url, poet_path)

        print(f"\n[+] [{counter}/{len(urls_poets) - len(scraping_buscapoemas.exclude_poets)}] "
              f"Extracting the verses from {poet_url}\n")
        for poem_url in urls_poems:
            verses.extend(scraping_buscapoemas.getting_the_verses(poem_url, poet_path))

    print("[+] Done", end="\n\n")

    return verses


def main() -> None:
    db_exist = input("Do you need to build the DB of verses? [y/n]")

    if db_exist.capitalize() != "Y":
        print(
            "[+] Requirements satisfied. Starting the poem generator...", end="\n\n"
        )
        poem_creator.create_poem()

    else:
        pg_username = input("Enter username to use for PostgreSQL: ")
        pg_pwd = getpass.getpass(prompt="Enter password for given user: ", stream=None)
        database_name = input("Enter name of the DB to be created: ")
        tablename = "verses"

        if not db_funcs.check_if_db_exists(pg_username, pg_pwd, database_name):
            db_funcs.create_db(pg_username, pg_pwd, database_name)
            db_funcs.create_db_table(pg_username, pg_pwd, database_name, tablename)

        if not db_funcs.check_if_table_exists(pg_username, pg_pwd, database_name, tablename):
            db_funcs.create_db_table(pg_username, pg_pwd, database_name, tablename)

        db_funcs.delete_rows_from_table(pg_username, pg_pwd, database_name, tablename)
        fetch_data()

        db_funcs.import_csv_to_db(pg_username, pg_pwd, database_name, tablename)

        print("[+] Requirements satisfied. Starting the poem generator...", end="\n\n")
        poem_creator.create_poem()


if __name__ == "__main__":
    main()
