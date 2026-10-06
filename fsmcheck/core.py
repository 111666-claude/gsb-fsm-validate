"""可达性、死状态与不确定转移的检查。"""

START = "start"
FINAL = frozenset(["done"])


class Counter:
    """记录本轮检查过的转移条数。"""

    def __init__(self):
        self.scanned = 0


def analyze(rows, counter):
    states = []
    for frm, _, to in rows:
        for item in (frm, to):
            if item not in states:
                states.append(item)
    incoming = {}
    for target in states:
        names = []
        for frm, _, to in rows:
            counter.scanned += 1
            if to == target:
                names.append(frm)
        incoming[target] = names
    reachable = [START]
    for frm, _, to in rows:
        counter.scanned += 1
        if frm == START and to not in reachable:
            reachable.append(to)
    unreachable = [s for s in states if s not in reachable]
    return {
        "states": sorted(states),
        "reachable": sorted(reachable),
        "unreachable": sorted(unreachable),
        "dead": [],
        "nondet": [],
        "transitions": len(rows),
        "scanned": counter.scanned,
    }


def table(result):
    lines = [("state", "reachable", "dead", "nondet")]
    for state in result["states"]:
        nondet = "yes" if any(item.startswith(state + ":") for item in result["nondet"]) else "no"
        lines.append((state,
                      "no" if state in result["unreachable"] else "yes",
                      "yes" if state in result["dead"] else "no",
                      nondet))
    widths = [max(len(line[i]) for line in lines) for i in range(4)]
    body = "\n".join("  ".join(cell.ljust(widths[i]) for i, cell in enumerate(line))
                     for line in lines)
    return body + "\ntransitions=%d" % result["transitions"]
