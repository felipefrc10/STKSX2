#!/usr/bin/env python3
"""Replace visible ARMSX2 onboarding/setup branding with STKSX2."""
from pathlib import Path
import sys

if len(sys.argv) != 2:
    raise SystemExit("Usage: customize_stksx2_onboarding.py <path-to-ARMSX2-source>")

root = Path(sys.argv[1]).resolve()
src = root / "platforms/android/app/src"
if not src.is_dir():
    raise SystemExit(f"Android source directory not found: {src}")

extensions = {".xml", ".kt", ".java", ".json", ".txt", ".html", ".md"}
replacements = (
    ("Bem-vindo à configuração do ARMSX2!", "Bem-vindo à configuração do STKSX2!"),
    ("O ARMSX2 guarda", "O STKSX2 guarda"),
    ("O ARMSX2 mantém", "O STKSX2 mantém"),
    ("Configuração do ARMSX2", "Configuração do STKSX2"),
    ("Bem-vindo ao ARMSX2", "Bem-vindo ao STKSX2"),
    ("Welcome to ARMSX2 setup", "Welcome to STKSX2 setup"),
    ("Welcome to ARMSX2!", "Welcome to STKSX2!"),
    ("ARMSX2 guarda", "STKSX2 guarda"),
    ("ARMSX2 setup", "STKSX2 setup"),
    ("ARMSX2!", "STKSX2!"),
)

changed_files = 0
replacements_count = 0
for path in src.rglob("*"):
    if not path.is_file() or path.suffix.lower() not in extensions:
        continue
    try:
        before = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        continue
    after = before
    for old, new in replacements:
        replacements_count += after.count(old)
        after = after.replace(old, new)
    if after != before:
        path.write_text(after, encoding="utf-8")
        changed_files += 1

print(f"STKSX2 onboarding branding applied: {changed_files} file(s), {replacements_count} replacement(s).")
if replacements_count == 0:
    raise SystemExit("No matching onboarding strings found. Search the upstream source for its actual setup text.")
