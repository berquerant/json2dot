from collections import defaultdict
from dataclasses import dataclass

from .ranking import Ranking as RawRanking


class NodeStat:
    """Node degree map."""

    def __init__(self) -> None:
        self.__nodes: dict[str, int] = defaultdict(int)

    def add(self, node_id: str) -> None:
        """Add a node to stat."""
        self.__nodes[node_id] += 1

    @property
    def nodes(self) -> dict[str, int]:
        """Return the stat as dict (node_id to degree)."""
        return self.__nodes

    def get(self, node_id: str, value: int = -1) -> int:
        """
        Get the degree of the node.

        Return value if not found.
        """
        return self.__nodes.get(node_id, value)


class EdgeStat:
    """Edge weight map."""

    def __init__(self) -> None:
        self.__edges: dict[tuple[str, str], int] = defaultdict(int)

    def add(self, src_node_id: str, dst_node_id: str) -> None:
        """Add an edge to stat."""
        self.__edges[(src_node_id, dst_node_id)] += 1

    @property
    def edges(self) -> dict[tuple[str, str], int]:
        """Return the stat as dict (edge to weight)."""
        return self.__edges

    def get(self, src_node_id: str, dst_node_id: str, value: int = -1) -> int:
        """
        Get the weight of the edge.

        Return value if not found.
        """
        return self.__edges.get((src_node_id, dst_node_id), value)


@dataclass
class Report:
    """Stat about specific vertex."""

    node_id: str
    in_deg: int
    out_deg: int
    in_uniq: int
    out_uniq: int


class Stat:
    """Graph stat."""

    def __init__(self, nodes: NodeStat, edges: EdgeStat) -> None:
        self.__nodes = nodes
        self.__edges = edges

    @staticmethod
    def default() -> "Stat":
        """Return a new default Stat."""
        return Stat(NodeStat(), EdgeStat())

    def add(self, src_node_id: str, dst_node_id: str) -> None:
        """Add an edge to stat."""
        self.__nodes.add(src_node_id)
        self.__nodes.add(dst_node_id)
        self.__edges.add(src_node_id, dst_node_id)

    @property
    def nodes(self) -> NodeStat:
        """Return node stat."""
        return self.__nodes

    @property
    def edges(self) -> EdgeStat:
        """Return edge stat."""
        return self.__edges

    def report(self, node_id: str) -> Report:
        """Build a new node report."""
        in_deg = 0
        out_deg = 0
        in_uniq = set()
        out_uniq = set()
        for (src, dst), c in self.edges.edges.items():
            if src == node_id:
                out_uniq.add(dst)
                out_deg += c
            if dst == node_id:
                in_uniq.add(src)
                in_deg += c
        return Report(node_id=node_id, in_deg=in_deg, out_deg=out_deg, in_uniq=len(in_uniq), out_uniq=len(out_uniq))


@dataclass
class Ranking:
    """Ranking of degrees and weights."""

    stat: Stat
    nodes: RawRanking[str]
    edges: RawRanking[tuple[str, str]]

    @staticmethod
    def new(stat: Stat) -> "Ranking":
        """Build a new Ranking."""
        nodes = RawRanking.build(stat.nodes.nodes)
        edges = RawRanking.build(stat.edges.edges)
        return Ranking(stat=stat, nodes=nodes, edges=edges)
