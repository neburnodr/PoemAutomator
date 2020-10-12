from data.processing_verses import recutting_the_still_long_verses as recut

some_long_verses = ["Esto puedes sentirlo cuando te extiendes sobre la tierra, boca arriba, y tu pelo penetra como un manojo de raíces, y toda tú eres un tronco caído",
                    "Y se tergiversan nociones que no deben ser tergiversadas porque son verdad en el plano que les corresponde, que es el de la experiencia sensorial",
                    "Según yo estaba en un lugar seguro llamado 'cuneta', pero nunca olvidaré la mirada de satisfacción del conductor, que hasta se ladeó con tal de centrarme",
                    ]

class TestRecutting:

    def test_one(self):
        assert recut("Los niños, que iban descalzos por la arena, por la mañana tenían sed de sangre, "
                     "por la tarde de cobre y por la noche lloraban.") == (["Los niños,",
                                                                            "que iban descalzos por la arena,",
                                                                            "por la mañana tenían sed de sangre,",
                                                                            "por la tarde de cobre y por la noche lloraban."])

        assert recut(",Los niños,,muertos de hambres,.,") == (["Los niños,","muertos de hambres,"])

        assert recut(some_long_verses[0]) == (["Esto puedes sentirlo cuando te extiendes sobre la tierra,", "boca arriba,", "y tu pelo penetra como un manojo de raíces,", "y toda tú eres un tronco caído"])
