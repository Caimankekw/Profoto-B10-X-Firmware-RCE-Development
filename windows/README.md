# REV1 Windows package source

[English](README.md) | [简体中文](README.zh-CN.md)

Copyright 2026 Caimankekw. SPDX-License-Identifier: AGPL-3.0-only. See [LICENSE](../LICENSE) and [scope notice](../NOTICE.md). This license covers the original custom scripts and patches; the manufacturer's executable, firmware, Qt runtime, drivers, and other third-party components retain their own terms.

These sources reproduce this branch's frozen GUI resource patch and build its Windows portable ZIP and NSIS extractor. They contain no vendor binaries and do not download inputs. Run the repository firmware build first; this wrapper uses `REV1/build/RC1.bin` and `.dfu`. The GUI title is `RC1 CUSTOM`, firmware metadata is `D3-RC1`, and ABOUT is `D3`.

## Inputs

- Python 3.9+; install the repository build dependencies and `python -m pip install -r windows/requirements.txt` (`pefile==2024.8.26`).
- Your original D3 Windows updater, fully extracted: supply the **Profoto_DFU-app** directory with all 30 original runtime files, including its original EXE, DLLs, plugins, and driver files. Do not supply the custom updater directory.
- The official `license_3rd_party.txt` and `Profoto-FW-Trouble-Shooting-FAQ.pdf`, in one supplied folder.
- Full [NSIS 3.13](https://sourceforge.net/projects/nsis/files/NSIS%203/3.13/) directory, and [7-Zip 26.04 x64](https://github.com/ip7z/7zip/releases/tag/26.04) extracted files with `7z.exe` beside `7z.dll`.

[input_manifest.json](input_manifest.json) pins the complete original runtime, both documents, and the build/archive tools. A different or incomplete input is refused. The original EXE must be 2,874,880 bytes, SHA-256 `4fe18a566843afde2bb1b3b4e8600495d9d010afeab1e1902519022fa3356fa5`.

## Build

From the repository root in PowerShell, replace the example input paths:

```powershell
python build.py
python -m pip install -r windows/requirements.txt
python windows/build_package.py `
  --runtime "C:\inputs\D3\Profoto_DFU-app" `
  --vendor-docs "C:\inputs\D3" `
  --nsis-dir "C:\tools\nsis-3.13" `
  --seven-zip "C:\tools\7zip\7z.exe"
```

The default output is a new `windows/build/<UTC timestamp>/` folder. Optional `--output` must name a new directory; existing files are never deleted or overwritten. Optional `--bin` and `--dfu` select firmware files, but the frozen hashes still apply. There are no references to the original developer's workspace or another development branch.

The build creates the complete updater directory, portable ZIP, NSIS EXE, logs, SHA256SUMS, and `package_verification.json`. It changes only the audited resource registration pointers/PE fields and appends the new resource section; all other original updater code is preserved. It verifies both firmware hashes and DfuSe CRC/address/length, the PE/QRC whitelist, eight corruption cases, all 30 runtime files (29 unchanged), DLL import closure, ZIP roundtrip, and the installer payload through 7-Zip extraction. It invokes only the supplied NSIS compiler and archive tool—not the installer, updater, driver script, or USB.

You can also run `build_gui.py --original-exe ... --bin ... --dfu ... --output ...` or `verify_gui.py --original-exe ... --bin ... --dfu ... --gui ...` for the GUI alone.

## Frozen payloads

| Artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| RC1.bin | 682596 | `7661a83958caf5cd62a477575a8ffe8a6be9d0153ef076b5d7bf2e5850df3a0e` |
| RC1.dfu | 682905 | `c8088fafa8d224d203c023442f0157050800169ded67282e62088bc833b1bcbe` |
| Profoto_DFU-app.exe | 4445184 | `2db2a88b37ffb678955458b4427fd7cda898b1228522d80d95f036af2ec68b81` |

Firmware and GUI reproduction must be byte-exact. The outer installer/ZIP may have different metadata or timestamps from the published assets; this build validates the extracted payload and does not claim the outer EXE hash is reproducible. Offline success does not establish GUI startup, device flashing, electrical margin, or optical behavior. The installer extracts per-user, shows the original-code AGPL scope, and offers to open the updater; it does not automatically install drivers or flash.

Package documentation is kept in [templates](templates/) and the NSIS source is [installer.nsi](installer.nsi). The package receives the repository root LICENSE; vendor and NSIS notices come from the supplied inputs.
