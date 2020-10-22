import re
from typing import List


def clean_verses(verses: List) -> List:
    print("[+] Processing the scraped verses...")

    new_verses_list = []

    for verse in verses:
        if len(verse) < 70:
            new_verses_list.append(verse)

    print("[+] Done processing the verses")
    return removing_junk(new_verses_list)


def removing_junk(verse_list: List) -> List:
    new_verse_list = []

    for verse in verse_list:
        verse = verse.strip("*/ ►").lstrip("?!»)],;:*.- ").rstrip("¿¡«([* ").strip()

        if len(verse) < 6:
            continue
        if re.search("([A-Z\W]{2,} [A-Z\W]{2,})", verse):
            continue
        if re.search("\d{4,}", verse):
            continue
        if re.search("Soneto \d+", verse):
            continue
        if re.search("pag. \d+", verse):
            continue
        if re.search("Proverbios, \d+", verse):
            continue

        if verse[0] == "¿" and verse.count("?") == 0:
            verse = verse[1:]
        if verse[0] == "¡" and verse.count("!") == 0:
            verse = verse[1:]
        if verse[0] == '"' and verse.count('"') == 1:
            verse = verse[1:]
        if verse[0] == "«" and verse.count("»") == 0:
            verse = verse[1:]
        if verse[0] == "(" and verse.count(")") == 0:
            verse = verse[1:]
        if verse[0] == "[" and verse.count("]") == 0:
            verse = verse[1:]
        if verse[-1] == ")" and verse.count("(") == 0:
            verse = verse[:-1]
        if verse[-1] == "]" and verse.count("[") == 0:
            verse = verse[:-1]
        if verse[-1] == "»" and verse.count("«") == 0:
            verse = verse[:-1]
        if verse[-1] == '"' and verse.count('"') == 1:
            verse = verse[:-1]
        if verse[-1] == "!" and verse.count("¡") == 0:
            verse = verse[:-1]
        if verse[-1] == "?" and verse.count("¿") == 0:
            verse = verse[:-1]
        if verse.count('"') % 2 != 0:
            verse = verse.strip('"')
        if (verse.startswith('"')
            and verse.endswith('"')
        ):
            verse = verse.strip('". -')

        new_verse_list.append(verse.lstrip(".").strip())

    return new_verse_list
