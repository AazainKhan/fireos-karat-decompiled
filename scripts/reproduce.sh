#!/bin/bash
# Rebuild data/ and index/ from your own copy of the Fire OS 8 OTA for karat.
# Extracted images and decompiled code stay in $WORK and are never committed.
#
# Usage: scripts/reproduce.sh /path/to/update-kindle-karat-RS8182_user_3811_0032548774788.bin [work_dir]
# Needs: python3, brotli, e2fsprogs (debugfs), aapt2 (Android build-tools), jadx,
#        sdat2img.py (github.com/xpirt/sdat2img) at $SDAT2IMG.
set -euo pipefail

OTA="${1:?path to the OTA .bin}"
WORK="${2:-$PWD/.work}"
REPO="$(cd "$(dirname "$0")/.." && pwd)"
SDAT2IMG="${SDAT2IMG:?set SDAT2IMG to the path of sdat2img.py}"
DEBUGFS="${DEBUGFS:-$(command -v debugfs || echo /opt/homebrew/opt/e2fsprogs/sbin/debugfs)}"
export AAPT2="${AAPT2:-$HOME/Library/Android/sdk/build-tools/36.0.0/aapt2}"

# Packages decompiled for index/java (the integration surfaces Glass cares about).
KEY_PACKAGES=(
  com.amazon.tv.launcher com.amazon.firehomestarter com.amazon.autopairservice com.amazon.uxcontrollerservice
  com.amazon.dialservice com.amazon.tv.settings.v2 com.amazon.tv.settings.core com.amazon.cast.sink
  com.amazon.whisperlink.core.android com.amazon.tv.notificationcenter com.amazon.tv.matter
  com.amazon.tv.mattercohost com.amazon.fireinputdevices com.amazon.device.bluetoothkeymaplib
  com.amazon.tv.ffsprovisioneeclient
)

mkdir -p "$WORK/ota" "$WORK/extracted"
echo "[1/7] unpack OTA"
unzip -o -q "$OTA" '*.new.dat.br' '*.transfer.list' -d "$WORK/ota"

echo "[2/7] dat.br -> raw ext4 -> files"
for p in system vendor product; do
  [ -f "$WORK/ota/$p.img" ] || {
    brotli -d -f "$WORK/ota/$p.new.dat.br" -o "$WORK/ota/$p.new.dat"
    python3 "$SDAT2IMG" "$WORK/ota/$p.transfer.list" "$WORK/ota/$p.new.dat" "$WORK/ota/$p.img"
  }
  mkdir -p "$WORK/extracted/$p"
  "$DEBUGFS" -R "rdump / $WORK/extracted/$p" "$WORK/ota/$p.img" >/dev/null 2>&1
done

echo "[3/7] manifest DB (aapt2)"
python3 "$REPO/scripts/manifest_db.py" "$WORK/extracted" "$REPO/data/manifests.json"

echo "[4/7] shared libraries and features"
find "$WORK/extracted" -path '*/etc/permissions/*.xml' -print0 \
  | xargs -0 grep -h -E '<library|<feature' > "$REPO/data/libs_features.txt" || true

echo "[5/7] dependency graph"
python3 "$REPO/scripts/graph.py" "$REPO/data/manifests.json" "$REPO/data/libs_features.txt" "$REPO/data/graph.json"
python3 "$REPO/scripts/index_components.py" "$REPO/data/manifests.json" "$REPO/index"

echo "[6/7] decompile key packages (jadx, local only)"
for pkg in "${KEY_PACKAGES[@]}"; do
  apk=$(python3 -c "import json,sys;print(json.load(open(sys.argv[1]))[sys.argv[2]][0]['file'])" "$REPO/data/manifests.json" "$pkg")
  [ -d "$WORK/decompiled/$pkg" ] || jadx -q -j 4 --no-res --show-bad-code -d "$WORK/decompiled/$pkg" "$WORK/extracted/$apk" || true
done

echo "[7/7] declaration indexes"
python3 "$REPO/scripts/index_jadx.py" "$WORK/decompiled" "$REPO/index/java"
echo "done: data/ and index/ rebuilt"
