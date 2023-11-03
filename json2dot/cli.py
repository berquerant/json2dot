"""Entry point of CLI."""
import sys
from pathlib import Path
from textwrap import dedent

from .build import GroupNameMap, NodeNameMap, build_nodemap, build_stat
from .command import Debug, Draw
from .mathx import Clamp
from .row import Node
from .scale import Scaler, Setting
from .stat import Ranking, Stat


def main() -> int:
    """Entry point of CLI."""
    import argparse

    parser = argparse.ArgumentParser(
        prog="json2dot",
        description=dedent(
            """\
        Generate dot source from jsonl considering node degrees and edge weights.

        Load edges from stdin, format:

          {"src": NODE, "dst": NODE}

        src is head, dst is tail.
        NODE fomat:

          {"id": NODE_ID, "other_key": OTHER_VALUE, ...}

        NODE_ID is string. Other keys are optional node descriptions.
        No need to give descriptions to all nodes, descriptions of nodes with the same NODE_ID are merged.
        """
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--penwidth_min", action="store", type=int, default=1)
    parser.add_argument("--penwidth_max", action="store", type=int, default=5)
    parser.add_argument("--arrowsize_min", action="store", type=int, default=1)
    parser.add_argument("--arrowsize_max", action="store", type=int, default=2)
    parser.add_argument("--weight_min", action="store", type=int, default=1)
    parser.add_argument("--weight_max", action="store", type=int, default=100)
    parser.add_argument("--fontsize_min", action="store", type=int, default=8)
    parser.add_argument("--fontsize_max", action="store", type=int, default=48)
    parser.add_argument("--display_selfloop", "-s", action="store_true")
    parser.add_argument("--name_key", "-k", action="store", type=str, help="select node name from node desc")
    parser.add_argument("--group_key", "-g", action="store", type=str, help="select group name from node desc")
    parser.add_argument("--out", "-o", action="store", type=str, help="filename for saving the rendered image")
    parser.add_argument("--debug", action="store_true")

    args = parser.parse_args()

    nodes = build_nodemap(iter(sys.stdin))
    stat = build_stat(rows=nodes.source, ignore_selfloop=not args.display_selfloop)
    ranking = Ranking.new(stat)

    node_name_map = NodeNameMap(nodes.source, args.name_key)

    group_name_map: GroupNameMap | None = None
    grouped_stat: Stat | None = None
    grouped_ranking: Ranking | None = None

    if args.group_key:
        group_name_map = GroupNameMap(nodes.source, args.group_key)

        def group_key(node: Node) -> str | None:
            return node.desc.get(args.group_key)

        grouped_stat = GroupNameMap.build_stat(nodes=nodes, ignore_selfloop=not args.display_selfloop, key=group_key)
        grouped_ranking = Ranking.new(grouped_stat)

    if args.debug:
        print(
            Debug(
                nodes=nodes,
                node_name_map=node_name_map,
                group_name_map=group_name_map,
                ranking=ranking,
                grouped_ranking=grouped_ranking,
            ).run()
        )
        return 0

    def new_setting(x: int, y: int) -> Setting:
        return Setting(clamp=Clamp.new(x, y))

    scaler = Scaler(
        ranking=ranking,
        penwidth=new_setting(args.penwidth_min, args.penwidth_max),
        arrowsize=new_setting(args.arrowsize_min, args.arrowsize_max),
        weight=new_setting(args.weight_min, args.weight_max),
        fontsize=new_setting(args.fontsize_min, args.fontsize_max),
    )
    grouped_scaler: Scaler | None = None
    if grouped_ranking:
        grouped_scaler = Scaler(
            ranking=grouped_ranking,
            penwidth=new_setting(args.penwidth_min, args.penwidth_max),
            arrowsize=new_setting(args.arrowsize_min, args.arrowsize_max),
            weight=new_setting(args.weight_min, args.weight_max),
            fontsize=new_setting(args.fontsize_min, args.fontsize_max),
        )
    g = Draw(
        nodes=nodes,
        scaler=scaler,
        stat=stat,
        node_name_map=node_name_map,
        group_name_map=group_name_map,
        grouped_stat=grouped_stat,
        grouped_scaler=grouped_scaler,
        ignore_selfloop=not args.display_selfloop,
    ).run()
    if args.out is None:
        print(g.source)
        return 0
    g.render(Path(args.out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
