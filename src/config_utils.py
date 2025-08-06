import sys
from pathlib import Path

import json5

from logging_utils import log_error, log_info, log_warning


def load_config(configfile_path: Path):
    CONFIGFILE = Path(configfile_path)
    if not CONFIGFILE.exists():
        log_error("config.json not found!")
        sys.exit(1)
    with open(CONFIGFILE, encoding="utf-8") as f:
        raw_config = json5.load(f)
    config = {k.lower(): v for k, v in raw_config.items()}
    if "branch" not in config:
        log_error("'branch' missing in config.json!")
        sys.exit(1)
    if "openasar" not in config:
        log_error("'OpenAsar' missing in config.json!")
        sys.exit(1)
    if "autostart" not in config:
        log_warning("'Autostart' not set in config.json! Default: False")
        config["autostart"] = False
    if "startdiscordminimized" not in config:
        log_warning("'StartDiscordMinimized' not set in config.json! Default: True")
        config["startdiscordminimized"] = True
    log_info(
        f"Loaded config. Using branch: {config['branch']} | "
        f"OpenAsar: {config['openasar']} | "
        f"Autostart: {config['autostart']} | "
        f"StartDiscordMinimized: {config['startdiscordminimized']}"
    )
    return (
        config["branch"],
        config["openasar"],
        config["autostart"],
        config["startdiscordminimized"],
    )
