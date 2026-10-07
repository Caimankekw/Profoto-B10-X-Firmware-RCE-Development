# SPDX-License-Identifier: AGPL-3.0-only
# Copyright (C) 2026 Caimankekw.
"""Build the two minimal D3 patch projects and check the frozen release bytes."""
from pathlib import Path
import argparse
import hashlib
import struct
import subprocess
import sys
import zlib

ROOT = Path(__file__).resolve().parent
PINS = {'REV5': {'RC5.bin': 'ad8b5ff203bd1d7426f66666124432f154c00bc46c31878d660ff0e0ea506ea8', 'RC5.dfu': 'c6c2343921b302c2ce45e9bf06ffa5e66d591700f59dd0218388327c24d57f4f', 'powerboard.bin': 'be56734b508ef577fa5c4c257499e3a65ef06003aa4d7c8d526cccaf09a85fac'}}

def check(condition, message):
    if not condition:
        raise ValueError(message)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('version', choices=['REV5'], default='REV5', nargs='?')
    args = parser.parse_args()
    check(not sys.flags.optimize, 'Run without -O: the patch builders use assertions')
    for version in [args.version]:
        print('Building ' + version, flush=True)
        subprocess.run([sys.executable, str(ROOT / version / 'source/build_recharge.py')],
                       cwd=ROOT, check=True, shell=False)
        data = {}
        for name, digest in PINS[version].items():
            data[name] = (ROOT / version / 'build' / name).read_bytes()
            check(hashlib.sha256(data[name]).hexdigest() == digest, version + ': hash mismatch: ' + name)
        prefix = 'RC5'
        binary, dfu, pb = data[prefix + '.bin'], data[prefix + '.dfu'], data['powerboard.bin']
        check(dfu[293:-16] == binary, 'DFU payload mismatch')
        check(struct.unpack_from('<II', dfu, 285) == (0x08000000, len(binary)), 'DFU address/size mismatch')
        check(struct.unpack_from('<I', dfu, len(dfu)-4)[0] == zlib.crc32(dfu[:-4]) ^ 0xffffffff, 'DFU CRC mismatch')
        size = struct.unpack_from('<I', binary, 0xB6A4)[0]
        offset = struct.unpack_from('<I', binary, 0xB6A8)[0] - 0x08000000
        check(binary[offset:offset+size] == pb, 'Embedded powerboard mismatch')
        print(version + ': PASS (main / DFU / powerboard match the frozen release)', flush=True)


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError, subprocess.CalledProcessError) as error:
        print('FAIL: ' + str(error), file=sys.stderr)
        raise SystemExit(1)
