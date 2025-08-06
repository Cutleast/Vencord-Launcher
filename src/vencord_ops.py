import glob
import os
import subprocess
import sys
import urllib.request
from pathlib import Path
from typing import NoReturn

from logging_utils import log_error, log_info, log_warning


def find_discord_appdir() -> Path | NoReturn:
    """
    Searches for the latest Discord app-* folder.

    Returns:
        Path | NoReturn:
            The path to the latest Discord app-* folder. Exits the program if not found.
    """

    localappdata = Path(os.environ.get("LOCALAPPDATA", ""))
    discord_dir = localappdata / "Discord"
    app_dirs = sorted(discord_dir.glob("app-*"), reverse=True)
    if not app_dirs:
        log_error("No Discord app-* folder found.")
        sys.exit(1)
    app_dir = app_dirs[0]
    log_info(f"Found Discord installation: {app_dir}")
    return app_dir


def is_vencord_present(app_dir: Path) -> bool:
    """
    Checks if Vencord is present in the Discord app-* folder.

    Args:
        app_dir (Path): The path to the Discord app-* folder.

    Returns:
        bool: True if Vencord is present, False otherwise.
    """

    resources_dir = app_dir / "resources"
    found = any(Path(f).exists() for f in glob.glob(str(resources_dir / "_app.asar")))
    log_info("Vencord status: " + ("Installed" if found else "Not installed"))
    return found


def ensure_vencord_cli(cli_path: Path) -> None:
    """
    Ensures that VencordInstallerCli.exe is present, exits the program if not.

    Args:
        cli_path (Path): The path to the VencordInstallerCli.exe file.
    """

    if cli_path.exists():
        return
    log_warning("VencordInstallerCli.exe not found. Downloading latest version...")
    url = "https://github.com/Vencord/Installer/releases/latest/download/VencordInstallerCli.exe"
    try:
        urllib.request.urlretrieve(url, str(cli_path))
        log_info("Downloaded VencordInstallerCli.exe successfully.")
    except Exception as e:
        log_error(f"Failed to download VencordInstallerCli.exe: {e}")
        sys.exit(1)


def update_vencord_cli(cli_path: Path) -> None:
    """
    Checks for updates for VencordInstallerCli.

    Args:
        cli_path (Path): The path to the VencordInstallerCli.exe file.
    """

    log_info("Checking for updates for VencordInstallerCli...")
    try:
        subprocess.run([str(cli_path), "-update-self"], check=True)
    except subprocess.CalledProcessError:
        log_warning(
            "VencordInstallerCli self-update failed or no update available (see above)."
        )


def install_openasar(cli_path: Path, branch: str) -> None:
    """
    Installs OpenAsar for Vencord.

    Args:
        cli_path (Path): The path to the VencordInstallerCli.exe file.
        branch (str): The branch to install OpenAsar for.
    """

    log_info(f"Installing OpenAsar for branch '{branch}'...")
    try:
        subprocess.run(
            [str(cli_path), "-install-openasar", "-branch", branch], check=True
        )
    except subprocess.CalledProcessError as e:
        log_error(f"Error installing OpenAsar: {e}")
        print("Failed to install OpenAsar. Please check manually.")
        sys.exit(1)


def install_vencord(cli_path: Path, branch: str) -> None:
    """
    Installs Vencord.

    Args:
        cli_path (Path): The path to the VencordInstallerCli.exe file.
        branch (str): The branch to install Vencord for.
    """

    log_info(f"Patching Discord ({branch})...")
    try:
        subprocess.run([str(cli_path), "-install", "-branch", branch], check=True)
    except subprocess.CalledProcessError as e:
        log_error(f"Error installing Vencord: {e}")
        print("Failed to install Vencord. Please check manually.")
        sys.exit(1)


def start_discord(app_dir: Path, minimized: bool) -> None:
    """
    Starts Discord.

    Args:
        app_dir (Path): The path to the Discord app-* folder.
        minimized (bool): Whether to start Discord minimized.
    """

    exe_path = app_dir / "Discord.exe"
    if not exe_path.exists():
        log_error("Discord.exe not found in latest app-* folder.")
        sys.exit(1)
    if minimized:
        log_info("Starting Discord minimized...")
        subprocess.Popen([str(exe_path), "--start-minimized"], close_fds=True)
        log_info("Discord started (minimized).")
    else:
        log_info("Starting Discord...")
        subprocess.Popen([str(exe_path)], close_fds=True)
        log_info("Discord started.")
