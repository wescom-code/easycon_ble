from enum import Enum

DOMAIN = "easycon_ble"

# Default AES Key used by the WeChat mini program
AES_KEY = b"210766f2405de886"

# GATT Service UUIDs
SERVICE_UUID = "fa879af4-d601-420c-b2b4-07ffb528dde3"
CHAR_WRITE_UUID = "b02eaeaa-f6bc-4a7e-bc94-f7b7fc8ded0b"
CHAR_NOTIFY_UUID = "10e2fde2-d7fe-4845-b3f3-a32010ebb095"

# Known manufacturer data filters for discovery
MANUFACTURER_FILTERS = {
    "5649": "Silicone Light/Night Light (e.g. KLT003)",
    "5749": "Lighting",
    "6549": "Smart Desk Lamp"
}

class CommandType(Enum):
    HANDSHAKE = "5011"
    QUERY_STATUS = "3004"
    POWER = "3221"
    BRIGHTNESS = "3227"
    MODE = "3226"
    RGB = "2001"
