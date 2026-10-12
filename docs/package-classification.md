# Package classification (Glass OS)

Generated 2026-10-10 from the stock OTA 0032548774788 (280 APKs, 280 packages; aapt2 manifests in `work/manifests/`, graph in `work/graph.json`). Inputs: `config/classification.tsv`, `config/remove-candidates.tsv`. Regenerate with Task 2 of the plan. 2026-10-10 revision: whisperjoin.middleware.v2.np and spotify.mediabrowserservice moved REMOVE → INVESTIGATE (now 30 REMOVE); Kids, AOSP leftovers and Silk get batches 6-8 (plan Task 3).

**Counts:** KEEP 194 · REMOVE 32 · INVESTIGATE 54

## How the evidence was gathered

- Every APK in system, system_ext, vendor, product was dumped with `aapt2 dump xmltree` and parsed into: sharedUserId, uses-library (required/optional), declared permissions + protectionLevel, uses-permission, exported components and their guard permission, provider authorities, HOME category.
- An edge P→Q exists when P requests a permission only Q declares, needs a shared library whose file is Q's APK, or names Q in meta-data. `R` = number of packages with an edge into this one.
- `tools/lint_removals.py` turns this into a gate: it fails if any kept package needs a required library from a removed APK, and warns when a kept component is guarded by a permission only removed packages declare while a kept package requests it. With the full REMOVE list (batches 1-5) it reports 0 errors and 0 warnings. Negative test: removing MetricsApi/MinervaApi gives 20+ errors (vizzini, venezia, settings…), so those libraries are KEEP.
- `DEBLOAT-LOG.md` is the runtime evidence: packages disabled since 2026-10-07/08 with no fallout. Disabled ≠ removed: a disabled package still declares its permissions and libraries, so removal is batched and gated even for these.
- **Limit:** the manifest graph misses runtime coupling. `com.amazon.aria` has only 6 manifest dependants, yet removing it crashed Alexa ("windowTemplateId cannot be null"). Hence: each batch is followed by the feature checklist and the Glass e2e suite.

## HOME-category packages

Stock: android (ResolverActivity), com.amazon.tv.launcher, com.amazon.firehomestarter, com.amazon.tahoe, com.amazon.ftv.xpicker, com.amazon.tv.oobe, com.amazon.tv.settings.v2, com.amazon.whisperlink.core.android. After batch 5 the launcher and starter are gone; Glass must be made the preferred home (plan Tasks 10 and 20) or Android shows a chooser / an Amazon HOME activity wins.

## Native services (not removed in v1, flagged)

`perfstatsd`, `integrity_logger`, `wlan_stats`, `read_diskstat`, `read_lifetime`, `salenativeservice_daemon`, `appstoreapkdropboxd`, `smarthomed`, `inlocservice` look like telemetry/retail/optional. `vendor_flash_recovery` (`/vendor/bin/install-recovery.sh` + `recovery-from-boot.p`) can rewrite the recovery partition from boot: see spec risk R4.

## Table

