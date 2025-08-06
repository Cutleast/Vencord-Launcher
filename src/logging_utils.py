from datetime import datetime
from pathlib import Path
from typing import Optional

RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
BOLD = "\033[1m"
RESET = "\033[0m"

logfile: Optional[Path] = None


def init_logfile(logfile_path: Path) -> None:
    global logfile
    logfile = Path(logfile_path)
    if logfile.exists():
        logfile.unlink()


def write_logfile(line: str) -> None:
    if logfile is None:
        return
    with open(logfile, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def log_with_type(prefix: str, color: str, msg: str) -> None:
    ts = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    line = f"{ts} {prefix} {msg}"
    print(f"{color}{prefix}{RESET} {msg}")
    write_logfile(line)


def log_error(msg: str) -> None:
    log_with_type("ERROR", RED + BOLD, msg)


def log_info(msg: str) -> None:
    log_with_type("INFO ", BLUE, msg)


def log_warning(msg: str) -> None:
    log_with_type("Warning:", YELLOW, msg)
