"""Support for locks through the SmartThings cloud API."""
from __future__ import annotations


from collections.abc import Sequence
from typing import Any

from .pysmartthings import Attribute, Capability

from homeassistant.components.lock import LockEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback


ST_CMD_LOCK = "lock"
ST_CMD_UNLOCK = "unlock"

from .common import *

from .lock import ST_LOCK_ATTR_MAP

import logging
_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Add switches for a config entry."""
    broker = hass.data[DOMAIN][DATA_BROKERS][config_entry.entry_id]
    entities = []
    settings = SettingManager.get_capa_settings(broker, Platform.LOCK)
    for s in settings:
        _LOGGER.debug("cap setting : " + str(s[1]))
        entities.append(SmartThingsLock_custom(hass=hass, setting=s))

    async_add_entities(entities)


class SmartThingsLock_custom(SmartThingsEntity_custom, LockEntity):
    def __init__(self, hass, setting) -> None:
        super().__init__(hass, platform=Platform.LOCK, setting=setting)

    async def async_lock(self, **kwargs: Any) -> None:
        """Lock the device."""
        await self.send_command(Platform.LOCK, self.get_command(Platform.LOCK, {ST_CMD_LOCK: ST_CMD_LOCK}).get(ST_CMD_LOCK), self.get_argument(Platform.LOCK, {ST_CMD_LOCK: []}).get(ST_CMD_LOCK, []))

    async def async_unlock(self, **kwargs: Any) -> None:
        """Unlock the device."""
        await self.send_command(Platform.LOCK, self.get_command(Platform.LOCK, {ST_CMD_UNLOCK: ST_CMD_UNLOCK}).get(ST_CMD_UNLOCK), self.get_argument(Platform.LOCK, {ST_CMD_UNLOCK: []}).get(ST_CMD_UNLOCK, []))

    @property
    def is_locked(self) -> bool | None:
        """Return true if lock is locked."""
        # Current lock status value from device (e.g., "locked"/"unlocked")
        value = self.get_attr_value(Platform.LOCK, CONF_STATE)
        # Expected values that represent the locked state from YAML config.
        # Support both keys: "locked_state" (new) and "lock_state" (legacy/example).
        locked_state = self.get_attr_value(Platform.LOCK, "locked_state")
        if locked_state is None:
            locked_state = self.get_attr_value(Platform.LOCK, "lock_state")

        # If we don't have a current value yet, report unknown
        if value is None:
            return None

        # Handle misconfiguration or missing setting defensively
        if locked_state is None:
            # Fallback to common defaults if not configured
            return value in ("locked", True, "on")

        # If configured as a list (recommended), do membership check
        if isinstance(locked_state, list):
            return value in locked_state

        # If configured as a single value, compare directly
        return value == locked_state

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return device specific state attributes."""
        
        conf = self._capability[Platform.LOCK].get(CONF_STATE, [])
        status = self.get_attr_status(conf, Platform.LOCK)
        if status.value:
            self._extra_state_attributes["lock_state"] = status.value
        if isinstance(status.data, dict):
            for st_attr, ha_attr in ST_LOCK_ATTR_MAP.items():
                if (data_val := status.data.get(st_attr)) is not None:
                    self._extra_state_attributes[ha_attr] = data_val
        return self._extra_state_attributes
