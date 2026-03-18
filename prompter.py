"""Interactive prompts to gather cron schedule information from the user."""

import logging

logger = logging.getLogger(__name__)

FREQUENCY_MENU = """
How often should this run?
  1) Every N minutes
  2) Every hour
  3) Every day
  4) Every week
  5) Weekdays (Mon-Fri)
  6) Every month
  7) Every year
  8) Custom cron expression
"""

FREQUENCY_MAP = {
    "1": "every_n_minutes",
    "2": "every_hour",
    "3": "every_day",
    "4": "every_week",
    "5": "weekdays",
    "6": "every_month",
    "7": "every_year",
    "8": "custom",
}


def ask(prompt: str, default: str = "") -> str:
    """Prompt the user for input, with an optional default value."""
    display = f"{prompt} [{default}]: " if default else f"{prompt}: "
    response = input(display).strip()
    return response if response else default


def ask_int(prompt: str, min_val: int, max_val: int, default: int) -> int:
    """Prompt the user for an integer within a valid range."""
    while True:
        raw = ask(prompt, str(default))
        if raw.isdigit() and min_val <= int(raw) <= max_val:
            return int(raw)
        print(f"  Please enter a number between {min_val} and {max_val}.")


def gather_frequency() -> str:
    """Ask the user to choose how often the job should run."""
    print(FREQUENCY_MENU)
    while True:
        choice = ask("Enter choice (1-8)").strip()
        if choice in FREQUENCY_MAP:
            return FREQUENCY_MAP[choice]
        print("  Invalid choice. Enter a number from 1 to 8.")


def gather_command() -> str:
    """Ask the user for the command to run."""
    print("\nTip: Use full paths for reliability, e.g. /usr/bin/python3 /home/user/script.py")
    while True:
        command = ask("Command to run")
        if command:
            return command
        print("  Command cannot be empty.")


def gather_schedule(frequency: str) -> dict:
    """Gather schedule-specific details based on the chosen frequency."""
    schedule: dict = {"frequency": frequency}

    if frequency == "every_n_minutes":
        schedule["interval"] = ask_int("Run every how many minutes?", 1, 59, 5)

    elif frequency == "every_hour":
        schedule["minute"] = ask_int("At which minute past the hour?", 0, 59, 0)

    elif frequency == "every_day":
        schedule["hour"] = ask_int("At what hour (0-23)?", 0, 23, 0)
        schedule["minute"] = ask_int("At what minute (0-59)?", 0, 59, 0)

    elif frequency == "every_week":
        schedule["day_of_week"] = ask(
            "Which day of the week? (e.g. monday, tuesday, 1-7)", "monday"
        )
        schedule["hour"] = ask_int("At what hour (0-23)?", 0, 23, 0)
        schedule["minute"] = ask_int("At what minute (0-59)?", 0, 59, 0)

    elif frequency == "weekdays":
        schedule["hour"] = ask_int("At what hour (0-23)?", 0, 23, 0)
        schedule["minute"] = ask_int("At what minute (0-59)?", 0, 59, 0)

    elif frequency == "every_month":
        schedule["day_of_month"] = ask_int("On which day of the month (1-31)?", 1, 31, 1)
        schedule["hour"] = ask_int("At what hour (0-23)?", 0, 23, 0)
        schedule["minute"] = ask_int("At what minute (0-59)?", 0, 59, 0)

    elif frequency == "every_year":
        schedule["month"] = ask("Which month? (e.g. january, jan, or 1-12)", "january")
        schedule["day_of_month"] = ask_int("On which day of the month (1-31)?", 1, 31, 1)
        schedule["hour"] = ask_int("At what hour (0-23)?", 0, 23, 0)
        schedule["minute"] = ask_int("At what minute (0-59)?", 0, 59, 0)

    elif frequency == "custom":
        print("Enter a raw cron expression (minute hour dom month dow).")
        print("Example: 30 6 * * 1-5   (weekdays at 6:30 AM)")
        schedule["expression"] = ask("Cron expression")

    comment = ask("\nOptional comment to add above this entry (press Enter to skip)", "")
    if comment:
        schedule["comment"] = comment

    return schedule
