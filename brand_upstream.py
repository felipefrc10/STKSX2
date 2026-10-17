#!/usr/bin/env python3
"""Apply the STKSX2 launcher label to a checked-out Play! source tree.

This deliberately changes only the visible launcher name; it does not rename
Java/JNI packages or claim that the upstream emulator core has been rewritten.
"""
from pathlib import Path
import re
import sys

if len(sys.argv) != 2:
    raise SystemExit("Usage: brand_upstream.py <path-to-Play-source>")
root = Path(sys.argv[1]).resolve()
if not root.is_dir():
    raise SystemExit(f"Source directory not found: {root}")

changed = []
# First target the known Play! launcher resource, which currently has no
# app_name key. Use about_play as the app-identifying label and also update
# app_name if a future upstream version adds it.
targets = [root / "build_android/src/main/res/values/strings.xml"]
for path in targets:
    if not path.is_file():
        continue
    original = path.read_text(encoding="utf-8")
    updated, count = re.subn(
        r'(<string\s+name=["\']about_play["\'][^>]*>).*?(</string\s*>)',
        r'\1About STKSX2\2', original, count=1, flags=re.S,
    )
    if count:
        path.write_text(updated, encoding="utf-8")
        changed.append(str(path.relative_to(root)))

# Also update any app_name key in resources, wherever a newer upstream puts it.
for path in root.rglob("*.xml"):
    if any(part in {".git", ".gradle", "build"} for part in path.parts):
        continue
    try:
        original = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        continue
    updated, count = re.subn(
        r'(<string\s+name=["\']app_name["\'][^>]*>).*?(</string\s*>)',
        r'\1STKSX2\2', original, count=1, flags=re.S,
    )
    if count:
        path.write_text(updated, encoding="utf-8")
        changed.append(str(path.relative_to(root)))

# If upstream uses a literal manifest label instead of an app_name resource,
# replace only that literal. Do not replace @string/... references.
if not changed:
    for path in root.rglob("AndroidManifest.xml"):
        if any(part in {".git", ".gradle", "build"} for part in path.parts):
            continue
        try:
            original = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        updated, count = re.subn(
            r'android:label\s*=\s*(["\'])(?!@)(.*?)\1',
            'android:label="STKSX2"', original, count=1,
        )
        if count:
            path.write_text(updated, encoding="utf-8")
            changed.append(str(path.relative_to(root)))
            break

if not changed:
    raise SystemExit(
        "Could not find an app_name string resource or literal manifest label. "
        "Refusing to produce an APK that might still be branded Play!. Update this script for the upstream tree."
    )
print("STKSX2 launcher label applied in:")
for item in changed:
    print(f" - {item}")
