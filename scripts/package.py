"""Create the three distributable archives from the checked-in binaries."""
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

root = Path(__file__).resolve().parents[1]
out = root / 'dist'
out.mkdir(exist_ok=True)
common = ['RuEn.py', 'RuEn.manifest', 'hotkeys.py']
platforms = {'universal': ['libruen_v2.dylib', 'ruen_filter.dll'],
             'macos': ['libruen_v2.dylib'], 'windows': ['ruen_filter.dll']}
for platform, libraries in platforms.items():
    with ZipFile(out / f'RuEn-1.0.0-{platform}.zip', 'w', ZIP_DEFLATED) as archive:
        for name in common + libraries:
            archive.write(root / 'RuEn' / name, 'RuEn/' + name)
        for name in ('README.md', 'LICENSE', 'RELEASE_NOTES.md'):
            archive.write(root / name, name)
