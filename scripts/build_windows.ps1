$ErrorActionPreference = "Stop"
if (-not $env:QT_SDK) { throw "Set QT_SDK to the matching Qt MSVC 64-bit SDK directory." }
if (-not (Get-Command cl.exe -ErrorAction SilentlyContinue)) { throw "Run from an x64 Native Tools Command Prompt with MSVC installed." }
$root = Split-Path -Parent $PSScriptRoot
$include = Join-Path $env:QT_SDK "include"
$lib = Join-Path $env:QT_SDK "lib"
$source = Join-Path $root "native/ruen_filter.cpp"
$output = Join-Path $root "RuEn/ruen_filter.dll"
$build = Join-Path $root "dist/windows-build"
New-Item -ItemType Directory -Force -Path $build | Out-Null
Push-Location $build
try {
    & cl.exe /nologo /std:c++17 /Zc:__cplusplus /permissive- /EHsc /LD /MD /utf-8 "/I$include" "/I$include/QtCore" "/I$include/QtGui" "/I$include/QtWidgets" $source /link "/LIBPATH:$lib" Qt6Core.lib Qt6Gui.lib Qt6Widgets.lib "/OUT:$output"
    if ($LASTEXITCODE -ne 0) { throw "Windows build failed ($LASTEXITCODE)." }
} finally { Pop-Location }
