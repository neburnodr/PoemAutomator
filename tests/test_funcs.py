from data.processing_verses import recutting_the_still_long_verses as recut



class TestRecutting:

    def test_one(self):
        assert recut("Los niños, que iban descalzos por la arena, por la mañana tenían sed de sangre, "
                     "por la tarde de cobre y por la noche lloraban.") == (["Los niños,",
                                                                            "que iban descalzos por la arena,",
                                                                            "por la mañana tenían sed de sangre,",
                                                                            "por la tarde de cobre y por la noche lloraban."])

        assert recut(",Los niños,,muertos de hambres,.,") == ([",Los niños,,muertos de hambres,.,"])