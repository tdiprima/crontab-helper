#!/usr/bin/env python3
"""
crontab-helper — interactive tool to build and install crontab entries.

Usage:
    python3 main.py
    python3 main.py --log-level DEBUG
"""

import argparse
import logging
import sys

from prompter import gather_command, gather_frequency, gather_schedule
from cron_builder import build_cron_line
from cron_writer import add_to_crontab, preview_crontab


def configure_logging(level: str) -> None:
    """Set up structured logging to stderr."""
    logging.basicConfig(
        stream=sys.stderr,
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Interactively build and install a crontab entry."
    )
    parser.add_argument(
        "--log-level",
        default="WARNING",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="Logging verbosity (default: WARNING)",
    )
    return parser.parse_args()


def confirm(prompt: str) -> bool:
    """Ask a yes/no question and return True for yes."""
    while True:
        answer = input(f"{prompt} [y/n]: ").strip().lower()
        if answer in ("y", "yes"):
            return True
        if answer in ("n", "no"):
            return False
        print("  Please enter y or n.")


def main() -> None:
    args = parse_args()
    configure_logging(args.log_level)

    logger = logging.getLogger(__name__)
    logger.info("crontab-helper starting")

    print("=== crontab helper ===\n")

    try:
        command = gather_command()
        frequency = gather_frequency()
        schedule = gather_schedule(frequency)
        cron_line = build_cron_line(schedule, command)

        print(f"\nGenerated cron entry:\n\n  {cron_line}\n")

        preview_crontab(cron_line)

        if confirm("\nAdd this entry to your crontab?"):
            add_to_crontab(cron_line)
            print("Done. Entry added to your crontab.")
        else:
            print("Nothing written. You can copy the entry above manually.")

    except KeyboardInterrupt:
        print("\nAborted.")
        sys.exit(0)
    except ValueError as exc:
        print(f"\nError: {exc}", file=sys.stderr)
        sys.exit(1)
    except RuntimeError as exc:
        print(f"\nError: {exc}", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
