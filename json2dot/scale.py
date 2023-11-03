from dataclasses import dataclass

from .mathx import Clamp
from .stat import Ranking


@dataclass
class Setting:
    """Scale range."""

    clamp: Clamp

    def __call__(self, percentile: float) -> float:
        """Return scaled value."""
        v = (self.clamp.maximum - self.clamp.minimum) * percentile / 100 + self.clamp.minimum
        return self.clamp(v)


@dataclass
class Scaler:
    """Scaler of strength of emphasis."""

    ranking: Ranking
    penwidth: Setting
    arrowsize: Setting
    weight: Setting
    fontsize: Setting

    @property
    def __node_top_percentile(self) -> float:
        return self.ranking.nodes.elems[0].value_percentile

    @property
    def __edge_top_percentile(self) -> float:
        return self.ranking.edges.elems[0].value_percentile

    def __get_node_percentile(self, node_id: str) -> float:
        if node_id not in self.ranking.nodes.elem_map:
            return 100  # lowest
        return self.ranking.nodes.elem_map[node_id].value_percentile

    def __get_edge_percentile(self, src_node_id: str, dst_node_id: str) -> float:
        key = (src_node_id, dst_node_id)
        if key not in self.ranking.edges.elem_map:
            return 100  # lowest
        return self.ranking.edges.elem_map[key].value_percentile

    def get_fontsize(self, node_id: str) -> float:
        return self.fontsize(100 - self.__get_node_percentile(node_id))

    def __get_edge(self, src: str, dst: str, setting: Setting) -> float:
        return setting(100 - self.__get_edge_percentile(src, dst))

    def get_penwidth(self, src_node_id: str, dst_node_id: str) -> float:
        return self.__get_edge(src_node_id, dst_node_id, self.penwidth)

    def get_arrowsize(self, src_node_id: str, dst_node_id: str) -> float:
        return self.__get_edge(src_node_id, dst_node_id, self.arrowsize)

    def get_weight(self, src_node_id: str, dst_node_id: str) -> float:
        return self.__get_edge(src_node_id, dst_node_id, self.weight)
