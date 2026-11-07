<h1 align="center">RuEn for Autodesk Fusion</h1>
<p align="center"><strong>Keep your Fusion shortcuts working in Russian.</strong><br>Use assigned keyboard shortcuts in Fusion 360 without switching away from the Russian keyboard layout.</p>

<p align="center"><a href="https://github.com/4FusionLab/RuEn/releases/latest"><strong>Download RuEn</strong></a> · <a href="README.ru.md">Русский</a> · <a href="https://github.com/4FusionLab/RuEn/issues">Report an issue</a></p>

RuEn is a **Fusion 360 add-in for Russian keyboard shortcuts** on macOS and Windows. It maps Russian-layout letter keys to their Latin counterparts for existing Autodesk Fusion hotkey assignments; your Fusion shortcut settings stay unchanged.

## How it works

RuEn reads registered shortcuts through `HotKey.List` and handles supported single-letter shortcuts, including modifier keys, while the Fusion `QTCanvas` is focused. It does not change shortcut assignments in Fusion.

Use **RuEn: обновить хоткеи** to refresh the mapping after editing Fusion shortcuts, or **RuEn: включить / выключить** to turn the filter on or off.

## Compatibility and limitations

- **macOS:** Apple Silicon.
- **Windows:** x64.
- **Supported shortcuts:** registered combinations with one Latin letter and optional modifiers.
- **Not supported:** symbol-based or multi-step shortcuts.

The keyboard filter relies on Fusion's internal `QTCanvas` class and Qt rather than a public Autodesk API. Future Fusion updates may affect compatibility.

## Installation

1. Download the [latest release](https://github.com/4FusionLab/RuEn/releases/latest): choose **universal** (both platforms), **macos** (Apple Silicon), or **windows** (x64). The universal package selects the appropriate native library automatically.
2. Extract the archive and keep the `RuEn` folder intact.
3. In Autodesk Fusion, open **Utilities → Add-Ins → Scripts and Add-Ins**, choose **+ → Script or add-in from device**, and select the `RuEn` folder.
4. Choose **RuEn → Run** and enable **Run on Startup** so the add-in starts with Fusion.
5. Use your existing assigned shortcuts with the Russian keyboard layout in the Design workspace.

**Upgrading from RuEnProbe?** Stop the old add-in, disable its startup setting, and remove its entry before adding RuEn. Do not run both versions together. The manifest identifier remains the same, and your Fusion shortcuts are preserved.

To uninstall, stop RuEn, disable **Run on Startup**, remove its entry from Fusion, and delete the extracted folder. If loading fails, check that the release archive matches your operating system and that the native library is alongside `RuEn.py`.

## For developers

Python code lives in [`RuEn/`](RuEn/); the native filter is in [`native/ruen_filter.cpp`](native/ruen_filter.cpp). `python scripts/package.py --version X.Y.Z` packages existing libraries into three versioned ZIP archives with SHA-256 checksums under `dist/` but does not build them. CI supplies `X.Y.Z` from GitVersion; the manifest inside each ZIP is updated without modifying the checked-in manifest. Build the macOS library with `scripts/build_macos.sh` and `QT_SDK` for Qt 6.8.3, or use `scripts/build_windows.ps1` with MSVC x64 and a compatible Qt 6.8.1 SDK. `experiments/native_filter_test.py` is a separate PySide experiment and is not included in the distribution.

## More Fusion 360 tools from 4FusionLab

[Perfora — parametric hole patterns](https://github.com/4FusionLab/Perfora) · [Selectra — select similar faces and edges](https://github.com/4FusionLab/Selectra) · [Ejix — extract solid volumes](https://github.com/4FusionLab/Ejix) · [Planara — planned surface flattening](https://github.com/4FusionLab/Planara)

[Release notes](RELEASE_NOTES.md) · [License](LICENSE) · [4FusionLab](https://github.com/4FusionLab)

<sub>Independent project, not affiliated with or endorsed by Autodesk.</sub>
