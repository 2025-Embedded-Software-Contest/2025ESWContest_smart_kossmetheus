from __future__ import annotations

import os
from typing import Optional

# Home Assistant Pyscript: Raspberry Pi 5 PWM Fan Control via sysfs
# Exposes two services:
# - pyscript.pi5_fan_set_percent(percent: int)
# - pyscript.pi5_fan_set_auto(enabled: bool)


def _find_hwmon_path() -> Optional[str]:
    base = "/sys/devices/platform/cooling_fan/hwmon"
    if not os.path.isdir(base):
        return None
    for entry in os.scandir(base):
        if entry.is_dir():
            return entry.path
    return None


def _write_int(path: str, value: int) -> None:
    with open(path, "w", encoding="utf-8") as f:
        f.write(str(value))


def _clamp(val: int, low: int, high: int) -> int:
    return max(low, min(high, val))


@service
def pi5_fan_set_percent(percent: int = None):
    """Set fan speed percentage (0-100). Disables auto mode."""
    if percent is None:
        log.error("pi5_fan_set_percent: percent is required")
        return
    percent = _clamp(int(percent), 0, 100)

    hwmon = _find_hwmon_path()
    if not hwmon:
        log.error("Pi5 fan hwmon path not found")
        return

    try:
        # Disable automatic control
        auto_path = os.path.join(hwmon, "pwm1_enable")
        _write_int(auto_path, 0)

        # Determine pwm range
        max_path = os.path.join(hwmon, "pwm1_max")
        try:
            with open(max_path, "r", encoding="utf-8") as f:
                pwm_max = int(f.read().strip())
        except FileNotFoundError:
            pwm_max = 255

        pwm_val = int(round(pwm_max * (percent / 100.0)))
        pwm_val = _clamp(pwm_val, 0, pwm_max)
        pwm_path = os.path.join(hwmon, "pwm1")
        _write_int(pwm_path, pwm_val)

        log.info(f"Pi5 fan set to {percent}% (pwm={pwm_val}/{pwm_max})")
    except Exception as exc:  # noqa: BLE001
        log.exception(f"Failed to set fan percent: {exc}")


@service
def pi5_fan_set_auto(enabled: bool = True):
    """Enable/disable automatic fan control by firmware."""
    hwmon = _find_hwmon_path()
    if not hwmon:
        log.error("Pi5 fan hwmon path not found")
        return

    try:
        auto_path = os.path.join(hwmon, "pwm1_enable")
        _write_int(auto_path, 1 if enabled else 0)
        log.info(f"Pi5 fan auto mode {'enabled' if enabled else 'disabled'}")
    except Exception as exc:  # noqa: BLE001
        log.exception(f"Failed to set auto mode: {exc}")


