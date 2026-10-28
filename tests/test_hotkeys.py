import importlib.util
import json
import pathlib
import unittest

spec = importlib.util.spec_from_file_location('hotkeys', pathlib.Path(__file__).resolve().parents[1] / 'RuEnProbe' / 'hotkeys.py')
hotkeys = importlib.util.module_from_spec(spec)
spec.loader.exec_module(hotkeys)

class HotkeysTest(unittest.TestCase):
    def entry(self, sequence, commands=None):
        return {'hotkey_sequence': sequence, 'commands': commands if commands is not None else [{'command_id': 'someCommand'}]}
    def test_bound_letters_and_mac_modifiers(self):
        data={'hotkeys':[self.entry('e'), self.entry('shift+command+z'), self.entry('control+alt+a'), self.entry('e')]}
        self.assertEqual(hotkeys.extract_bindings(json.dumps(data)), [(65,0x18000000),(69,0),(90,0x06000000)])
    def test_unsupported_and_unassigned_are_ignored(self):
        data={'hotkeys':[self.entry('command+/',[{}]),self.entry('f1',[{}]),self.entry('shift+shift+a',[{}]),self.entry('unknown+a',[{}]),self.entry('x',[]), {'file_version':'2'}]}
        self.assertEqual(hotkeys.extract_bindings(json.dumps(data)), [])
    def test_invalid_data_fails_closed(self):
        for raw in ('{}','{"hotkeys": null}','[]','not json'):
            with self.assertRaises(ValueError): hotkeys.extract_bindings(raw)

if __name__=='__main__': unittest.main()
