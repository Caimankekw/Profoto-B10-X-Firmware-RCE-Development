# REV5 Windows firmware updater

[简体中文](README.zh-CN.md) | English

Developer: [Caimankekw](https://github.com/Caimankekw)

**Custom experimental firmware, not an official Profoto release.** This package reuses the manufacturer's D3 Qt updater interface and bundled runtime. The custom installer and updater are not Authenticode signed; no manufacturer signature or endorsement is claimed.

RECHARGE CTRL offers NON-X / X / BOOST. Plus models also receive ECO (470 V, including HSS), with the recharge profile shown on the home screen. BOOST/ECO remain restricted to 500 Ws Plus models. A 20% recharge-time reduction is a development target, not a guaranteed measurement.

This is the named RC5 payload, published here as REV5. The updater and lamp ABOUT screen identify RC5. When migrating older settings, an old BOOST selection becomes X; select BOOST explicitly after updating if wanted.

## License and source

Caimankekw's original custom development and packaging code is licensed under **AGPL-3.0-only**. Read the complete [LICENSE](LICENSE) and the bilingual [NOTICE.md](NOTICE.md) for scope. The vendor firmware, manufacturer updater/runtime and third-party components retain their original terms; this package does not relicense those components under AGPL.

Source: [REV5 branch](https://github.com/Caimankekw/Profoto-B10-X-Firmware-RCE-Development/tree/REV5) · [Windows updater patch and packaging source](https://github.com/Caimankekw/Profoto-B10-X-Firmware-RCE-Development/tree/REV5/windows).

## Update

1. Run `Profoto-B10-REV5-Custom-Updater.exe`. It extracts to a per-user folder under `%LOCALAPPDATA%\Profoto-B10-Custom\REV5`; administrative rights are not requested. The finish page can open the updater. It does not install drivers or start flashing automatically.
2. Turn the lamp off, remove its battery, and connect one target lamp by USB. Follow the original updater's instructions. Check the detected device and target firmware version before clicking update yourself.
3. Keep USB connected until the updater completes writing and full image readback comparison.
4. Disconnect USB, reinstall the battery, then power on. Maintain power until any first-boot internal power-board update finishes.

To open the updater again, run `REV5.cmd` in the extracted folder. Keep the complete `app` folder. Python is not needed. If using the portable ZIP, extract it completely before running the command file.

The manufacturer's PC family check accepts the shared B10/B10X family (0x8C); it does not independently distinguish Plus from non-Plus. Firmware-side model checks remain unchanged. Use this package only for its supported B10-family hardware; it is not for unrelated products.

## Drivers and behavior

Keep a working existing driver. If a new computer cannot detect the device, consult the included original troubleshooting PDF. Original driver files are preserved in `app/driver_package`. Manual installation, if necessary, requires an administrator command prompt with **app as the working directory**: `driver_package\install_driver.cmd`. The installer never invokes this script.

The GUI retains the manufacturer's enumeration, family/version checks, write/readback and leave/reconnect flow. It does not include the separate Python tool's pre-write full backup, known-image whitelist or failure-transaction recovery. Identical installed firmware follows the original no-update behavior. No private device backup, OTP dump or device serial number is distributed.

## Verification and limits

The package was checked offline: firmware hashes and DfuSe CRC/address/length, PE resource pointers and change whitelist, all 30 runtime files (29 byte-identical), eight corruption tests per GUI, ZIP roundtrip and installer extraction. The updater and installer were not launched, no driver installed, and no USB or lamp accessed during packaging. This does not establish live Windows/Qt operation or an actual flashing result. Optical output, color temperature, thermal margins and HSS uniformity are not newly validated by packaging.

Firmware BIN SHA-256: `ad8b5ff203bd1d7426f66666124432f154c00bc46c31878d660ff0e0ea506ea8`  
Firmware DFU SHA-256: `c6c2343921b302c2ce45e9bf06ffa5e66d591700f59dd0218388327c24d57f4f`

`package_manifest.json` and `SHA256SUMS.txt` identify the exact extracted files. Original dependency notices and troubleshooting PDF are retained; they do not certify this custom firmware. The outer extractor uses unmodified NSIS 3.13 components; its notices are in `NSIS-COPYING.txt`, and source is available from [the NSIS project](https://sourceforge.net/projects/nsis/files/NSIS%203/3.13/).
