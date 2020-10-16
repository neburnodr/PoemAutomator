from data.analyse_verses import Syllabifier
from random import randint


class Buscador:
    def __init__(self, num_syll, rhy, type):
        self.number_syllables = num_syll
        self.rhyme = rhy
        if 0 < type < 2:
            self.type = "com"
        elif type < 3:
            self.type = "int"
        else:
            self.type = "fin"

    def searcher(self):
        with open(f"/sil_{self.type}/{self.number_syllables}_{self.rhyme}.txt") as f:
            verses = f.read().split("\n")

        if len(verses) < 10:
            return verses

        else:
            verses_choice = []
            for i in range(10):
                verses_choice.append(verses.pop(randint(0, len(verses))))

            return verses_choice




