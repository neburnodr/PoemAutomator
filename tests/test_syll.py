from data.analyse_verses import Syllabifier

class TestSyll:
    def test_one(self):
        assert Syllabifier("quiero quemarme así si así me miras,").asonant_rhyme == "ia"

    def test_two(self):
        assert Syllabifier("Anatomía de la melancolía Alegra el corazón haber vivido,").asonant_rhyme == "io"


