"""Config flow for Easycon integration."""
import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.components.bluetooth import (
    BluetoothServiceInfoBleak,
    async_discovered_service_info,
)
from homeassistant.const import CONF_ADDRESS, CONF_NAME
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers import selector

from .const import DOMAIN, MANUFACTURER_FILTERS
from .devices import get_model_name

_LOGGER = logging.getLogger(__name__)

class EasyconConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Easycon."""

    VERSION = 1
    _name_cache: dict[str, str] = {}

    def __init__(self):
        """Initialize the config flow."""
        self._discovery_info: BluetoothServiceInfoBleak | None = None
        self._discovered_devices: dict[str, BluetoothServiceInfoBleak] = {}

    async def async_step_bluetooth(
        self, discovery_info: BluetoothServiceInfoBleak
    ) -> FlowResult:
        """Handle the bluetooth discovery step."""
        _LOGGER.debug("Discovered bluetooth device: %s", discovery_info.as_dict())
        await self.async_set_unique_id(discovery_info.address)
        self._abort_if_unique_id_configured()

        # Check if it matches our manufacturer data filters
        is_easycon = False
        for mfg_id, mfg_data in discovery_info.manufacturer_data.items():
            # Usually the filter (e.g. 4956) is in the first 2 bytes of the payload or it is the manufacturer ID
            # In hex, 4956 is 0x4956. We'll check if the hex string representation is in our known list.
            mfg_id_hex = f"{mfg_id:04x}"
            if mfg_id_hex in MANUFACTURER_FILTERS:
                is_easycon = True
                break
            
            # Sometimes it's in the data payload
            data_hex = mfg_data.hex()
            for known_filter in MANUFACTURER_FILTERS:
                if data_hex.startswith(known_filter):
                    is_easycon = True
                    break

        if not is_easycon:
            # Check by name just in case
            if discovery_info.name and (discovery_info.name.startswith("KLT") or "Easycon" in discovery_info.name):
                is_easycon = True

        if not is_easycon:
            return self.async_abort(reason="not_supported")

        self._discovery_info = discovery_info
        
        # Try to pre-warm the cache from the initial bluetooth discovery
        self._get_device_name(discovery_info)
        
        return await self.async_step_bluetooth_confirm()

    async def async_step_bluetooth_confirm(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Confirm discovery."""
        if user_input is not None:
            return self.async_create_entry(
                title=self._discovery_info.name or "EasyCon BLE",
                data={
                    CONF_ADDRESS: self._discovery_info.address,
                    CONF_NAME: self._discovery_info.name or "EasyCon BLE",
                },
            )

        self._set_confirm_only()
        return self.async_show_form(
            step_id="bluetooth_confirm",
            description_placeholders={"name": self._discovery_info.name},
        )

    def _get_device_name(self, info: BluetoothServiceInfoBleak) -> str:
        """Extract or retrieve the cached device name."""
        if info.address in self._name_cache:
            return self._name_cache[info.address]

        import re
        is_easycon = False
        
        # Try to extract from manufacturer data
        for mfg_id, mfg_data in info.manufacturer_data.items():
            mfg_id_hex = f"{mfg_id:04x}"
            if mfg_id_hex in MANUFACTURER_FILTERS:
                is_easycon = True
            data_hex = mfg_data.hex()
            for known_filter in MANUFACTURER_FILTERS:
                if data_hex.startswith(known_filter):
                    is_easycon = True

            # EasyCon devices use formats like KLT003, ALMD01, BSL009
            match = re.search(b'([A-Za-z]{3,4}\\d{2,3})', mfg_data)
            if match:
                product_id = match.group(1).decode('ascii').upper()
                final_name = get_model_name(product_id)
                self._name_cache[info.address] = final_name
                return final_name
        
        # Try to extract from the device name directly (sometimes OS sets it)
        if info.name:
            if info.name.startswith("KLT") or "EasyCon" in info.name or "Easycon" in info.name:
                is_easycon = True
            match = re.search(r'([A-Za-z]{3,4}\d{2,3})', info.name)
            if match:
                product_id = match.group(1).upper()
                final_name = get_model_name(product_id)
                self._name_cache[info.address] = final_name
                return final_name

        # If the device has a valid name that isn't just its MAC address, use it.
        if info.name and info.name.upper() != info.address.upper() and info.name.upper() != "UNKNOWN":
            self._name_cache[info.address] = info.name
            return info.name
        
        return "EasyCon BLE Device" if is_easycon else "Unknown"

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the user step to pick discovered device."""
        if user_input is not None:
            address = user_input[CONF_ADDRESS]
            discovery_info = self._discovered_devices.get(address)
            
            await self.async_set_unique_id(address, raise_on_progress=False)
            self._abort_if_unique_id_configured()
            
            if discovery_info:
                name = self._get_device_name(discovery_info)
            else:
                name = "Manual EasyCon Device"
                
            final_name = name or address
            
            return self.async_create_entry(
                title=final_name,
                data={
                    CONF_ADDRESS: address,
                    CONF_NAME: final_name,
                },
            )

        current_addresses = self._async_current_ids()
        for discovery_info in async_discovered_service_info(self.hass):
            address = discovery_info.address
            if address in current_addresses:
                continue

            # To help with debugging and manual addition, we show all discovered devices
            # Non-EasyCon devices will show as 'Unknown' or their true names, while
            # EasyCon devices without parsed names will fallback safely.
            self._discovered_devices[address] = discovery_info

        if not self._discovered_devices:
            return self.async_abort(reason="no_devices_found")

        # Sort devices by RSSI (signal strength) so the closest ones appear first
        sorted_devices = sorted(
            self._discovered_devices.values(),
            key=lambda device: device.rssi,
            reverse=True
        )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_ADDRESS): selector.SelectSelector(
                        selector.SelectSelectorConfig(
                            options=[
                                selector.SelectOptionDict(
                                    value=info.address,
                                    label=f"{self._get_device_name(info)} ({info.address}) [RSSI: {info.rssi}]"
                                )
                                for info in sorted_devices
                            ],
                            mode=selector.SelectSelectorMode.DROPDOWN,
                            custom_value=True,
                        )
                    )
                }
            ),
        )
