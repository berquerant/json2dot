from unittest import TestCase

import json2dot.row as row


class TestRow(TestCase):
    def test_node_join(self):
        with self.subTest("other id mismatch"):
            with self.assertRaises(row.RowException):
                row.Node(id="a").join(row.Node(id="b"))

        cases = [
            (
                "identity",
                row.Node(id="a"),
                row.Node(id="a"),
                row.Node(id="a"),
            ),
            (
                "merge desc",
                row.Node(id="a", desc={"n": 0, "m": 1}),
                row.Node(id="a", desc={"n": 10}),
                row.Node(id="a", desc={"n": 10, "m": 1}),
            ),
        ]
        for c in cases:
            with self.subTest(c[0]):
                got = c[1].join(c[2])
                self.assertEqual(c[3], got)

    def test_node_new(self):
        failures = [
            (
                "id required",
                {},
            ),
            (
                "id should be str",
                {"id": 1},
            ),
        ]
        for c in failures:
            with self.subTest(c[0]):
                with self.assertRaises(row.RowException):
                    row.Node.new(c[1])

        cases = [
            (
                "id",
                {"id": "a"},
                row.Node(id="a"),
            ),
            (
                "desc",
                {"id": "a", "n": 1},
                row.Node(id="a", desc={"n": 1}),
            ),
        ]
        for c in cases:
            with self.subTest(c[0]):
                got = row.Node.new(c[1])
                self.assertEqual(c[2], got)

    def test_row_loads(self):
        failures = [
            (
                "src required",
                '{"dst":{"id":"b"}}',
            ),
            (
                "src should be dict",
                '{"src":{"id":10},"dst":{"id":"b"}}',
            ),
            (
                "dst required",
                '{"dst":{"id":"b"}}',
            ),
            (
                "dst should be dict",
                '{"src":{"id":"a"},"dst":{"id":[]}}',
            ),
        ]
        for c in failures:
            with self.subTest(c[0]):
                with self.assertRaises(row.RowException):
                    row.Row.loads(c[1])

        cases = [
            (
                "id",
                '{"src":{"id":"a"},"dst":{"id":"b"}}',
                row.Row(row.Node(id="a"), row.Node(id="b")),
            ),
            (
                "desc",
                '{"src":{"id":"a","n":0},"dst":{"id":"b","n":1}}',
                row.Row(row.Node(id="a", desc={"n": 0}), row.Node(id="b", desc={"n": 1})),
            ),
        ]
        for c in cases:
            with self.subTest(c[0]):
                got = row.Row.loads(c[1])
                self.assertEqual(c[2], got)
