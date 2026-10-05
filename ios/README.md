# OmegaSim for iOS

This directory contains the iOS Capacitor shell for OmegaSim. It embeds the same generated
web application used by the browser and Android builds. The existing JavaScript bridge in
`src/05-app-bruecke.js` maps OmegaSim's Web Bluetooth calls to the native
`@capacitor-community/bluetooth-le` implementation.

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
