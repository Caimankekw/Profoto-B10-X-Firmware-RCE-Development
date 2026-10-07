# B10 REV1 development

[English](README.md) | [简体中文](README.zh-CN.md)

Custom firmware developer: [Caimankekw](https://github.com/Caimankekw) (REV1 / REV5). Original components retain their respective ownership notices.

This branch contains the independent D3-based REV1 development project. It adds `SETTINGS → ADVANCED → RECHARGE CTRL` with `NON-X / X` selection while preserving the 250 / 500 Ws model families. Firmware metadata is `D3-RC1`; the ABOUT screen retains the original `D3` display.

| Directory | Contents |
| --- | --- |
| [D3](D3/README.md) | Original firmware reverse engineering, inspection tools, and required build inputs |
| [REV1](REV1/README.md) | Patch source, implementation notes, and fixed release hashes |

This is a binary patch project, not the manufacturer's complete C source or an official update. This branch does not require other development versions.

## Build

Python 3.11 is recommended. From the repository root:

```powershell
python -m pip install -r requirements.txt
python build.py
```

Dependencies are pinned to `capstone==5.0.9`, `keystone-engine==0.9.2`, and `Pillow==11.3.0`. Output goes to `REV1/build/`: `RC1.bin`, `RC1.dfu`, `powerboard.bin`, and patch records. The main image already embeds the power-board image; do not flash the standalone power-board BIN as main firmware.

The build verifies fixed SHA-256 values, the embedded power-board bytes, and DFU CRC. It reproduces the frozen REV1 release byte for byte. Building does not access USB or flash a light.

## Windows package and other branches

The custom Windows package `Profoto-B10-REV1-Custom-Updater.exe` is available alongside REV5 in the [combined release](https://github.com/Caimankekw/Profoto-B10-X-Firmware-RCE-Development/releases/tag/rev1-rev5-20261007). It uses the original-style updater interface and does not require Python. It is not an official Profoto release or a claim of official signing. Follow its included README.

See [main](https://github.com/Caimankekw/Profoto-B10-X-Firmware-RCE-Development/tree/main) for D3-only reverse engineering, or [REV5](https://github.com/Caimankekw/Profoto-B10-X-Firmware-RCE-Development/tree/REV5) for BOOST / ECO development.

Keeping original protection code does not establish the electrical margin of applying the X policy to non-X hardware. Image verification does not replace electrical, thermal, exposure, or color-temperature measurements. The original firmware and resources remain the property of their respective rights holders.
