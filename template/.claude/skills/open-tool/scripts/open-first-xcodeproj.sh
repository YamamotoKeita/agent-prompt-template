#!/usr/bin/env bash
set -euo pipefail

search_root="${1:-$PWD}"
swift_file="${2:-}"

if [[ ! -d "$search_root" ]]; then
  echo "Search root does not exist: $search_root" >&2
  exit 1
fi

if ! command -v open >/dev/null 2>&1; then
  echo "The 'open' command is not available on this system." >&2
  exit 1
fi

# 依存ライブラリ等の .xcodeproj を除外し、浅い階層のプロジェクトを優先して選ぶ
first_project="$(
  find "$search_root" \
    \( -type d \( -name Carthage -o -name Pods -o -name .build -o -name DerivedData -o -name node_modules \) -prune \) \
    -o \( -type d -name '*.xcodeproj' -print \) |
    awk -F/ '{print NF"\t"$0}' | LC_ALL=C sort -k1,1n -k2 | head -n 1 | cut -f2-
)"

if [[ -z "$first_project" ]]; then
  echo "No .xcodeproj file was found under: $search_root" >&2
  exit 2
fi

open -a Xcode "$first_project"
echo "Opened in Xcode: $first_project"

if [[ -n "$swift_file" ]]; then
  sleep 5
  xed "$swift_file"
  echo "Opened in editor: $swift_file"
fi
