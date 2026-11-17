"""Command-line entry point for credential-free local assessments."""

import argparse
from pathlib import Path
from typing import Sequence

from .assessment import AssessmentRunner
from .reporting import json_report, text_report


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="opentrust", description="OpenTrust local demo")
    commands = parser.add_subparsers(dest="command", required=True)
    demo = commands.add_parser("demo", help="Run the four synthetic assessment cases")
    demo.add_argument("--format", choices=("text", "json"), default="text")
    demo.add_argument("--output", type=Path, help="Optional report destination")
    args = parser.parse_args(argv)

    report = AssessmentRunner().run()
    output = json_report(report) if args.format == "json" else text_report(report)
    if args.output is None:
        print(output, end="")
    else:
        args.output.write_text(output, encoding="utf-8")
        print(f"Report written to {args.output}")
    return 1 if report.summary["failed"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
