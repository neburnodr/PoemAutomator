from automator import parsing_amediavoz
from automator import parsing_buscapoemas
from automator.processing_verses import cutting_the_long_verses, recutting_the_still_long_verses
from automator import db_funcs
from automator import poem_creator
from automator.analyse_verses import Syllabifier
from os import path


urls = ["http://amediavoz.com/indice-A-K.htm",
        "http://amediavoz.com/indice-L-Z.htm",
        "https://www.buscapoemas.net/poetas.html",
        ]


def get_verses():
    print("[+] Getting the poet urls from amediavoz.com")
    urls_poets_amediavoz = parsing_amediavoz.getting_amediavoz_links(urls[:2])
    print("[+] Done", end="\n\n")

    verses = parsing_amediavoz.getting_the_verses(urls_poets_amediavoz)
    print("[+] Done scraping amediavoz.com", end="\n\n")
    print("_____________________________________________________________", end="\n\n")

    urls_poems_buscapoemas = parsing_buscapoemas.getting_poems(urls[2])

    print("[+] Extracting the verses")
    for poem_url in urls_poems_buscapoemas:
        verses.extend(parsing_buscapoemas.getting_the_verses(poem_url))

    print("[+] Done", end="\n\n")

    return verses


def clean_verses(verses):
    print("[+] Processing the scraped verses")

    new_verses_list = []

    for verse in verses:

        if len(verse) < 50:
            new_verses_list.append(verse)

        else:
            cutted_verses = cutting_the_long_verses(verse)

            for cutted_verse in cutted_verses:

                if cutted_verse < 50:
                    new_verses_list.append(verse)

                else:
                    recutted_verses = recutting_the_still_long_verses(cutted_verse)

                    for recutted in recutted_verses:

                        if recutted < 50:
                            new_verses_list.append(recutted)

                        else:
                            pass

    print("[+] Done processing the verses", end="\n\n")
    return new_verses_list


def main():
    if db_funcs.check_if_db_exists():
        poem_creator.create_poem()

    else:
        db_funcs.create_db()
        db_funcs.create_db_table()

        verses = get_verses()
        cleaned_verses = clean_verses(verses)

        for i, verse in enumerate(cleaned_verses):

            print("[+] Analysing the verses and creating the CSV File.")
            analysed_verse = Syllabifier(verse)

            ready_verse = [i,
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


if __name__ == "__main__":
    main()
