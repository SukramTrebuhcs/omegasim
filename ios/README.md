# OmegaSim for iOS

This directory contains the iOS Capacitor shell for OmegaSim. It embeds the same generated
web application used by the browser and Android builds. The existing JavaScript bridge in
`src/05-app-bruecke.js` maps OmegaSim's Web Bluetooth calls to the native
`@capacitor-community/bluetooth-le` implementation.

## Current status

The iOS foundation is working on a physical device. The following behavior has been
verified:

- The application builds and launches on iOS.
- A Carrera Hybrid car is discoverable and connectable.
- A connected controller sends driving commands through the application to the car.

This confirms the complete basic control path:

```text
Controller → OmegaSim web logic → Capacitor bridge → native iOS BLE → car
```

Ghost driving, long-running multi-car reliability, backup and restore, native multiplayer
hosting, and release packaging still require additional implementation or device testing.
The detailed checklist is maintained in `IOS_TODO.md`.

## What has been implemented

- A Capacitor 8 iOS application using the same OmegaSim interface and driving logic as the
  browser and Android versions.
- An Xcode project at `ios/App/App.xcodeproj` relative to this directory.
- Native BLE discovery, connection, service discovery, characteristic access,
  notifications, reads, and writes through `@capacitor-community/bluetooth-le`.
- The existing Web Bluetooth compatibility API from `src/05-app-bruecke.js`, allowing the
  shared application code to use the native iOS BLE implementation without a separate
  driving stack.
- Bluetooth and local-network permission descriptions in the iOS `Info.plist`.
- Local-network transport permission for the multiplayer client.
- Screen-awake behavior during use and a hidden native status bar.
- A dedicated `tools/ios_www.py` builder that copies the versioned OmegaSim web bundle into
  the iOS application.
- npm commands for generating assets, synchronizing Capacitor, and opening Xcode.
- A Swift compatibility fix for Bluetooth LE plugin 8.3.0. The plugin attempted to cast a
  Capacitor JavaScript value directly to `UInt16`; it now reads a range-checked `Int` first.
- A durable npm `postinstall` script that reapplies the Bluetooth fix after dependency
  installation.
- A successful unsigned iOS Simulator build using `xcodebuild`.

## Requirements

- macOS with Xcode 26 or newer
- Node.js and npm
- An Apple development team for installation on a physical device
- iOS 15 or newer (the Capacitor 8 deployment baseline)

Bluetooth must be tested on a physical iPhone or iPad; the Simulator cannot communicate
with the Carrera cars.

## Generate and open the project

```sh
cd ios
npm install
npm run sync
npm run open
```

Select an Apple development team for the `App` target, connect an iPhone, and run the app.

The Xcode project can also be opened directly:

```text
ios/ios/App/App.xcodeproj
```

## Keeping the embedded application current

After changing the web application, rebuild the root `index.html` and update manifest first,
then synchronize iOS:

```sh
python3 tools/build.py
cd ios
npm run sync
```

## Native behavior

- BLE discovery, connection, services, characteristics, notifications, reads, and writes are
  provided by `@capacitor-community/bluetooth-le`.
- The Android-only `OmegaBle` fast writer is intentionally absent. The JavaScript bridge
  detects this and uses the community BLE plugin.
- The screen is kept awake while the app is active.
- The native status bar is hidden; the existing responsive web UI controls orientation and layout.
- Bluetooth usage descriptions are stored in the Xcode project's `Info.plist`.

Android-specific self-update and embedded multiplayer-host plugins are not portable to iOS
as-is. The web application remains usable as a multiplayer client. Native iOS host and update
delivery require separate App Store-compliant implementations.
