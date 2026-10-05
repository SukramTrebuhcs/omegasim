# OmegaSim iOS Status and Remaining Work

## Current status

The iOS project is a Capacitor application that embeds the same OmegaSim web interface and
game logic as the browser and Android versions.

The Xcode project is located at:

```text
ios/ios/App/App.xcodeproj
```

The application currently builds successfully for the iOS Simulator.

## Completed

- Created the Capacitor iOS project.
- Included the existing OmegaSim web application and assets.
- Added an iOS web-bundle generation script: `tools/ios_www.py`.
- Added the Capacitor Community Bluetooth LE plugin.
- Connected the existing Web Bluetooth compatibility layer to the native plugin.
- Added Bluetooth permission descriptions to `Info.plist`.
- Added local-network permission and local-network transport configuration.
- Disabled the idle timer so the display does not sleep during a race.
- Hid the native iOS status bar.
- Added npm scripts for asset generation, synchronization, and opening Xcode.
- Fixed the Bluetooth plugin's Swift compilation error involving `UInt16`.
- Added a durable npm `postinstall` patch for that plugin issue.
- Verified a complete unsigned iOS Simulator build with `xcodebuild`.

## Required before physical-device testing

- Open `ios/ios/App/App.xcodeproj` in Xcode.
- Select the `App` target.
- Select an Apple Development Team under **Signing & Capabilities**.
- Confirm or change the bundle identifier `de.lroeseler.omegasim` if necessary.
- Connect a physical iPhone or iPad.
- Build and install the application on that device.
- Accept the Bluetooth and local-network permission prompts.

Bluetooth car communication cannot be meaningfully tested in the iOS Simulator.

## BLE verification still required

- Discover Carrera Hybrid cars.
- Cancel and restart device discovery.
- Connect to one car.
- Discover its services and characteristics.
- Subscribe to telemetry notifications.
- Verify tile code, tile counter, battery, and movement bytes.
- Send steering, throttle, brake, light, and mode packets.
- Verify sustained control at the intended approximately 45 ms interval.
- Connect and drive multiple cars simultaneously.
- Verify ghosts receive independent control packets.
- Verify disconnection and reconnection.
- Verify connections are released when the app closes or enters an unsuitable state.
- Measure control latency and dropped writes on a physical device.

## Android feature parity still required

### Low-latency BLE writer

Android provides a custom `OmegaBle` plugin with a fire-and-forget, newest-command-wins
control path. The iOS version currently uses the standard community BLE plugin.

An iOS equivalent should be implemented if physical-device measurements show excessive
control latency or dropped commands. It should:

- Use CoreBluetooth directly or safely share the plugin's peripheral connection.
- Avoid accumulating stale control commands.
- Retain only the newest pending command per car.
- Support pausing while reads, subscriptions, or writes with response are active.
- Report written, replaced, retried, and discarded command counts.
- Preserve the existing `OmegaBle` JavaScript API where practical.

### Native backup and restore

Implement an iOS equivalent of Android's `OmegaSicherung` plugin:

- Export `OmegaSim-Sicherung.json` through the iOS document picker/share sheet.
- Import a selected JSON backup through the document picker.
- Return the same `{ text, name }` contract used by the web application.
- Handle cancellation and invalid or inaccessible files clearly.
- Test backups containing large embedded car images.

### Multiplayer hosting and discovery

Implement an iOS equivalent of Android's `OmegaHost` functionality if the iPhone must act
as the multiplayer host:

- Run the OmegaSim HTTP/WebSocket host while the app is active.
- Advertise it through Bonjour as `_omegasim._tcp`.
- Discover and resolve other OmegaSim hosts.
- Return host information using the existing JavaScript contract.
- Handle Wi-Fi changes, backgrounding, host shutdown, and port conflicts.
- Confirm that Apple's background-execution limits are acceptable for race hosting.

The current iOS application can use the web application's multiplayer client, but native
on-device hosting has not yet been ported.

### Application updates

Android's self-update plugin cannot be copied directly because iOS does not allow an app to
replace its installed executable or downloaded native code.

Choose and implement an Apple-compatible distribution strategy:

- TestFlight for testing and private beta distribution, or
- App Store releases for production distribution.

If remotely updating only web content is considered, it must be reviewed against current
App Store rules before implementation. The bundled web application should remain the safe
fallback.

## UI and platform verification

- Verify portrait and landscape layouts on representative iPhone sizes.
- Verify safe-area handling around the Dynamic Island and Home indicator.
- Decide whether rotation should remain enabled or the application should be orientation-locked.
- Replace the generated Capacitor icons and launch screen with final OmegaSim artwork.
- Verify all audio files play correctly and that audio resumes after interruption.
- Verify controller support and controller button mappings on iOS.
- Verify file downloads, generated SVG sheets, and sharing behavior.
- Verify keyboard behavior on iPad if iPad support is retained.
- Check accessibility labels, text scaling, contrast, and reduced-motion behavior.

## Lifecycle and reliability verification

- Test incoming calls, notifications, Control Center, and app switching during driving.
- Stop sending drive commands immediately when control is no longer safe.
- Decide whether BLE connections should remain active while briefly backgrounded.
- Restore the UI and telemetry correctly when returning to the foreground.
- Prevent stale connections from making a car unavailable after relaunch.
- Verify local storage survives ordinary application updates.
- Verify behavior after force-quit, device restart, and Bluetooth being toggled off and on.

## Release preparation

- Choose the minimum supported iOS version.
- Configure final signing, certificates, provisioning, and bundle identifier.
- Set marketing version and build number.
- Add App Store privacy descriptions and privacy-manifest entries as required.
- Prepare App Store screenshots, description, support URL, and privacy policy.
- Run a release configuration build and archive.
- Test through TestFlight on at least one physical device before production release.

## Definition of done

The iOS port can be considered complete when:

- The application builds and installs from a clean checkout.
- Core driving and ghost behavior matches Android on physical cars.
- Multi-car BLE control remains responsive and reliable for a full race.
- Required Android-native features have iOS equivalents or documented platform-appropriate
  replacements.
- Backup and restore work with real user data.
- Multiplayer behavior matches the chosen iOS scope.
- Lifecycle interruptions fail safely.
- A signed release archive passes validation and completes TestFlight testing.
