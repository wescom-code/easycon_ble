import logging
import struct
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

_LOGGER = logging.getLogger(__name__)

class EasyconProtocol:
    """Implementation of the Easycon BLE protocol."""

    def __init__(self, key: bytes):
        self._key = key

    def _encrypt(self, plaintext: bytes) -> bytes:
        """Encrypt payload using AES-128-ECB with PKCS7 padding."""
        cipher = AES.new(self._key, AES.MODE_ECB)
        padded_data = pad(plaintext, AES.block_size)
        return cipher.encrypt(padded_data)

    def _decrypt(self, ciphertext: bytes) -> bytes:
        """Decrypt payload using AES-128-ECB with PKCS7 padding."""
        cipher = AES.new(self._key, AES.MODE_ECB)
        decrypted_padded = cipher.decrypt(ciphertext)
        try:
            return unpad(decrypted_padded, AES.block_size)
        except ValueError:
            _LOGGER.error("Padding error during decryption")
            return decrypted_padded # Return raw if padding is bad

    def pack_frame(self, payload_hex: str, encrypted: bool = True) -> bytes:
        """
        Pack and optionally encrypt a payload.
        """
        payload = bytes.fromhex(payload_hex)
        
        if encrypted:
            # PKCS7 padding
            pad_len = 16 - (len(payload) % 16)
            if pad_len == 0:
                pad_len = 16
            payload += bytes([pad_len] * pad_len)
            
            cipher = AES.new(self._key, AES.MODE_ECB)
            payload = cipher.encrypt(payload)
            header = b'\x55\xaa'
        else:
            header = b'\xfe\x01'
            
        length_bytes = struct.pack(">H", len(payload))
        return header + length_bytes + payload

    def unpack_frame(self, frame: bytes) -> tuple[bool, bytes]:
        """
        Unpack a BLE frame.
        Returns (is_encrypted, payload_bytes)
        """
        if len(frame) < 4:
            raise ValueError("Frame too short")
            
        header = frame[0:2]
        length = struct.unpack(">H", frame[2:4])[0]
        data = frame[4:4+length]
        
        if header == b'\x55\xaa':
            decrypted = self._decrypt(data)
            return True, decrypted
        elif header == b'\xfe\x01':
            return False, data
        else:
            raise ValueError(f"Unknown frame header: {header.hex()}")

    def cmd_handshake(self) -> bytes:
        """Generate handshake init command (Plaintext)"""
        return self.pack_frame("5011", encrypted=False)

    def cmd_query_status(self) -> bytes:
        """Generate status query command"""
        return self.pack_frame("3004", encrypted=False)

    def cmd_auth_response(self, random_hex: str) -> bytes:
        """Generate auth response (plaintext). random_hex must be 32 chars (16 bytes)."""
        return self.pack_frame(f"0100{random_hex}", encrypted=False)

    def cmd_power(self, state: bool, channel: int = 0) -> bytes:
        """
        Generate power command.
        state: True for ON, False for OFF
        KLT003 uses the unified property ID (0001) for power control instead of 32xx.
        """
        st_hex = "01" if state else "00"
        return self.pack_frame(f"0001{st_hex}", encrypted=False)

    def cmd_brightness(self, brightness: int) -> bytes:
        """
        Generate brightness command.
        brightness: 0-255 (app uses 0-100)
        KLT003 uses the unified property ID (1002).
        """
        br_hex = f"{brightness:02x}"
        return self.pack_frame(f"1002{br_hex}", encrypted=False)

    def cmd_color_temp(self, kelvin: int) -> bytes:
        """
        Generate color temperature command.
        KLT003 uses the unified property ID (3060) and expects 2 bytes of raw Kelvin.
        """
        k_hex = f"{kelvin:04x}"
        return self.pack_frame(f"3060{k_hex}", encrypted=False)

    def cmd_rgb(self, r: int, g: int, b: int) -> bytes:
        """
        Generate RGB command.
        r, g, b: 0-255
        """
        r_hex = f"{r:02x}"
        g_hex = f"{g:02x}"
        b_hex = f"{b:02x}"
        return self.pack_frame(f"2001{r_hex}{g_hex}{b_hex}", encrypted=False)

    def parse_status_response(self, payload: bytes) -> dict:
        """
        Parse a 3005 status response payload.
        The format is: 30 05 [cnt] [block1] [block2] ...
        Each block is: [total_len] [type:2 bytes] [value]
        """
        result = {}
        if len(payload) < 3:
            return result
            
        cnt = payload[2]
        idx = 3
        
        for _ in range(cnt):
            if idx >= len(payload):
                break
            
            block_len = payload[idx]
            if block_len < 3:
                break
                
            block_type = payload[idx+1:idx+3].hex()
            block_val = payload[idx+3:idx+block_len]
            
            if block_type == "0001" and len(block_val) >= 1:
                result["power"] = block_val[0] == 1
            elif block_type == "1002" and len(block_val) >= 1:
                result["brightness"] = block_val[0]
            elif block_type == "3060" and len(block_val) >= 2:
                result["color_temp"] = int.from_bytes(block_val[:2], "big")
                
            idx += block_len
            
        return result
