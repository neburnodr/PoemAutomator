from data import parsing_amediavoz, parsing_buscapoemas, db_funcs
from data.processing_verses import clean_verses
from data.analyse_verses import Syllabifier
from automator import poem_creator

urls = [
    "http://amediavoz.com/indice-A-K.htm",
    "http://amediavoz.com/indice-L-Z.htm",
    "https://www.buscapoemas.net/poetas.html",
]


def fetch_data():
    print("[+] Starting the webscraping process to create a database of verses...")

    verses = get_verses()
    cleaned_verses = clean_verses(verses)

    print("[+] Analysing the verses and creating the CSV File.")
    for i, verse in enumerate(cleaned_verses):

        analysed_verse = Syllabifier(verse)

        ready_verse = [
            i,
            verse,
            analysed_verse.syllables,
            analysed_verse.consonant_rhyme,
            analysed_verse.asonant_rhyme,
            analysed_verse.beg,
            analysed_verse.end,
            analysed_verse.int,
        ]

        db_funcs.csv_file_creator(ready_verse)

    print("[+] Done analysing the verses. CSV File ready to use.")


def get_verses():
    print("[+] Getting the poet urls from amediavoz.com")
    urls_poets_amediavoz = parsing_amediavoz.getting_amediavoz_links(urls[:2])
    print("[+] Done", end="\n\n")

    verses = parsing_amediavoz.getting_the_verses(urls_poets_amediavoz)
    print("[+] Done scraping amediavoz.com", end="\n\n")
    print("_____________________________________________________________", end="\n\n")

    urls_poems_buscapoemas = parsing_buscapoemas.getting_poems(urls[2])

    print("")
    print("[+] Extracting the verses")
    for poem_url in urls_poems_buscapoemas:
        print("[+] Extracting {}".format(poem_url))
        verses.extend(parsing_buscapoemas.getting_the_verses(poem_url))

    print("[+] Done", end="\n\n")

    return verses


def main():
    if db_funcs.check_if_db_exists():

        if db_funcs.check_if_table_exists():

            print(
                "[+] Requirements satisfied. Starting the poem generator...", end="\n\n"
            )
            poem_creator.create_poem()

        else:

            db_funcs.create_db_table()

            fetch_data()

            print(
                "[+] Requirements satisfied. Starting the poem generator...", end="\n\n"
            )
            poem_creator.create_poem()

    else:
        db_funcs.create_db()

        db_funcs.create_db_table()

        fetch_data()

        poem_creator.create_poem()


if __name__ == "__main__":
    main()