| Class | Package | APK path | R | Batch | Reason / evidence |
|---|---|---|---|---|---|
| REMOVE | `com.amazon.storm.lightning.tutorial` | system_ext/priv-app/com.amazon.storm.lightning.tutorial/com.amazon.storm.lightning.tutorial.apk | 0 | 1 | Tutorial; only depends on launcher/turnstile perms; no reverse deps |
| REMOVE | `com.amazon.tmm.tutorial` | system_ext/priv-app/com.amazon.tmm.tutorial/com.amazon.tmm.tutorial.apk | 0 | 1 | Tutorial app, no reverse deps, no declared perms in use |
| REMOVE | `com.amazon.device.metrics` | system_ext/app/AmazonDeviceMetrics/AmazonDeviceMetrics.apk | 0 | 2 | Metrics; disabled since 2026-10-07; no reverse deps |
| REMOVE | `com.amazon.device.software.ota.override` | system_ext/priv-app/DeviceSoftwareOTAIdleOverride/DeviceSoftwareOTAIdleOverride.apk | 0 | 2 | OTA idle override; disabled since 2026-10-07; no reverse deps |
| REMOVE | `com.amazon.device.telemetry.emitter` | system_ext/priv-app/com.amazon.device.telemetry.emitter-arm/com.amazon.device.telemetry.emitter-arm.apk | 0 | 2 | Telemetry; disabled since 2026-10-07; no reverse deps |
| REMOVE | `com.amazon.firetv.troubleshooting` | system_ext/priv-app/com.amazon.firetv.troubleshooting-stub/com.amazon.firetv.troubleshooting-stub.apk | 0 | 2 | Stub; disabled since 2026-10-08 (DEBLOAT-LOG) with no fallout |
| REMOVE | `com.amazon.ftvads.deeplinking` | system_ext/priv-app/com.amazon.ftvads.deeplinking/com.amazon.ftvads.deeplinking.apk | 0 | 2 | Ads deep-linking; disabled since 2026-10-07 with no fallout; no reverse deps |
| REMOVE | `com.amazon.tv.forcedotaupdater.v2` | system_ext/priv-app/com.amazon.tv.forcedotaupdater.v2/com.amazon.tv.forcedotaupdater.v2.apk | 2 | 2 | Forced OTA updater; disabled; reverse deps only oobe/settings uses-permission (grants become no-ops) |
| REMOVE | `com.amazon.whad` | system_ext/app/whad_app/whad_app.apk | 0 | 2 | Disabled since 2026-10-07; no reverse deps |
| REMOVE | `com.amazon.whisperjoin.middleware.v2.np` | system_ext/priv-app/com.amazon.whisperjoin.middleware.v2.np/com.amazon.whisperjoin.middleware.v2.np.apk | 0 | 2 | FFS Wi-Fi provisioning middleware; disabled since 2026-10-07; no reverse deps |
| REMOVE | `com.amazon.wirelessmetrics.service` | system_ext/app/AmazonWirelessMetricsService/AmazonWirelessMetricsService.apk | 0 | 2 | Wireless metrics; disabled since 2026-10-07; no reverse deps |
| REMOVE | `com.amazon.gamehub` | system_ext/priv-app/com.amazon.gamehub/com.amazon.gamehub.apk | 0 | 3 | Game hub promo; no reverse deps |
| REMOVE | `com.amazon.hybridadidservice` | system_ext/priv-app/HybridAdInfoService/HybridAdInfoService.apk | 0 | 3 | Advertising ID service; no reverse deps |
| REMOVE | `com.amazon.minitv.android.app` | system_ext/priv-app/com.amazon.minitv.android.app-stub/com.amazon.minitv.android.app-stub.apk | 0 | 3 | miniTV stub; no reverse deps |
| REMOVE | `com.amazon.neo.minerva.logcat` | system_ext/priv-app/com.amazon.neo.minerva.logcat-arm/com.amazon.neo.minerva.logcat-arm.apk | 0 | 3 | Log uploader; no reverse deps |
| REMOVE | `com.amazon.perfc` | system_ext/priv-app/com.amazon.perfc/com.amazon.perfc.apk | 0 | 3 | Perf collection; no reverse deps |
| REMOVE | `com.amazon.perfcollection` | system_ext/priv-app/com.amazon.perfcollection/com.amazon.perfcollection.apk | 0 | 3 | Perf collection; no reverse deps |
| REMOVE | `com.amazon.shoptv.client` | system_ext/priv-app/com.amazon.shoptv.client/com.amazon.shoptv.client.apk | 0 | 3 | Shopping; no reverse deps |
| REMOVE | `com.amazon.shoptv.firetv.client` | system_ext/priv-app/com.amazon.shoptv.firetv.client/com.amazon.shoptv.firetv.client.apk | 0 | 3 | Shopping; no reverse deps |
| REMOVE | `com.amazon.sneakpeek` | system_ext/priv-app/com.amazon.sneakpeek/com.amazon.sneakpeek.apk | 0 | 3 | Content promo; no reverse deps |
| REMOVE | `com.amazon.spotify.mediabrowserservice` | system_ext/priv-app/com.amazon.spotify.mediabrowserservice-stub/com.amazon.spotify.mediabrowserservice-stub.apk | 0 | 3 | Spotify browse stub; no reverse deps |
| REMOVE | `com.amazon.tv.acr` | system_ext/priv-app/com.amazon.tv.acr-stub/com.amazon.tv.acr-stub.apk | 0 | 3 | ACR (automatic content recognition) stub; no reverse deps |
| REMOVE | `com.amazon.tv.csapp` | system_ext/priv-app/com.amazon.tv.csapp/com.amazon.tv.csapp.apk | 0 | 3 | Customer-support app; no reverse deps |
| REMOVE | `com.amazon.tv.earlyaccess` | system_ext/priv-app/com.amazon.tv.earlyaccess-stub/com.amazon.tv.earlyaccess-stub.apk | 0 | 3 | Early-access stub; no reverse deps |
| REMOVE | `com.amazon.tv.releasenotes` | system_ext/priv-app/com.amazon.tv.releasenotes/com.amazon.tv.releasenotes.apk | 0 | 3 | Release notes for OTAs; no reverse deps |
| REMOVE | `com.fireos.usagestats.proxy` | system_ext/priv-app/AmazonUsageStatsListener/AmazonUsageStatsListener.apk | 0 | 3 | Usage-stats listener; no reverse deps |
| REMOVE | `com.amazon.device.crashmanager` | system_ext/priv-app/com.amazon.device.crashmanager/com.amazon.device.crashmanager.apk | 2 | 4 | Crash uploader; disabled since 2026-10-07; reverse deps csapp,wifilocker only |
| REMOVE | `com.amazon.device.software.ota` | system_ext/priv-app/DeviceSoftwareOTA/DeviceSoftwareOTA.apk | 19 | 4 | OTA service; disabled since 2026-10-07; sharedUserId with override; declares perms used by 19 pkgs |
| REMOVE | `com.amazon.media.recommendations` | system_ext/priv-app/FireTvNotificationService/FireTvNotificationService.apk | 8 | 4 | FireTvNotificationService recommendations; disabled since 2026-10-07; declares perms used by 8 pkgs |
| REMOVE | `com.amazon.neo.minerva` | system_ext/priv-app/com.amazon.neo.minerva-arm/com.amazon.neo.minerva-arm.apk | 106 | 4 | Minerva metrics service; disabled since 2026-10-07; declares perms used by 106 pkgs (uses-permission only) |
| REMOVE | `com.amazon.firehomestarter` | system_ext/priv-app/com.amazon.firehomestarter/com.amazon.firehomestarter.apk | 0 | 5 | Home starter; disabled today; no reverse deps, no declared perms |
| REMOVE | `com.amazon.tv.launcher` | system_ext/priv-app/com.amazon.tv.launcher/com.amazon.tv.launcher.apk | 41 | 5 | Amazon launcher; disabled today; declares 41 perms; guarded components outside launcher are launcher-card flows only |
| INVESTIGATE | `com.amazon.aca` | system_ext/priv-app/com.amazon.aca/com.amazon.aca.apk | 3 |  | R3 launcher, venezia, ambient |
| INVESTIGATE | `com.amazon.adep` | system_ext/priv-app/com.amazon.adep/com.amazon.adep.apk | 0 |  | Unknown |
| INVESTIGATE | `com.amazon.aiondec` | system_ext/priv-app/com.amazon.aiondec-stub/com.amazon.aiondec-stub.apk | 0 |  | Stub depending on vizzini+aria; purpose unknown |
| INVESTIGATE | `com.amazon.ale` | system_ext/priv-app/com.amazon.ale/com.amazon.ale.apk | 0 |  | Unknown |
| INVESTIGATE | `com.amazon.alta.h2clientservice` | system_ext/priv-app/com.amazon.h2clientservice/com.amazon.h2clientservice.apk | 5 |  | H2 client; R5 incl. profilepicker chain (prism) |
| INVESTIGATE | `com.amazon.android.marketplace` | system_ext/priv-app/marketplace_service_receiver/marketplace_service_receiver.apk | 0 |  | Marketplace receiver (system uid) |
| INVESTIGATE | `com.amazon.appaccesskeyprovider` | system_ext/priv-app/com.amazon.appaccesskeyprovider/com.amazon.appaccesskeyprovider.apk | 0 |  | App access keys for settings |
| INVESTIGATE | `com.amazon.application.compatibility.enforcer` | system_ext/priv-app/FireApplicationCompatibilityEnforcer/FireApplicationCompatibilityEnforcer.apk | 0 |  | App compatibility enforcer (may block apps) |
| INVESTIGATE | `com.amazon.application.compatibility.enforcer.sdk.library` | system_ext/priv-app/FireApplicationCompatibilityEnforcerSDK/FireApplicationCompatibilityEnforcerSDK.apk | 0 |  | Its SDK library |
| INVESTIGATE | `com.amazon.audiohome` | system_ext/priv-app/com.amazon.audiohome-stub/com.amazon.audiohome-stub.apk | 0 |  | Multi-room audio stub |
| INVESTIGATE | `com.amazon.avls.experience` | system_ext/priv-app/com.amazon.avls.experience/com.amazon.avls.experience.apk | 0 |  | Audio/video latency experience |
| INVESTIGATE | `com.amazon.bueller.music` | system_ext/priv-app/com.amazon.bueller.music-stub/com.amazon.bueller.music-stub.apk | 0 |  | Amazon Music stub |
| INVESTIGATE | `com.amazon.bueller.photos` | system_ext/priv-app/com.amazon.bueller.photos-stub/com.amazon.bueller.photos-stub.apk | 1 |  | Amazon Photos stub; screensaver photo source; R1 parentalcontrols |
| INVESTIGATE | `com.amazon.cloud9` | system_ext/priv-app/com.amazon.cloud9-stub/com.amazon.cloud9-stub.apk | 0 |  | Silk browser stub |
| INVESTIGATE | `com.amazon.d3` | system_ext/priv-app/com.amazon.d3/com.amazon.d3.apk | 0 |  | Unknown; uses OTA + devicecontrol perms |
| INVESTIGATE | `com.amazon.dcp` | system_ext/priv-app/FireOsMiddlewareDebugApp/FireOsMiddlewareDebugApp.apk | 1 |  | FireOsMiddlewareDebugApp; R1 device.sync |
| INVESTIGATE | `com.amazon.dcp.contracts.library` | system_ext/priv-app/DeviceSoftwareOTAContracts/DeviceSoftwareOTAContracts.apk | 0 |  | DeviceSoftwareOTAContracts library; remove only with lint green |
| INVESTIGATE | `com.amazon.device.details` | system_ext/priv-app/com.amazon.device.details/com.amazon.device.details.apk | 0 |  | Device details |
| INVESTIGATE | `com.amazon.device.logmanager` | system_ext/priv-app/com.amazon.device.logmanager/com.amazon.device.logmanager.apk | 6 |  | Log manager (system uid); R6 |
| INVESTIGATE | `com.amazon.device.sync` | system_ext/priv-app/com.amazon.device.sync/com.amazon.device.sync.apk | 0 |  | Device sync |
| INVESTIGATE | `com.amazon.device.sync.sdk.internal` | system_ext/priv-app/com.amazon.device.sync.sdk.internal/com.amazon.device.sync.sdk.internal.apk | 0 |  | Device sync SDK |
| INVESTIGATE | `com.amazon.device_remote_config_sync_service` | system_ext/priv-app/DRCSService-arm/DRCSService-arm.apk | 0 |  | Remote config sync (DRCS) |
| INVESTIGATE | `com.amazon.diode` | system_ext/priv-app/com.amazon.diode/com.amazon.diode.apk | 0 |  | Unknown; uses logan |
| INVESTIGATE | `com.amazon.dpcclient` | system_ext/priv-app/com.amazon.dpcclient/com.amazon.dpcclient.apk | 0 |  | Device policy client |
| INVESTIGATE | `com.amazon.firebat` | system_ext/priv-app/com.amazon.firebat-stub/com.amazon.firebat-stub.apk | 2 |  | Prime Video stub (Glass references it); keep if user watches Prime Video |
| INVESTIGATE | `com.amazon.fireos.cirruscloud` | system_ext/priv-app/cirrus.cloudservice/cirrus.cloudservice.apk | 0 |  | Cirrus cloud service (system uid) |
| INVESTIGATE | `com.amazon.franktvinput` | system_ext/priv-app/com.amazon.franktvinput/com.amazon.franktvinput.apk | 0 |  | TV input for Amazon channels |
| INVESTIGATE | `com.amazon.ftv.xpicker` | system_ext/priv-app/com.amazon.ftv.xpicker/com.amazon.ftv.xpicker.apk | 0 |  | HOME category; picker for profiles/kids |
| INVESTIGATE | `com.amazon.ftvcalibrationservice` | system_ext/app/aht_ftv_service/aht_ftv_service.apk | 0 |  | aht_ftv_service calibration |
| INVESTIGATE | `com.amazon.ftvspatial` | system_ext/priv-app/com.amazon.ftvspatial/com.amazon.ftvspatial.apk | 0 |  | Spatial audio? |
| INVESTIGATE | `com.amazon.hedwig` | system_ext/priv-app/com.amazon.hedwig-stub/com.amazon.hedwig-stub.apk | 0 |  | Stub; Glass hides it |
| INVESTIGATE | `com.amazon.kso.blackbird` | system_ext/priv-app/com.amazon.kso.blackbird/com.amazon.kso.blackbird.apk | 4 |  | KSO (special offers/ads) but screensaver and launcher use its perms; R4 |
| INVESTIGATE | `com.amazon.logan` | system_ext/priv-app/Logan/Logan.apk | 6 |  | R6 incl. vizzini, quicksettings, settings; name suggests logging |
| INVESTIGATE | `com.amazon.neopactservice` | system_ext/priv-app/com.amazon.neopactservice/com.amazon.neopactservice.apk | 0 |  | Pact service; purpose unclear |
| INVESTIGATE | `com.amazon.ods.kindleconnect` | system_ext/priv-app/com.amazon.ods.kindleconnect/com.amazon.ods.kindleconnect.apk | 0 |  | On-device support/connect |
| INVESTIGATE | `com.amazon.privacypassservice` | system_ext/priv-app/com.amazon.privacypassservice/com.amazon.privacypassservice.apk | 0 |  | Privacy Pass tokens (may be used by streaming auth) |
| INVESTIGATE | `com.amazon.rtcsessioncontroller` | system_ext/priv-app/com.amazon.rtcsessioncontroller/com.amazon.rtcsessioncontroller.apk | 1 |  | Video calling; R1 smarthome |
| INVESTIGATE | `com.amazon.securitysyncclient` | system_ext/priv-app/com.amazon.securitysyncclient/com.amazon.securitysyncclient.apk | 0 |  | Security sync |
| INVESTIGATE | `com.amazon.sharingservice.android.client.proxy` | system_ext/priv-app/com.amazon.sharingservice.android.client.proxy.release/com.amazon.sharingservice.android.client.proxy.release.apk | 0 |  | Sharing service |
| INVESTIGATE | `com.amazon.spiderpork` | system_ext/priv-app/com.amazon.spiderpork/com.amazon.spiderpork.apk | 0 |  | Unknown; uses logmanager |
| INVESTIGATE | `com.amazon.ssm` | system_ext/priv-app/SystemStatusMonitor/SystemStatusMonitor.apk | 0 |  | System status monitor |
| INVESTIGATE | `com.amazon.ssmsys` | system_ext/priv-app/com.amazon.ssmsys/com.amazon.ssmsys.apk | 2 |  | R2 ssm, launcher |
| INVESTIGATE | `com.amazon.tahoe` | system_ext/priv-app/com.amazon.tahoe/com.amazon.tahoe.apk | 3 |  | Amazon Kids; HOME category; R3 profilepicker,xpicker |
| INVESTIGATE | `com.amazon.tigris` | system_ext/priv-app/com.amazon.tigris/com.amazon.tigris.apk | 0 |  | Unknown; uses launcher perms |
| INVESTIGATE | `com.amazon.tv.easyupgrade` | system_ext/priv-app/com.amazon.tv.easyupgrade/com.amazon.tv.easyupgrade.apk | 4 |  | Upgrade promo; but R4 incl. oobe, settings, parentalcontrols |
| INVESTIGATE | `com.amazon.tv.ffsprovisioneeclient` | system_ext/priv-app/com.amazon.tv.ffsprovisioneeclient/com.amazon.tv.ffsprovisioneeclient.apk | 0 |  | Frustration-free setup client; only needed at setup |
| INVESTIGATE | `com.amazon.tv.ftvambient` | system_ext/priv-app/com.amazon.tv.ftvambient-stub/com.amazon.tv.ftvambient-stub.apk | 0 |  | Ambient experience stub; screensaver alternative |
| INVESTIGATE | `com.amazon.tv.matter` | system_ext/priv-app/com.amazon.tv.matter/com.amazon.tv.matter.apk | 1 |  | Matter smart home |
| INVESTIGATE | `com.amazon.tv.mattercohost` | system_ext/priv-app/com.amazon.tv.mattercohost/com.amazon.tv.mattercohost.apk | 1 |  | Matter co-host (system uid) |
| INVESTIGATE | `com.amazon.tv.turnstile` | system_ext/priv-app/com.amazon.tv.turnstile/com.amazon.tv.turnstile.apk | 4 |  | R4 incl. vizzini; turnstile/onboarding |
| INVESTIGATE | `com.amazon.tv.website_launcher` | system_ext/priv-app/com.amazon.tv.website_launcher/com.amazon.tv.website_launcher.apk | 0 |  | Website launcher |
| INVESTIGATE | `com.amazon.whasettings` | system_ext/priv-app/com.amazon.whasettings/com.amazon.whasettings.apk | 1 |  | Whole-home audio settings |
| INVESTIGATE | `com.amazon.wifilocker` | system_ext/priv-app/CredentialLockerAndroid-tablet-release/CredentialLockerAndroid-tablet-release.apk | 1 |  | Wi-Fi credential locker (cloud sync); R1 settings |
| INVESTIGATE | `com.fireos.arcus.proxy` | system_ext/priv-app/ArcusListener/ArcusListener.apk | 0 |  | Arcus remote config listener |
| KEEP | `amazon.fireos` | system_ext/app/fireos-res/fireos-res.apk | 0 |  | fireos-res framework resources |
| KEEP | `android` | system/framework/framework-res.apk | 178 |  | Framework |
| KEEP | `android.amazon.perm` | system_ext/app/android.amazon.perm/android.amazon.perm.apk | 128 |  | Declares Amazon platform permissions used by 128 pkgs |
| KEEP | `android.auto_generated_rro_product__` | product/overlay/framework-res/auto_generated_rro_product.apk | 0 |  | AOSP/platform component; out of scope for v1 removal |
| KEEP | `android.auto_generated_rro_vendor__` | vendor/overlay/framework-res/auto_generated_rro_vendor.apk | 0 |  | AOSP/platform component; out of scope for v1 removal |
| KEEP | `android.ext.shared` | system/app/ExtShared/ExtShared.apk | 0 |  | AOSP/platform component; out of scope for v1 removal |
| KEEP | `com.amazon.accessoryconfigservice` | system_ext/priv-app/AmazonAccessoryConfigService/AmazonAccessoryConfigService.apk | 4 |  | Accessory config; R4 incl. vizzini, ime |
| KEEP | `com.amazon.ace.sensorsd.service` | system_ext/priv-app/AmazonSensorsService/AmazonSensorsService.apk | 0 |  | Sensors service |
| KEEP | `com.amazon.alexa.datastore.app` | system_ext/priv-app/com.amazon.alexa.datastore.app-stub/com.amazon.alexa.datastore.app-stub.apk | 6 |  | Alexa datastore stub; R6 incl. aria |
| KEEP | `com.amazon.alexa.externalmediaplayer.fireos` | system_ext/priv-app/com.amazon.alexa.externalmediaplayer.fireos/com.amazon.alexa.externalmediaplayer.fireos.apk | 0 |  | Alexa media control of 3P apps |
| KEEP | `com.amazon.alexadirectivebrokerservice` | system_ext/priv-app/alexadirectivebrokerservice/alexadirectivebrokerservice.apk | 0 |  | Alexa directive broker (vizzini client) |
| KEEP | `com.amazon.alexamediaplayer.runtime.ftv` | system_ext/priv-app/com.amazon.alexamediaplayer.runtime.ftv-stub/com.amazon.alexamediaplayer.runtime.ftv-stub.apk | 0 |  | Alexa media player runtime stub |
| KEEP | `com.amazon.android.devicemodelinfo.resources` | system_ext/app/DeviceModelInfo-res/DeviceModelInfo-res.apk | 0 |  | Resource pkg |
| KEEP | `com.amazon.aria` | system_ext/priv-app/com.amazon.aria/com.amazon.aria.apk | 6 |  | Alexa runtime; removing it broke Alexa on 2026-10-07 (CLAUDE.md); declares Alexa extension perms |
| KEEP | `com.amazon.autopairservice` | system_ext/priv-app/AutoPairService/AutoPairService.apk | 0 |  | Remote auto-pair (keepalive script depends on it) |
| KEEP | `com.amazon.avsyncslider` | system_ext/priv-app/com.amazon.avsyncslider/com.amazon.avsyncslider.apk | 0 |  | AV sync slider (audio settings) |
| KEEP | `com.amazon.awvflingreceiver` | system_ext/priv-app/FireTVDefaultMediaReceiver/FireTVDefaultMediaReceiver.apk | 0 |  | Fling/default media receiver |
| KEEP | `com.amazon.cast.sink` | system_ext/priv-app/DisplayMirroring/DisplayMirroring.apk | 0 |  | Screen mirroring (Miracast) |
| KEEP | `com.amazon.ceviche` | system_ext/priv-app/com.amazon.ceviche/com.amazon.ceviche.apk | 29 |  | Device registration/config client; R29 |
| KEEP | `com.amazon.client.metrics.api` | system_ext/priv-app/MetricsApi/MetricsApi.apk | 6 |  | Required shared library com.fireos.sdk.metrics (venezia, livetv, routing...); lint fails without it |
| KEEP | `com.amazon.connection_manager_neo_service` | system_ext/priv-app/com.amazon.connection_manager_neo_service-arm/com.amazon.connection_manager_neo_service-arm.apk | 0 |  | Connection manager |
| KEEP | `com.amazon.connectivitycontroller` | system_ext/priv-app/ConnectivityControllerService/ConnectivityControllerService.apk | 0 |  | Wi-Fi/network UX |
| KEEP | `com.amazon.connectivitydiag` | system_ext/priv-app/ConnectivityDiag-default/ConnectivityDiag-default.apk | 0 |  | Network diagnostics (system uid) |
| KEEP | `com.amazon.cpl` | system_ext/priv-app/CaptivePortalLauncher/CaptivePortalLauncher.apk | 0 |  | Captive portal launcher |
| KEEP | `com.amazon.csm.htmlruntime` | system_ext/priv-app/com.amazon.csm.htmlruntime/com.amazon.csm.htmlruntime.apk | 0 |  | Alexa visual cards runtime (aria/vizzini) |
| KEEP | `com.amazon.dcp.contracts.framework.library` | system_ext/priv-app/DeviceClientPlatformContractsFramework/DeviceClientPlatformContractsFramework.apk | 0 |  | Shared library (DeviceClientPlatformContractsFramework) |
| KEEP | `com.amazon.device.blepa` | system_ext/priv-app/com.amazon.device.blepa/com.amazon.device.blepa.apk | 0 |  | BLE pairing agent (remotes) |
| KEEP | `com.amazon.device.bluetoothkeymaplib` | system_ext/priv-app/BluetoothKeyMapLib/BluetoothKeyMapLib.apk | 0 |  | Remote key maps |
| KEEP | `com.amazon.device.bluetoothpa` | system_ext/priv-app/com.amazon.device.bluetoothpa/com.amazon.device.bluetoothpa.apk | 0 |  | Bluetooth pairing agent |
| KEEP | `com.amazon.device.lowstoragemanager` | system_ext/priv-app/com.amazon.device.lowstoragemanager/com.amazon.device.lowstoragemanager.apk | 0 |  | Low-storage handling |
| KEEP | `com.amazon.device.messaging` | system_ext/priv-app/DeviceMessagingAndroid/DeviceMessagingAndroid.apk | 33 |  | ADM messaging; R33; apps' push |
| KEEP | `com.amazon.device.messaging.sdk.internal.library` | system_ext/priv-app/DeviceMessagingAndroidInternalSDK/DeviceMessagingAndroidInternalSDK.apk | 8 |  | Required shared library (com.fireos.sdk.messaging); R8 |
| KEEP | `com.amazon.device.messaging.sdk.library` | system_ext/priv-app/DeviceMessagingAndroidSDK/DeviceMessagingAndroidSDK.apk | 0 |  | Shared library com.fireos.sdk.adm used by 3P apps (ADM push) |
| KEEP | `com.amazon.dialservice` | system_ext/priv-app/com.amazon.dialservice/com.amazon.dialservice.apk | 0 |  | DIAL (YouTube/Netflix cast from phone) |
| KEEP | `com.amazon.dp.logger` | system_ext/priv-app/com.amazon.dp.logger/com.amazon.dp.logger.apk | 3 |  | Shared library for whisperplay stack; R3 |
| KEEP | `com.amazon.dummy.alarmclock` | system_ext/app/DummyAlarmClock/DummyAlarmClock.apk | 0 |  | Intent sink so apps don't crash |
| KEEP | `com.amazon.dummy.calendar` | system_ext/app/DummyCalendar/DummyCalendar.apk | 0 |  | Intent sink |
| KEEP | `com.amazon.dummy.contacts` | system_ext/app/DummyContacts/DummyContacts.apk | 0 |  | Intent sink |
| KEEP | `com.amazon.dummy.gallery` | system_ext/app/DummyGallery/DummyGallery.apk | 0 |  | Intent sink |
| KEEP | `com.amazon.dummy.music` | system_ext/app/DummyMusic/DummyMusic.apk | 0 |  | Intent sink |
| KEEP | `com.amazon.dummy.settings` | system_ext/app/DummySettings/DummySettings.apk | 0 |  | Intent sink |
| KEEP | `com.amazon.dummy.soundpicker` | system_ext/app/DummySoundPicker/DummySoundPicker.apk | 0 |  | Intent sink |
| KEEP | `com.amazon.fireinputdevices` | system_ext/priv-app/com.amazon.fireinputdevices/com.amazon.fireinputdevices.apk | 0 |  | Input devices |
| KEEP | `com.amazon.firetv.androidskillconnectioncapability` | system_ext/priv-app/com.amazon.firetv.androidskillconnectioncapability/com.amazon.firetv.androidskillconnectioncapability.apk | 3 |  | Alexa-to-app skills ("Alexa, open X"); R3 |
| KEEP | `com.amazon.ftv.profilepicker` | system_ext/priv-app/com.amazon.ftv.profilepicker/com.amazon.ftv.profilepicker.apk | 7 |  | Profiles; R7 |
| KEEP | `com.amazon.ftv.screensaver` | system_ext/priv-app/com.amazon.ftv.screensaver/com.amazon.ftv.screensaver.apk | 4 |  | Screensaver path (Fire only runs Amazon screensavers) |
| KEEP | `com.amazon.identity.auth.device.authorization` | system_ext/priv-app/com.amazon.identity.auth.device.authorization/com.amazon.identity.auth.device.authorization.apk | 3 |  | Amazon account / MAP auth; R3 incl. vizzini, device.messaging |
| KEEP | `com.amazon.imp` | system_ext/priv-app/com.amazon.imp/com.amazon.imp.apk | 96 |  | Declares perms used by 96 pkgs (core platform plumbing) |
| KEEP | `com.amazon.kindleautomatictimezone` | system_ext/priv-app/AutomaticTimeZone.appservice/AutomaticTimeZone.appservice.apk | 0 |  | Automatic time zone (system uid) |
| KEEP | `com.amazon.livedeviceservice` | system_ext/priv-app/com.amazon.livedeviceservice/com.amazon.livedeviceservice.apk | 3 |  | Live device service; R3 |
| KEEP | `com.amazon.minerva.client.api` | system_ext/priv-app/MinervaApi/MinervaApi.apk | 33 |  | Required shared library com.fireos.sdk.minerva (vizzini, venezia, settings...); lint fails without it |
| KEEP | `com.amazon.neodelegate` | system/priv-app/com.amazon.neo.delegateservice/com.amazon.neo.delegateservice.apk | 2 |  | Neo platform delegate (system uid, /system/priv-app) |
| KEEP | `com.amazon.platform.fdra` | system_ext/app/fdra/fdra.apk | 2 |  | FDRA (system uid); R2 incl. ivona |
| KEEP | `com.amazon.prism.android.service` | system_ext/priv-app/com.amazon.prism.android.service/com.amazon.prism.android.service.apk | 1 |  | Profile sync for profilepicker |
| KEEP | `com.amazon.providers.contentsupport` | system_ext/priv-app/com.amazon.providers.contentsupport/com.amazon.providers.contentsupport.apk | 2 |  | Content support provider (system uid); R2 logan, ivona |
| KEEP | `com.amazon.providers.tv` | system_ext/priv-app/com.amazon.providers.tv/com.amazon.providers.tv.apk | 0 |  | TV provider extensions |
| KEEP | `com.amazon.smarthomemapviewapp` | system_ext/priv-app/com.amazon.smarthomemapviewapp/com.amazon.smarthomemapviewapp.apk | 1 |  | Smart-home dashboard; Glass Control Center opens it |
| KEEP | `com.amazon.storage.manager` | system_ext/priv-app/com.amazon.storage.manager/com.amazon.storage.manager.apk | 1 |  | Storage manager |
| KEEP | `com.amazon.systemnotices` | system_ext/app/AmazonSystemNoticesService/AmazonSystemNoticesService.apk | 0 |  | System notices |
| KEEP | `com.amazon.tcomm` | system_ext/priv-app/com.amazon.tcomm/com.amazon.tcomm.apk | 9 |  | Cloud comms; R9 incl. device.messaging |
| KEEP | `com.amazon.tcomm.client` | system_ext/priv-app/com.amazon.communication/com.amazon.communication.apk | 1 |  | tcomm client (com.amazon.communication) |
| KEEP | `com.amazon.tcomm.jackson` | system_ext/priv-app/com.amazon.tcomm.jackson/com.amazon.tcomm.jackson.apk | 0 |  | Shared library com.amazon.tcomm.jackson_lib |
| KEEP | `com.amazon.tifobserver` | system_ext/priv-app/TIFObserverService/TIFObserverService.apk | 2 |  | TIF observer (system uid); R2 |
| KEEP | `com.amazon.tiramisubootsupport` | system_ext/priv-app/TiramisuBootSupport/TiramisuBootSupport.apk | 0 |  | Boot support (has init service) |
| KEEP | `com.amazon.tv.alexaalerts` | system_ext/priv-app/com.amazon.tv.alexaalerts/com.amazon.tv.alexaalerts.apk | 1 |  | Alexa alerts; aria depends on its perms |
| KEEP | `com.amazon.tv.alexanotifications` | system_ext/priv-app/com.amazon.tv.alexanotifications/com.amazon.tv.alexanotifications.apk | 0 |  | Alexa notifications |
| KEEP | `com.amazon.tv.arc` | system_ext/priv-app/com.amazon.tv.arc/com.amazon.tv.arc.apk | 0 |  | HDMI ARC; part of volume path |
| KEEP | `com.amazon.tv.consents` | system_ext/priv-app/com.amazon.tv.consents/com.amazon.tv.consents.apk | 2 |  | Privacy consents used by oobe/settings |
| KEEP | `com.amazon.tv.developer.dataservice` | system_ext/priv-app/com.amazon.tv.developer.dataservice/com.amazon.tv.developer.dataservice.apk | 1 |  | Content SDK data service for 3P apps |
| KEEP | `com.amazon.tv.devicecontrol` | system_ext/priv-app/com.amazon.tv.devicecontrol/com.amazon.tv.devicecontrol.apk | 10 |  | Equipment control (CEC/IR volume); R10 |
| KEEP | `com.amazon.tv.devicecontrolsettings` | system_ext/priv-app/com.amazon.tv.devicecontrolsettings/com.amazon.tv.devicecontrolsettings.apk | 1 |  | Equipment control settings |
| KEEP | `com.amazon.tv.ime` | system_ext/priv-app/com.amazon.tv.ime/com.amazon.tv.ime.apk | 3 |  | Fire keyboard; R3 |
| KEEP | `com.amazon.tv.inputpreference.service` | system_ext/priv-app/com.amazon.tv.inputpreference/com.amazon.tv.inputpreference.apk | 5 |  | Input/HDMI preference; R5 |
| KEEP | `com.amazon.tv.intentsupport` | system_ext/app/TvUnsupportedIntent/TvUnsupportedIntent.apk | 0 |  | Unsupported-intent handler for apps |
| KEEP | `com.amazon.tv.keypolicymanager` | system_ext/app/KeyPolicyManagerUI/KeyPolicyManagerUI.apk | 0 |  | Key policy UI; interacts with remote-keys remap |
| KEEP | `com.amazon.tv.legal.notices` | system_ext/priv-app/com.amazon.tv.legal.notices/com.amazon.tv.legal.notices.apk | 4 |  | Legal notices; R4 |
| KEEP | `com.amazon.tv.legalresources` | system_ext/app/legalresources/legalresources.apk | 0 |  | Legal resources |
| KEEP | `com.amazon.tv.livetv` | system_ext/priv-app/com.amazon.tv.livetv/com.amazon.tv.livetv.apk | 10 |  | Live TV; R10 |
| KEEP | `com.amazon.tv.notificationcenter` | system_ext/priv-app/com.amazon.tv.notificationcenter/com.amazon.tv.notificationcenter.apk | 1 |  | Notifications |
| KEEP | `com.amazon.tv.oobe` | system_ext/priv-app/com.amazon.tv.oobe/com.amazon.tv.oobe.apk | 15 |  | Setup wizard (needed after factory reset); R15 |
| KEEP | `com.amazon.tv.ooberesource` | system_ext/app/ooberesource/ooberesource.apk | 0 |  | OOBE resources (system uid) |
| KEEP | `com.amazon.tv.ottssocompanionapp` | system_ext/priv-app/com.amazon.tv.ottssocompanionapp/com.amazon.tv.ottssocompanionapp.apk | 0 |  | SSO companion for streaming-app sign-in |
| KEEP | `com.amazon.tv.parentalcontrols` | system_ext/priv-app/com.amazon.tv.parentalcontrols/com.amazon.tv.parentalcontrols.apk | 13 |  | Parental controls / PIN; R13 |
| KEEP | `com.amazon.tv.quicksettings.ui` | system_ext/priv-app/com.amazon.tv.quicksettings.ui/com.amazon.tv.quicksettings.ui.apk | 5 |  | Fire quick menu (user wants it left in place) |
| KEEP | `com.amazon.tv.quicksettings.ui.overlay` | product/overlay/com.amazon.tv.quicksettings.ui.overlay.apk | 0 |  | RRO for quick settings |
| KEEP | `com.amazon.tv.resolutioncycler` | system_ext/app/FireTvResolutionCycler/FireTvResolutionCycler.apk | 0 |  | Display mode recovery |
| KEEP | `com.amazon.tv.routing` | system_ext/priv-app/com.amazon.tv.routing/com.amazon.tv.routing.apk | 9 |  | Deep-link routing; R9 |
| KEEP | `com.amazon.tv.settings.core` | system_ext/priv-app/com.amazon.tv.settings.core/com.amazon.tv.settings.core.apk | 1 |  | Settings core (system uid) |
| KEEP | `com.amazon.tv.settings.v2` | system_ext/priv-app/com.amazon.tv.settings.v2/com.amazon.tv.settings.v2.apk | 52 |  | Fire Settings; R52; Glass opens Settings intents |
| KEEP | `com.amazon.tv.support` | system_ext/priv-app/com.amazon.tv.aiv.support/com.amazon.tv.aiv.support.apk | 4 |  | aiv.support: Prime Video playback/purchase support; R4 |
| KEEP | `com.amazon.tv.sysappsinternal.resources` | system_ext/app/FireTvSysappsLib-res/FireTvSysappsLib-res.apk | 0 |  | Resource pkg |
| KEEP | `com.amazon.uxcontrollerservice` | system_ext/priv-app/UXControllerService/UXControllerService.apk | 2 |  | Pairing UX controller; R2 incl. autopairservice |
| KEEP | `com.amazon.uxnotification` | system_ext/priv-app/UXNotificationService/UXNotificationService.apk | 2 |  | Pairing UX notifications; R2 |
| KEEP | `com.amazon.venezia` | system_ext/priv-app/com.amazon.venezia/com.amazon.venezia.apk | 53 |  | Appstore runtime: installs, IAP, licensing/DRM for Amazon-store apps; R53 |
| KEEP | `com.amazon.vizzini` | system_ext/priv-app/com.amazon.vizzini/com.amazon.vizzini.apk | 97 |  | Alexa voice; declares perms used by 97 pkgs; Glass AlexaIcon targets it |
| KEEP | `com.amazon.webview.chromium` | system_ext/app/AmazonWebView/AmazonWebView.apk | 0 |  | WebView (apps, sign-in pages) |
| KEEP | `com.amazon.whisperlink.core.android` | system_ext/priv-app/WhisperplayCore/WhisperplayCore.apk | 1 |  | WhisperPlay core (DIAL/fling); has HOME category, check home resolution |
| KEEP | `com.amazon.whisperplay.contracts` | system_ext/priv-app/WhisperlinkSdk/WhisperlinkSdk.apk | 4 |  | WhisperlinkSdk shared library; R4 |
| KEEP | `com.amazon.whisperplay.service.install` | system_ext/priv-app/WhisperplayInstall/WhisperplayInstall.apk | 0 |  | WhisperPlay install |
| KEEP | `com.android.backupconfirm` | system/priv-app/BackupRestoreConfirmation/BackupRestoreConfirmation.apk | 0 |  | AOSP/platform component; out of scope for v1 removal |
| KEEP | `com.android.bluetooth` | system/app/Bluetooth/Bluetooth.apk | 0 |  | AOSP/platform component; out of scope for v1 removal |
| KEEP | `com.android.bluetoothmidiservice` | system/app/BluetoothMidiService/BluetoothMidiService.apk | 0 |  | AOSP/platform component; out of scope for v1 removal |
| KEEP | `com.android.bookmarkprovider` | system/app/BookmarkProvider/BookmarkProvider.apk | 0 |  | AOSP/platform component; out of scope for v1 removal |
| KEEP | `com.android.calllogbackup` | system/priv-app/CallLogBackup/CallLogBackup.apk | 0 |  | AOSP/platform component; out of scope for v1 removal |
| KEEP | `com.android.carrierconfig` | system_ext/priv-app/CarrierConfig/CarrierConfig.apk | 0 |  | AOSP/platform component; out of scope for v1 removal |
| KEEP | `com.android.certinstaller` | system/app/CertInstaller/CertInstaller.apk | 0 |  | AOSP/platform component; out of scope for v1 removal |
| KEEP | `com.android.companiondevicemanager` | system/app/CompanionDeviceManager/CompanionDeviceManager.apk | 0 |  | AOSP/platform component; out of scope for v1 removal |
| KEEP | `com.android.cts.ctsshim` | system/app/CtsShimPrebuilt/CtsShimPrebuilt.apk | 0 |  | AOSP/platform component; out of scope for v1 removal |
| KEEP | `com.android.cts.priv.ctsshim` | system/priv-app/CtsShimPrivPrebuilt/CtsShimPrivPrebuilt.apk | 0 |  | AOSP/platform component; out of scope for v1 removal |
| KEEP | `com.android.dreams.basic` | system/app/BasicDreams/BasicDreams.apk | 0 |  | AOSP/platform component; out of scope for v1 removal |
| KEEP | `com.android.dynsystem` | system/priv-app/DynamicSystemInstallationService/DynamicSystemInstallationService.apk | 0 |  | AOSP/platform component; out of scope for v1 removal |
| KEEP | `com.android.externalstorage` | system/priv-app/ExternalStorageProvider/ExternalStorageProvider.apk | 0 |  | AOSP/platform component; out of scope for v1 removal |
| KEEP | `com.android.htmlviewer` | system/app/HTMLViewer/HTMLViewer.apk | 0 |  | AOSP/platform component; out of scope for v1 removal |
| KEEP | `com.android.internal.display.cutout.emulation.corner` | product/overlay/DisplayCutoutEmulationCorner/DisplayCutoutEmulationCornerOverlay.apk | 0 |  | AOSP/platform component; out of scope for v1 removal |
| KEEP | `com.android.internal.display.cutout.emulation.double` | product/overlay/DisplayCutoutEmulationDouble/DisplayCutoutEmulationDoubleOverlay.apk | 0 |  | AOSP/platform component; out of scope for v1 removal |
| KEEP | `com.android.internal.display.cutout.emulation.hole` | product/overlay/DisplayCutoutEmulationHole/DisplayCutoutEmulationHoleOverlay.apk | 0 |  | AOSP/platform component; out of scope for v1 removal |
| KEEP | `com.android.internal.display.cutout.emulation.tall` | product/overlay/DisplayCutoutEmulationTall/DisplayCutoutEmulationTallOverlay.apk | 0 |  | AOSP/platform component; out of scope for v1 removal |
| KEEP | `com.android.internal.display.cutout.emulation.waterfall` | product/overlay/DisplayCutoutEmulationWaterfall/DisplayCutoutEmulationWaterfallOverlay.apk | 0 |  | AOSP/platform component; out of scope for v1 removal |
| KEEP | `com.android.internal.systemui.navbar.gestural` | product/overlay/NavigationBarModeGestural/NavigationBarModeGesturalOverlay.apk | 0 |  | AOSP/platform component; out of scope for v1 removal |
| KEEP | `com.android.internal.systemui.navbar.gestural_extra_wide_back` | product/overlay/NavigationBarModeGesturalExtraWideBack/NavigationBarModeGesturalOverlayExtraWideBack.apk | 0 |  | AOSP/platform component; out of scope for v1 removal |
| KEEP | `com.android.internal.systemui.navbar.gestural_narrow_back` | product/overlay/NavigationBarModeGesturalNarrowBack/NavigationBarModeGesturalOverlayNarrowBack.apk | 0 |  | AOSP/platform component; out of scope for v1 removal |
| KEEP | `com.android.internal.systemui.navbar.gestural_wide_back` | product/overlay/NavigationBarModeGesturalWideBack/NavigationBarModeGesturalOverlayWideBack.apk | 0 |  | AOSP/platform component; out of scope for v1 removal |
| KEEP | `com.android.internal.systemui.navbar.threebutton` | product/overlay/NavigationBarMode3Button/NavigationBarMode3ButtonOverlay.apk | 0 |  | AOSP/platform component; out of scope for v1 removal |
| KEEP | `com.android.keychain` | system/app/KeyChain/KeyChain.apk | 0 |  | AOSP/platform component; out of scope for v1 removal |
| KEEP | `com.android.localtransport` | system/priv-app/LocalTransport/LocalTransport.apk | 0 |  | AOSP/platform component; out of scope for v1 removal |
| KEEP | `com.android.location.fused` | system/priv-app/FusedLocation/FusedLocation.apk | 0 |  | AOSP/platform component; out of scope for v1 removal |
| KEEP | `com.android.mms.service` | system/priv-app/MmsService/MmsService.apk | 0 |  | AOSP/platform component; out of scope for v1 removal |
| KEEP | `com.android.modulemetadata` | product/app/ModuleMetadata/ModuleMetadata.apk | 0 |  | AOSP/platform component; out of scope for v1 removal |
| KEEP | `com.android.mtp` | system/priv-app/MtpService/MtpService.apk | 0 |  | AOSP/platform component; out of scope for v1 removal |
| KEEP | `com.android.musicfx` | system/priv-app/MusicFX/MusicFX.apk | 0 |  | AOSP/platform component; out of scope for v1 removal |
| KEEP | `com.android.networkstack` | system/priv-app/NetworkStack/NetworkStack.apk | 0 |  | AOSP/platform component; out of scope for v1 removal |
| KEEP | `com.android.networkstack.permissionconfig` | system/priv-app/NetworkPermissionConfig/NetworkPermissionConfig.apk | 1 |  | AOSP/platform component; out of scope for v1 removal |
| KEEP | `com.android.networkstack.tethering.inprocess.overlay` | vendor/app/InProcessTetheringResOverlay/InProcessTetheringResOverlay.apk | 0 |  | AOSP/platform component; out of scope for v1 removal |
| KEEP | `com.android.networkstack.tethering.overlay` | vendor/app/TetheringResOverlay/TetheringResOverlay.apk | 0 |  | AOSP/platform component; out of scope for v1 removal |
| KEEP | `com.android.onetimeinitializer` | product/priv-app/OneTimeInitializer/OneTimeInitializer.apk | 0 |  | AOSP/platform component; out of scope for v1 removal |
| KEEP | `com.android.packageinstaller` | system/priv-app/PackageInstaller/PackageInstaller.apk | 0 |  | AOSP/platform component; out of scope for v1 removal |
| KEEP | `com.android.pacprocessor` | system/app/PacProcessor/PacProcessor.apk | 0 |  | AOSP/platform component; out of scope for v1 removal |
| KEEP | `com.android.printservice.recommendation` | system/app/PrintRecommendationService/PrintRecommendationService.apk | 0 |  | AOSP/platform component; out of scope for v1 removal |
| KEEP | `com.android.protips` | system/app/Protips/Protips.apk | 0 |  | AOSP/platform component; out of scope for v1 removal |
| KEEP | `com.android.providers.blockednumber` | system/priv-app/BlockedNumberProvider/BlockedNumberProvider.apk | 0 |  | AOSP/platform component; out of scope for v1 removal |
| KEEP | `com.android.providers.contacts` | system/priv-app/ContactsProvider/ContactsProvider.apk | 0 |  | AOSP/platform component; out of scope for v1 removal |
| KEEP | `com.android.providers.downloads` | system_ext/priv-app/FireOSDownloadProvider/FireOSDownloadProvider.apk | 10 |  | AOSP/platform component; out of scope for v1 removal |
| KEEP | `com.android.providers.downloads.ui` | system/priv-app/DownloadProviderUi/DownloadProviderUi.apk | 0 |  | AOSP/platform component; out of scope for v1 removal |
| KEEP | `com.android.providers.media` | system/priv-app/MediaProviderLegacy/MediaProviderLegacy.apk | 0 |  | AOSP/platform component; out of scope for v1 removal |
| KEEP | `com.android.providers.partnerbookmarks` | system/app/PartnerBookmarksProvider/PartnerBookmarksProvider.apk | 0 |  | AOSP/platform component; out of scope for v1 removal |
| KEEP | `com.android.providers.settings` | system/priv-app/SettingsProvider/SettingsProvider.apk | 0 |  | AOSP/platform component; out of scope for v1 removal |
| KEEP | `com.android.providers.tv` | system/priv-app/TvProvider/TvProvider.apk | 11 |  | AOSP/platform component; out of scope for v1 removal |
| KEEP | `com.android.providers.userdictionary` | system/priv-app/UserDictionaryProvider/UserDictionaryProvider.apk | 0 |  | AOSP/platform component; out of scope for v1 removal |
| KEEP | `com.android.proxyhandler` | system/priv-app/ProxyHandler/ProxyHandler.apk | 0 |  | AOSP/platform component; out of scope for v1 removal |
| KEEP | `com.android.safetyregulatoryinfo` | system/app/SafetyRegulatoryInfo/SafetyRegulatoryInfo.apk | 0 |  | AOSP/platform component; out of scope for v1 removal |
| KEEP | `com.android.sharedstoragebackup` | system/priv-app/SharedStorageBackup/SharedStorageBackup.apk | 0 |  | AOSP/platform component; out of scope for v1 removal |
| KEEP | `com.android.shell` | system/priv-app/Shell/Shell.apk | 0 |  | AOSP/platform component; out of scope for v1 removal |
| KEEP | `com.android.smspush` | system_ext/app/WAPPushManager/WAPPushManager.apk | 0 |  | AOSP/platform component; out of scope for v1 removal |
| KEEP | `com.android.statementservice` | system/priv-app/StatementService/StatementService.apk | 0 |  | AOSP/platform component; out of scope for v1 removal |
| KEEP | `com.android.storagemanager` | system_ext/priv-app/StorageManager/StorageManager.apk | 0 |  | AOSP/platform component; out of scope for v1 removal |
| KEEP | `com.android.systemui` | system_ext/priv-app/FireTVSystemUI/FireTVSystemUI.apk | 0 |  | AOSP/platform component; out of scope for v1 removal |
| KEEP | `com.android.theme.color.black` | product/overlay/AccentColorBlack/AccentColorBlackOverlay.apk | 0 |  | AOSP/platform component; out of scope for v1 removal |
| KEEP | `com.android.theme.color.cinnamon` | product/overlay/AccentColorCinnamon/AccentColorCinnamonOverlay.apk | 0 |  | AOSP/platform component; out of scope for v1 removal |
| KEEP | `com.android.theme.color.green` | product/overlay/AccentColorGreen/AccentColorGreenOverlay.apk | 0 |  | AOSP/platform component; out of scope for v1 removal |
| KEEP | `com.android.theme.color.ocean` | product/overlay/AccentColorOcean/AccentColorOceanOverlay.apk | 0 |  | AOSP/platform component; out of scope for v1 removal |
| KEEP | `com.android.theme.color.orchid` | product/overlay/AccentColorOrchid/AccentColorOrchidOverlay.apk | 0 |  | AOSP/platform component; out of scope for v1 removal |
| KEEP | `com.android.theme.color.purple` | product/overlay/AccentColorPurple/AccentColorPurpleOverlay.apk | 0 |  | AOSP/platform component; out of scope for v1 removal |
| KEEP | `com.android.theme.color.space` | product/overlay/AccentColorSpace/AccentColorSpaceOverlay.apk | 0 |  | AOSP/platform component; out of scope for v1 removal |
| KEEP | `com.android.theme.font.notoserifsource` | product/overlay/FontNotoSerifSource/FontNotoSerifSourceOverlay.apk | 0 |  | AOSP/platform component; out of scope for v1 removal |
| KEEP | `com.android.theme.icon.pebble` | product/overlay/IconShapePebble/IconShapePebbleOverlay.apk | 0 |  | AOSP/platform component; out of scope for v1 removal |
| KEEP | `com.android.theme.icon.roundedrect` | product/overlay/IconShapeRoundedRect/IconShapeRoundedRectOverlay.apk | 0 |  | AOSP/platform component; out of scope for v1 removal |
| KEEP | `com.android.theme.icon.squircle` | product/overlay/IconShapeSquircle/IconShapeSquircleOverlay.apk | 0 |  | AOSP/platform component; out of scope for v1 removal |
| KEEP | `com.android.theme.icon.taperedrect` | product/overlay/IconShapeTaperedRect/IconShapeTaperedRectOverlay.apk | 0 |  | AOSP/platform component; out of scope for v1 removal |
| KEEP | `com.android.theme.icon.teardrop` | product/overlay/IconShapeTeardrop/IconShapeTeardropOverlay.apk | 0 |  | AOSP/platform component; out of scope for v1 removal |
| KEEP | `com.android.theme.icon.vessel` | product/overlay/IconShapeVessel/IconShapeVesselOverlay.apk | 0 |  | AOSP/platform component; out of scope for v1 removal |
| KEEP | `com.android.theme.icon_pack.circular.android` | product/overlay/IconPackCircularAndroid/IconPackCircularAndroidOverlay.apk | 0 |  | AOSP/platform component; out of scope for v1 removal |
| KEEP | `com.android.theme.icon_pack.circular.launcher` | product/overlay/IconPackCircularLauncher/IconPackCircularLauncherOverlay.apk | 0 |  | AOSP/platform component; out of scope for v1 removal |
| KEEP | `com.android.theme.icon_pack.circular.settings` | product/overlay/IconPackCircularSettings/IconPackCircularSettingsOverlay.apk | 0 |  | AOSP/platform component; out of scope for v1 removal |
| KEEP | `com.android.theme.icon_pack.circular.systemui` | product/overlay/IconPackCircularSystemUI/IconPackCircularSystemUIOverlay.apk | 0 |  | AOSP/platform component; out of scope for v1 removal |
| KEEP | `com.android.theme.icon_pack.circular.themepicker` | product/overlay/IconPackCircularThemePicker/IconPackCircularThemePickerOverlay.apk | 0 |  | AOSP/platform component; out of scope for v1 removal |
| KEEP | `com.android.theme.icon_pack.filled.android` | product/overlay/IconPackFilledAndroid/IconPackFilledAndroidOverlay.apk | 0 |  | AOSP/platform component; out of scope for v1 removal |
| KEEP | `com.android.theme.icon_pack.filled.launcher` | product/overlay/IconPackFilledLauncher/IconPackFilledLauncherOverlay.apk | 0 |  | AOSP/platform component; out of scope for v1 removal |
| KEEP | `com.android.theme.icon_pack.filled.settings` | product/overlay/IconPackFilledSettings/IconPackFilledSettingsOverlay.apk | 0 |  | AOSP/platform component; out of scope for v1 removal |
| KEEP | `com.android.theme.icon_pack.filled.systemui` | product/overlay/IconPackFilledSystemUI/IconPackFilledSystemUIOverlay.apk | 0 |  | AOSP/platform component; out of scope for v1 removal |
| KEEP | `com.android.theme.icon_pack.filled.themepicker` | product/overlay/IconPackFilledThemePicker/IconPackFilledThemePickerOverlay.apk | 0 |  | AOSP/platform component; out of scope for v1 removal |
| KEEP | `com.android.theme.icon_pack.rounded.android` | product/overlay/IconPackRoundedAndroid/IconPackRoundedAndroidOverlay.apk | 0 |  | AOSP/platform component; out of scope for v1 removal |
| KEEP | `com.android.theme.icon_pack.rounded.launcher` | product/overlay/IconPackRoundedLauncher/IconPackRoundedLauncherOverlay.apk | 0 |  | AOSP/platform component; out of scope for v1 removal |
| KEEP | `com.android.theme.icon_pack.rounded.settings` | product/overlay/IconPackRoundedSettings/IconPackRoundedSettingsOverlay.apk | 0 |  | AOSP/platform component; out of scope for v1 removal |
| KEEP | `com.android.theme.icon_pack.rounded.systemui` | product/overlay/IconPackRoundedSystemUI/IconPackRoundedSystemUIOverlay.apk | 0 |  | AOSP/platform component; out of scope for v1 removal |
| KEEP | `com.android.theme.icon_pack.rounded.themepicker` | product/overlay/IconPackRoundedThemePicker/IconPackRoundedThemePickerOverlay.apk | 0 |  | AOSP/platform component; out of scope for v1 removal |
| KEEP | `com.android.traceur` | system/app/Traceurlite/Traceurlite.apk | 0 |  | AOSP/platform component; out of scope for v1 removal |
| KEEP | `com.android.vpndialogs` | system/priv-app/VpnDialogs/VpnDialogs.apk | 0 |  | AOSP/platform component; out of scope for v1 removal |
| KEEP | `com.android.wallpaperbackup` | system/app/WallpaperBackup/WallpaperBackup.apk | 0 |  | AOSP/platform component; out of scope for v1 removal |
| KEEP | `com.android.wallpaperpicker` | product/app/WallpaperPicker/WallpaperPicker.apk | 0 |  | AOSP/platform component; out of scope for v1 removal |
| KEEP | `com.google.android.networkstack.tethering.overlay` | vendor/app/GoogleTetheringResOverlay/GoogleTetheringResOverlay.apk | 0 |  | AOSP/platform component; out of scope for v1 removal |
| KEEP | `com.ivona.orchestrator` | system_ext/priv-app/IvonaTtsOrchestrator/IvonaTtsOrchestrator.apk | 0 |  | TTS orchestrator |
| KEEP | `com.ivona.tts.oem` | system_ext/priv-app/IvonaTTS/IvonaTTS.apk | 0 |  | TTS (VoiceView, Alexa) |
| KEEP | `com.mediatek.tvinput` | system/priv-app/MtkArcInputService/MtkArcInputService.apk | 0 |  | MtkArcInputService (ARC) |
| KEEP | `com.svox.pico` | system_ext/app/PicoTts/PicoTts.apk | 0 |  | Fallback TTS |
