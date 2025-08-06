from datetime import datetime
from pathlib import Path

RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
BOLD = "\033[1m"
RESET = "\033[0m"

LOGFILE = None


def init_logfile(logfile_path):
    global LOGFILE
    LOGFILE = Path(logfile_path)
    if LOGFILE.exists():
        LOGFILE.unlink()


def write_logfile(line):
    if LOGFILE is None:
        return
    with open(LOGFILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def log_with_type(prefix, color, msg):
    ts = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    line = f"{ts} {prefix} {msg}"
    print(f"{color}{prefix}{RESET} {msg}")
    write_logfile(line)


def log_error(msg):
    log_with_type("ERROR", RED + BOLD, msg)


def log_info(msg):
    log_with_type("INFO ", BLUE, msg)


def log_warning(msg):
    log_with_type("Warning:", YELLOW, msg)
