"""命令行入口。"""

import argparse
import csv

from . import core, samples


def main(argv=None):
    ap = argparse.ArgumentParser(prog="fsmcheck")
    ap.add_argument("--sample", choices=["reach", "dead", "nondet", "dup", "work"])
    sub = ap.add_subparsers(dest="cmd")
    check_parser = sub.add_parser("check")
    check_parser.add_argument("--file", required=True)
    args = ap.parse_args(argv)

    if args.sample:
        return samples.run(args.sample)
    if args.cmd is None:
        ap.print_help()
        return 2

    with open(args.file, newline="", encoding="utf-8") as fh:
        rows = [tuple(row) for row in csv.reader(fh) if row and row[0] != "from"]
    print(core.table(core.analyze(rows, core.Counter())))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
