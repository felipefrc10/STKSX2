#!/usr/bin/env python3
"""Brand an ARMSX2 build as STKSX2 while preserving the existing Play! icon.

This script changes only the launcher label, launcher icon resource wiring,
and the APK builder's Gradle arguments. Existing icon PNGs are copied from the
Play! source used by the prior STKSX2 workflow.
"""
from pathlib import Path
import re
import shutil
import sys

if len(sys.argv) != 3:
    raise SystemExit("Usage: brand_armsx2.py <path-to-ARMSX2-source> <path-to-Play-icon-source>")
root = Path(sys.argv[1]).resolve()
play_root = Path(sys.argv[2]).resolve()
if not root.is_dir():
    raise SystemExit(f"ARMSX2 source directory not found: {root}")
if not play_root.is_dir():
    raise SystemExit(f"Play! icon source directory not found: {play_root}")

android_root = root / "platforms/android"
app_root = android_root / "app"
builder = android_root / "tools/build-universal-page-apk.sh"
gradle_file = app_root / "build.gradle.kts"
manifest = app_root / "src/main/AndroidManifest.xml"
for required in (builder, gradle_file, manifest):
    if not required.is_file():
        raise SystemExit(f"Required upstream file not found: {required}")

gradle_text = gradle_file.read_text(encoding="utf-8")
if 'armsx2.appLabel' not in gradle_text or 'manifestPlaceholders["appLabel"]' not in gradle_text:
    raise SystemExit("Upstream no longer supports the armsx2.appLabel Gradle property; refusing an unbranded build.")
manifest_text = manifest.read_text(encoding="utf-8")
if 'android:label="${appLabel}"' not in manifest_text:
    raise SystemExit("Android manifest no longer uses the appLabel placeholder; refusing a blind branding change.")

# The previous STKSX2 workflow used Play!'s density-qualified launcher PNGs.
icon_relpaths = [
    Path("build_android/src/main/res/drawable-xhdpi/ic_launcher.png"),
    Path("build_android/src/main/res/drawable-xxhdpi/ic_launcher.png"),
    Path("build_android/src/main/res/drawable-xxxhdpi/ic_launcher.png"),
]
icon_sources = [play_root / rel for rel in icon_relpaths]
missing = [str(path) for path in icon_sources if not path.is_file()]
if missing:
    raise SystemExit("Could not find all existing Play! launcher icon PNGs; refusing to silently change the icon: " + ", ".join(missing))
for rel, source in zip(icon_relpaths, icon_sources):
    density_dir = rel.parts[-2]
    destination = app_root / "src/main/res" / density_dir / "ic_launcher.png"
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)

# Both regular and round icon declarations now use the copied density-specific PNG.
manifest_updated = re.sub(r'android:icon="[^"]+"', 'android:icon="@drawable/ic_launcher"', manifest_text, count=1)
if manifest_updated == manifest_text:
    raise SystemExit("Could not locate android:icon in the ARMSX2 manifest.")
manifest_updated, round_count = re.subn(r'android:roundIcon="[^"]+"', 'android:roundIcon="@drawable/ic_launcher"', manifest_updated, count=1)
if round_count != 1:
    raise SystemExit("Could not locate android:roundIcon in the ARMSX2 manifest.")
manifest.write_text(manifest_updated, encoding="utf-8")

# Add the visible app name to the official upstream universal-APK builder.
original = builder.read_text(encoding="utf-8")
anchor = 'if [[ -n "$APPLICATION_ID" ]]; then\n\t\tid_args+=("-Parmsx2.applicationId=$APPLICATION_ID")\n\tfi\n'
replacement = anchor + '\tid_args+=("-Parmsx2.appLabel=STKSX2")\n'
if '"-Parmsx2.appLabel=STKSX2"' not in original:
    if anchor not in original:
        raise SystemExit("Could not locate the expected application-id argument block in upstream APK builder; refusing a blind patch.")
    builder.write_text(original.replace(anchor, replacement, 1), encoding="utf-8")

print("STKSX2 launcher label configured.")
print("Existing Play! launcher icon PNGs copied and referenced by the manifest.")
print("Emulator core and settings/menu implementation files were not edited by this branding script.")
