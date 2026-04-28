# score a pandas-free csv in pure stdlib for tiny batch jobs
from __future__ import annotations

import csv
import math
import random
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Tuple


@dataclass
class Weights:
    # toy logistic weights; swap with loaded json in real life
    w: Dict[str, float]
    b: float

    def score_row(self, row: Dict[str, str]) -> float:
        z = self.b
        for k, wt in self.w.items():
            v = float(row.get(k, "0") or 0.0)
            z += wt * v
        return 1.0 / (1.0 + math.exp(-z))


def read_rows(path: Path) -> List[Dict[str, str]]:
    with path.open(encoding="utf-8") as f:
        r = csv.DictReader(f)
        return list(r)


def summarize(scores: Iterable[float]) -> Tuple[float, float]:
    xs = list(scores)
    if not xs:
        return 0.0, 0.0
    mean = sum(xs) / len(xs)
    var = sum((x - mean) ** 2 for x in xs) / len(xs)
    return mean, math.sqrt(var)


def main() -> None:
    rng = random.Random(0)
    w = Weights(w={"amt": 0.02, "velocity": 0.35}, b=-1.0)
    rows = [{"amt": str(rng.random() * 500), "velocity": str(rng.random())} for _ in range(200)]
    scores = [w.score_row(r) for r in rows]
    print("mean std", summarize(scores))


if __name__ == "__main__":
    main()
