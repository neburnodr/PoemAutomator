from data.processing_verses import removing_junk

junk_list = ["estos",
              "Alondras compartiendo amor",
              "LUIS ARRILLAGA (España, 1951)",
              "ANTÃ“N ARRUFAT (Cuba, 1935)",
              '( Perú, 1887 - 1966 )',
              "la pag. 34",
              "Proverbios, 34,25",]


class TestRemovingJunk:
    def test_one(self):

        assert removing_junk(junk_list) == ["Alondras compartiendo amor"]