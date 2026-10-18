#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
command -v git >/dev/null || { echo "git is required" >&2; exit 1; }
command -v gh >/dev/null || { echo "Install GitHub CLI and run gh auth login first" >&2; exit 1; }
gh auth status >/dev/null
repo="kmosoti/compositional-intelligence"
tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT
git clone "https://github.com/${repo}.wiki.git" "$tmp/wiki"
cp wiki/*.md "$tmp/wiki/"
git -C "$tmp/wiki" add '*.md'
if git -C "$tmp/wiki" diff --cached --quiet; then
  echo "Wiki already matches local source."
  exit 0
fi
git -C "$tmp/wiki" commit -m "Synchronize research documentation"
git -C "$tmp/wiki" push origin HEAD
echo "Published wiki pages to https://github.com/${repo}/wiki"
