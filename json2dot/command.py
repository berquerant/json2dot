import json
from collections import defaultdict
from dataclasses import asdict, dataclass
from typing import Any, cast

import graphviz

from .build import GroupNameMap, NodeNameMap, build_label, build_tooltip
from .dot import Graph
from .row import NodeMap
from .scale import Scaler
from .stat import Ranking, Stat


@dataclass
class Draw:
    nodes: NodeMap
    scaler: Scaler
    stat: Stat
    node_name_map: NodeNameMap
    group_name_map: GroupNameMap | None
    grouped_stat: Stat | None
    grouped_scaler: Scaler | None
    ignore_selfloop: bool

    @property
    def __is_grouped(self) -> bool:
        return None not in [self.group_name_map, self.grouped_stat, self.grouped_scaler]

    def __add_grouped_nodes(
        self, g: graphviz.Digraph, group_name_map: GroupNameMap, grouped_stat: Stat, grouped_scaler: Scaler
    ) -> None:
        groups: dict[str, set[str]] = defaultdict(set)
        for node_id in self.stat.nodes.nodes.keys():
            group = group_name_map.get(node_id)
            groups[group].add(node_id)

        for group, node_id_set in groups.items():
            if group == GroupNameMap.nil_group:
                for node_id in node_id_set:
                    self.__add_node(g, node_id)
                continue

            subgraph_name = f"cluster_{group}"  # as a cluster subgraph
            tooltip = build_tooltip(asdict(grouped_stat.report(group)))
            subgraph_attrs = {
                "color": "lightgrey",
                "style": "filled",
                "label": group,
                "tooltip": tooltip,
                "fontsize": str(grouped_scaler.get_fontsize(group)),
            }
            with g.subgraph(name=subgraph_name, graph_attr=subgraph_attrs) as c:
                for node_id in node_id_set:
                    self.__add_node(c, node_id)

    def __add_node(self, g: graphviz.dot.Dot, node_id: str) -> None:
        node = self.nodes.map[node_id]
        name = self.node_name_map.get(node_id)
        label_args = {"name": name}
        if node.desc:
            label_args.update(node.desc)
        if self.node_name_map.key in label_args:
            del label_args[self.node_name_map.key]
        if len(label_args) > 1:
            label = build_label(label_args)
        else:
            label = name
        tooltip = build_tooltip(asdict(self.stat.report(node_id)))
        args = {
            "name": node_id,
            "color": "white",
            "style": "filled",
            "shape": "box",
            "label": label,
            "fontsize": str(self.scaler.get_fontsize(node_id)),
            "tooltip": tooltip,
        }
        g.node(**args)

    def __add_nodes(self, g: graphviz.Digraph) -> None:
        for node_id in self.stat.nodes.nodes.keys():
            self.__add_node(g, node_id)

    def __add_edges(self, g: graphviz.Digraph) -> None:
        for (src_node_id, dst_node_id), w in self.stat.edges.edges.items():
            if self.ignore_selfloop and src_node_id == dst_node_id:
                continue

            src_name = self.node_name_map.get(src_node_id)
            dst_name = self.node_name_map.get(dst_node_id)
            args = {
                "tail_name": src_node_id,
                "head_name": dst_node_id,
                "arrowsize": str(self.scaler.get_arrowsize(src_node_id, dst_node_id)),
                "penwidth": str(self.scaler.get_penwidth(src_node_id, dst_node_id)),
                "weight": str(self.scaler.get_weight(src_node_id, dst_node_id)),
            }
            label = str(w) if w > 1 else ""
            args["label"] = label
            tooltip = f"{src_name} -> {dst_name}"
            if label:
                tooltip += f" [{label}]"
            args["tooltip"] = tooltip
            args["labeltooltip"] = tooltip
            g.edge(**args)

    def run(self) -> Graph:
        g = graphviz.Digraph(strict=True)
        if self.__is_grouped:
            self.__add_grouped_nodes(
                g,
                group_name_map=cast(GroupNameMap, self.group_name_map),
                grouped_stat=cast(Stat, self.grouped_stat),
                grouped_scaler=cast(Scaler, self.grouped_scaler),
            )
        else:
            self.__add_nodes(g)
        self.__add_edges(g)
        return Graph(g)


@dataclass
class Debug:
    nodes: NodeMap
    node_name_map: NodeNameMap
    group_name_map: GroupNameMap | None
    grouped_ranking: Ranking | None
    ranking: Ranking

    def run(self) -> str:
        r = {
            "nodes": {
                "map": {k: asdict(v) for k, v in self.nodes.map.items()},
                "source": [{"src": asdict(x.src), "dst": asdict(x.dst)} for x in self.nodes.source],
                "name": self.node_name_map.map,
            },
            "stat": {
                "nodes": self.ranking.stat.nodes.nodes,
                "edges": {f"{s}|{d}": v for (s, d), v in self.ranking.stat.edges.edges.items()},
            },
            "ranking": {
                "nodes": [asdict(x) for x in self.ranking.nodes.elems],
                "edges": {f"{s}|{d}": asdict(v) for (s, d), v in self.ranking.edges.elem_map.items()},
            },
        }
        g: dict[str, Any] = {}
        if self.group_name_map:
            g["name"] = self.group_name_map.map
        if self.grouped_ranking:
            g["stat"] = {
                "nodes": self.grouped_ranking.stat.nodes.nodes,
                "edges": {f"{s}|{d}": v for (s, d), v in self.grouped_ranking.stat.edges.edges.items()},
            }
            g["ranking"] = {
                "nodes": [asdict(x) for x in self.grouped_ranking.nodes.elems],
                "edges": {f"{s}|{d}": asdict(v) for (s, d), v in self.grouped_ranking.edges.elem_map.items()},
            }
        r["group"] = g
        return json.dumps(r, separators=(",", ":"))
