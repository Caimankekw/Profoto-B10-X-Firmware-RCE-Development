# B10 REV5 development

[English](README.md) | [简体中文](README.zh-CN.md)

Custom firmware developer: [Caimankekw](https://github.com/Caimankekw) (REV1 / REV5). Original components retain their respective ownership notices.

This branch contains the independent D3-based REV5 development project. It provides `NON-X / X / BOOST` under RECHARGE CTRL, a home-screen selection indicator, and ECO with HSS adaptation. Firmware metadata and ABOUT display `RC5`. BOOST and ECO are available only on 500 Ws Plus models.

| Directory | Contents |
| --- | --- |
| [D3](D3/README.md) | Original firmware reverse engineering, inspection tools, and required build inputs |
| [REV5](REV5/README.md) | Patch source, implementation notes, and fixed release hashes |

This is a binary patch project, not the manufacturer's complete C source or an official update. It builds directly from D3 without intermediate development versions.

## Build

Python 3.11 is recommended. From the repository root:

```powershell
python -m pip install -r requirements.txt
python build.py
```

Dependencies are pinned to `capstone==5.0.9`, `keystone-engine==0.9.2`, and `Pillow==11.3.0`. Output goes to `REV5/build/`: `RC5.bin`, `RC5.dfu`, `powerboard.bin`, and patch records. The main image already embeds the power-board image; do not flash the standalone power-board BIN as main firmware.

The build verifies fixed SHA-256 values, the embedded power-board bytes, and DFU CRC. It reproduces the frozen named RC5 release byte for byte. Building does not access USB or flash a light.

## Windows package and other branches

The custom Windows package `Profoto-B10-REV5-Custom-Updater.exe` is available alongside REV1 in the [combined release](https://github.com/Caimankekw/Profoto-B10-X-Firmware-RCE-Development/releases/tag/rev1-rev5-20261007). It uses the original-style updater interface and does not require Python. It is not an official Profoto release or a claim of official signing. Follow its included README.

See [main](https://github.com/Caimankekw/Profoto-B10-X-Firmware-RCE-Development/tree/main) for D3-only reverse engineering, or [REV1](https://github.com/Caimankekw/Profoto-B10-X-Firmware-RCE-Development/tree/REV1) for NON-X / X development.

A 20% reduction in recycle time is a design target, not a measured guarantee. The selected home-screen value does not confirm that enhanced charging is active at that instant. Image verification does not replace electrical, thermal, exposure, HSS-uniformity, or color-temperature measurements. The original firmware and resources remain the property of their respective rights holders.

## License / 许可

Original code and documentation are licensed under [AGPL-3.0-only](LICENSE), by **Caimankekw**. Original firmware, recovered original machine code, and third-party components retain their respective rights and are not relicensed by this project; see [NOTICE](NOTICE.md) for the scope. Custom Windows updater and installer build source is available in `windows/` on the corresponding development branch.
