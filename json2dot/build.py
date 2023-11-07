from typing import Any, Callable, Iterator

from .row import Node, NodeMap, Row
from .stat import Stat


def build_nodemap(source: Iterator[str]) -> NodeMap:
    """Build new NodeMap from text."""
    nodes = NodeMap()
    for line in source:
        nodes.add(Row.loads(line))
    return nodes


class DescMap:
    """node_id to desc[key] map."""

    def __init__(self, rows: list[Row], key: str | None = None) -> None:
        self.__key = key
        self.__map = (
            {
                **{r.src.id: r.src.desc[key] for r in rows if key in r.src.desc},
                **{r.dst.id: r.dst.desc[key] for r in rows if key in r.dst.desc},
            }
            if key is not None
            else {}
        )

    @property
    def map(self) -> dict[str, str]:
        """Unwrap DescMap."""
        return self.__map

    @property
    def key(self) -> str | None:
        return self.__key


class NodeNameMap(DescMap):
    """node_id to node name map."""

    def get(self, node_id: str) -> str:
        """
        Get name of node.

        Return node_id if not found.
        """
        return self.map.get(node_id, node_id)


class GroupNameMap(DescMap):
    """node_id to group name map."""

    nil_group = "__json2dot__group_name_map__nil_group"

    def get(self, node_id: str) -> str:
        """
        Get group name of node.

        Return GroupNameMap.nil_group if not found.
        """
        return self.map.get(node_id, self.nil_group)

    @classmethod
    def build_stat(cls, nodes: NodeMap, key: Callable[[Node], str | None], ignore_selfloop=False) -> Stat:
        rows = nodes.source
        if ignore_selfloop:
            rows = [x for x in rows if x.src.id != x.dst.id]

        node_map = nodes.map
        s = Stat.default()
        for row in rows:
            sv = key(node_map[row.src.id])
            if sv is None:
                sv = cls.nil_group
            dv = key(node_map[row.dst.id])
            if dv is None:
                dv = cls.nil_group
            if ignore_selfloop and sv == dv:
                continue
            s.add(sv, dv)
        return s


def __build_stat(rows: list[Row]) -> Stat:
    s = Stat.default()
    for row in rows:
        s.add(row.src.id, row.dst.id)
    return s


def build_stat(rows: list[Row], key: Callable[[Node], str | None] | None = None, ignore_selfloop=False) -> Stat:
    """
    Build new Stat from rows.

    If ignore_selfloop, ignore edges that have the same head and tail.
    If key, replace node_id.
    """
    if ignore_selfloop:
        rows = [x for x in rows if x.src.id != x.dst.id]
    if key is None:
        return __build_stat(rows)

    node_map = {
        **{r.src.id: r.src for r in rows},
        **{r.dst.id: r.dst for r in rows},
    }
    s = Stat.default()
    for row in rows:
        sv = key(node_map[row.src.id])
        if sv is None:
            continue
        dv = key(node_map[row.dst.id])
        if dv is None:
            continue
        s.add(sv, dv)
    return s


def build_label(obj: dict[str, Any]) -> str:
    """Build human readable label."""
    keys = sorted(obj.keys())
    rows = [
        f"""<tr>
<td align="left"><b>{k}</b></td>
<td align="right">{obj[k]}</td>
</tr>"""
        for k in keys
    ]
    table = f'<table border="0">{"".join(rows)}</table>'
    return f"""<
{table}
>"""


def build_tooltip(obj: dict[str, Any]) -> str:
    """Build human readable tooltip."""
    keys = sorted(obj.keys())
    rows = [f"{k}: {obj[k]}" for k in keys]
    return "\n".join(rows)
