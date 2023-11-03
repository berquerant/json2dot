import json
from dataclasses import dataclass, field
from typing import Any


class RowException(Exception):
    pass


@dataclass
class Node:
    """Graph node."""

    id: str
    desc: dict[str, Any] = field(default_factory=dict)  # other info

    @classmethod
    def new(cls, obj: dict[str, Any]) -> "Node":
        id = cls.__parse_id(obj)
        return Node(id=id, desc=obj)

    @staticmethod
    def __parse_id(obj: dict[str, Any]) -> str:
        if "id" not in obj:
            raise RowException('"id" required')
        id = obj.pop("id")
        if not isinstance(id, str):
            raise RowException(f'"id" should be str, {id}')
        return id

    def join(self, other: "Node") -> "Node":
        if self.id != other.id:
            raise RowException(f"cannot join Node, {self.id} != {other.id}")
        return Node(id=self.id, desc={**self.desc, **other.desc})


@dataclass
class Row:
    """Graph edge."""

    src: Node
    dst: Node

    @classmethod
    def loads(cls, s: str) -> "Row":
        obj = json.loads(s)
        if "src" not in obj:
            raise RowException('"src" required')
        src = obj["src"]
        if not isinstance(src, dict):
            raise RowException(f'"src" should be dict, {src}')
        if "dst" not in obj:
            raise RowException('"dst" required')
        dst = obj["dst"]
        if not isinstance(dst, dict):
            raise RowException(f'"dst" should be dict, {dst}')
        return Row(src=Node.new(src), dst=Node.new(dst))


class NodeMap:
    """node_id to Node map."""

    def __init__(self) -> None:
        self.__map: dict[str, Node] = {}
        self.__source: list[Row] = []

    @property
    def map(self) -> dict[str, Node]:
        return self.__map

    @property
    def source(self) -> list[Row]:
        return self.__source

    def __add_node(self, node: Node) -> None:
        n = self.__map.get(node.id)
        if n is None:
            self.__map[node.id] = node
            return
        self.__map[node.id] = n.join(node)

    def add(self, row: Row) -> None:
        """
        Add an edge to map.

        Nodes with duplicated ids will be joined.
        """
        self.__source.append(row)
        self.__add_node(row.src)
        self.__add_node(row.dst)
