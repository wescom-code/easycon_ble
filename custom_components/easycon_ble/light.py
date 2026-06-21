"""Light platform for Easycon integration."""
from typing import Any

from homeassistant.components.light import (
    ATTR_BRIGHTNESS,
    ATTR_COLOR_TEMP_KELVIN,
    ATTR_RGB_COLOR,
    ColorMode,
    LightEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import EasyconCoordinator


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the light platform."""
    coordinator: EasyconCoordinator = hass.data[DOMAIN][entry.entry_id]
    
    # KLT003 and most single-channel lights use channel 0 (0-indexed).
    async_add_entities([EasyconLight(coordinator, entry.title, channel=0)])


class EasyconLight(CoordinatorEntity, LightEntity):
    """Representation of an Easycon Light."""

    def __init__(self, coordinator: EasyconCoordinator, name: str, channel: int) -> None:
        """Initialize the light."""
        super().__init__(coordinator)
        self._mac = coordinator.ble_device.address
        self._channel = channel
        self._original_name = name
        self._attr_unique_id = f"easycon_ble_{self._mac}_{channel}"
        self._attr_has_entity_name = True
        self._attr_name = f"Channel {channel}" if channel > 0 else None
        
        # KLT003 is a CCT (Color Temp) + Brightness light.
        self._attr_supported_color_modes = {ColorMode.COLOR_TEMP}
        self._attr_color_mode = ColorMode.COLOR_TEMP
        self._attr_min_color_temp_kelvin = 2000
        self._attr_max_color_temp_kelvin = 4000

    @property
    def device_info(self) -> DeviceInfo:
        """Return device information about this EasyCon device."""
        from homeassistant.helpers.device_registry import CONNECTION_BLUETOOTH
        return DeviceInfo(
            identifiers={(DOMAIN, self._mac)},
            name=self.coordinator.name or self._original_name,
            manufacturer="EasyCon",
            model=self._original_name or "Smart BLE Light",
            connections={(CONNECTION_BLUETOOTH, self._mac)}
        )

    @property
    def is_on(self) -> bool:
        """Return true if light is on."""
        if self.coordinator.data:
            return self.coordinator.data.get('power', False)
        return False

    @property
    def brightness(self) -> int | None:
        """Return the brightness of the light (0-255)."""
        if self.coordinator.data:
            # Device reports 0-100, scale to 0-255
            val = self.coordinator.data.get('brightness', 0)
            return int(val * 255 / 100)
        return None

    @property
    def color_temp_kelvin(self) -> int | None:
        """Return the color temperature in Kelvin."""
        if self.coordinator.data:
            return self.coordinator.data.get('color_temp')
        return None

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the light on."""
        import asyncio
        commands_sent = 0
        
        # 1. Turn on power only if it's currently off, OR if there are no kwargs (just a toggle ON)
        if not self.is_on or not kwargs:
            cmd = self.coordinator.protocol.cmd_power(True, self._channel)
            await self.coordinator.async_send_command(cmd)
            commands_sent += 1

        # 2. Set brightness if requested
        if ATTR_BRIGHTNESS in kwargs:
            if commands_sent > 0:
                await asyncio.sleep(0.05) # Tiny delay to prevent BLE buffer overflow
            br_100 = int(kwargs[ATTR_BRIGHTNESS] * 100 / 255)
            cmd_br = self.coordinator.protocol.cmd_brightness(br_100)
            await self.coordinator.async_send_command(cmd_br, response=False)
            commands_sent += 1

        # 3. Set color temp if requested
        if ATTR_COLOR_TEMP_KELVIN in kwargs:
            if commands_sent > 0:
                await asyncio.sleep(0.05)
            kelvin = kwargs[ATTR_COLOR_TEMP_KELVIN]
            k_min = self.min_color_temp_kelvin
            k_max = self.max_color_temp_kelvin
            k_clamped = max(k_min, min(k_max, kelvin))
            
            # KLT003 directly accepts raw Kelvin values
            cmd_ct = self.coordinator.protocol.cmd_color_temp(k_clamped)
            await self.coordinator.async_send_command(cmd_ct, response=False)

        # Optimistically update state
        if self.coordinator.data is None:
            self.coordinator.data = {}
        self.coordinator.data['power'] = True
        if ATTR_BRIGHTNESS in kwargs:
            self.coordinator.data['brightness'] = br_100
        if ATTR_COLOR_TEMP_KELVIN in kwargs:
            self.coordinator.data['color_temp'] = k_clamped
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the light off."""
        cmd = self.coordinator.protocol.cmd_power(False, self._channel)
        await self.coordinator.async_send_command(cmd)
        
        # Optimistically update state
        if self.coordinator.data is None:
            self.coordinator.data = {}
        self.coordinator.data['power'] = False
        self.async_write_ha_state()
