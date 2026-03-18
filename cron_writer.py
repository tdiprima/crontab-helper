"""Read from and write to the user's crontab safely."""

import logging
import subprocess

logger = logging.getLogger(__name__)


def read_crontab() -> str:
    """Return the current crontab contents, or empty string if none exists."""
    result = subprocess.run(
        ["crontab", "-l"],
        capture_output=True,
        text=True,
    )
    if result.returncode == 0:
        return result.stdout
    # Exit code 1 with "no crontab" message is normal for a fresh crontab
    if "no crontab for" in result.stderr.lower():
        return ""
    logger.error("crontab -l failed: %s", result.stderr.strip())
    raise RuntimeError(f"Failed to read crontab: {result.stderr.strip()}")


def write_crontab(content: str) -> None:
    """Write the given content to the user's crontab."""
    result = subprocess.run(
        ["crontab", "-"],
        input=content,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        logger.error("crontab write failed: %s", result.stderr.strip())
        raise RuntimeError(f"Failed to write crontab: {result.stderr.strip()}")
    logger.info("Crontab updated successfully.")


def add_to_crontab(cron_line: str) -> None:
    """Append a cron line to the existing crontab."""
    current = read_crontab()

    # Ensure existing content ends with a newline before appending
    if current and not current.endswith("\n"):
        current += "\n"

    new_content = current + cron_line + "\n"
    write_crontab(new_content)
    logger.info("Added cron entry.")


def preview_crontab(cron_line: str) -> None:
    """Print the full crontab as it would look after the addition."""
    current = read_crontab()
    if current and not current.endswith("\n"):
        current += "\n"
    print("\n--- Preview of updated crontab ---")
    print(current + cron_line)
    print("----------------------------------")
