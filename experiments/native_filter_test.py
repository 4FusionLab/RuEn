import ctypes, os, pathlib, sys
os.environ['QT_QPA_PLATFORM']='offscreen'
base=pathlib.Path(os.environ['FUSION_FRAMEWORKS'])
for n in ('QtCore','QtGui','QtWidgets'):
    ctypes.CDLL(str(base/(n+'.framework')/n),mode=ctypes.RTLD_GLOBAL)
sys.path.insert(0,os.environ['PYSIDE_SITE'])
from PySide6.QtCore import QEvent, Qt, QCoreApplication
from PySide6.QtGui import QKeyEvent, QKeySequence, QShortcut
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit
app=QApplication([]); w=QWidget(); w.setFocusPolicy(Qt.FocusPolicy.StrongFocus); lay=QVBoxLayout(w); field=QLineEdit(); lay.addWidget(field); w.show(); app.processEvents(); w.activateWindow(); w.setFocus(); app.processEvents()
hits=[]; shortcut=QShortcut(QKeySequence('E'),w); shortcut.activated.connect(lambda: hits.append('E'))
shift_hits=[]; shifted=QShortcut(QKeySequence('Shift+E'),w); shifted.activated.connect(lambda: shift_hits.append('shift+E'))
unregistered=[]; other=QShortcut(QKeySequence('D'),w); other.activated.connect(lambda: unregistered.append('D'))
lib=ctypes.CDLL(str(pathlib.Path(__file__).resolve().parents[1]/'RuEnProbe/libruen_v2.dylib')); lib.ruen_enable.argtypes=[ctypes.c_char_p]; lib.ruen_enable.restype=ctypes.c_int; lib.ruen_disable.restype=ctypes.c_int
class Binding(ctypes.Structure):
 _fields_=[('key',ctypes.c_int),('modifiers',ctypes.c_uint)]
lib.ruen_set_bindings.argtypes=[ctypes.POINTER(Binding),ctypes.c_int]; lib.ruen_set_bindings.restype=ctypes.c_int
values=(Binding*2)(Binding(ord('E'),0), Binding(ord('E'),0x02000000)); assert lib.ruen_set_bindings(values,2)==2
assert lib.ruen_enable(b'QWidget')==1
for i in range(3):
 QCoreApplication.sendEvent(w,QKeyEvent(QEvent.Type.KeyPress,0x423,Qt.KeyboardModifier.NoModifier,'у')); app.processEvents()
assert hits==['E']*3, hits
QCoreApplication.sendEvent(w,QKeyEvent(QEvent.Type.KeyPress,0x423,Qt.KeyboardModifier.ShiftModifier,'У')); app.processEvents()
assert shift_hits==['shift+E'], shift_hits
QCoreApplication.sendEvent(w,QKeyEvent(QEvent.Type.KeyPress,0x412,Qt.KeyboardModifier.NoModifier,'в')); app.processEvents()
assert len(hits)==3 and len(shift_hits)==1 and not unregistered
assert lib.ruen_set_bindings(None,0)==0
QCoreApplication.sendEvent(w,QKeyEvent(QEvent.Type.KeyPress,0x423,Qt.KeyboardModifier.NoModifier,'у')); app.processEvents(); assert len(hits)==3
assert lib.ruen_set_bindings(values,2)==2
field.setFocus(); app.processEvents(); QCoreApplication.sendEvent(field,QKeyEvent(QEvent.Type.KeyPress,0x423,Qt.KeyboardModifier.NoModifier,'у')); assert field.text()=='у'; assert len(hits)==3
w.setFocus(); app.processEvents(); assert lib.ruen_disable()==1
QCoreApplication.sendEvent(w,QKeyEvent(QEvent.Type.KeyPress,0x423,Qt.KeyboardModifier.NoModifier,'у')); app.processEvents(); assert len(hits)==3
assert lib.ruen_disable()==0
print('PASS: repeated shortcuts, text input, disabled state')
