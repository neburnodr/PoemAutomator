from data import scraping_amediavoz, scraping_buscapoemas, db_funcs
from data.processing_verses import clean_verses
from data.analyse_verses import Syllabifier
from automator import poem_creator
from typing import List
from os import path
import getpass


pg_user = "postgres"
pg_pwd = getpass.getpass("user 'postgres' password: ")


def fetch_data() -> None:
    if not path.exists("data/raw_verses.txt"):

        print("[+] Starting the webscraping process to create a database of verses...")
        verses = scrape_verses()
        verses = set(verses)
        print("[+] Saving the raw verses in 'raw_verses.txt'")
        with open("data/raw_verses.txt", "w") as f:
            f.write("\n".join(sorted(verses)))

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

        if (not analysed_verse.consonant_rhyme
            or not analysed_verse.assonant_rhyme):
            continue

        ready_verse = [
            i,
            verse,
            analysed_verse.syllables,
            analysed_verse.consonant_rhyme,
            analysed_verse.assonant_rhyme,
            analysed_verse.last_word,
            analysed_verse.beg,
            analysed_verse.int,
            analysed_verse.end,

        ]

        db_funcs.csv_file_appender(ready_verse)

    print("[+] Done analysing the verses. CSV File ready to use.")


def scrape_verses() -> List[str]:
    """Scraping Amediavoz and Buscapoemas"""
    urls_poets_amediavoz = scraping_amediavoz.getting_amediavoz_links()
    verses = scraping_amediavoz.getting_the_verses(urls_poets_amediavoz)

    # Scraping Buscapoemas
    urls_poets = scraping_buscapoemas.getting_poets()

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


def if_db():
    """First check if DB is created"""
    global pg_pwd

    try:
        if not db_funcs.check_if_user_exists(pg_user, pg_pwd):
            db_funcs.create_user(pg_user, pg_pwd)

    except:
        pg_pwd = getpass.getpass("Incorrect Password, try again: ")
        if not db_funcs.check_if_user_exists(pg_user, pg_pwd):
            db_funcs.create_user(pg_user, pg_pwd)

    if not db_funcs.check_if_db_exists(pg_user, pg_pwd):
        db_funcs.create_db(pg_user, pg_pwd)
        db_funcs.grant_access(pg_user, pg_pwd)

    if not db_funcs.check_if_table_exists():
        db_funcs.create_db_table()

    if (not path.exists("/home/nebur/Desktop/poemautomator/data/raw_verses.txt")
        or not path.exists("/home/nebur/Desktop/poemautomator/data/verses.txt")
        or not path.exists("/home/nebur/Desktop/poemautomator/data/verse_list.csv")
    ):

        db_funcs.delete_rows_from_table()
        fetch_data()
        db_funcs.import_csv_to_db(pg_user, pg_pwd)


def main() -> None:
    if_db()

    print("[+] Requirements satisfied. Starting the poem generator...", end="\n\n")
    poem_creator.create_poem()

    another = input("Would you like to create another poem? [Y/N]")
    if another.upper() == "Y":
        poem_creator.create_poem()

if __name__ == "__main__":
    main()
