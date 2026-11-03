"""Extract single-letter Fusion hotkeys in platform-specific Qt modifier form."""
import json
import sys

_MODIFIERS = {'shift': 0x02000000, 'command': 0x04000000,
              'alt': 0x08000000, 'control': 0x10000000}


def extract_bindings(raw, platform=None):
    platform = platform or sys.platform
    modifiers_map = dict(_MODIFIERS)
    if platform == "win32":
        modifiers_map["control"] = 0x04000000
        modifiers_map["ctrl"] = 0x04000000
        modifiers_map["meta"] = 0x10000000
        modifiers_map["win"] = 0x10000000
        modifiers_map.pop("command")
    document = json.loads(raw)
    if not isinstance(document, dict) or not isinstance(document.get('hotkeys'), list):
        raise ValueError('Неверный формат списка хоткеев Fusion')
    bindings = set()
    for entry in document['hotkeys']:
        if not isinstance(entry, dict) or not entry.get('commands'):
            continue
        sequence = entry.get('hotkey_sequence')
        if not isinstance(sequence, str):
            continue
        parts = sequence.lower().split('+')
        if not parts or len(parts[-1]) != 1 or parts[-1] not in 'abcdefghijklmnopqrstuvwxyz':
            continue
        modifiers = parts[:-1]
        if len(set(modifiers)) != len(modifiers) or any(mod not in modifiers_map for mod in modifiers):
            continue
        flags = 0
        for mod in modifiers:
            flags |= modifiers_map[mod]
        bindings.add((ord(parts[-1].upper()), flags))
    return sorted(bindings)
