"""可达性、死状态与不确定转移的检查。"""

START = "start"
FINAL = frozenset(["done"])


class Counter:
    """记录本轮检查过的转移条数。"""

    def __init__(self):
        self.scanned = 0


def analyze(rows, counter):
    unique_rows = []
    seen = set()
    for row in rows:
        counter.scanned += 1
        if row not in seen:
            seen.add(row)
            unique_rows.append(row)

    states = set()
    adjacency = {}
    choices = {}
    for frm, event, to in unique_rows:
        counter.scanned += 1
        states.add(frm)
        states.add(to)
        adjacency.setdefault(frm, []).append((event, to))
        choices.setdefault((frm, event), set()).add(to)

    reachable = {START}
    stack = [START]
    while stack:
        current = stack.pop()
        for _, target in adjacency.get(current, ()):
            if target not in reachable:
                reachable.add(target)
                stack.append(target)

    nondet = sorted("%s:%s" % key
                    for key, targets in choices.items()
                    if len(targets) > 1)
    dead = sorted(state for state in states
                  if state in reachable
                  and state not in FINAL
                  and state not in adjacency)
    unreachable = sorted(states - reachable)
    return {
        "states": sorted(states),
        "reachable": sorted(reachable),
        "unreachable": unreachable,
        "dead": dead,
        "nondet": nondet,
        "transitions": len(unique_rows),
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
