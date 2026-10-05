import { readFileSync, writeFileSync } from 'node:fs';
import { resolve } from 'node:path';

const plugin = resolve(
  'node_modules/@capacitor-community/bluetooth-le/ios/Sources/BluetoothLe/Plugin.swift'
);
const oldCode = `let companyIdentifier = dataObject["companyIdentifier"] as? UInt16 else {`;
const newCode = `let companyIdentifierValue = dataObject["companyIdentifier"] as? Int,
                  let companyIdentifier = UInt16(exactly: companyIdentifierValue) else {`;

const source = readFileSync(plugin, 'utf8');
if (source.includes(newCode)) {
  console.log('Bluetooth LE Swift 6 patch already applied.');
} else if (source.includes(oldCode)) {
  writeFileSync(plugin, source.replace(oldCode, newCode));
  console.log('Applied Bluetooth LE Swift 6 companyIdentifier patch.');
} else {
  throw new Error('Bluetooth LE plugin source changed; review the Swift 6 patch.');
}
