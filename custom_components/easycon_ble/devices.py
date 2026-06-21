import json
import os

_DEVICES_FILE = os.path.join(os.path.dirname(__file__), 'devices.json')
_DEVICES_CACHE = None

def get_device_info(product_id: str) -> dict:
    """Return device info (name and type) from the devices.json dictionary."""
    global _DEVICES_CACHE
    if _DEVICES_CACHE is None:
        try:
            with open(_DEVICES_FILE, 'r', encoding='utf-8') as f:
                _DEVICES_CACHE = json.load(f)
        except Exception:
            _DEVICES_CACHE = {}
    
    return _DEVICES_CACHE.get(product_id, {})

def get_model_name(product_id: str) -> str:
    """Return a combined model string like 'KLT003 (酷毙灯)'."""
    info = get_device_info(product_id)
    if info and info.get('name'):
        return f"{product_id} ({info['name']})"
    return product_id
