import json
import os
import subprocess
from contextlib import contextmanager
from pathlib import Path
from unittest import TestCase

from json2dot.__version__ import __version__


@contextmanager
def cd(p: Path):
    now = Path.cwd()
    try:
        os.chdir(str(p))
        yield
    finally:
        os.chdir(str(now))


def run(cmd: str | list[str], dir: Path, *args, **kwargs) -> subprocess.CompletedProcess:
    with cd(dir):
        return subprocess.run(cmd, check=True, *args, **kwargs)


class TestEndToEnd(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pwd = Path.cwd()
        with cd(cls.pwd / "tests"):
            with open("test.json") as f:
                cls.source = f.read()
            with open("debug.json") as f:
                cls.debug = json.load(f)
            with open("debug_name_another.json") as f:
                cls.debug_name_another = json.load(f)
            with open("debug_group.json") as f:
                cls.debug_group = json.load(f)

    def test_build_and_help(self):
        pwd = self.pwd
        run(["make", "dist"], pwd)
        run(
            [
                "pip",
                "install",
                f"dist/json2dot-{__version__}.tar.gz",
            ],
            pwd,
        )
        run(
            ["python", "-m", "json2dot.cli", "--help"],
            pwd,
            text=True,
            capture_output=True,
        )

    def test_run(self):
        cases = [
            (
                "run",
                [],
            ),
            (
                "namekey",
                ["-k", "another"],
            ),
            (
                "groupkey",
                ["-g", "group"],
            ),
        ]
        for c in cases:
            with self.subTest(c[0]):
                run(
                    cmd=["python", "-m", "json2dot.cli", *c[1]],
                    dir=self.pwd,
                    input=self.source,
                    text=True,
                    capture_output=True,
                )

    def test_debug_golden(self):
        cases = [
            (
                "debug",
                ["--debug"],
                self.debug,
            ),
            (
                "namekey",
                ["--debug", "-k", "another"],
                self.debug_name_another,
            ),
            (
                "groupkey",
                ["--debug", "-g", "group"],
                self.debug_group,
            ),
        ]
        for c in cases:
            with self.subTest(c[0]):
                r = run(
                    cmd=["python", "-m", "json2dot.cli", *c[1]],
                    dir=self.pwd,
                    input=self.source,
                    capture_output=True,
                    text=True,
                ).stdout
                got = json.loads(r)
                self.assertEqual(c[2], got)
