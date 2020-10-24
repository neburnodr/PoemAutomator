from automator.poem_creator import online_rhyme_finder
from data.online_rhymer import getting_word_type


class TestOnlineRhymes:
    def test_one(self):
        assert getting_word_type("obtuso") == "0"
        assert online_rhyme_finder("majareta",
                                   "c",
                                   3,
                                   word_type="0",
                                   first_letter="true",
                                   words_used=["pandereta",
                                              "voltereta",
                                              "aleta",
                                              "atleta",
                                              "isleta",
                                              "inquieta",
                                              "escueta",
                                              "esteta",
                                              "asueta",
                                              "arqueta",
                                              "horqueta"]) == ["asceta",
                                                               "aceta",
                                                               "anfeta",
                                                               "agreta",
                                                               "ancheta",
                                                               "anqueta",
                                                               "arieta",
                                                               "eleta",
                                                               "excreta",
                                                               "haldeta",
                                                               "holgueta",
                                                               "olleta",
                                                               "oseta",
                                                               "uñeta"]


