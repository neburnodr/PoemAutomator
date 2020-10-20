# imports
import random
import string
import datetime
from os import path
import sys
import re
import argparse
from data.analyse_verses import Syllabifier
from data.online_rhymer import Rhymer


punct = string.punctuation + " ¡¿"
vowels = "aeiouáéíóúÁÉÍÓÚAEIOU"


class PoemAutomator:
    """Types of lines: beginnings (com), intermediate (int), endings (fin)
    To iterate through"""
    TYPES_VERSES = ["int", "com", "fin"]

    def __init__(self, num_ver, long_ver, rhy_seq):
        """User-defined variables"""
        self.num_verses = int(num_ver)
        self.long_verses = int(long_ver)
        self.rhy_seq = rhy_seq

        """Dict of rhymes to use.
        The keys are the code associated with the rhyme (A/B or 1/2 or whatever)
        the values will later be the concrete fragment-to-rhyme"""
        self.rhymes_to_use = {}

        """words_used is a list that'll make sure that no word that ends a verse will repeat itself at the end of 
        another verse """
        self.words_used = {}

        for rhyme in rhy_seq:
            if rhyme != " ":
                self.rhymes_to_use[rhyme] = ""
                self.words_used[rhyme] = []

        """verses_used differs from the variable poem in the way that poem can have it's lines manipulated
        verses_used on the contrary saves the lines used as they're in the database"""
        self.verses_used = []

        """If the user wants to decide the concrete endings-to-rhyme"""
        self.decide_rhyme()

        self.poem = self.poem_random_generator()

    def poem_random_generator(self):
        poem = []

        for i, rhyme in enumerate(self.rhy_seq):
            if rhyme == " ":
                poem.append("")
                continue

            elif not self.rhymes_to_use[rhyme]:
                type_verse = self.type_of_verse(poem)

                rhyme_block_to_use = ""
                while rhyme_block_to_use in self.rhymes_to_use.values():
                    verse = self.select_verse_without_rhyme(type_verse)
                    verse_analyzed = Syllabifier(verse)
                    rhyme_block_to_use = verse_analyzed.consonant_rhyme

                self.rhymes_to_use[rhyme] = rhyme_block_to_use

            else:
                rhyme_block = self.rhymes_to_use[rhyme]
                type_verse = self.type_of_verse(poem)

                verse = self.select_verse_with_rhyme(rhyme_block, type_verse)

                counter = 0
                while not self.is_valid(verse):
                    verse = self.select_verse_with_rhyme(rhyme_block, type_verse)
                    counter += 1

                    if counter == 20:
                        verse = self.alternative_verse_selecting_method(
                            rhyme_block, type_verse
                        )
                        break

            poem.append(verse.strip(")("))
            last_word = last_word_finder(verse)
            self.words_used[rhyme].append(last_word.strip(punct))
            self.verses_used.append(decapitalize(verse.strip(punct)))

        return "\t" + "\n\t".join(poem)

    def select_verse_with_rhyme(self, block_to_rhyme, type_of_verse, cut=False):
        if cut:
            with open(
                f"sil_{type_of_verse}/{self.long_verses}_{block_to_rhyme}.txt",
                "r",
                encoding="UTF-8",
            ) as f:
                verses = f.read().split("\n")

            filtered_verses = [
                verse
                for verse in verses
                if not last_word_finder(verse) not in self.words_used[block_to_rhyme]
            ]

            if not filtered_verses:
                verse = self.alternative_verse_selecting_method(
                    block_to_rhyme, type_of_verse
                )
                return verse
            else:
                verse = random.choice(filtered_verses)
                return verse

        else:
            try:
                with open(
                    f"sil_{type_of_verse}/{self.long_verses}_{block_to_rhyme}.txt",
                    "r",
                    encoding="UTF-8",
                ) as f:
                    verses = f.read().split("\n")

                verse = random.choice(verses)
                return verse

            except FileNotFoundError:
                index_verses = self.TYPES_VERSES.index(type_of_verse)
                new_type_of_verse = self.TYPES_VERSES[(index_verses + 1) % 2]

                try:
                    with open(
                        f"sil_{new_type_of_verse}/{self.long_verses}_{block_to_rhyme}.txt"
                    ) as f:
                        verses = f.read().split("\n")

                    verse = random.choice(verses)

                    while verse == "":
                        verse = random.choice(verses)

                    if index_verses == 0:
                        return verse.capitalize()

                    elif index_verses == 1:
                        return decapitalize(verse)

                    return decapitalize(verse) + "."

                except FileNotFoundError:
                    last_word = last_word_finder(verse)
                    new_last_word = self.online_rhyme_dict(
                        last_word, words_used=self.words_used[block_to_rhyme]
                    )
                    verse.replace(last_word, new_last_word)
                    return verse

    def select_verse_without_rhyme(self, type_verse):
        try:
            with open(f"{self.long_verses}_sil_{type_verse}.txt") as f:
                verses = f.read().split("\n")

            verse = random.choice(verses)
            while verse == "":
                verse = random.choice(verses)

            return verse

        except FileNotFoundError:
            index_verses = self.TYPES_VERSES.index(type_verse)
            type_verse_new = self.TYPES_VERSES[(index_verses + 1) % 2]

            try:
                with open(f"{self.long_verses}_sil_{type_verse_new}.txt") as f:
                    verses = f.read().split("\n")

                verse = random.choice(verses)
                while verse == "":
                    verse = random.choice(verses)

                if index_verses == 0:
                    return verse.capitalize()

                elif index_verses == 1:
                    return decapitalize(verse)

                return decapitalize(verse) + "."

            except FileNotFoundError:
                print(
                    "Hasta aquí hemos llegado -> final de la func select_verse_without_rhyme"
                )

    def type_of_verse(self, poem):
        """Returns 'com', 'int' or 'fin' depending on which kind of verse we need at each time"""
        if len(poem) == 0:
            return "com"

        elif len(poem) == self.num_verses - 1:
            return "fin"

        elif poem[-1].endswith("."):
            return "com"

        else:
            return "int"

    def alternative_verse_selecting_method(self, rhyme_block, type_verse):
        """This method is to deal with the absence of enough lines of a certain type after running is_valid
        several times.

        Possible solutions:
        - (FOR ME) -> expand DB
        1. Convert other kinds of lines into the one whe needs (com -> int, com -> fin etc.)
        2. find possible words to replace the final with ( needs another DB ) -> online? create other script!
        3. Try RegEx for different but similar rhymes -> another script!
        4. Another length of verse -> maybe here after the other fail."""

        index_verses = self.TYPES_VERSES.index(type_verse)
        new_type_verse = self.TYPES_VERSES[(index_verses + 1) % 2]
        """     'int' -> 'com'
                'com' -> 'int'
                'fin' -> 'com'      """

        verse = self.select_verse_with_rhyme(rhyme_block, new_type_verse)

        counter = 0
        while not self.is_valid(verse):
            verse = self.select_verse_with_rhyme(rhyme_block, new_type_verse)
            counter += 1

            if rhyme_block == "y":
                rhyme_block = "í"

            if counter == 10:
                last_word = last_word_finder(verse)
                new_last_word = self.online_rhyme_dict(
                    last_word, words_used=self.words_used[rhyme_block]
                )  # puede dar NONE -> Investigar
                while decapitalize(verse.strip(punct)) in self.verses_used:
                    verse = self.select_verse_with_rhyme(rhyme_block, type_verse)

                new_verse = verse.replace(last_word, new_last_word)

                if type_verse == "fin":
                    return new_verse + "."
                return new_verse

        if index_verses == 0:
            # 'com' -> 'int'
            return decapitalize(verse, strict=False)

        elif index_verses == 1:
            # 'int' -> 'com'
            return verse.capitalize()

        return decapitalize(verse, strict=False) + "."

    def online_rhyme_dict(self, word, words_used=[]):
        syllabyfied_word = Syllabifier(word)
        syllables = syllabyfied_word.syllables
        rhymes_object = Rhymer(word, syllables, words_used)
        new_word = rhymes_object.rhyme

        if new_word is None:
            rhymes_object = Rhymer(word, syllables="I", words_to_discard=words_used)
            new_word = rhymes_object.rhyme

        return new_word

    def is_valid(self, verse):
        """Method that discards invalid lines either the verse is empty or the verse/last_word is already used"""
        last_word = last_word_finder(verse)

        if last_word in self.words_used:
            return False

        if verse == "":
            return False

        if decapitalize(verse.strip(punct)) in self.verses_used:
            return False

        return True

    def decide_rhyme(self) -> None:
        """Populates the rhymes_to_use dict if the user wants to decide the rhyme-endings beforehand"""
        self_decide = input("Quieres elegir las rimas? [Y/N]: ")

        if self_decide.capitalize().strip() == "Y":
            for key in self.rhymes_to_use.keys():
                self.rhymes_to_use[key] = input(f"Rima {key}: ")
                while not path.exists(f"./sil_int/{self.long_verses}_{self.rhymes_to_use[key]}.txt"):
                    self.rhymes_to_use[key] = input(
                        f"La rima que has especificado no existe en la base de datos. Prueba de nuevo: "
                    )


