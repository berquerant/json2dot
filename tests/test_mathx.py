from unittest import TestCase

import json2dot.mathx as mathx


class TestMathx(TestCase):
    def test_clamp(self):
        cases = [
            (
                mathx.Clamp.new(0, 10),
                1,
                1,
            ),
            (
                mathx.Clamp.new(0, 10),
                0,
                0,
            ),
            (
                mathx.Clamp.new(0, 10),
                10,
                10,
            ),
            (
                mathx.Clamp.new(0, 10),
                -1,
                0,
            ),
            (
                mathx.Clamp.new(0, 10),
                100,
                10,
            ),
            (
                mathx.Clamp.new(0, 0),
                0,
                0,
            ),
            (
                mathx.Clamp.new(0, 0),
                -1,
                0,
            ),
            (
                mathx.Clamp.new(0, 0),
                1,
                0,
            ),
            (
                mathx.Clamp.new(10, 0),
                1,
                1,
            ),
            (
                mathx.Clamp.new(10, 0),
                100,
                10,
            ),
        ]
        for t in cases:
            c = t[0]
            v = t[1]
            want = t[2]
            with self.subTest(f"{c}({v}) should return {want}"):
                got = c(v)
                self.assertEqual(want, got)
