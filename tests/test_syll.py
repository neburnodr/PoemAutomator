from data.analyse_verses import Syllabifier

class TestSyll:

    def test_one(self):
        sentence = "quiero quemarme así si así me miras,"
        syll = Syllabifier(sentence)
        assert syll.consonant_rhyme == "iras"
        assert syll.assonant_rhyme == "ia"

    def test_two(self):
        sentence = "Anatomía de la melancolía Alegra el corazón haber vivido,"
        syll = Syllabifier(sentence)
        assert syll.consonant_rhyme == "ido"
        assert syll.assonant_rhyme == "io"
        assert syll.syllables == 22

    def test_three(self):
        sentence = "si nos quemó la llama del vivir,"
        syll = Syllabifier(sentence)
        assert syll.consonant_rhyme == "ir"
        assert syll.assonant_rhyme == "i"
        assert syll.syllables == 11

    def test_four(self):
        sentence = "su huella es una herida hecha de orgullo"
        syll = Syllabifier(sentence)
        assert syll.consonant_rhyme == "uio"
        assert syll.assonant_rhyme == "uo"
        assert syll.syllables == 11

    def test_five(self):
        sentence = "y si no fue el amor, mi amor por ti"
        syll = Syllabifier(sentence)
        assert syll.consonant_rhyme == "i"
        assert syll.assonant_rhyme == "i"
        assert syll.syllables == 11

    def test_six(self):
        sentence = "gente"
        syll = Syllabifier(sentence)
        assert syll.consonant_rhyme == "ente"
        assert syll.assonant_rhyme == "ee"
        assert syll.syllables == 2

    def test_seven(self):
        sentence = "inútilmente"
        syll = Syllabifier(sentence)
        assert syll.consonant_rhyme == "ente"
        assert syll.assonant_rhyme == "ee"
        assert syll.syllables == 5

    def test_eight(self):
        sentence = "La amistad danza en torno a la Tierra y,"
        syll = Syllabifier(sentence)
        assert syll.consonant_rhyme == "errai"
        assert syll.assonant_rhyme == "ea"
        assert syll.syllables == 10

    def test_nine(self):
        sentence = "pero yo no puedo huir"
        syll = Syllabifier(sentence)
        assert syll.consonant_rhyme == "ir"
        assert syll.assonant_rhyme == "i"
        assert syll.syllables == 8

    def test_ten(self):
        sentence = "del huerto de fray Luis."
        syll = Syllabifier(sentence)
        assert syll.syllables == 7
        assert syll.assonant_rhyme == "i"
        assert syll.consonant_rhyme == "is"

    def test_elve(self):
        sentence = "plegándose en mi pubis."
        syll = Syllabifier(sentence)
        assert syll.consonant_rhyme == "ubis"
        assert syll.assonant_rhyme == "ui"
        assert syll.syllables == 7

    def test_twelve(self):
        sentence = "A este trabajo ruin."
        syll = Syllabifier(sentence)
        assert syll.consonant_rhyme == "in"
        assert syll.assonant_rhyme == "i"
        assert syll.syllables == 7
