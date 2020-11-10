from data.processing_verses import removing_junk

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
        assert removing_junk(['De angustia lleno y doloroso asombro :',
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

    def test_three(self):
        assert removing_junk(['1, 15... y su voz como ruido de muchas aguas.',
                              '1, 16... y de su boca salía una espada aguda de dos filos.',
                              '13, 39... y la siega es el fin del mundo...',
                              '14, 2 Y oí una voz del cielo como ruido de muchas aguas...',
                              '15, 2 Y vi así como un mar de vidrio mezclado con fuego...',
                              '2, 2 Yo sé tus obras, y tu trabajo, y paciencia...',
                              '2, 23... y daré a cada uno de vosotros según sus obras.',
                              '2, 28 Y le daré la estrella de la mañana.',
                              '2, 7... Al que venciere, daré a comer del árbol de la vida...',
                              'Lc. 11, 5']) == ['... y su voz como ruido de muchas aguas.',
                                                '... y de su boca salía una espada aguda de dos filos.',
                                                '... y la siega es el fin del mundo...',
                                                'Y oí una voz del cielo como ruido de muchas aguas...',
                                                'Y vi así como un mar de vidrio mezclado con fuego...',
                                                'Yo sé tus obras, y tu trabajo, y paciencia...',
                                                '... y daré a cada uno de vosotros según sus obras.',
                                                'Y le daré la estrella de la mañana.',
                                                '... Al que venciere, daré a comer del árbol de la vida...']
