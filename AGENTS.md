# RuEn development

[Русская версия](AGENTS.ru.md)

RuEn supports the Russian keyboard layout for existing Autodesk Fusion keyboard shortcuts.

## Shared 4FusionLab rules

- Shared standards: https://github.com/4FusionLab/.github/blob/main/AGENTS.md; shared CI model: https://github.com/4FusionLab/.github/blob/main/RELEASE_PLATFORM.md.
- Communicate with the user and make plans in Russian; use English for Fusion command names, code and UI. Retain separate README.md and README.ru.md where the project has them.
- Inspect current code and `git status` before changes; preserve unrelated work. Use Conventional Commits; small PRs with tests are preferred, while direct pushes to `main` are allowed by the existing policy.
- Do not change the Fusion manifest UUID, command IDs, OS support or distribution structure without a separate task and migration plan. Keep secrets, personal CAD files, tokens and unauthorized external services out of the repository.
- Where shippable runtime exists, release is triggered only by a push/merge to `main` affecting `.github/release-paths.txt`. CI checks code, GitVersion.Tool 6.8.2 determines the version, and GitHub automatically creates the tag and Release. **Never create or move release tags manually**, or overwrite published ZIPs.
- README, docs, tests, CI settings and `AGENTS.md` must not independently trigger a release. Pin shared Actions to an **immutable commit SHA** from `4FusionLab/.github`, not `@main`.
- Unit tests and ZIP checks are not live Autodesk Fusion tests. For API/UX changes record what was actually tested and on which OS.

## Platform compatibility

- `RuEn/RuEn.py` and `RuEn/hotkeys.py` handle registered Fusion shortcuts; native `RuEn/libruen_v2.dylib` (macOS Apple Silicon) and `RuEn/ruen_filter.dll` (Windows x64) are included in the package.
- `native/ruen_filter.cpp` and `scripts/build_macos.sh`, `scripts/build_windows.ps1` are the native library build sources. Changes to them do not themselves alter the shipped product: rebuild and verify the corresponding DLL/dylib first.
- `QTCanvas` uses internal Qt API; document the risk of incompatibility with Autodesk Fusion versions and do not claim this is a public stable SDK.
- Do not change established user hotkey mappings, modifier combinations or filter enable/disable behavior without tests. Do not change the existing UUID after RuEnProbe.

## Verification

- `python -m unittest discover -s tests -v`
- `python scripts/package.py --version X.Y.Z`; output is universal/macos/windows ZIPs and SHA-256, not a new DLL/dylib compilation.
- Qt and keyboard behavior require native tests on the relevant platform; Linux CI does not replace them.
