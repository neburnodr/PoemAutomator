# imports
import random
import string
import datetime
from os import path, mkdir
import sys
import argparse
from data.analyse_verses import Syllabifier, last_word_finder, decapitalize
from data.online_rhymer import Rhymer, getting_word_type, find_first_letter
from data.db_funcs import fetch_verses, fetch_rhyme
from typing import Tuple, List, Optional

Verse = Tuple[bool, bool, bool, str, str]
punct = string.punctuation + " ¡¿"
vowels = "aeiouáéíóúÁÉÍÓÚAEIOU"


class PoemAutomator:
    """Types of lines: beginnings (com), intermediate (int), endings (fin) to iterate through"""
    TYPES_VERSES = ["beg", "int", "end"]

    def __init__(self, num_ver: int, long_ver: int, rhy_seq: str) -> None:
        """User-defined variables"""
        self.num_verses = num_ver  # -> INT -> 7. Number of verses in the final poem
        self.long_verses = long_ver  # -> INT -> 8. Possibility RANGES in the FUTURE: 5-7 (5<=long<=7)
        self.rhy_seq = rhy_seq  # STR  -> "ABAB BABA" -> Each character is a RHYME_CODE. Space = emptyline

        self.verses_to_use = {}  # DICT -> {RHYME_CODE: TUPLE(verse, last_word, beg, int, end)} from DB
        self.rhymes_to_use = {}  # DICT -> {RHYME_CODE: str} -> Example: {A: "ado", B: "es"}
        self.words_used = {}  # DICT -> {RHYME_CODE: LIST[last_word, last_word], RHYME_CODE: LIST[last_word, etc]}

        for rhyme_code in rhy_seq:
            if rhyme_code != " ":
                self.rhymes_to_use[rhyme_code] = ""
                self.verses_to_use[rhyme_code] = []
                self.words_used[rhyme_code] = []

        self.rhymes()  # If the user wants to decide the concrete endings-to-rhyme
        self.poem = self.poem_random_generator()

    def rhymes(self) -> None:
        """Func to decide which path to follow -> self.decide_rhymes() or self.random_rhymes()"""
        self_decide = input("Quieres elegir las rimas? [Y/N]: ")

        if self_decide.capitalize().strip() == "Y":
            self.decide_rhymes()

        else:
            self.random_rhymes()

    def decide_rhymes(self) -> None:
        """Populates the rhymes_to_use dict if the user wants to decide the rhyme-endings beforehand"""
        for key in self.rhymes_to_use.keys():
            if key == key.upper():
                self.rhymes_to_use[key] = input(f"Rima consonante {key}: -")

                verses_to_use = fetch_verses(self.long_verses, self.rhymes_to_use[key], cons=True, unique=True)
                while not verses_to_use:
                    self.rhymes_to_use[key] = input(
                        f"La rima consonante que has especificado no existe en la base de datos. Prueba de nuevo: ")

                    verses_to_use = fetch_verses(self.long_verses, self.rhymes_to_use[key], cons=True, unique=True)

                self.verses_to_use[key] = verses_to_use

            else:
                self.rhymes_to_use[key] = input(f"Rima asonante {key}: -")

                verses_to_use = fetch_verses(self.long_verses, self.rhymes_to_use[key], cons=False, unique=True)
                while not verses_to_use:
                    self.rhymes_to_use[key] = input(
                        f"La rima asonante que has especificado no existe en la base de datos. Prueba de nuevo: ")

                    verses_to_use = fetch_verses(self.long_verses, self.rhymes_to_use[key], cons=False, unique=True)

                self.verses_to_use[key] = verses_to_use

    def random_rhymes(self) -> None:
        """If USER choose not to decide the rhymes the DICT gets populated by random rhymes"""
        for key in self.rhymes_to_use.keys():
            cons = True if key == key.upper() else False

            rhyme_to_use = fetch_rhyme(self.long_verses, self.rhy_seq.count(key), cons=cons)
            verses_to_use = fetch_verses(self.long_verses, rhyme_to_use, cons=cons, unique=True)
            while len(verses_to_use) < self.rhy_seq.count(key):
                rhyme_to_use = fetch_rhyme(self.long_verses, self.rhy_seq.count(key), cons=cons)
                verses_to_use = fetch_verses(self.long_verses, rhyme_to_use, cons=cons, unique=True)

            self.rhymes_to_use[key] = rhyme_to_use
            self.verses_to_use[key] = verses_to_use

    def poem_random_generator(self) -> str:
        poem = []

        for i, rhyme_code in enumerate(self.rhy_seq):
            if rhyme_code == " ":
                poem[-1] = poem[-1] + "\n"
                continue

            else:
                type_verse = self.type_determiner(poem)
                verse = self.select_verse_with_rhyme(rhyme_code, type_verse)

            poem.append(verse)

        return "\t" + "\n\t".join(poem)

    def select_verse_with_rhyme(self, rhyme_code: str, type_verse: int) -> str:
        verses = [verse for verse in self.verses_to_use[rhyme_code] if verse[type_verse]]

        try:
            verse = random.choice(verses)

        except IndexError:
            new_type = change_type(type_verse)
            verses = [verse for verse in self.verses_to_use[rhyme_code] if verse[new_type]]

            try:
                verse = random.choice(verses)
                self.delete_verse_from_verses_to_use(rhyme_code, verse)

                verse_text = changes_after_type_change(verse[3], type_verse, new_type)
                self.words_used[rhyme_code].append(verse[4])
                return verse_text

            except IndexError:
                type_str = "beg" if type_verse == 0 else "int" if type_verse == 1 else "end"
                rhyme_to_use_now = fetch_rhyme(self.long_verses, 10)
                verses = fetch_verses(self.long_verses,
                                      rhyme_to_use_now,
                                      type_verse=type_str)

                verse = random.choice(verses)  # This Verse is a random verse with anther rhyme.
                last_word = verse[4]  # The new word need the same number of syllables and the same type as this one.

                word_to_rhyme_with = random.choice(self.words_used[rhyme_code])
                rhy_type = "c" if rhyme_code.upper() == rhyme_code else "a"
                num_syll = Syllabifier(last_word).syllables
                last_word_type = getting_word_type(last_word)
                first_letter = find_first_letter(last_word)

                words_used = []
                for word_list in self.words_used.values():
                    for word in word_list:
                        words_used.append(word)

                new_word = online_rhyme_finder(word_to_rhyme_with,
                                               rhy_type,
                                               num_syll,
                                               last_word_type,
                                               first_letter,
                                               words_used)

                verse_last_word = last_word_finder(verse)
                verse_text = verse[3].replace(verse_last_word, new_word)

                self.words_used[rhyme_code].append(new_word)

                return verse_text

        self.delete_verse_from_verses_to_use(rhyme_code, verse)

        #  Add last_word to self.words_used and return the verse to poem_random_generator
        self.words_used[rhyme_code].append(verse[4])
        verse_text = verse[3]
        return verse_text

    def delete_verse_from_verses_to_use(self, rhyme_code: str, verse: Verse) -> None:
        verse_index = self.verses_to_use[rhyme_code].index(verse)
        del self.verses_to_use[rhyme_code][verse_index]

    def type_determiner(self, poem: List) -> int:
        """Returns 0, 1 or 2 depending on which kind of verse we need at each moment. The number stands for the index
        of 'beg', 'int' and 'end' in self.verses_to_use. Tuple(verse, last_word, beg, int, end)"""

        if len(poem) == 0:
            return 0

        elif len(poem) == self.num_verses - 1:
            return 2

        elif poem[-1].endswith("."):
            return 0

        else:
            return 1


