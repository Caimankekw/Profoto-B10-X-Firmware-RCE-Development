# Profoto B10 firmware reverse engineering

[English](README.md) | [简体中文](README.zh-CN.md)

Custom firmware developer: [Caimankekw](https://github.com/Caimankekw) (REV1 / REV5). Original components retain their respective ownership notices.

The `main` branch contains reverse-engineered code for the original B10 REV-D3 firmware, its analysis, and inspection tools. Start with the [D3 analysis](D3/README.md) and [recovered assembly excerpts](D3/source/).

The recovered names, annotations, and pseudocode are research results, not the manufacturer's original C source. This is a partial reconstruction, not a complete decompilation or a buildable copy of the original firmware.

## Branches

| Branch | Contents |
| --- | --- |
| `main` | D3 reverse engineering and inspection tools; no firmware binaries or development patches |
| [REV1](https://github.com/Caimankekw/Profoto-B10-X-Firmware-RCE-Development/tree/REV1) | Independent D3-based development code for NON-X / X recharge selection; firmware metadata `D3-RC1` |
| [REV5](https://github.com/Caimankekw/Profoto-B10-X-Firmware-RCE-Development/tree/REV5) | Independent D3-based development code for NON-X / X / BOOST, ECO, and HSS adaptation; firmware identifier `RC5` |

Each development branch includes its own build entry point and the required original D3 inputs. No intermediate development version is required. See [D3 input instructions](D3/README.md#firmware-inputs-and-branches) to run inspection tools on `main`.

## Windows updates

Both custom Windows update packages are provided together in the [REV1 + REV5 release](https://github.com/Caimankekw/Profoto-B10-X-Firmware-RCE-Development/releases/tag/rev1-rev5-20261007): `Profoto-B10-REV1-Custom-Updater.exe` and `Profoto-B10-REV5-Custom-Updater.exe`. They use the original-style Windows updater interface. They are custom firmware packages, not official Profoto releases or a claim of official signing. Follow the README included with the selected package.

Code and image verification do not establish electrical margin, measured recycle time, exposure consistency, or color-temperature accuracy. The original firmware and resources remain the property of their respective rights holders.

## License / 许可

Original code and documentation are licensed under [AGPL-3.0-only](LICENSE), by **Caimankekw**. Original firmware, recovered original machine code, and third-party components retain their respective rights and are not relicensed by this project; see [NOTICE](NOTICE.md) for the scope. Custom Windows updater and installer build source is available in `windows/` on the corresponding development branch.
