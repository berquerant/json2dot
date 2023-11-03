from unittest import TestCase

import json2dot.stat as stat


class TestStat(TestCase):
    def test_edge_stat(self):
        with self.subTest("get"):
            s = stat.EdgeStat()
            s.add("n1", "n2")
            self.assertEqual(1, s.get("n1", "n2"), -1)
            self.assertEqual(-1, s.get("n1", "n3"), -1)
        cases = [
            (
                "empty",
                [],
                {},
            ),
            (
                "1 edge",
                [("n1", "n2")],
                {("n1", "n2"): 1},
            ),
            (
                "2 edges",
                [("n1", "n2"), ("n2", "n3")],
                {("n1", "n2"): 1, ("n2", "n3"): 1},
            ),
            (
                "3 edges and 1 duplicated",
                [("n1", "n2"), ("n2", "n3")],
                {("n1", "n2"): 1, ("n2", "n3"): 1},
            ),
        ]
        for c in cases:
            with self.subTest(c[0]):
                s = stat.EdgeStat()
                for x, y in c[1]:
                    s.add(x, y)
                self.assertEqual(c[2], s.edges)

    def test_node_stat(self):
        with self.subTest("get"):
            s = stat.NodeStat()
            s.add("n1")
            self.assertEqual(1, s.get("n1", -1))
            self.assertEqual(-1, s.get("n2", -1))
        cases = [
            (
                "empty",
                [],
                {},
            ),
            (
                "1 node",
                ["n1"],
                {"n1": 1},
            ),
            (
                "2 nodes",
                ["n1", "n2"],
                {"n1": 1, "n2": 1},
            ),
            (
                "3 nodes and 1 duplicated",
                ["n1", "n2", "n1"],
                {"n1": 2, "n2": 1},
            ),
        ]
        for c in cases:
            with self.subTest(c[0]):
                s = stat.NodeStat()
                for x in c[1]:
                    s.add(x)
                self.assertEqual(c[2], s.nodes)
