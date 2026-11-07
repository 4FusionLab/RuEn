"""Build three RuEn distributions from checked-in native binaries.

Pass --version from GitVersion in CI to embed the numeric version in Fusion's
manifest without changing a checked-in manifest or creating Git tags.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
from zipfile import ZIP_DEFLATED, ZipFile

root = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--version', help='GitVersion MajorMinorPatch for release packages')
args = parser.parse_args()
license_file = root / 'LICENSE'
if not license_file.is_file() or not license_file.read_text(encoding='utf-8').strip():
    parser.error('Distribution license must exist and be nonempty')
manifest_file = root / 'RuEn/RuEn.manifest'
manifest = json.loads(manifest_file.read_text(encoding='utf-8'))
version = args.version or manifest['version']
if not re.fullmatch(r'\d+\.\d+\.\d+', version):
    parser.error('Expected a numeric GitVersion MAJOR.MINOR.PATCH version')
manifest['version'] = version

out = root / 'dist'
out.mkdir(exist_ok=True)
common = ['RuEn.py', 'RuEn.manifest', 'hotkeys.py']
platforms = {'universal': ['libruen_v2.dylib', 'ruen_filter.dll'],
             'macos': ['libruen_v2.dylib'], 'windows': ['ruen_filter.dll']}
for platform, libraries in platforms.items():
    target = out / f'RuEn-{version}-{platform}.zip'
    with ZipFile(target, 'w', ZIP_DEFLATED) as archive:
        for name in common + libraries:
            if name == 'RuEn.manifest' and args.version:
                archive.writestr('RuEn/RuEn.manifest',
                                 json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
            else:
                archive.write(root / 'RuEn' / name, 'RuEn/' + name)
        for name in ('README.md', 'LICENSE'):
            archive.write(root / name, name)
        reviewed_notes = root / 'docs/releases' / (version + '.md')
        if reviewed_notes.is_file():
            archive.writestr('RELEASE_NOTES.md', reviewed_notes.read_bytes())
        elif version == '1.0.0':
            archive.write(root / 'RELEASE_NOTES.md', 'RELEASE_NOTES.md')
    digest = hashlib.sha256(target.read_bytes()).hexdigest()
    target.with_suffix('.zip.sha256').write_text(
        digest + '  ' + target.name + '\n', encoding='ascii')
    print(target)
