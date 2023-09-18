#!/usr/bin/env python
from . import convert
from .pdf import PDF
import argparse
from itertools import chain
import sys


def parse_page_spec(p_str):
    if "-" not in p_str:
        return [int(p_str)]
    start, end = map(int, p_str.split("-"))
    return range(start, end + 1)


def parse_args(args_raw):
    parser = argparse.ArgumentParser("pdfplumber")

    parser.add_argument(
        "infile", nargs="?", type=argparse.FileType("rb"), default=sys.stdin.buffer
    )

    parser.add_argument("--format", choices=["csv", "json"], default="csv")

    parser.add_argument(
        "--types",
        nargs="+",
        default=convert.DEFAULT_TYPES,
        choices=convert.DEFAULT_TYPES,
    )

    parser.add_argument("--pages", nargs="+", type=parse_page_spec)

    parser.add_argument(
        "--indent", type=int, help="Indent level for JSON pretty-printing."
    )

    args = parser.parse_args(args_raw)
    if args.pages is not None:
        args.pages = list(chain(*args.pages))
    return args


def main(args_raw=sys.argv[1:]):
    args = parse_args(args_raw)
    converter = {"csv": convert.to_csv, "json": convert.to_json}[args.format]
    kwargs = {"csv": {}, "json": {"indent": args.indent}}[args.format]
    with PDF.open(args.infile, pages=args.pages) as pdf:
        converter(pdf, sys.stdout, args.types, **kwargs)


if __name__ == "__main__":
    main()
