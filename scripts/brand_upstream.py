#!/usr/bin/env python3
"""Apply STKSX2 branding and a first real Android performance preset to Play!.

This script is run by GitHub Actions after checking out upstream Play!. It
modifies only the generated upstream working tree, not the upstream repository.
It fails closed when expected source anchors are missing.
"""
from pathlib import Path
import re
import sys

if len(sys.argv) != 2:
    raise SystemExit("Usage: brand_upstream.py <path-to-Play-source>")
root = Path(sys.argv[1]).resolve()
if not root.is_dir():
    raise SystemExit(f"Source directory not found: {root}")


def replace_once(path: Path, pattern: str, replacement: str, label: str) -> None:
    if not path.is_file():
        raise SystemExit(f"Required upstream file missing for {label}: {path}")
    original = path.read_text(encoding="utf-8")
    updated, count = re.subn(pattern, replacement, original, count=1, flags=re.S)
    if count != 1:
        raise SystemExit(f"Could not apply {label}; upstream source layout changed: {path}")
    if updated != original:
        path.write_text(updated, encoding="utf-8")


# Brand the app's existing about label and any app_name string.
changed = []
strings_path = root / "build_android/src/main/res/values/strings.xml"
if strings_path.is_file():
    original = strings_path.read_text(encoding="utf-8")
    updated, count = re.subn(
        r'(<string\s+name=["\']about_play["\'][^>]*>).*?(</string\s*>)',
        r'\1About STKSX2\2', original, count=1, flags=re.S,
    )
    if count:
        strings_path.write_text(updated, encoding="utf-8")
        changed.append(str(strings_path.relative_to(root)))

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
    raise SystemExit("Could not find an app_name string resource or literal manifest label.")


# Add a preset selector that changes real Play! settings (resolution factor and
# bilinear filtering), rather than exposing UI-only switches with no effect.
prefs_path = root / "build_android/src/main/res/xml/preferences_emu.xml"
replace_once(
    prefs_path,
    r'(\s*<PreferenceCategory\s+android:title="@string/pref_emu_general".*?>)',
    r'\1\n\n        <ListPreference\n'
    r'            android:key="stksx2.performanceprofile"\n'
    r'            android:defaultValue="0"\n'
    r'            android:persistent="false"\n'
    r'            android:entries="@array/stksx2_performance_profile_entries"\n'
    r'            android:entryValues="@array/stksx2_performance_profile_values"\n'
    r'            android:title="@string/stksx2_performance_profile_title"\n'
    r'            android:summary="@string/stksx2_performance_profile_summary"\n'
    r'            app:iconSpaceReserved="false"\n'
    r'            app:useSimpleSummaryProvider="true" />',
    "performance preset preference",
)

strings_path = root / "build_android/src/main/res/values/strings.xml"
replace_once(
    strings_path,
    r'(\s*<string name="pref_emu_general">)',
    r'\n\t<string name="stksx2_performance_profile_title">Performance profile</string>'
    r'\n\t<string name="stksx2_performance_profile_summary">Choose a preset for lower-end phones, balanced use, or higher visual quality. The preset changes internal resolution and bilinear filtering.</string>\1',
    "performance preset labels",
)

values_path = root / "build_android/src/main/res/values/donottranslate.xml"
replace_once(
    values_path,
    r'(\s*</resources>)',
    r'\n\t<string-array name="stksx2_performance_profile_entries">'
    r'\n\t\t<item>Low-end / lower load</item>'
    r'\n\t\t<item>Balanced</item>'
    r'\n\t\t<item>Visual quality</item>'
    r'\n\t</string-array>'
    r'\n\t<string-array name="stksx2_performance_profile_values">'
    r'\n\t\t<item>0</item>'
    r'\n\t\t<item>1</item>'
    r'\n\t\t<item>2</item>'
    r'\n\t</string-array>\1',
    "performance preset values",
)

fragment_path = root / "Source/ui_android/java/com/virtualapplications/play/settings/EmulatorSettingsFragment.java"
replace_once(
    fragment_path,
    r'([ \t]*readFromPreferences\(getPreferenceScreen\(\)\);)',
    r'\1\n\t\tapplyPerformanceProfile(SettingsManager.getPreferenceInteger("stksx2.performanceprofile"));',
    "performance preset application hook",
)
replace_once(
    fragment_path,
    r'\n}\s*$',
    '''
\n\tprivate void applyPerformanceProfile(final int profile)
\t{
\t\t// These are existing core preferences. No fake toggles are added.
\t\tfinal int resolutionFactor;
\t\tfinal boolean forceBilinear;
\t\tswitch(profile)
\t\t{
\t\tcase 0: // Lower load: baseline internal resolution and no forced bilinear.
\t\t\tresolutionFactor = 1;
\t\t\tforceBilinear = false;
\t\t\tbreak;
\t\tcase 2: // Higher visual quality; may be slower and use more GPU memory.
\t\t\tresolutionFactor = 2;
\t\t\tforceBilinear = true;
\t\t\tbreak;
\t\tcase 1:
\t\tdefault: // Balanced preset prioritizes compatibility and modest resource use.
\t\t\tresolutionFactor = 1;
\t\t\tforceBilinear = true;
\t\t\tbreak;
\t\t}
\t\tSettingsManager.setPreferenceInteger("renderer.opengl.resfactor", resolutionFactor);
\t\tSettingsManager.setPreferenceBoolean("renderer.opengl.forcebilineartextures", forceBilinear);
\t}
}
''',
    "performance preset implementation",
)

print("STKSX2 branding applied in:")
for item in changed:
    print(f" - {item}")
print("STKSX2 Android performance presets added: Low-end, Balanced, Visual quality.")
