#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# Copyright 2026 Caimankekw
"""Build one Windows package offline; never execute an updater or installer."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import zipfile

import build_gui as gui
import verify_gui as verify

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
RELEASE = gui.RELEASE
SOURCE_URL = "https://github.com/Caimankekw/Profoto-B10-X-Firmware-RCE-Development/tree/" + RELEASE
LICENSE_SHA256 = "d8a6cc31abc16b6748c7a21f21611f5a1ec33f67d22ca23d7da1c19b95496bee"
SYSTEM_IMPORTS = {
    'advapi32.dll', 'gdi32.dll', 'imm32.dll', 'kernel32.dll', 'mpr.dll', 'oleaut32.dll',
    'rpcrt4.dll', 'setupapi.dll', 'shell32.dll', 'shlwapi.dll', 'user32.dll', 'winmm.dll',
    'ws2_32.dll', 'd3d9.dll', 'imagehlp.dll', 'msvcrt.dll', 'ntdll.dll', 'ole32.dll',
}
NSIS_COMPONENTS = {
    '$PLUGINSDIR/LangDLL.dll': 'Plugins/x86-unicode/LangDLL.dll',
    '$PLUGINSDIR/System.dll': 'Plugins/x86-unicode/System.dll',
    '$PLUGINSDIR/nsDialogs.dll': 'Plugins/x86-unicode/nsDialogs.dll',
    '$PLUGINSDIR/modern-wizard.bmp': 'Contrib/Graphics/Wizard/win.bmp',
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def encoded(value):
    return (json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode('utf-8')


def entry(data):
    return {'size': len(data), 'sha256': hashlib.sha256(data).hexdigest()}


def regular_files(directory):
    require(directory.is_dir() and not directory.is_symlink(), 'Input directory missing or is a symbolic link')
    result = {}
    for path in sorted(directory.rglob('*')):
        require(not path.is_symlink(), 'Symbolic links are not accepted')
        if path.is_file():
            result[path.relative_to(directory).as_posix()] = path.read_bytes()
    return result


def preflight(args):
    required = json.loads((HERE / 'input_manifest.json').read_text(encoding='utf-8'))
    runtime = regular_files(args.runtime)
    require({name: entry(data) for name, data in runtime.items()} == required['runtime'],
            'Official D3 runtime differs: expected all 30 exact files from input_manifest.json')
    documents = {}
    for name, expected in required['vendor_documents'].items():
        data = (args.vendor_docs / name).read_bytes()
        require(entry(data) == expected, 'Official document fingerprint differs: ' + name)
        documents[name] = data
    for name, expected in required['tools'].items():
        group, relative = name.split('/', 1)
        if group == 'nsis-3.13':
            path = args.nsis_dir / relative
        else:
            path = args.seven_zip if relative == '7z.exe' else args.seven_zip.parent / relative
        require(entry(path.read_bytes()) == expected, 'Build tool fingerprint differs: ' + name)
    license_text = (ROOT / 'LICENSE').read_bytes()
    require(gui.sha(license_text) == LICENSE_SHA256, 'Repository AGPL-3.0-only LICENSE fingerprint differs')
    return runtime, documents, license_text


def execute(argv, cwd, logfile, timeout):
    result = subprocess.run([str(a) for a in argv], cwd=cwd, shell=False,
                            capture_output=True, encoding='utf-8', errors='replace', timeout=timeout)
    logfile.write_text(result.stdout + result.stderr, encoding='utf-8')
    require(result.returncode == 0, 'Build/archive command failed; see ' + logfile.name)


def build_package(args):
    runtime, documents, license_text = preflight(args)
    original = runtime['Profoto_DFU-app.exe']
    binary, dfu = args.binary.read_bytes(), args.dfu.read_bytes()
    output_gui, details = gui.build_image(original, binary, dfu)
    checked = verify.verify_image(original, binary, dfu, output_gui)
    negatives = verify.negative_controls(original, binary, dfu, output_gui)
    require(len(negatives) == 8, 'Eight negative controls required')
    require(gui.build_image(original, binary, dfu)[0] == output_gui, 'GUI rebuild is not deterministic')
    require(len(output_gui) == gui.GUI_SIZE and gui.sha(output_gui) == gui.GUI_SHA, 'Frozen GUI hash/size')
    dependencies = gui.local_dependencies(args.runtime)
    require({name.lower() for dep in dependencies for name in dep['external_imports']} == SYSTEM_IMPORTS,
            'Unexpected external Windows runtime import')
    for dep in dependencies:
        require(all(local in runtime for local in dep['local_imports']), 'Missing local runtime dependency')

    # A fresh destination prevents mixing stale files or overwriting an old build.
    out = args.output.resolve()
    for external in (args.runtime, args.vendor_docs, args.nsis_dir, args.seven_zip.parent):
        require(out != external and external not in out.parents, 'Output must be outside supplied input directories')
    out.mkdir(parents=True, exist_ok=False)
    logs = out / 'logs'
    logs.mkdir()
    files = {'app/' + name: output_gui if name == 'Profoto_DFU-app.exe' else data
             for name, data in runtime.items()}
    runtime_record = {'app/' + name: {'original_sha256': gui.sha(data),
                                     'changed': name == 'Profoto_DFU-app.exe'}
                      for name, data in runtime.items()}
    for name in ('README.md', 'README.zh-CN.md', 'NOTICE.md'):
        files[name] = (HERE / 'templates' / name).read_bytes()
    files['LICENSE'] = license_text
    files.update(documents)
    files['NSIS-COPYING.txt'] = (args.nsis_dir / 'COPYING').read_bytes()
    files[RELEASE + '.cmd'] = (
        '@echo off\r\nsetlocal\r\npushd "%~dp0app"\r\nif errorlevel 1 exit /b 1\r\n'
        'start "" "Profoto_DFU-app.exe"\r\npopd\r\nendlocal\r\n').encode('ascii')
    manifest = {
        'release': RELEASE, 'developer': 'Caimankekw', 'developer_url': 'https://github.com/Caimankekw',
        'firmware_revision': gui.REVISION, 'firmware_about': gui.ABOUT,
        'custom_experimental_not_official': True,
        'license': 'AGPL-3.0-only', 'license_scope': 'Original custom code by Caimankekw only; vendor and third-party components retain their terms',
        'source_url': SOURCE_URL, 'windows_source_url': SOURCE_URL + '/windows',
        'main_bin_sha256': gui.sha(binary), 'main_dfu_sha256': gui.sha(dfu),
        'gui_sha256': gui.sha(output_gui), 'runtime': runtime_record, 'dependencies': dependencies,
        'files': {name: entry(data) for name, data in sorted(files.items())},
    }
    files['package_manifest.json'] = encoded(manifest)
    files['SHA256SUMS.txt'] = ''.join(gui.sha(data) + '  ' + name + '\n'
                                    for name, data in sorted(files.items())).encode('utf-8')
    destination = out / RELEASE
    for name, data in files.items():
        path = destination / name
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open('xb') as stream:
            stream.write(data)
    archive = out / ('Profoto-B10-' + RELEASE + '-Windows-portable.zip')
    with zipfile.ZipFile(archive, 'x', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zipped:
        for name, data in sorted(files.items()):
            info = zipfile.ZipInfo(RELEASE + '/' + name, (2026, 10, 7, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            zipped.writestr(info, data)
    with zipfile.ZipFile(archive) as zipped:
        require(zipped.testzip() is None, 'ZIP CRC failure')
        require(set(zipped.namelist()) == {RELEASE + '/' + name for name in files}, 'ZIP inventory mismatch')
        require(all(zipped.read(RELEASE + '/' + name) == data for name, data in files.items()), 'ZIP byte mismatch')

    installer = out / ('Profoto-B10-' + RELEASE + '-Custom-Updater.exe')
    execute([args.nsis_dir / 'makensis.exe', '/NOCD', '/V3',
             '/DOUTPUT_EXE=' + installer.name, '/DPACKAGE_DIR=' + RELEASE, HERE / 'installer.nsi'],
            out, logs / 'nsis_compile.log', 300)
    extracted_dir = out / 'installer_roundtrip'
    execute([args.seven_zip, 'x', '-y', '-o' + str(extracted_dir), installer],
            out, logs / 'installer_extract.log', 120)
    extracted = regular_files(extracted_dir)
    require(all(extracted.get(name) == data for name, data in files.items()), 'Installer payload byte mismatch')
    require(set(extracted) - set(files) == set(NSIS_COMPONENTS), 'Unexpected installer embedded components')
    for name, source in NSIS_COMPONENTS.items():
        require(extracted[name] == (args.nsis_dir / source).read_bytes(), 'NSIS component byte mismatch: ' + name)
    blob = installer.read_bytes()
    pe = gui.pefile.PE(data=blob)
    require(pe.OPTIONAL_HEADER.DATA_DIRECTORY[4].VirtualAddress == 0, 'Unexpected Authenticode directory')
    require(b'level="asInvoker"' in blob, 'Installer must run per-user')
    version_strings = {}
    for group in pe.FileInfo:
        for item in group:
            if item.Key == b'StringFileInfo':
                for table in item.StringTable:
                    version_strings.update(table.entries)
    require(version_strings.get(b'CompanyName') == b'Caimankekw', 'Installer developer attribution')
    for private in {str(ROOT), str(Path.home()), str(args.runtime), str(args.vendor_docs)}:
        for needle in (private.encode('utf-8'), private.encode('utf-16le')):
            require(needle not in blob and all(needle not in data for data in files.values()), 'Private input path leaked to output')
    require(runtime == regular_files(args.runtime), 'Original runtime changed during packaging')
    require(args.binary.read_bytes() == binary and args.dfu.read_bytes() == dfu, 'Firmware input changed during packaging')
    report = {
        'status': 'PASS', 'release': RELEASE, 'gui': checked, 'gui_details': details,
        'gui_negative_controls': negatives, 'runtime_files': len(runtime), 'runtime_unchanged': 29,
        'staged_files': len(files), 'zip': {'name': archive.name, **entry(archive.read_bytes())},
        'installer': {'name': installer.name, **entry(blob)},
        'zip_roundtrip': True, 'installer_payload_roundtrip': True, 'installer_as_invoker': True,
        'installer_extra_nsis_plugins': sorted(NSIS_COMPONENTS),
        'updater_executed': False, 'installer_executed': False, 'usb_accessed': False,
        'drivers_installed': False, 'input_files_unchanged': True,
    }
    (out / 'package_verification.json').write_bytes(encoded(report))
    (out / 'SHA256SUMS.txt').write_text(gui.sha(blob) + '  ' + installer.name + '\n' +
                                      gui.sha(archive.read_bytes()) + '  ' + archive.name + '\n', encoding='ascii')
    print(json.dumps({'status': 'PASS', 'release': RELEASE, 'gui_sha256': gui.sha(output_gui),
                      'installer_sha256': gui.sha(blob), 'negative_controls': len(negatives),
                      'runtime_unchanged': 29, 'report': 'package_verification.json'}, indent=2))


def main():
    require(not sys.flags.optimize, "Run Python without -O/-OO")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--runtime', type=Path, required=True, help='Original D3 Profoto_DFU-app folder containing all 30 runtime files')
    parser.add_argument('--vendor-docs', type=Path, required=True, help='Folder containing original FAQ PDF and license_3rd_party.txt')
    parser.add_argument('--nsis-dir', type=Path, required=True, help='Full extracted NSIS 3.13 directory')
    parser.add_argument('--seven-zip', type=Path, required=True, help='7-Zip 26.04 x64 7z.exe; matching 7z.dll must be beside it')
    parser.add_argument('--bin', dest='binary', type=Path, default=ROOT / RELEASE / 'build' / 'RC5.bin')
    parser.add_argument('--dfu', type=Path, default=ROOT / RELEASE / 'build' / 'RC5.dfu')
    parser.add_argument('--output', type=Path,
                        default=HERE / 'build' / datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S.%fZ'),
                        help='New directory only; defaults to windows/build/<UTC timestamp>')
    args = parser.parse_args()
    for key in ('runtime', 'vendor_docs', 'nsis_dir', 'seven_zip', 'binary', 'dfu'):
        setattr(args, key, getattr(args, key).resolve(strict=True))
    build_package(args)


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError, subprocess.SubprocessError) as error:
        print('FAIL: ' + str(error), file=sys.stderr)
        raise SystemExit(1)
