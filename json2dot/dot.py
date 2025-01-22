import sys
from pathlib import Path
from typing import cast

import graphviz


class Graph:
    def __init__(self, g: graphviz.Digraph) -> None:
        self.__g = g

    @property
    def source(self) -> str:
        return cast(str, self.__g.source)

    def render(self, out: Path) -> None:
        p = out.absolute()
        filename = p.stem
        directory = str(p.parent)
        format = p.suffix.lstrip(".")
        self.__g.render(
            filename=filename,
            directory=directory,
            format=format,
        )
        print(f"rendered to {p} as {format}", file=sys.stderr)
