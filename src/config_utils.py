from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import json5

from logging_utils import log_error, log_info


@dataclass
class Config:
    """Dataclass for app configuration."""

    branch: str
    """Discord branch to patch: stable, ptb or canary."""

    openasar: str
    """Whether to install OpenAsar."""

    autostart: bool = False
    """Whether to enable autostart of this app and therefore Discord."""

    startdiscordminimized: bool = True
    """Whether to start Discord minimized."""

    @staticmethod
    def load_config(configfile_path: Path) -> Config:
        CONFIGFILE = Path(configfile_path)
        if not CONFIGFILE.exists():
            log_error("config.json not found!")
            sys.exit(1)

        with open(CONFIGFILE, encoding="utf-8") as f:
            raw_config: dict[str, Any] = json5.load(f)

        raw_config = {k.lower(): v for k, v in raw_config.items()}

        config = Config(**raw_config)
        log_info(
            f"Loaded config. Using branch: {config.branch} | "
            f"OpenAsar: {config.openasar} | "
            f"Autostart: {config.autostart} | "
            f"StartDiscordMinimized: {config.startdiscordminimized}"
        )

        return config
