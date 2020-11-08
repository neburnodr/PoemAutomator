from data.processing_verses import removing_junk, clean_verses
from data.help_funcs import try_to_clean

junk_list = ["estos",
             "Alondras compartiendo amor",
             "LUIS ARRILLAGA (España, 1951)",
             "ANTÃ“N ARRUFAT (Cuba, 1935)",
             '( Perú, 1887 - 1966 )',
             "la pag. 34",
             "Proverbios, 34,25", ]


class TestRemovingJunk:
    def test_one(self):
        assert removing_junk(junk_list) == ["Alondras compartiendo amor"]


class TestCleanVerses:
    def test_two(self):
        assert try_to_clean(['De angustia lleno y doloroso asombro :',
                             '¿Será posible ?',
                             'esperanza infinita -,',
                             '( Cuerpo de agua en el cristal de un vaso )',
                             '"No juréis por la luna" .....',
                             '"Fontainebleau" .']) == ['De angustia lleno y doloroso asombro:',
                                                       '¿Será posible?',
                                                       'esperanza infinita,',
                                                       '(Cuerpo de agua en el cristal de un vaso)',
                                                       '"No juréis por la luna "...',
                                                       '" Fontainebleau".']
