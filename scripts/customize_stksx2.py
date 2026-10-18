#!/usr/bin/env python3
"""Apply STKSX2 product-level UI changes to the checked-out ARMSX2 source.

This deliberately preserves the emulation core and existing functional settings.
It fails fast if upstream moves the expected integration points.
"""
from pathlib import Path
import re
import sys

if len(sys.argv) != 2:
    raise SystemExit("Usage: customize_stksx2.py <path-to-ARMSX2-source>")
root = Path(sys.argv[1]).resolve()
app = root / "platforms/android/app"
required = {
    "runtime": app / "src/main/java/com/armsx2/runtime/MainActivityRuntime.kt",
    "drawer": app / "src/main/java/com/armsx2/navigation/NavigationDrawer.kt",
    "about": app / "src/main/java/com/armsx2/ui/about/AboutScreen.kt",
    "settings_screen": app / "src/main/java/com/armsx2/ui/settingshub/SettingsScreen.kt",
    "manifest": app / "src/main/AndroidManifest.xml",
    "gradle": app / "build.gradle.kts",
}
missing = [str(p) for p in required.values() if not p.is_file()]
if missing:
    raise SystemExit("Required ARMSX2 files missing; no changes applied: " + ", ".join(missing))

# 1) Disable Discord presence startup. The Discord drawer entry is removed below too.
p = required["runtime"]
s = p.read_text(encoding="utf-8")
discord_block = """        com.armsx2.DiscordPresence.attachActivity(this)
        com.armsx2.DiscordPresence.start()
"""
if discord_block in s:
    s = s.replace(discord_block, "", 1)
elif "com.armsx2.DiscordPresence.start()" in s:
    raise SystemExit("Discord startup code changed upstream; refusing partial customization.")
p.write_text(s, encoding="utf-8")

# 2) Remove Discord/community/social rows and point the repository link to STKSX2.
p = required["drawer"]
s = p.read_text(encoding="utf-8")
s = s.replace('private const val GithubUrl = "https://github.com/ARMSX2/ARMSX2"',
              'private const val GithubUrl = "https://github.com/felipefrc10/STKSX2"', 1)
s = re.sub(
    r'        DrawerItem\("about\.discord", "💬", iconRes = com\.armsx2\.R\.drawable\.ic_discord,\n'
    r'            onAction = \{ openExternalUrl\(context, DiscordUrl\); onDismiss\(\) \}\),\n',
    '', s, count=1)
for line in (
    '        DrawerItem("about.website", "🌐", onAction = { openExternalUrl(context, WebsiteUrl); onDismiss() }),\n',
    '        DrawerItem("news.title", "📰", AppRoute.News),\n',
    '        DrawerItem("friends.title", "👥", AppRoute.Friends, friendsBadge = true),\n',
    '        DrawerItem("remoteplay.title", "📡", AppRoute.RemotePlay),\n',
):
    s = s.replace(line, "", 1)
if 'DrawerItem("about.discord"' in s or 'DrawerItem("friends.title"' in s or 'DrawerItem("remoteplay.title"' in s:
    raise SystemExit("Could not remove every upstream social drawer entry; refusing partial customization.")
# Replace the ARMSX2 logo in the drawer with the STKSX2 wordmark.
s = s.replace(
    '            ArmsLogo(Modifier.weight(1f))',
    '            Text("STKSX2", modifier = Modifier.weight(1f), style = MaterialTheme.typography.headlineSmall, fontWeight = FontWeight.ExtraBold, color = MaterialTheme.colorScheme.primary)',
    1)
# Persistir as alterações do menu lateral antes de trocar para o arquivo de runtime.
# Sem esta gravação, as alterações em NavigationDrawer.kt eram descartadas.
p.write_text(s, encoding="utf-8")

# Corrigir a orientação durante a emulação.
# Ler explicitamente o arquivo de runtime, sem reutilizar o texto do menu lateral.
p = required["runtime"]
s = p.read_text(encoding="utf-8")

orientation_pattern = re.compile(
    r'val orientation = if \(emulationOwnsOrientation\)\s+'
    r'com\.armsx2\.config\.ConfigStore\.resolveForGame'
    r'\(currentGame\.value\?\.settingsKey\)\.output\.orientation\s+'
    r'else\s+'
    r'com\.armsx2\.ui\.theme\.LauncherOrientationPreferences\.mode\.value'
)

orientation_new = """val orientation = if (emulationOwnsOrientation) {
            val gameOrientation =
                com.armsx2.config.ConfigStore.resolveForGame(currentGame.value?.settingsKey).output.orientation
            if (gameOrientation == 0)
                com.armsx2.ui.theme.LauncherOrientationPreferences.mode.value
            else
                gameOrientation
        } else
            com.armsx2.ui.theme.LauncherOrientationPreferences.mode.value"""

