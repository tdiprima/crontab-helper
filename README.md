# crontab-helper

Python CLI that turns plain scheduling questions into crontab entries and installs them for you.

## The Lookup You're Tired of Doing

Cron syntax is simple once you know it. But every time you sit down to schedule something new, you end up Googling "cron every 15 minutes" or "cron first day of month" just to get the field order right.

`*/15 * * * *` — minute, hour, day, month, weekday. Fine. But you shouldn't have to remember that.

## Answer Prompts. Get a Cron Line. Done.

`crontab-helper` walks you through scheduling a job interactively. Pick a frequency, answer a few questions about timing, provide your command, and it writes the entry directly to your crontab — no editor, no syntax lookup, no manual copy-paste.

Supports: every N minutes · hourly · daily · weekly · weekdays (Mon–Fri) · monthly · yearly · raw custom expression

Previews the full updated crontab before writing anything.

## Example Output

```
=== crontab helper ===

Tip: Use full paths for reliability, e.g. /usr/bin/python3 /home/user/script.py
Command to run: /usr/bin/python3 /home/alice/scripts/backup.py

How often should this run?
  1) Every N minutes
  2) Every hour
  3) Every day
  4) Every week
  5) Weekdays (Mon-Fri)
  6) Every month
  7) Every year
  8) Custom cron expression

Enter choice (1-8): 3
At what hour (0-23)? [0]: 6
At what minute (0-59)? [0]: 30

Optional comment to add above this entry (press Enter to skip): daily backup

Generated cron entry:

  # daily backup
  30 6 * * * /usr/bin/python3 /home/alice/scripts/backup.py

--- Preview of updated crontab ---
# daily backup
30 6 * * * /usr/bin/python3 /home/alice/scripts/backup.py
----------------------------------

Add this entry to your crontab? [y/n]: y
Done. Entry added to your crontab.
```

## Usage

**Requirements:** Python 3.10+, Unix-like OS (Linux, macOS)

```bash
git clone https://github.com/tdiprima/crontab-helper.git
cd crontab-helper
python3 main.py
```

No dependencies. No install step. Just run it.

**Optional flag:**

```bash
python3 main.py --log-level DEBUG   # verbose output for troubleshooting
```

**Frequency options and the expressions they produce:**

| Choice        | Example expression       | Meaning                        |
|---------------|--------------------------|--------------------------------|
| Every N mins  | `*/15 * * * *`           | Every 15 minutes               |
| Every hour    | `30 * * * *`             | At 30 minutes past every hour  |
| Every day     | `30 6 * * *`             | Daily at 6:30 AM               |
| Every week    | `0 9 * * 1`              | Mondays at 9:00 AM             |
| Weekdays      | `30 8 * * 1-5`           | Mon–Fri at 8:30 AM             |
| Every month   | `0 0 1 * *`              | 1st of the month at midnight   |
| Every year    | `0 0 1 1 *`              | January 1st at midnight        |
| Custom        | `0 7 * * *`              | Whatever you enter directly    |

**Files:**

| File              | Responsibility                          |
|-------------------|-----------------------------------------|
| `main.py`         | Entry point and orchestration           |
| `prompter.py`     | Interactive prompts                     |
| `cron_builder.py` | Converts schedule data to cron syntax   |
| `cron_writer.py`  | Reads and writes crontab via subprocess |

<br>
