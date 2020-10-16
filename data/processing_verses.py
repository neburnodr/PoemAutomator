def clean_verses(verses):
    print("[+] Processing the scraped verses...")

    new_verses_list = []

    for verse in verses:

        if len(verse) < 60:
            new_verses_list.append(verse)

        else:
            cutted_verses = cutting_the_long_verses(verse)

            for cutted_verse in cutted_verses:

                if len(cutted_verse) < 60:
                    new_verses_list.append(cutted_verse)

                else:
                    recutted_verses = recutting_the_still_long_verses(cutted_verse)

                    for recutted in recutted_verses:

                        if len(recutted) < 70:
                            new_verses_list.append(recutted)

                        else:
                            pass

    print("[+] Done processing the verses", end="\n\n")
    return removing_junk(new_verses_list)


def cutting_the_long_verses(verse):
    new_verses_list = []

    sub_verses = verse.split(".")
    for sub_verse in sub_verses:
        sub_verse = sub_verse.strip()

        if len(sub_verse) < 5:
            continue

        if sub_verse[0] == "¿" and sub_verse.count("?") == 0:
            sub_verse = sub_verse[1:]
        if sub_verse[0] == "¡" and sub_verse.count("!") == 0:
            sub_verse = sub_verse[1:]
        if sub_verse[0] == '"' and sub_verse.count('"') == 1:
            sub_verse = sub_verse[1:]
        if sub_verse[0] == "«" and sub_verse.count("»") == 0:
            sub_verse = sub_verse[1:]
        if sub_verse[0] == "(" and sub_verse.count(")") == 0:
            sub_verse = sub_verse[1:]
        if sub_verse[0] == "[" and sub_verse.count("]") == 0:
            sub_verse = sub_verse[1:]
        if sub_verse[-1] == ")" and sub_verse.count("(") == 0:
            sub_verse = sub_verse[:-1]
        if sub_verse[-1] == "]" and sub_verse.count("[") == 0:
            sub_verse = sub_verse[:-1]
        if sub_verse[-1] == "»" and sub_verse.count("«") == 0:
            sub_verse = sub_verse[:-1]
        if sub_verse[-1] == '"' and sub_verse.count('"') == 1:
            sub_verse = sub_verse[:-1]
        if sub_verse[-1] == "!" and sub_verse.count("¡") == 0:
            sub_verse = sub_verse[:-1]
        if sub_verse[-1] == "?" and sub_verse.count("¿") == 0:
            sub_verse = sub_verse[:-1]

        if (
            isinstance(sub_verses, list)
            and len(sub_verses) > 1
            and sub_verse != sub_verses[-1].strip()
        ):
            new_verses_list.append(sub_verse + ".")
        else:
            new_verses_list.append(sub_verse)

    return removing_junk(new_verses_list)


def recutting_the_still_long_verses(verse):
    new_verses_list = []

    sub_verses = verse.split(",")

    for sub_verse in sub_verses:
        sub_verse = sub_verse.strip()

        if sub_verse == sub_verses[-1].strip():
            new_verses_list.append(sub_verse)
        else:
            new_verses_list.append(sub_verse + ",")

    return removing_junk(new_verses_list)


def removing_junk(verse_list):
    new_verse_list = []

    for verse in verse_list:
        if verse and len(verse) > 5:
            new_verse_list.append(verse)

    return new_verse_list