def decapitalize(strg, strict=True):
    if strict:
        return strg.lower()
    return strg[0].lower() + strg[1:]


def last_word_finder(sentence):
    if sentence.count(" ") != 0:
        return decapitalize(sentence[sentence.rfind(" "):].strip(punct))

    return decapitalize(sentence.strip(punct))


def save_poem(poem):
    now = datetime.datetime.now()

    abs_path = path.dirname(__file__)
    rel_path = "poemas/"
    _path = path.join(abs_path, rel_path)
    file_name = f"{_path}poema{now.strftime('%H:%M:%S_%d-%m-%Y')}.txt"

    with open(file_name, "w") as f:
        print(poem, file=f)


def getting_inputs():
    number_verses = input("Número de versos: ")
    while not number_verses.isdigit():
        number_verses = input(
            "La variable number_verses solo puede contener valores numéricos: "
        )

    size_verses = input("Longitud de los versos en sílabas: ")
    while not size_verses.isdigit():
        size_verses = input(
            "La variable size_verses solo puede contener valores numéricos: "
        )

    size_verses = int(size_verses)
    while not 3 < size_verses < 15:
        size_verses = int(
            input("La longitud de los versos ha de ser entre 4 y 14 sílabas: ")
        )

    rhyme_sequence = input("Secuencia de rimas (p.ej ABBA): ")
    while int(number_verses) != len([seq for seq in rhyme_sequence if seq != " "]):
        rhyme_sequence = input(
            "Secuencia de rimas (Debe ser igual de larga que el número de versos explicitado anteriormente): "
        )

    return number_verses, size_verses, rhyme_sequence


def parsing_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("lines")
    parser.add_argument("longitud")
    parser.add_argument("sequence")
    args = parser.parse_args()
    num_verses = args.verses
    long_verses = args.longitud
    seq_rhymes = args.sequence
    return num_verses, long_verses, seq_rhymes


def create_poem():
    pass


def main():
    if len(sys.argv) == 1:
        num_ver, long_ver, rhy_seq = getting_inputs()
    else:
        num_ver, long_ver, rhy_seq = parsing_arguments()

    poem = PoemAutomator(num_ver, long_ver, rhy_seq)
    print(poem.poem)

    print("")
    save = input("Would you like to save this poem? [Y/N]")
    if save.capitalize() == "Y":
        save_poem(poem.poem)


if __name__ == "__main__":
    main()
