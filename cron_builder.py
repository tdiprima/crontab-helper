"""Build crontab expressions from structured schedule data."""

import logging

logger = logging.getLogger(__name__)

WEEKDAY_NAMES = {
    "monday": "1",
    "tuesday": "2",
    "wednesday": "3",
    "thursday": "4",
    "friday": "5",
    "saturday": "6",
    "sunday": "0",
    "mon": "1",
    "tue": "2",
    "wed": "3",
    "thu": "4",
    "fri": "5",
    "sat": "6",
    "sun": "0",
}

MONTH_NAMES = {
    "january": "1", "jan": "1",
    "february": "2", "feb": "2",
    "march": "3", "mar": "3",
    "april": "4", "apr": "4",
    "may": "5",
    "june": "6", "jun": "6",
    "july": "7", "jul": "7",
    "august": "8", "aug": "8",
    "september": "9", "sep": "9",
    "october": "10", "oct": "10",
    "november": "11", "nov": "11",
    "december": "12", "dec": "12",
}


def resolve_weekday(value: str) -> str:
    """Resolve a weekday name or number to a cron-compatible value."""
    lower = value.strip().lower()
    if lower in WEEKDAY_NAMES:
        return WEEKDAY_NAMES[lower]
    if value.strip().isdigit() and 0 <= int(value.strip()) <= 7:
        return value.strip()
    raise ValueError(f"Unrecognized weekday: '{value}'")


def resolve_month(value: str) -> str:
    """Resolve a month name or number to a cron-compatible value."""
    lower = value.strip().lower()
    if lower in MONTH_NAMES:
        return MONTH_NAMES[lower]
    if value.strip().isdigit() and 1 <= int(value.strip()) <= 12:
        return value.strip()
    raise ValueError(f"Unrecognized month: '{value}'")


def build_cron_expression(schedule: dict) -> str:
    """
    Build a cron expression from a schedule dictionary.

    Expected keys: frequency, minute, hour, day_of_month, month, day_of_week
    """
    frequency = schedule.get("frequency")

    if frequency == "every_n_minutes":
        interval = schedule["interval"]
        return f"*/{interval} * * * *"

    if frequency == "every_hour":
        minute = schedule.get("minute", "0")
        return f"{minute} * * * *"

    if frequency == "every_day":
        hour = schedule.get("hour", "0")
        minute = schedule.get("minute", "0")
        return f"{minute} {hour} * * *"

    if frequency == "every_week":
        hour = schedule.get("hour", "0")
        minute = schedule.get("minute", "0")
        weekday = resolve_weekday(schedule.get("day_of_week", "1"))
        return f"{minute} {hour} * * {weekday}"

    if frequency == "weekdays":
        hour = schedule.get("hour", "0")
        minute = schedule.get("minute", "0")
        return f"{minute} {hour} * * 1-5"

    if frequency == "every_month":
        hour = schedule.get("hour", "0")
        minute = schedule.get("minute", "0")
        day = schedule.get("day_of_month", "1")
        return f"{minute} {hour} {day} * *"

    if frequency == "every_year":
        hour = schedule.get("hour", "0")
        minute = schedule.get("minute", "0")
        day = schedule.get("day_of_month", "1")
        month = resolve_month(schedule.get("month", "1"))
        return f"{minute} {hour} {day} {month} *"

    if frequency == "custom":
        return schedule["expression"]

    raise ValueError(f"Unknown frequency: '{frequency}'")


def build_cron_line(schedule: dict, command: str) -> str:
    """Combine a cron expression with a command into a full crontab line."""
    expression = build_cron_expression(schedule)
    comment = schedule.get("comment", "").strip()
    line = f"{expression} {command}"
    if comment:
        line = f"# {comment}\n{line}"
    logger.debug("Built cron line: %s", line)
    return line
