import string


vowels = "aeiouáéíóúAEIOUÁÉÍÓÚ"
vowels_h = vowels + "h"
consonants = (
    "".join((letter for letter in string.ascii_letters if letter not in vowels)) + "ñÑ"
)
debiles = "UIui"
debiles_tonicas = "ÚÍúí"
fuertes = "AEOaeo"
fuertes_tildadas = "ÁÉÓáéó"
##############################
vowels_tildadas = "áéíóúÁÉÍÓÚ"
punct = "!\"#$%&'()*+,./:;<=>?@[\\]^_`{|}~"
capitals = string.ascii_uppercase


class Syllabifier:
    def __init__(self, sentence):
        self.sentence = sentence.strip(".,¿?¡!«'—»();:\"-* ")
        self.syllabified_sentence = self.syllabify(self.sentence)
        self.syllables, self.agullaesdr = self.counter(self.syllabified_sentence)
        self.consonant_rhyme, self.asonant_rhyme = self.rhymer(
            self.syllabified_sentence
        )
        self.beg = self.is_beg(sentence)
        self.end = self.is_end(sentence)
        self.int = self.is_int(sentence)

    def syllabify(self, sentence):
        block = ""
        syllabified_sentence = ""

        for i, letter in enumerate(sentence):
            block += letter
            if letter == " ":
                syllabified_sentence += block
                block = ""

            elif len(block) == 1 and letter in string.punctuation:
                syllabified_sentence += block
                block = ""

            elif letter in vowels:
                if len(block) == 1:
                    try:
                        if syllabified_sentence.strip()[-1] in vowels:
                            syllabified_sentence += block
                            block = ""
                        else:
                            syllabified_sentence += "-" + block
                            block = ""
                    except IndexError:
                        syllabified_sentence += "-" + block
                        block = ""

                elif len(block) == 2:
                    try:
                        if (
                            block[0] in "hH"
                            and syllabified_sentence.strip()[-1] in vowels
                            and (not sentence[i+1] in fuertes or sentence[i+1] in debiles_tonicas)
                        ):
                            syllabified_sentence += block
                            block = ""
                        else:
                            syllabified_sentence += "-" + block
                            block = ""
                    except IndexError:
                        syllabified_sentence += "-" + block
                        block = ""

                elif len(block) == 3:
                    if block[-2] in "rlhRLH":
                        syllabified_sentence += "-" + block
                        block = ""
                    else:
                        syllabified_sentence += block[0] + "-" + block[1:]
                        block = ""

                elif len(block) == 4:
                    if block[-2] in "rlhRLH":
                        syllabified_sentence += block[0] + "-" + block[1:]
                        block = ""
                    else:
                        syllabified_sentence += block[0:2] + "-" + block[2:]
                        block = ""

                elif len(block) == 5:
                    if block[-2] in "rlhRLH":
                        syllabified_sentence += block[0:2] + "-" + block[2:]
                        block = ""
                    else:
                        syllabified_sentence += block[0:3] + "-" + block[3:]
                        block = ""

            elif i == len(sentence) - 1 and (
                letter in consonants or letter in string.punctuation
            ):
                syllabified_sentence += letter

        return self.second_scan(syllabified_sentence.strip(".,!?¡¿:;"))

    def second_scan(self, sentence):
        separated_sentence = ""

        while sentence:
            try:
                cut_point = sentence.index("-", sentence.index("-") + 1)
                block = sentence[0:cut_point]
                sentence = sentence[cut_point:]
            except ValueError:
                block = sentence
                sentence = ""

            new_block = self.block_separator(block)
            separated_sentence += new_block

        return separated_sentence

    def block_separator(self, block):
        separated_block = ""

        block = block.strip("-")

        i = 0
        while True:
            try:
                letter = block[i]

                if letter not in vowels:
                    separated_block += letter
                    i += 1

                elif letter in vowels:
                    try:
                        if block[i + 1] not in vowels_h:
                            separated_block += letter
                            i += 1

                        elif block[i + 1] == "h":
                            try:
                                if block[i + 2] in vowels:
                                    vowel_block = self.vowel_separator(block[i : i + 3])
                                    separated_block += vowel_block
                                    i += 3
                                else:
                                    separated_block += block[i : i + 3]
                                    i += 3
                            except IndexError:
                                separated_block += letter
                                i += 1

                        else:
                            vowel_block = self.vowel_separator(block[i : i + 2])
                            separated_block += vowel_block
                            i += 2
                    except IndexError:
                        separated_block += letter
                        i += 1

            except IndexError:
                break

        return "-" + separated_block

    def vowel_separator(self, vowel_block):
        """Grupos de 2 o de 3 letras (VV / VHV / VVV)"""

        if "h" in vowel_block:
            vocal_uno = vowel_block[0]
            vocal_dos = vowel_block[2]
            if vocal_dos in fuertes or vowel_block[1] in debiles_tonicas:
                if vocal_uno in fuertes or vocal_uno in debiles_tonicas:
                    return vocal_uno + "-" + "h" + vocal_dos
                else:
                    return vowel_block
            else:
                return vowel_block

        else:
            if vowel_block[1] in fuertes or vowel_block[1] in debiles_tonicas:
                if vowel_block[0] in fuertes or vowel_block[0] in debiles_tonicas:
                    return vowel_block[0] + "-" + vowel_block[1]
                return vowel_block
            return vowel_block

    def counter(self, sentence):
        sil_count = sentence.count("-")
        cut_point = sentence.rfind(" ")
        if cut_point != -1:
            last_word = sentence[cut_point:]
            type = self.agu_lla_esdr(last_word.strip())
            return sil_count + type, type
        type = self.agu_lla_esdr(sentence)
        return sil_count + type, type

    def agu_lla_esdr(self, word):
        """Returns -1 if esdrújula
        0 if llana
        1 if aguda"""

        if not word.startswith("-"):
            word = "-" + word

        if word.count("-") == 1:
            return 1

        for i, letter in enumerate(word):
            if letter in vowels_tildadas:
                remaining = word.count("-", i)
                if remaining == 2:
                    # Esdrújula
                    return -1
                elif remaining == 1:
                    # Llana
                    return 0
                # Aguda
                return 1

        if word[-1] in vowels or word[-1] in "ns":
            return 0

        return 1

    def rhymer(self, verso):
        cut_point = verso.rfind(" ")

        if cut_point != -1:
            last_word = verso[cut_point:].strip()
            consonant_rhyme = self.consonant_rhyme_finder(
                last_word.strip(punct), self.agullaesdr
            )
            asonant_rhyme = self.asonant_rhyme_finder(
                last_word.strip(punct), self.agullaesdr
            )
            return consonant_rhyme, asonant_rhyme

        word = verso
        consonant_rhyme = self.consonant_rhyme_finder(
            word.strip(punct), self.agullaesdr
        )
        asonant_rhyme = self.asonant_rhyme_finder(consonant_rhyme)
        return consonant_rhyme, asonant_rhyme

    def consonant_rhyme_finder(self, last_word, agullaesdr):
        if not last_word.startswith("-"):
            last_word = "-" + last_word
        if agullaesdr == -1:
            # esdrújula
            while last_word.count("-") > 3:
                last_word = last_word[last_word.find("-", 1) :]
        elif agullaesdr == 0:
            # llana
            while last_word.count("-") > 2:
                last_word = last_word[last_word.find("-", 1) :]
        else:
            # aguda
            while last_word.count("-") > 1:
                last_word = last_word[last_word.find("-", 1) :]

        block_clean = "".join([letter for letter in last_word if letter != "-"])

        if len(block_clean) > 1 and not all(
            letter in capitals for letter in block_clean
        ):

            while block_clean[0] not in vowels:
                if len(block_clean) > 2:
                    if block_clean[0].lower() in "qg" and (
                            block_clean[1].lower() == "u" and (
                            block_clean[2].lower() in "ieíé")):
                        block_clean = block_clean[2:]

                    else:
                        block_clean = block_clean[1:]
                else:
                    block_clean = block_clean[1:]

            if (len(block_clean) > 1
                and block_clean[0] in debiles
                and block_clean[1] in fuertes
            ):
                block_clean = block_clean[1:]

        return block_clean

    def asonant_rhyme_finder(self, consonant_rhyme):
        asonant_rhyme = "".join([letter for letter in consonant_rhyme if letter in vowels])
        return asonant_rhyme

    def is_beg(self, sentence):
        if sentence.capitalize() == sentence:
            return True
        else:
            return False

    def is_end(self, sentence):
        if sentence.endswith("."):
            return True
        else:
            return False

    def is_int(self, sentence):
        if not sentence.endswith(".") and sentence[0].upper() != sentence[0]:
            return True
        else:
            return False


def main():
    sentence = input("Enter word/sentence to syllabify: ")
    syllabifier = Syllabifier(sentence)
    print("[+] Sentence:", syllabifier.sentence)
    print("[+] Syllabified sentence:", syllabifier.syllabified_sentence)
    print("[+] Syllables:", syllabifier.syllables)
    print("[+] Aguda, llana o esdrújula?:", syllabifier.agullaesdr)
    print("[+] Bloque consonante a rimar:", syllabifier.consonant_rhyme)
    print("[+] Bloque asonante a rimar:", syllabifier.asonant_rhyme)


if __name__ == "__main__":
    main()
