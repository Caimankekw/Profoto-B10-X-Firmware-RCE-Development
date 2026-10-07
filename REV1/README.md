# REV1 development code

[English](README.md) | [简体中文](README.zh-CN.md)

Firmware metadata: `D3-RC1`. ABOUT retains the original `D3` display. REV1 adds `SETTINGS → ADVANCED → RECHARGE CTRL` with `NON-X / X` selection to D3.

## Implementation

- Preserves the actual model and 250 / 500 Ws family; changes only the recharge-policy selection.
- Without a valid saved record, non-X models default to NON-X and X models default to X.
- The X policy remains subject to the original modeling-light / DIM conditions; selecting X does not guarantee enhanced coefficients in every situation.
- Command `0x1032` sends the selection, which takes effect in the original parameter-loading path.
- An independent EEPROM record at `0x3E0` includes magic, version, complement, and CRC, with readback after writing.
- Preserves the NORMAL / FREEZE discharge tables and original target voltage.

| Source | Responsibility |
| --- | --- |
| [build_recharge.py](source/build_recharge.py) | Input validation, patch integration, power-board embedding, and DFU packaging |
| [config_codegen.py](source/config_codegen.py) | Main-controller settings, persistence, protocol, and menu helpers |
| [pb_patch.py](source/pb_patch.py) | Power-board command parsing and recharge selection |
| [ui_assets.py](source/ui_assets.py) | Menu assets derived from D3 bitmaps |

## Build and identity

Use Python 3.11 and run from the repository root:

```powershell
python -m pip install -r requirements.txt
python build.py
```

The root requirements pin `capstone==5.0.9`, `keystone-engine==0.9.2`, and `Pillow==11.3.0`. Outputs are `REV1/build/RC1.bin`, `RC1.dfu`, `powerboard.bin`, and patch records. The main image embeds the power-board image; the separate power-board BIN is for development verification and must not be flashed as main firmware. The build does not access USB.

The main image is 682,596 bytes. The build must reproduce the frozen release with these SHA-256 values:

```text
BIN  7661a83958caf5cd62a477575a8ffe8a6be9d0153ef076b5d7bf2e5850df3a0e
DFU  c8088fafa8d224d203c023442f0157050800169ded67282e62088bc833b1bcbe
PB   ce94c00388cdf755d4c343d8eeab5e517096ae8a81974efa09f67d175d6eb000
```

The root build also checks DFU CRC and the embedded power-board bytes. Keeping original protection code does not prove the electrical margin of using the X policy on non-X hardware. Output, color temperature, and electrical behavior still require measurement.

## Windows update package

Download `Profoto-B10-REV1-Custom-Updater.exe` from the [combined REV1 + REV5 release](https://github.com/Caimankekw/Profoto-B10-X-Firmware-RCE-Development/releases/tag/rev1-rev5-20261007). It wraps the original-style Windows updater for this custom firmware and does not require Python. This is not an official Profoto release or a claim of official signing. Follow the included package instructions.
