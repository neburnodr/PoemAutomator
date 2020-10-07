def cutting_the_long_verses(verse):
    new_verses_list = []

    sub_verses = verse.split(". ")
    for sub_verse in sub_verses:

        if sub_verse[0] == "¿" and sub_verse.count("?") == 0:
            sub_verse = sub_verse[1:]
        if sub_verse[0] == "¡" and sub_verse.count("!") == 0:
            sub_verse = sub_verse[1:]
        if sub_verse[0] == "\"" and sub_verse.count("\"") == 1:
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
        if sub_verse[-1] == "\"" and sub_verse.count("\"") == 1:
            sub_verse = sub_verse[:-1]
        if sub_verse[-1] == "!" and sub_verse.count("¡") == 0:
            sub_verse = sub_verse[:-1]
        if sub_verse[-1] == "?" and sub_verse.count("¿") == 0:
            sub_verse = sub_verse[:-1]

        if not sub_verse.endswith("."):
            new_verses_list.append(sub_verse + ".")
        else:
            new_verses_list.append(sub_verse)

    return new_verses_list


def recutting_the_still_long_verses(verse):
    new_verses_list = []

    sub_verses = verse.split(", ")

    for sub_verse in sub_verses:
        if sub_verse == sub_verses[-1]:
            new_verses_list.append(sub_verse)
        else:
            new_verses_list.append(sub_verse + ",")
