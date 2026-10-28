"""Translate registered Fusion hotkeys on the Russian keyboard layout."""
import ctypes
import importlib.util
import os
import sys
import traceback
import adsk.core

ID = 'RuEnToggle'
REFRESH_ID = 'RuEnRefresh'
_handlers = []
_library = None
_enabled = False


class Binding(ctypes.Structure):
    _fields_ = [('key', ctypes.c_int), ('modifiers', ctypes.c_uint)]


def _read_bindings():
    path = os.path.join(os.path.dirname(__file__), 'hotkeys.py')
    spec = importlib.util.spec_from_file_location('ruen_hotkeys', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    raw = adsk.core.Application.get().executeTextCommand('HotKey.List')
    return module.extract_bindings(raw)


def _refresh():
    values = _read_bindings()
    entries = (Binding * len(values))(*(Binding(key, modifiers) for key, modifiers in values))
    count = _get_library().ruen_set_bindings(entries, len(values))
    if count < 0:
        raise RuntimeError('Не удалось обновить список хоткеев.')
    return count


def _get_library():
    global _library
    if _library is None:
        if sys.platform != 'darwin':
            raise RuntimeError('Поддерживается только macOS.')
        lib = ctypes.CDLL(os.path.join(os.path.dirname(__file__), 'libruen_v2.dylib'))
        lib.ruen_enable.argtypes = [ctypes.c_char_p]
        lib.ruen_enable.restype = ctypes.c_int
        lib.ruen_disable.argtypes = []
        lib.ruen_disable.restype = ctypes.c_int
        lib.ruen_set_bindings.argtypes = [ctypes.POINTER(Binding), ctypes.c_int]
        lib.ruen_set_bindings.restype = ctypes.c_int
        _library = lib
    return _library


def _enable():
    global _enabled
    result = _get_library().ruen_enable(b'QTCanvas')
    if result < 0:
        raise RuntimeError('Фильтр должен запускаться в главном потоке Fusion.')
    _enabled = True


def _disable():
    global _enabled
    if _library is not None and _enabled:
        if _library.ruen_disable() < 0:
            raise RuntimeError('Фильтр должен останавливаться в главном потоке Fusion.')
    _enabled = False


class Execute(adsk.core.CommandEventHandler):
    def notify(self, args):
        ui = adsk.core.Application.get().userInterface
        try:
            if _enabled:
                _disable(); ui.messageBox('RuEn выключен.')
            else:
                count = _refresh(); _enable(); ui.messageBox(f'RuEn включён. Буквенных сочетаний: {count}.')
        except Exception:
            ui.messageBox('RuEn: ошибка:\n' + traceback.format_exc())


class Created(adsk.core.CommandCreatedEventHandler):
    def notify(self, args):
        handler = Execute()
        args.command.execute.add(handler)
        _handlers.append(handler)


class Refresh(adsk.core.CommandEventHandler):
    def notify(self, args):
        ui = adsk.core.Application.get().userInterface
        try:
            ui.messageBox(f'RuEn: обновлено сочетаний: {_refresh()}.')
        except Exception:
            ui.messageBox('RuEn: ошибка чтения хоткеев:\n' + traceback.format_exc())


class RefreshCreated(adsk.core.CommandCreatedEventHandler):
    def notify(self, args):
        handler = Refresh()
        args.command.execute.add(handler)
        _handlers.append(handler)


def run(context):
    ui = adsk.core.Application.get().userInterface
    try:
        _refresh()
        _enable()
        definition = ui.commandDefinitions.addButtonDefinition(ID, 'RuEn: включить / выключить', 'Включить или выключить поддержку русской раскладки')
        handler = Created()
        definition.commandCreated.add(handler)
        _handlers.append(handler)
        ui.allToolbarPanels.itemById('SolidScriptsAddinsPanel').controls.addCommand(definition)
        refresh = ui.commandDefinitions.addButtonDefinition(REFRESH_ID, 'RuEn: обновить хоткеи', 'Прочитать текущие сочетания Fusion')
        refresh_handler = RefreshCreated()
        refresh.commandCreated.add(refresh_handler)
        _handlers.append(refresh_handler)
        ui.allToolbarPanels.itemById('SolidScriptsAddinsPanel').controls.addCommand(refresh)
    except Exception:
        _disable()
        panel = ui.allToolbarPanels.itemById('SolidScriptsAddinsPanel')
        for command_id in (ID, REFRESH_ID):
            control = panel.controls.itemById(command_id)
            if control:
                control.deleteMe()
            definition = ui.commandDefinitions.itemById(command_id)
            if definition:
                definition.deleteMe()
        _handlers.clear()
        raise


def stop(context):
    _disable()
    ui = adsk.core.Application.get().userInterface
    panel = ui.allToolbarPanels.itemById('SolidScriptsAddinsPanel')
    for command_id in (ID, REFRESH_ID):
        control = panel.controls.itemById(command_id)
        if control:
            control.deleteMe()
        definition = ui.commandDefinitions.itemById(command_id)
        if definition:
            definition.deleteMe()
    _handlers.clear()
