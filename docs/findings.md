# Findings

Integration notes for replacing or interoperating with Fire OS components from a third-party launcher. Each entry names the evidence in this repo.

## Component triage

| Role | Package | Notes |
|---|---|---|
| Replace | `com.amazon.tv.launcher` | Declares 41 permissions; 41 packages depend on it (`data/graph.json`) |
| Replace | `com.amazon.firehomestarter` | No reverse dependencies |
| Replace (platform) | `com.android.systemui` (APK folder `FireTVSystemUI`) | Platform SystemUI, not an Amazon package |
| Wrap | `com.amazon.tv.settings.v2`, `com.amazon.tv.settings.core` | 52 and 1 dependants; a launcher can deep-link into their activities |
| Wrap | `com.amazon.tv.notificationcenter` | |
| Interop | `com.amazon.dialservice` | DIAL |
| Interop | `com.amazon.cast.sink` (APK folder `DisplayMirroring`) | Miracast sink |
| Interop | `com.amazon.whisperlink.core.android` | WhisperPlay/fling; also declares the HOME category |
| Interop | `com.amazon.tv.matter`, `com.amazon.tv.mattercohost` | Matter controller and co-host |
| Interop | `com.amazon.venezia` | Appstore runtime: installs, IAP, licensing; 53 dependants. Keep. |
| Interop | `com.amazon.autopairservice`, `com.amazon.uxcontrollerservice` | Remote auto-pair and its UX |
| Interop | `com.amazon.fireinputdevices`, `com.amazon.device.bluetoothkeymaplib` | Input devices and remote key maps |
| Understand only | DRM and provisioning | No `drm-*` APK in the 280 packages; DRM lives in native/vendor code. Never modified. |

## Early facts from the indexes

- **Remote auto-pair triggers.** `com.amazon.autopairservice.AutoPairService` reacts to `android.intent.action.BOOT_COMPLETED`, `amazon.intent.action.USER_SCREEN_ON`, `amazon.intent.action.USER_SCREEN_OFF`, and emits `com.amazon.device.action.AUTO_PAIR_COMPLETE_ACTION` (`index/java/com.amazon.autopairservice.strings.tsv`). This matches the observed re-pair shortly after boot.
- **Home start strategies.** `com.amazon.firehomestarter` chooses between `MainHomeStartStrategy`, `ChildHomeStartStrategy` and `OobeHomeStartStrategy` (`index/java/com.amazon.firehomestarter.classes.tsv`). A replacement launcher needs equivalents for the main profile, child profiles and out-of-box setup.
- **HOME competitors.** Packages that declare the HOME category: `android` (ResolverActivity), `com.amazon.tv.launcher`, `com.amazon.firehomestarter`, `com.amazon.tahoe`, `com.amazon.ftv.xpicker`, `com.amazon.tv.oobe`, `com.amazon.tv.settings.v2`, `com.amazon.whisperlink.core.android` (`index/packages.tsv`, `home=true`).

## Open questions

1. What gates the auto-pair dialog after boot, and can it be suppressed without root?
2. Which settings activities are exported and safe to deep-link (Wi-Fi, display, Bluetooth, HDMI-CEC)?
3. Does `com.amazon.whisperlink.core.android` ever win HOME resolution once the Amazon launcher is gone?
4. What does `com.amazon.tv.mattercohost` expose to other apps?
