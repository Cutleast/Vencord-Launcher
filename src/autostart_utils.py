import winreg
from pathlib import Path

from logging_utils import log_info, log_warning


def set_autostart(
    enabled: bool, exe_path: Path, reg_name: str = "VencordLauncher"
) -> None:
    log_info(f"set_autostart aufgerufen: enabled={enabled}, exe_path={exe_path}")
    try:
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Run",
            0,
            winreg.KEY_SET_VALUE,
        )
        if enabled:
            log_info("Enabling Autostart (visible in Task Manager)...")
            winreg.SetValueEx(key, reg_name, 0, winreg.REG_SZ, f'"{exe_path}"')
            log_info("Autostart entry added or updated.")
        else:
            try:
                winreg.DeleteValue(key, reg_name)
                log_info("Autostart entry removed.")
            except FileNotFoundError:
                log_info("No Autostart entry found, nothing to remove.")
        winreg.CloseKey(key)
    except Exception as e:
        log_warning(f"Failed to update Autostart entry: {e}")
