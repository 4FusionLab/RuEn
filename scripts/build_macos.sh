#!/bin/sh
set -eu
: "${QT_SDK:?Set QT_SDK to the Qt 6.8.3 macos directory}"
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
LIB="$QT_SDK/lib"
clang++ -std=c++17 -arch arm64 -include arm_acle.h -dynamiclib \
  -F"$LIB" -I"$LIB/QtWidgets.framework/Headers" \
  -I"$LIB/QtCore.framework/Headers" -I"$LIB/QtGui.framework/Headers" \
  -framework QtWidgets -framework QtGui -framework QtCore \
  "$ROOT/native/ruen_filter.cpp" -o "$ROOT/RuEnProbe/libruen_v2.dylib"
