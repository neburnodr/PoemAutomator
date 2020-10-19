from data.analyse_verses import Syllabifier

class TestSyll:

    def test_one(self):
        sentence = "quiero quemarme así si así me miras,"
        syll = Syllabifier(sentence)
        assert syll.consonant_rhyme == "iras"
        assert syll.asonant_rhyme == "ia"

    def test_two(self):
        assert Syllabifier("Anatomía de la melancolía Alegra el corazón haber vivido,").asonant_rhyme == "io"

    def test_three(self):
        sentence = "si nos quemó la llama del vivir,"
        syll = Syllabifier(sentence)
        assert syll.consonant_rhyme == "ir"
        assert syll.asonant_rhyme == "i"
        assert syll.syllables == 11

    def test_four(self):
        sentence = "su huella es una herida hecha de orgullo"
        syll = Syllabifier(sentence)
        assert syll.consonant_rhyme == "ullo"
        assert syll.asonant_rhyme == "uo"
        assert syll.syllables == 11

    def test_five(self):
        sentence = "y si no fue el amor, mi amor por ti"
        syll = Syllabifier(sentence)
        assert syll.consonant_rhyme == "i"
        assert syll.asonant_rhyme == "i"
        assert syll.syllables == 11

    def test_six(self):
        sentence = "gente"
        syll = Syllabifier(sentence)
        assert syll.consonant_rhyme == "ente"
        assert syll.asonant_rhyme == "ee"
        assert syll.syllables == 2

    def test_seven(self):
        sentence = "inútilmente"
        syll = Syllabifier(sentence)
        assert syll.consonant_rhyme == "ente"
        assert syll.asonant_rhyme == "ee"
        assert syll.syllables == 5

    def test_eight(self):
        sentence = "La amistad danza en torno a la Tierra y,"
        syll = Syllabifier(sentence)
        assert syll.consonant_rhyme == "ai"
        assert syll.asonant_rhyme == "ai"
        assert syll.syllables == 11
