"""可达性、死状态与不确定转移的检查。"""

from collections import deque

START = "start"
FINAL = frozenset(["done"])


class Counter:
    """记录本轮检查过的转移条数。"""

    def __init__(self):
        self.scanned = 0


def analyze(rows, counter):
    seen = set()
    transitions = []
    for row in rows:
        counter.scanned += 1
        if row in seen:
            continue
        seen.add(row)
        transitions.append(row)

    states = []
    for frm, _, to in transitions:
        for item in (frm, to):
            if item not in states:
                states.append(item)

    outgoing = {}
    for frm, event, to in transitions:
        outgoing.setdefault(frm, []).append((event, to))

    reachable = [START]
    queue = deque([START])
    while queue:
        current = queue.popleft()
        for _, to in outgoing.get(current, ()):
            if to not in reachable:
                reachable.append(to)
                queue.append(to)

    unreachable = [s for s in states if s not in reachable]
    dead = [s for s in states
            if s in reachable and s not in FINAL and not outgoing.get(s)]

    counts = {}
    for frm, event, _ in transitions:
        key = (frm, event)
        counts[key] = counts.get(key, 0) + 1
    nondet = ["%s:%s" % key for key, n in counts.items() if n > 1]

    return {
        "states": sorted(states),
        "reachable": sorted(reachable),
        "unreachable": sorted(unreachable),
        "dead": sorted(dead),
        "nondet": sorted(nondet),
        "transitions": len(transitions),
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
