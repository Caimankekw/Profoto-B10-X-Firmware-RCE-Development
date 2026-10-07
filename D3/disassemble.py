"""On-demand linear Thumb disassembly of the fixed original REV-D3 image.

This is not function discovery or decompilation. Data can decode as instructions.
No USB access and no pre-generated assembly is required by the project.
"""

import argparse
import hashlib
from pathlib import Path


BASE = 0x08000000
PB_START, PB_END = 0x8B670, 0x97C80
MAIN_SHA = "105de29fd444d22755e676c6474eb32f6f32e37ad333b8d232d49948e228b305"
PB_SHA = "6f8778d89a4d10ddc13b7726ff76814643accd3b37ad9743eb192faebb6a74b6"


def read_images():
    path = Path(__file__).resolve().parent / "firmware" / "B10_REV_D3.bin"
    main = path.read_bytes()
    if len(main) != 627548 or hashlib.sha256(main).hexdigest() != MAIN_SHA:
        raise ValueError("Input is not the fixed original REV-D3 BIN")
    powerboard = main[PB_START:PB_END]
    if hashlib.sha256(powerboard).hexdigest() != PB_SHA:
        raise ValueError("Embedded power-board SHA-256 mismatch")
    return {"main": main, "powerboard": powerboard}


def regions(name, data, start, end):
    lo = BASE if start is None else start
    hi = BASE + len(data) if end is None else end
    if lo % 2 or hi % 2 or not BASE <= lo < hi <= BASE + len(data):
        raise ValueError(f"Invalid even-aligned range for {name}: {lo:#x}..{hi:#x}")
    spans = [(0, PB_START), (PB_END, len(data))] if name == "main" else [(0, len(data))]
    return [(max(lo, BASE + a), min(hi, BASE + b))
            for a, b in spans if max(lo, BASE + a) < min(hi, BASE + b)]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--image", choices=("both", "main", "powerboard"), default="both")
    parser.add_argument("--start", type=lambda s: int(s, 0), help="inclusive virtual address")
    parser.add_argument("--end", type=lambda s: int(s, 0), help="exclusive virtual address")
    args = parser.parse_args()
    if args.image == "both" and (args.start is not None or args.end is not None):
        parser.error("Choose --image main or powerboard when specifying a range")
    try:
        from capstone import Cs, CS_ARCH_ARM, CS_MODE_THUMB, CS_MODE_MCLASS
    except ImportError:
        parser.error("Missing capstone; install the project Python requirements first")
    images = read_images()
    names = ("main", "powerboard") if args.image == "both" else (args.image,)
    jobs = [(name, regions(name, images[name], args.start, args.end)) for name in names]
    for name, spans in jobs:
        if not spans:
            parser.error("Main image range lies wholly inside the embedded power-board; select powerboard")
        destination = args.output_dir / f"{name}.asm"
        if destination.exists():
            parser.error(f"Refusing to overwrite existing file: {destination}")
    decoder = Cs(CS_ARCH_ARM, CS_MODE_THUMB | CS_MODE_MCLASS)
    decoder.skipdata = True
    args.output_dir.mkdir(parents=True, exist_ok=True)
    for name, spans in jobs:
        destination = args.output_dir / f"{name}.asm"
        data = images[name]
        with destination.open("x", encoding="utf-8", newline="\n") as out:
            out.write(f"; REV-D3 {name}, base {BASE:#010x}, SHA-256 {hashlib.sha256(data).hexdigest()}\n")
            out.write("; Linear disassembly only: data/literal pools can appear as instructions.\n")
            if name == "main":
                out.write("; Embedded power-board skipped; see powerboard.asm for its own address space.\n")
            for lo, hi in spans:
                out.write(f"\n; Range [{lo:#010x}, {hi:#010x})\n")
                for address, size, mnemonic, operands in decoder.disasm_lite(data[lo - BASE:hi - BASE], lo):
                    raw = data[address - BASE:address - BASE + size].hex()
                    out.write(f"{address:08x}: {raw:<10} {mnemonic:<9} {operands}\n")
        print(destination)


if __name__ == "__main__":
    main()
