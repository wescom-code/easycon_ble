"""Coordinator for Easycon BLE connection."""
import asyncio
import logging
import struct
from datetime import timedelta
from typing import Any

from bleak import BleakClient, BleakError
from bleak.backends.device import BLEDevice

from bleak_retry_connector import establish_connection
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import AES_KEY, CHAR_NOTIFY_UUID, CHAR_WRITE_UUID, DOMAIN
from .protocol import EasyconProtocol

_LOGGER = logging.getLogger(__name__)

class EasyconCoordinator(DataUpdateCoordinator):
    """Manage BLE connection and state for Easycon."""

    def __init__(self, hass: HomeAssistant, ble_device: BLEDevice) -> None:
        """Init the coordinator."""
        self.ble_device = ble_device
        self._client: BleakClient | None = None
        self.protocol = EasyconProtocol(AES_KEY)
        self.is_connected = False
        self._buffer = bytearray()
        
        super().__init__(
            hass,
            _LOGGER,
            name=f"{DOMAIN}_{ble_device.address}",
            update_interval=timedelta(seconds=60), # Poll occasionally
        )

    async def connect(self) -> bool:
        """Establish BLE connection and perform handshake."""
        if self._client and self._client.is_connected:
            return True

        try:
            self._client = await establish_connection(
                BleakClient,
                self.ble_device,
                self.ble_device.name or self.ble_device.address,
            )
            self.is_connected = True
            self._buffer.clear()
            
            # Start notifications
            await self._client.start_notify(
                CHAR_NOTIFY_UUID, self._notification_handler
            )

            # Wait for notifications to settle
            await asyncio.sleep(0.5)

            # KLT003 does not support 5011 handshake, it drops connection (Error 133).
            # We skip it and go straight to status polling.
            
            return True
        except Exception as e:
            _LOGGER.error("Failed to connect to %s: %s", self.ble_device.address, e)
            self.is_connected = False
            self._client = None
            return False

    async def disconnect(self):
        """Disconnect BLE connection."""
        if self._client and self._client.is_connected:
            await self._client.stop_notify(CHAR_NOTIFY_UUID)
            await self._client.disconnect()
        self.is_connected = False
        self._client = None

    def _notification_handler(self, sender: Any, data: bytearray) -> None:
        """Handle incoming BLE notifications."""
        self._buffer.extend(data)
        while len(self._buffer) >= 4:
            if self._buffer[0:2] not in (b'\xfe\x01', b'\x55\xaa'):
                _LOGGER.warning("Unknown frame header in buffer: %s, skipping 1 byte", self._buffer[0:2].hex())
                self._buffer.pop(0)
                continue
                
            length = struct.unpack(">H", self._buffer[2:4])[0]
            total_expected = 4 + length
            
            if len(self._buffer) < total_expected:
                # We don't have the full frame yet.
                # However, check if a NEW frame header appeared before this one finished!
                # This happens because the cheap BLE chip drops the 2nd MTU packet on physical touch.
                next_fe = self._buffer.find(b'\xfe\x01', 1)
                next_55 = self._buffer.find(b'\x55\xaa', 1)
                
                next_header = -1
                if next_fe != -1 and next_55 != -1:
                    next_header = min(next_fe, next_55)
                else:
                    next_header = max(next_fe, next_55)
                    
                if next_header != -1:
                    _LOGGER.warning("Frame truncated! Expected %d bytes but found new header at offset %d. Dropping %d bytes.", total_expected, next_header, next_header)
                    self._buffer = self._buffer[next_header:]
                    continue # Restart loop with new header
                
                break # Wait for more data
                
            # If we reach here and a new header is inside our complete frame, we also need to handle it.
            # Wait, if we have a "complete" frame but it actually contains a new header inside it, 
            # it means the previous frame was truncated and we just received enough bytes from the new frame to satisfy the old frame's length!
            next_fe = self._buffer[:total_expected].find(b'\xfe\x01', 1)
            next_55 = self._buffer[:total_expected].find(b'\x55\xaa', 1)
            next_header = -1
            if next_fe != -1 and next_55 != -1:
                next_header = min(next_fe, next_55)
            else:
                next_header = max(next_fe, next_55)
                
            if next_header != -1:
                _LOGGER.warning("Corrupted frame! Found new header at offset %d inside expected %d bytes. Dropping truncated prefix.", next_header, total_expected)
                self._buffer = self._buffer[next_header:]
                continue
                
            frame = bytes(self._buffer[:total_expected])
            self._buffer = self._buffer[total_expected:]
            
            try:
                is_encrypted, payload = self.protocol.unpack_frame(frame)
                payload_hex = payload.hex()
                _LOGGER.debug("Unpacked payload (encrypted=%s): %s", is_encrypted, payload_hex)
                
                # Handle auth request from device
                if payload_hex.startswith("0102"):
                    # The device sends 0102 + 16 bytes challenge (32 hex chars)
                    # We MUST echo back the EXACT same 16 bytes challenge in our 0100 response!
                    challenge_hex = payload_hex[4:36]
                    if len(challenge_hex) == 32:
                        _LOGGER.debug("Received 0102 auth request, echoing challenge: %s", challenge_hex)
                        auth_cmd = self.protocol.cmd_auth_response(challenge_hex)
                        self.hass.async_create_task(
                            self.async_send_command(auth_cmd)
                        )
                    else:
                        _LOGGER.error("Auth request 0102 payload too short: %s", payload_hex)
                
                elif payload_hex.startswith("3005"):
                    status = self.protocol.parse_status_response(payload)
                    if status:
                        if self.data is None:
                            self.data = {}
                        self.data.update(status)
                        self.async_set_updated_data(self.data)
            except Exception as e:
                _LOGGER.error("Failed to parse frame: %s", e)

    async def _async_update_data(self):
        """Update data via polling."""
        if not self.is_connected:
            connected = await self.connect()
            if not connected:
                raise UpdateFailed("Failed to connect")

        try:
            # Clear buffer before querying to prevent partial frames from previous queries
            # from causing massive buffer desyncs if the device dropped a packet.
            self._buffer.clear()
            cmd = self.protocol.cmd_query_status()
            await self._client.write_gatt_char(CHAR_WRITE_UUID, cmd, response=True)
            # The response will come via notification handler which updates self.data
            return self.data
        except Exception as e:
            self.is_connected = False
            raise UpdateFailed(f"Failed to communicate: {e}") from e

    async def async_send_command(self, payload: bytes, response: bool = True):
        """Send a command to the device."""
        if not self.is_connected:
            if not await self.connect():
                _LOGGER.error("Not connected, cannot send command")
                return

        try:
            await self._client.write_gatt_char(CHAR_WRITE_UUID, payload, response=response)
        except Exception as e:
            _LOGGER.error("Error sending command: %s", e)
            self.is_connected = False
