from dataclasses import dataclass
from typing import Generic, TypeVar

K = TypeVar("K")


@dataclass
class RankingElement(Generic[K]):
    key: K
    value: int
    place: int
    percentile: float
    value_percentile: float


@dataclass
class Ranking(Generic[K]):
    elems: list[RankingElement[K]]
    elem_map: dict[K, RankingElement[K]]

    @staticmethod
    def build(data: dict[K, int]) -> "Ranking[K]":
        xs = [(k, v) for k, v in data.items()]
        xs.sort(key=lambda x: x[1], reverse=True)

        elems = []
        elem_map = {}
        acc = 0
        card = len(xs)
        sum_value = sum(x[1] for x in xs)
        for i, x in enumerate(xs):
            value = x[1]
            acc += x[1]
            elem = RankingElement(
                key=x[0],
                value=value,
                place=i + 1,
                percentile=100 * (i + 1) / card,
                value_percentile=100 * acc / sum_value,
            )
            elems.append(elem)
            elem_map[x[0]] = elem

        return Ranking(elems=elems, elem_map=elem_map)
