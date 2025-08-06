import sys
import time
from pathlib import Path
from typing import NoReturn

from autostart_utils import set_autostart
from config_utils import Config
from logging_utils import init_logfile, log_info
from vencord_ops import (
    ensure_vencord_cli,
    find_discord_appdir,
    install_openasar,
    install_vencord,
    is_vencord_present,
    start_discord,
    update_vencord_cli,
)

# Always use the folder where the exe (or script) is located
if getattr(sys, "frozen", False):
    basedir = Path(sys.executable).parent
    exe_path = Path(sys.executable)
else:
    basedir = Path(__file__).parent
    exe_path = Path(sys.argv[0])

LOGFILE: Path = basedir / "latest.log"
CONFIGFILE: Path = basedir / "config.json"
CLI_PATH: Path = basedir / "VencordInstallerCli.exe"


def main() -> NoReturn:
    init_logfile(LOGFILE)
    print()
    log_info("VencordChecker started.")

    config: Config = Config.load_config(CONFIGFILE)

    set_autostart(config.autostart, exe_path)

    discord_app_dir: Path = find_discord_appdir()

    if is_vencord_present(discord_app_dir):
        log_info("Vencord already present. Launching Discord...")
        start_discord(discord_app_dir, config.startdiscordminimized)
        print()
        sys.exit(0)
    else:
        log_info("Vencord not found. Proceeding with installation...")
        ensure_vencord_cli(CLI_PATH)
        update_vencord_cli(CLI_PATH)
        if config.openasar:
            install_openasar(CLI_PATH, config.branch)
        install_vencord(CLI_PATH, config.branch)
        time.sleep(1)
        log_info("Launching Discord after Vencord installation...")
        start_discord(discord_app_dir, config.startdiscordminimized)
        print()
        sys.exit(0)


if __name__ == "__main__":
    main()
