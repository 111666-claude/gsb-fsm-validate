"""固定场景，用来复现题面里的锚点。"""

import json

from . import core


def _line(obj):
    print(json.dumps(obj, ensure_ascii=False))


def _rows(*items):
    return [tuple(item) for item in items]


def run(name):
    if name == "reach":
        rows = _rows(("start", "go", "a"), ("a", "go", "b"))
        out = core.analyze(rows, core.Counter())
        _line({"unreachable": out["unreachable"]})
        return 0
    if name == "dead":
        rows = _rows(("start", "go", "a"), ("start", "go", "c"), ("a", "go", "done"))
        out = core.analyze(rows, core.Counter())
        _line({"dead": out["dead"]})
        return 0
    if name == "nondet":
        rows = _rows(("start", "go", "a"), ("start", "go", "b"))
        out = core.analyze(rows, core.Counter())
        _line({"nondet": out["nondet"]})
        return 0
    if name == "dup":
        rows = _rows(("start", "go", "a"), ("start", "go", "a"), ("a", "go", "done"))
        out = core.analyze(rows, core.Counter())
        _line({"transitions": out["transitions"]})
        return 0
    if name == "work":
        rows = _rows(*[("start", "e%d" % i, "s%d" % i) for i in range(2000)])
        counter = core.Counter()
        core.analyze(rows, counter)
        _line({"rows": 2000, "scanned": counter.scanned})
        return 0
    raise SystemExit("未知场景：" + name)