def online_rhyme_finder(word: str,
                        rhyme_type: str,
                        syllables: int,
                        first_letter: Optional[str] = None,
                        word_type: Optional[str] = None,
                        words_used: Optional[List] = None) -> str:
        rhymes_object = Rhymer(word, rhyme_type, syllables, first_letter, word_type, words_used)
        rhymes_list = rhymes_object.getting_cronopista()

        if rhymes_list:
            new_word = random.choice(rhymes_list)
            return rhymes_list

        else:
            print("Yo que sé, joder")

def change_type(type_verse):
    """Possible solutions:
    1. Convert other kinds of lines into the one whe needs (com -> int, com -> fin etc.)
    3. Try RegEx for different but similar rhymes -> another script!
    4. Another length of verse -> maybe here after the other fail."""

    new_type = (type_verse + 1) % 2
    """  self.TYPES_VERSES = ["beg", "int", "end"]   
            'beg' -> 'int'
            'int' -> 'beg'
            'end' -> 'int'      """

    return new_type


def changes_after_type_change(verse, old_type, new_type):
    if new_type == 0:
        # new 'beg' -> old 'int'
        return decapitalize(verse, strict=False)

    elif new_type == 1 and old_type == 0:
        # new 'int' -> old 'beg'
        return verse.capitalize()

    # new 'int' -> old 'end'
    return verse.rstrip(string.punctuation) + "."


def save_poem(poem: str) -> None:
    now = datetime.datetime.now()

    abs_path = path.dirname(__file__)
    rel_path = "poemas/"
    _path = path.join(abs_path, rel_path)
    if not path.exists(_path):
        mkdir(_path)

    file_name = f"{_path}poema{now.strftime('%H:%M:%S_%d-%m-%Y')}.txt"

    with open(file_name, "w") as f:
        print(poem, file=f)


def getting_inputs() -> Tuple[int, int, str]:
    number_verses = input("Número de versos: ")
    while not number_verses.isdigit():
        number_verses = input(
            "La variable number_verses solo puede contener valores numéricos: "
        )

    number_verses = int(number_verses)

    size_verses = input("Longitud de los versos en sílabas: ")
    while not size_verses.isdigit():
        size_verses = input(
            "La variable size_verses solo puede contener valores numéricos: "
        )

    size_verses = int(size_verses)

    while not 3 < size_verses < 17:
        size_verses = int(
            input("La longitud de los versos ha de ser entre 4 y 16 sílabas: ")
        )

    rhyme_sequence = input("Secuencia de rimas (p.ej ABBA): ")
    while int(number_verses) != len([seq for seq in rhyme_sequence if seq != " "]):
        rhyme_sequence = input(
            "Secuencia de rimas (Debe ser igual de larga que el número de versos explicitado anteriormente): "
        )

    return number_verses, size_verses, rhyme_sequence


def parsing_arguments() -> Tuple[int, int, str]:
    parser = argparse.ArgumentParser()
    parser.add_argument("lines")
    parser.add_argument("longitud")
    parser.add_argument("sequence")
    args = parser.parse_args()
    num_verses = args.verses
    long_verses = args.longitud
    seq_rhymes = args.sequence
    return int(num_verses), int(long_verses), seq_rhymes


def create_poem():
    if len(sys.argv) == 1:
        num_ver, long_ver, rhy_seq = getting_inputs()
    else:
        num_ver, long_ver, rhy_seq = parsing_arguments()

    poem = PoemAutomator(num_ver, long_ver, rhy_seq)
    print(poem.poem)

    save = input("\nWould you like to save this poem? [Y/N]")
    if save.upper() == "Y":
        save_poem(poem.poem)

    another = input("Would you like to create another poem? [Y/N]")
    if another.upper() == "Y":
        create_poem()


if __name__ == "__main__":
    create_poem()
