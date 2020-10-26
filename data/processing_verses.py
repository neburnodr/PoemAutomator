import re
from typing import List


junk = "→*/►Â³=Ãâ¤§~²³°+"


def clean_verses(verses: List) -> List:
    print("[+] Processing the scraped verses...")

    new_verses_list = []

    for verse in verses:
        if len(verse) < 70:
            new_verses_list.append(verse)

    return removing_junk(new_verses_list)


def removing_junk(verse_list: List) -> List:
    verse_list = [v.strip(" " + junk).lstrip("?!»)],;:.-").rstrip("¿¡«([").strip(" " + junk) for v in verse_list]
    verse_list = list(filter(lambda v: len(v) > 6
                                       and not re.search("(\d+[-|.|/]\d+)|([-|.|/]\d+)|([,|;]\d+)", v)
                                       and not re.search("([A-Z\W]{2,} [A-Z\W]{2,})", v)
                                       and not re.search("\d{4,}", v)
                                       and not re.search("Proverbios, \d+", v)
                                       and not re.search("pag. \d+", v)
                                       and not re.search("Soneto", v)
                                       and not re.search("Versión", v)
                                       and not re.search("(Lucas \d|Juan \d|Mateo \d|Juan \d)", v)
                                       and not re.search("página \d+", v)
                                       and not re.search("(\[\d+])$", v)
                                       and not re.search("(\w[XVILD]+)", v)
                                       and not re.search("Este soneto forma", v),
                             verse_list)
                      )

    new_verse_list = []

    for verse in verse_list:
        if "ç" in verse or "Ç" in verse:
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
        if verse.startswith('"') and verse.endswith('"'):
            verse = verse.strip('"')

        matches_compiled = [re.compile("( \d{2,3}$)"),
                            re.compile("(\s\[...])"),
                            re.compile("(\s+\(\d+\))"),
                            re.compile("(\[\d+])"),
                            ]

        for pattern in matches_compiled:
            match = re.search(pattern, verse)
            if match:
                verse = verse.replace(match.group(1), "")

        match = re.search("(\s{2,})", verse)
        if match:
            verse = verse.replace(match.group(1), " ")

        matches = re.findall(f"([{junk}])", verse)
        if matches:
            for match in matches:
                verse = verse.replace(match, "")

        verse = verse.strip(" " + junk).lstrip("?!»)],;:.-").rstrip("¿¡«([").strip(" " + junk)

        new_verse_list.append(verse)

    print("[+] Done processing the verses")
    return new_verse_list