s, orientation_count = orientation_pattern.subn(
    orientation_new, s, count=1
)

if orientation_count != 1:
    raise SystemExit(
        "Não foi possível localizar a lógica de orientação no runtime. "
        "Nenhuma alteração de orientação foi gravada."
    )

p.write_text(s, encoding="utf-8")

# 3) Rebrand the About screen and repository destination.
p = required["about"]
s = p.read_text(encoding="utf-8")
s = s.replace('private const val RepositoryUrl = "https://github.com/ARMSX2/ARMSX2"',
              'private const val RepositoryUrl = "https://github.com/felipefrc10/STKSX2"', 1)
s = s.replace('repository = "ARMSX2/ARMSX2"', 'repository = "felipefrc10/STKSX2"')
s = s.replace(
    '                                ArmsLogo(showWordmark = true)',
    '                                Text("STKSX2", style = MaterialTheme.typography.headlineLarge, fontWeight = FontWeight.ExtraBold)',
    1)
p.write_text(s, encoding="utf-8")

# 3b) Show STKSX2 in both global settings and per-game settings headers.
p = required["settings_screen"]
s = p.read_text(encoding="utf-8")
old_title = 'title = scopeGame?.title ?: str("action.settings"),'
new_title = 'title = "STKSX2 · " + (scopeGame?.title ?: str("action.settings")),'
if old_title in s:
    s = s.replace(old_title, new_title, 1)
elif new_title not in s:
    raise SystemExit("Could not locate the settings header title; refusing a blind branding change.")
p.write_text(s, encoding="utf-8")

# 4) Bypass the ARMSX2 bundled intro video and open the actual STKSX2 library on launch.
p = required["manifest"]
s = p.read_text(encoding="utf-8")
splash_pat = r'(<activity\s+android:name="\.BootSplashActivity".*?</activity>)'
def remove_splash_launcher(m):
    block, count = re.subn(
        r'\s*<intent-filter>\s*<action android:name="android.intent.action.MAIN"\s*/>\s*'
        r'<category android:name="android.intent.category.LAUNCHER"\s*/>\s*'
        r'<category android:name="android.intent.category.GAME"\s*/>\s*</intent-filter>',
        '', m.group(1), count=1, flags=re.S)
    if count != 1:
        raise SystemExit("Could not detach the ARMSX2 intro from the launcher safely.")
    return block
s, n = re.subn(splash_pat, remove_splash_launcher, s, count=1, flags=re.S)
if n != 1:
    raise SystemExit("BootSplashActivity not found in manifest.")
main_pat = r'(<activity\s+android:name="\.Main".*?</activity>)'
def add_main_launcher(m):
    block = m.group(1)
    if "android.intent.action.MAIN" in block:
        return block
    addition = ('    <intent-filter>\n'
                '        <action android:name="android.intent.action.MAIN" />\n'
                '        <category android:name="android.intent.category.LAUNCHER" />\n'
                '        <category android:name="android.intent.category.GAME" />\n'
                '    </intent-filter>\n')
    return block.replace('</activity>', addition + '</activity>', 1)
s, n = re.subn(main_pat, add_main_launcher, s, count=1, flags=re.S)
if n != 1 or 'android:name=".Main"' not in s:
    raise SystemExit("Could not set Main as the launcher activity safely.")
p.write_text(s, encoding="utf-8")

# 5) Disable the upstream GitHub self-updater in the sideload flavor.
p = required["gradle"]
s = p.read_text(encoding="utf-8")
s, n = re.subn(
    r'(create\("github"\)\s*\{.*?buildConfigField\("boolean", "IN_APP_UPDATER", )"true"',
    r'\1"false"', s, count=1, flags=re.S)
if n != 1:
    raise SystemExit("Could not disable the upstream in-app updater.")
p.write_text(s, encoding="utf-8")


# Remove sideload-only permission/provider used solely to install upstream updates.
github_manifest = app / "src/github/AndroidManifest.xml"
if github_manifest.is_file():
    s = github_manifest.read_text(encoding="utf-8")

    # Remove the permission used by the upstream self-updater.
    s = re.sub(
        r'\s*<uses-permission android:name="android.permission.REQUEST_INSTALL_PACKAGES"\s*/>\s*',
        '\n', s, count=1
    )

    # Remove the entire explanatory comment, including its closing marker.
    s = re.sub(
        r'\s*<!-- FileProvider that hands the downloaded update APK.*?-->\s*',
        '\n', s, count=1, flags=re.S
    )

    # Remove the complete application/provider block.
    s, provider_count = re.subn(
        r'\s*<application>\s*<provider\b.*?</provider>\s*</application>\s*',
        '\n', s, count=1, flags=re.S
    )

    if provider_count != 1:
        raise SystemExit(
            "Could not safely remove the GitHub update FileProvider block."
        )

    github_manifest.write_text(s, encoding="utf-8")
