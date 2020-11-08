from data.online_rhymer import Rhymer
from data.online_rhymer import getting_word_type


class TestRhymer:
    def test_one(self):
        assert getting_word_type("obtuso") == "0"

        word_type = getting_word_type("obtuso")

        rhymer = Rhymer("majareta",
                        "c",
                        3,
                        word_type=word_type,
                        first_letter="true",
                        words_to_discard=["pandereta",
                                          "voltereta",
                                          "aleta",
                                          "atleta",
                                          "isleta",
                                          "inquieta",
                                          "escueta",
                                          "esteta",
                                          "asueta",
                                          "arqueta",
                                          "horqueta"])

        assert rhymer.getting_cronopista() == ["asceta",
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
