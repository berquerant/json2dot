from typing import TypeVar
from unittest import TestCase

import json2dot.ranking as ranking

K = TypeVar("K")


class TestRanking(TestCase):
    def test_ranking_str(self):
        data = {
            "b": 2,
            "c": 3,
            "a": 1,
            "d": 4,
        }
        want_elems = [
            ranking.RankingElement(key="d", value=4, place=1, percentile=25, value_percentile=40),
            ranking.RankingElement(key="c", value=3, place=2, percentile=50, value_percentile=70),
            ranking.RankingElement(key="b", value=2, place=3, percentile=75, value_percentile=90),
            ranking.RankingElement(key="a", value=1, place=4, percentile=100, value_percentile=100),
        ]
        got = ranking.Ranking.build(data)
        self.assertEqual(len(want_elems), len(got.elems))
        for i, w in enumerate(want_elems):
            g = got.elems[i]
            self.assert_ranking_element(w, g)

    def assert_ranking_element(self, want: ranking.RankingElement[K], got: ranking.RankingElement[K]):
        self.assertEqual(want.key, got.key)
        self.assertEqual(want.value, got.value)
        self.assertEqual(want.place, got.place)
        self.assertAlmostEqual(want.percentile, got.percentile)
        self.assertAlmostEqual(want.value_percentile, got.value_percentile)
