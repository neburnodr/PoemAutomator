import re
from typing import List
from string import punctuation
from os import path, mkdir

from data.help_funcs import delete_captures_within_matches

junk = "→*/►◄←‹><Â=Ãâ¤§~º¹²³°+…¯”“·"


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
                                       and not re.search("Este soneto forma", v)
                                       and not re.search("\d\.", v)
                                       and not all([letter in punctuation for letter in v]),
                             verse_list)
                      )

    new_verse_list = []

    for verse in verse_list:
        if "ç" in verse or "Ç" in verse:
            save_verse(verse, "Ç_versos")
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
        if verse.count("—") == 1:
            verse.replace("—", "")
        if verse[-1] == "!" and verse.count("¡") == 0:
            verse = verse[:-1]
        if verse[-1] == "?" and verse.count("¿") == 0:
            verse = verse[:-1]
        if verse.count("¡") - verse.count("!") == 1:
            verse = verse + "!"
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

        if len(verse) < 6:
            save_verse(verse, "pequeños")
            continue

        match = re.search("[a-zA-Z]+(\d+)", verse)
        if match:
            verse = verse.replace(match.group(1), "")

        match = re.search("([\.,]){4,}", verse)
        if match:
            verse = verse.replace(match.group(0), "...")

        match = re.search("(( )+[?!.,:»;]+)", verse)
        if match:
            empty_space = match.group(2)
            replacement = match.group(0).replace(empty_space, "")
            verse = verse.replace(match.group(0), replacement)

        match = re.findall(",\w", verse)
        if match:
            for m in match:
                repl = m[0] + " " + m[1]
                verse = verse.replace(m, repl)

        match = re.findall("(\.{3}[a-zA-Z])", verse)
        if match:
            for m in match:
                repl = m[0:3] + " " + m[-1]
                verse = verse.replace(m, repl)

        match = re.findall("(\.{1}[a-z])", verse)
        if match:
            for m in match:
                repl = " " + m[-1]
                verse = verse.replace(m, repl)


        new_verse_list.append(verse)

    print("[+] Done processing the verses")
    return new_verse_list


def save_verse(verse, name):
    if not path.exists("data/versos_desechados"):
        mkdir("data/versos_desechados")

    with open(f"data/versos_desechados/{name}.txt", "a") as f:
        print(verse, file=f)
