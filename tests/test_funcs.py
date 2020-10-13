from data.processing_verses import cutting_the_long_verses as cut
from data.processing_verses import recutting_the_still_long_verses as recut
from data.processing_verses import clean_verses as clean

some_long_verses = [
    "Esto puedes sentirlo cuando te extiendes sobre la tierra, boca arriba, y tu pelo penetra como un manojo de raíces, y toda tú eres un tronco caído",
    "Y se tergiversan nociones que no deben ser tergiversadas porque son verdad en el plano que les corresponde, que es el de la experiencia sensorial",
    "Según yo estaba en un lugar seguro llamado 'cuneta', pero nunca olvidaré la mirada de satisfacción del conductor, que hasta se ladeó con tal de centrarme",
]


class TestCutting:
    def test_one(self):
        assert cut("ante tu golpe fiero. Cuerpo a cuerpo, en la noche,") == (
            ["ante tu golpe fiero.", "Cuerpo a cuerpo, en la noche,"]
        )


class TestRecutting:
    def test_one(self):
        assert recut(
            "Los niños, que iban descalzos por la arena, por la mañana tenían sed de sangre, "
            "por la tarde de cobre y por la noche lloraban."
        ) == (
            [
                "Los niños,",
                "que iban descalzos por la arena,",
                "por la mañana tenían sed de sangre,",
                "por la tarde de cobre y por la noche lloraban.",
            ]
        )

    def test_two(self):
        assert recut(",Los niños,,muertos de hambres,.,") == (
            ["Los niños,", "muertos de hambres,"]
        )

    def test_three(self):
        assert recut(some_long_verses) == (
            [
                "Esto puedes sentirlo cuando te extiendes sobre la tierra,",
                "boca arriba,",
                "y tu pelo penetra como un manojo de raíces,",
                "y toda tú eres un tronco caído",
                "Y se tergiversan nociones que no deben ser tergiversadas porque son verdad en el plano que les corresponde," 
                "que es el de la experiencia sensorial",
                "Según yo estaba en un lugar seguro llamado 'cuneta',",
                "pero nunca olvidaré la mirada de satisfacción del conductor,",
                "que hasta se ladeó con tal de centrarme",
            ]
        )


class TestClean:
    def test_one(self):
        assert (
            clean(
                [
                    "ante tu golpe fiero. Cuerpo a cuerpo, en la noche,",
                    """Los vientos del alba son feos. y las mentes de los céfiros, 
                      doblegadas por las bañeras, aumentan sus tormentos. Mañana""",
                ]
            )
            == (
                [
                    "ante tu golpe fiero.",
                    "Cuerpo a cuerpo, en la noche,",
                    "Los vientos del alba son feos.",
                    "y las mentes de los céfiros,",
                    "doblegadas por las bañeras,",
                    "aumentan sus tormentos.",
                    "Mañana",
                ]
            )
        )
