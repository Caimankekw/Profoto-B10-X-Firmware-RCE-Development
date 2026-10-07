# REV5 development code

[English](README.md) | [简体中文](README.zh-CN.md)

Custom firmware developer: [Caimankekw](https://github.com/Caimankekw) (REV1 / REV5). Original components retain their respective ownership notices.

Firmware identifier: `RC5`, built directly from D3. Firmware metadata and ABOUT display `RC5`.

## Implementation

- RECHARGE CTRL: NON-X / X / BOOST, with the selected value on the home screen.
- FLASH MODE: NORMAL / FREEZE / ECO, with a home-screen mode indicator.
- ECO uses a 470 V target for ordinary flash and HSS, preserving associated feedback and boundary controls.
- BOOST and ECO are enabled only for 500 Ws Plus models.
- BOOST uses K375 / T445 / C20. Enhancement is limited to the eligible main charging segment; soft start, the final charging segment, and protection conditions remain in place.
- Settings record version is 4, retaining migration of older records and the fallback from an older saved BOOST choice to X.

The home screen shows the selected policy, not confirmation that a particular recharge cycle is currently in the enhanced segment. A 20% reduction in recycle time is a design target, not a measured guarantee.

| Source | Responsibility |
| --- | --- |
| [build_recharge.py](source/build_recharge.py) | Integrate patches from D3 and generate the named RC5 release |
| [config_codegen.py](source/config_codegen.py) | Recharge / ECO settings, model restrictions, migration, protocol, and UI |
| [pb_patch.py](source/pb_patch.py) | Recharge state machine, BOOST conditions, and target voltage |
| [eco_guard.py](source/eco_guard.py) | ECO HSS-reference and calibration guard hooks |
| [ui_assets.py](source/ui_assets.py) | Menu and home-screen bitmaps |

## Build and identity

Use Python 3.11 and run from the repository root:

```powershell
python -m pip install -r requirements.txt
python build.py
```

The root requirements pin `capstone==5.0.9`, `keystone-engine==0.9.2`, and `Pillow==11.3.0`. Outputs are `REV5/build/RC5.bin`, `RC5.dfu`, `powerboard.bin`, and patch records. The build first verifies the control image before the naming changes, then changes only two version fields and ABOUT to RC5 and recalculates the DFU CRC. It does not access USB.

The main image is 691,644 bytes. The power-board image is 55,996 bytes, with identifier `b0e69569`. The build must reproduce the frozen named release byte for byte:

```text
BIN  ad8b5ff203bd1d7426f66666124432f154c00bc46c31878d660ff0e0ea506ea8
DFU  c6c2343921b302c2ce45e9bf06ffa5e66d591700f59dd0218388327c24d57f4f
PB   be56734b508ef577fa5c4c257499e3a65ef06003aa4d7c8d526cccaf09a85fac
```

The root build also checks DFU CRC and the embedded power-board bytes. The separate power-board BIN is for verification only and must not be flashed as main firmware. Light output, color temperature, HSS uniformity, and electrical stability still require measurement.

## Windows update package

Download `Profoto-B10-REV5-Custom-Updater.exe` from the [combined REV1 + REV5 release](https://github.com/Caimankekw/Profoto-B10-X-Firmware-RCE-Development/releases/tag/rev1-rev5-20261007). It wraps the original-style Windows updater for this custom firmware and does not require Python. This is not an official Profoto release or a claim of official signing. Follow the included package instructions.
