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
PINS = {'REV1': {'RC1.bin': '7661a83958caf5cd62a477575a8ffe8a6be9d0153ef076b5d7bf2e5850df3a0e', 'RC1.dfu': 'c8088fafa8d224d203c023442f0157050800169ded67282e62088bc833b1bcbe', 'powerboard.bin': 'ce94c00388cdf755d4c343d8eeab5e517096ae8a81974efa09f67d175d6eb000'}}

def check(condition, message):
    if not condition:
        raise ValueError(message)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('version', choices=['REV1'], default='REV1', nargs='?')
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
        prefix = 'RC1'
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
