# fireos-karat-re

A machine-readable map of **Fire OS 8** (Android 11) on the **Fire TV Stick 4K, 2nd gen** (`AFTKRT`, codename `karat`, build `RS8182.3811N`, OTA `0032548774788`): every package, component, intent action, content provider, permission and dependency, plus declaration-level indexes of the 15 Amazon packages that matter most for building a replacement launcher.

Built for coding agents (Claude Code, Codex, Cursor…) and people building Fire TV launchers or debloated ROMs, such as [Glass](https://github.com/AazainKhan/glass-tv-launcher) and [Glass OS](https://github.com/AazainKhan/glass-os). Ask "what listens to BOOT_COMPLETED?" or "what breaks if I remove X?" without pulling a 750 MB OTA.

**This repo contains no Amazon code, APKs, images or artwork.** It holds names, signatures, intent strings and dependency facts derived from the firmware, plus scripts that regenerate everything from your own copy of the OTA. See [NOTICE.md](NOTICE.md).

## What's inside

| Path | What it is | Rows |
|---|---|---|
| `index/packages.tsv` | Every package: APK path, sharedUserId, HOME category, persistent, counts | 280 |
| `index/components.tsv` | Every activity, service, receiver, provider: exported or not, guard permission | 2,593 |
| `index/actions.tsv` | Intent actions and categories each package handles | 2,057 |
| `index/providers.tsv` | Content provider authorities | 191 |
| `index/permissions.tsv` | Permissions each package declares, with protection level | 1,781 |
| `data/manifests.json` | Full manifest DB (uses-permission, uses-library, components, authorities) | 280 |
| `data/graph.json` | Dependency graph: who needs whom, and why (permission, library, meta-data) | |
| `data/classification.tsv` | KEEP / REMOVE / INVESTIGATE verdict per package, with reason | |
| `data/remove-candidates.tsv` | Removal batches proven safe by the lint gate | |
| `index/java/<pkg>.classes.tsv` | Classes, superclass, interfaces (Amazon code only) | 15 packages |
| `index/java/<pkg>.members.tsv` | Method and field declarations, no bodies | |
| `index/java/<pkg>.strings.tsv` | Intent actions, extras, URIs, settings keys and properties referenced in code | |
| `docs/findings.md` | Triage and first facts (auto-pair triggers, home start strategies, HOME competitors) | |
| `docs/package-classification.md` | Per-package removal evidence | |

Decompiled packages: `com.amazon.tv.launcher`, `com.amazon.firehomestarter`, `com.amazon.autopairservice`, `com.amazon.uxcontrollerservice`, `com.amazon.dialservice`, `com.amazon.tv.settings.v2`, `com.amazon.tv.settings.core`, `com.amazon.cast.sink`, `com.amazon.whisperlink.core.android`, `com.amazon.tv.notificationcenter`, `com.amazon.tv.matter`, `com.amazon.tv.mattercohost`, `com.amazon.fireinputdevices`, `com.amazon.device.bluetoothkeymaplib`, `com.amazon.tv.ffsprovisioneeclient`. Bundled third-party libraries (androidx, Kotlin, Google, Glide…) are filtered out.

## Use cases

For agents working on a Fire TV launcher, ROM or companion app:

1. **Take over Home cleanly.** Find every package that claims HOME and what re-asserts it at boot.
   `awk -F'\t' '$4=="true"' index/packages.tsv` and `grep -h BOOT_COMPLETED index/java/*.strings.tsv`
2. **Debloat with evidence.** Before removing a package, see who depends on it and why.
   `python3 -c "import json;g=json.load(open('data/graph.json'));print(g['rev'].get('com.amazon.aria'))"`
   Then gate the batch: `python3 scripts/lint_removals.py data/manifests.json data/libs_features.txt data/remove-candidates.tsv`
3. **Deep-link into Fire settings.** List exported settings activities and the actions they accept.
   `grep com.amazon.tv.settings.v2 index/components.tsv | awk -F'\t' '$4=="yes"'`
4. **Fix the remote pairing behaviour.** See what triggers AutoPairService and what it broadcasts.
   `cat index/java/com.amazon.autopairservice.strings.tsv`
5. **Interoperate with casting.** Find the DIAL, Miracast and WhisperPlay receivers and their intents before adding an AirPlay or Cast receiver alongside.
   `grep -E "dialservice|cast.sink|whisperlink" index/actions.tsv`
6. **Find the permission you need.** Which package declares a permission, and at what protection level, so you know if an APK can request it.
   `grep -i bluetooth index/permissions.tsv`
7. **Diff Fire OS updates.** Re-run on a newer OTA and `git diff index/` to see new components, actions and permissions.

## Regenerate from your own OTA

Needs Python 3, `brotli`, `e2fsprogs` (`debugfs`), Android build-tools (`aapt2`), `jadx`, and [`sdat2img.py`](https://github.com/xpirt/sdat2img).

```bash
SDAT2IMG=/path/to/sdat2img.py scripts/reproduce.sh /path/to/update-kindle-karat-RS8182_user_3811_0032548774788.bin
```

Extracted partitions and jadx output go to `.work/` (git-ignored). Note: the indexes in this repo were produced step by step from the same OTA; the script collects those steps but has not yet been run end to end in one pass.

| Script | Does |
|---|---|
| `scripts/manifest_db.py` | APKs → manifest DB (aapt2) |
| `scripts/graph.py` | manifest DB + libraries → dependency graph |
| `scripts/lint_removals.py` | fails a removal list that would break a kept package |
| `scripts/index_components.py` | manifest DB → components, actions, providers, permissions TSVs |
| `scripts/index_jadx.py` | jadx output → class, member and string-constant TSVs (no code bodies) |

## Related

- [tvos-26-re](https://github.com/AazainKhan/tvos-26-re): the same kind of map for tvOS 26.6, including every CoreAnimation spring and keyframe.
- [glass-os](https://github.com/AazainKhan/glass-os): the debloated Fire OS build this research feeds.
