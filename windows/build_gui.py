#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# Copyright 2026 Caimankekw
"""Offline REV1 GUI resource patch; never execute the updater or access USB."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import struct
import sys
import zlib
import pefile

RELEASE = "REV1"
REVISION = "D3-RC1"
ABOUT = "D3"
GUI_SHA = "2db2a88b37ffb678955458b4427fd7cda898b1228522d80d95f036af2ec68b81"
GUI_SIZE = 4445184
SOURCE_SHA = "4fe18a566843afde2bb1b3b4e8600495d9d010afeab1e1902519022fa3356fa5"
BIN_SHA = "7661a83958caf5cd62a477575a8ffe8a6be9d0153ef076b5d7bf2e5850df3a0e"
DFU_SHA = "c8088fafa8d224d203c023442f0157050800169ded67282e62088bc833b1bcbe"
SOURCE_SIZE = 2874880
BIN_SIZE = 682596
TREE_FILE, TREE_LEN = 0x102480, 84
NAMES_FILE, NAMES_LEN = 0x1024E0, 158
DATA_FILE, DATA_LEN = 0x102580, 1459650
NEW_RVA, NEW_RAW = 0x2C5000, 0x2BDE00
NEW_HEADER, NAMES_DELTA, DATA_DELTA = 0x2E0, 0x60, 0x100
POINTERS = {
    "tree": (0x504880, 0x6C5000, (0xBE7, 0xC17, 0xC47, 0x2A7C7), 4),
    "names": (0x5048E0, 0x6C5060, (0xBDF, 0xC0F, 0xC3F, 0x2A7BF), 8),
    "data": (0x504980, 0x6C5100, (0xBD7, 0xC07, 0xC37, 0x2A7B7), 12),
}
LABEL_EDITS = [
    {"id": "2", "old": "Firmware upgrade", "new": "RC1 CUSTOM"},
    {"id": "5", "old": "Follow the steps below\\nto upgrade your product.",
     "new": "EXPERIMENTAL firmware.\\nFollow the steps below."},
]

def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def align(value, boundary):
    return (value + boundary - 1) // boundary * boundary


def parse_dfuse(data):
    require(len(data) == BIN_SIZE + 309, "RC1 DFU length")
    require(struct.unpack_from("<5sBIB", data) == (b"DfuSe", 1, len(data) - 16, 1), "DFU prefix/image size")
    signature, alt, named, _name, size, elements = struct.unpack_from("<6sBI255sII", data, 11)
    require(signature == b"Target" and alt == 0 and named in (0, 1), "DFU target")
    require((size, elements) == (len(data) - 301, 1), "DFU target size/count")
    require(struct.unpack_from("<II", data, 285) == (0x08000000, BIN_SIZE), "DFU element address/size")
    _device, pid, vid, version, signature, size, crc = struct.unpack_from("<HHHH3sBI", data, len(data) - 16)
    require((pid, vid, version, signature, size) == (0xDF11, 0x0483, 0x011A, b"UFD", 16), "DFU suffix")
    require(crc == zlib.crc32(data[:-4]) ^ 0xFFFFFFFF, "DFU CRC")
    return data[293:-16]


def validate_inputs(original, binary, dfu):
    require(len(original) == SOURCE_SIZE and sha(original) == SOURCE_SHA, "Pinned original EXE hash/size")
    require(len(binary) == BIN_SIZE and sha(binary) == BIN_SHA, "Pinned RC1 BIN hash/size")
    require(len(dfu) == BIN_SIZE + 309 and sha(dfu) == DFU_SHA, "Pinned RC1 DFU hash/size")
    require(parse_dfuse(dfu) == binary, "RC1 BIN/DFU payload mismatch")
    require(binary[0x1AC:0x1B0] == bytes.fromhex("12472301"), "Metadata start marker")
    require(binary[0x2F4:0x2F8] == bytes.fromhex("13472301"), "Metadata end marker")
    require(binary[0x1B0] == 0x8C, "Metadata family")
    require(binary[0x1D4:0x1F4] == REVISION.encode().ljust(32, b"\0"), "Metadata revision")
    require(binary[0x1AC:0x2F8] == binary[0x980A4:0x981F0], "Metadata copies")
    require(binary[0x55530:0x55534] == ABOUT.encode().ljust(4, b"\0"), "Firmware ABOUT revision")


def original_resources(original):
    tree = original[TREE_FILE:TREE_FILE + TREE_LEN]
    names = original[NAMES_FILE:NAMES_FILE + NAMES_LEN]
    data = original[DATA_FILE:DATA_FILE + DATA_LEN]
    records = []
    for index in range(2, 6):
        name_offset, flags, country, language, data_offset = struct.unpack_from(">IHHHI", tree, index * 14)
        length = struct.unpack_from(">H", names, name_offset)[0]
        name = names[name_offset + 6:name_offset + 6 + 2 * length].decode("utf-16-be")
        size = struct.unpack_from(">I", data, data_offset)[0]
        payload = data[data_offset + 4:data_offset + 4 + size]
        require(len(payload) == size and country == 0 and language == 1, "Original QRC resource bounds/locale")
        require(flags == (1 if name == "settings_GUI.json" else 0), "Original resource flags")
        records.append({"index": index, "name": name, "flags": flags, "data_offset": data_offset, "payload": payload})
    require({r["name"] for r in records} == {"firmware.bin", "firmware.dfu", "background.jpg", "settings_GUI.json"}, "QRC names")
    return tree, names, data, sorted(records, key=lambda r: r["data_offset"])


def rebuild_arrays(tree, records, replacements):
    result_tree, result_data = bytearray(tree), bytearray()
    for record in records:
        payload = replacements.get(record["name"], record["payload"])
        require(len(payload) <= 0xFFFFFFFF and len(result_data) <= 0xFFFFFFFF, "QRC uint32 overflow")
        struct.pack_into(">I", result_tree, record["index"] * 14 + 10, len(result_data))
        result_data.extend(struct.pack(">I", len(payload)))
        result_data.extend(payload)
    return bytes(result_tree), bytes(result_data)


def modify_display_settings(payload):
    require(len(payload) > 4, "qCompress settings header")
    decoded = zlib.decompress(payload[4:])
    require(len(decoded) == struct.unpack_from(">I", payload)[0], "qCompress settings length")
    # The vendor's text contains literal CR/LF inside JSON string values. Keep
    # their representation and all bytes except these two exact display texts.
    before = json.loads(decoded, strict=False)
    updated = decoded
    for edit in LABEL_EDITS:
        old, new = edit["old"].encode("ascii"), edit["new"].encode("ascii")
        require(updated.count(old) == 1, "Display replacement must be unique")
        updated = updated.replace(old, new, 1)
    after = json.loads(updated, strict=False)
    expected = json.loads(decoded, strict=False)
    for edit in LABEL_EDITS:
        labels = [label for label in expected["labels"] if label["id"] == edit["id"]]
        require(len(labels) == 1, "Display label id")
        old = edit["old"].replace("\\n", "\n")
        new = edit["new"].replace("\\n", "\n")
        require(old in labels[0]["text"], "Display label text")
        labels[0]["text"] = labels[0]["text"].replace(old, new)
    require(before.keys() == {"labels", "circles"} and after == expected, "Only two display labels may change")
    return struct.pack(">I", len(updated)) + zlib.compress(updated, level=9), updated


def build_image(original, binary, dfu):
    validate_inputs(original, binary, dfu)
    pe = pefile.PE(data=original)
    require(pe.FILE_HEADER.Machine == 0x14C and pe.FILE_HEADER.NumberOfSections == 9, "Original PE architecture/sections")
    require((pe.OPTIONAL_HEADER.ImageBase, pe.OPTIONAL_HEADER.FileAlignment, pe.OPTIONAL_HEADER.SectionAlignment) == (0x400000, 0x200, 0x1000), "Original PE alignments/base")
    require(pe.OPTIONAL_HEADER.SizeOfHeaders == 0x400 and not any(original[NEW_HEADER:0x400]), "PE section header slack")
    require(pe.get_overlay_data_start_offset() is None, "Original PE overlay")
    require(pe.OPTIONAL_HEADER.SizeOfImage == NEW_RVA, "Original image size")
    require(pe.OPTIONAL_HEADER.DATA_DIRECTORY[4].VirtualAddress == 0 and pe.OPTIONAL_HEADER.DATA_DIRECTORY[4].Size == 0, "Original certificate directory")
    tree, names, data, records = original_resources(original)
    require(rebuild_arrays(tree, records, {}) == (tree, data), "Original QRC exact reconstruction")
    settings = next(r["payload"] for r in records if r["name"] == "settings_GUI.json")
    settings_new, settings_text = modify_display_settings(settings)
    new_tree, new_data = rebuild_arrays(tree, records, {
        "firmware.bin": binary, "firmware.dfu": dfu, "settings_GUI.json": settings_new,
    })
    section = new_tree + bytes(NAMES_DELTA - len(new_tree)) + names
    section += bytes(DATA_DELTA - len(section)) + new_data
    raw_size = align(len(section), 0x200)
    out = bytearray(original + section + bytes(raw_size - len(section)))
    struct.pack_into("<8sIIIIIIHHI", out, NEW_HEADER, b".qrcupd\0", len(section), NEW_RVA, raw_size, NEW_RAW, 0, 0, 0, 0, 0x40000040)
    struct.pack_into("<H", out, 0x86, 10)
    struct.pack_into("<I", out, 0xA0, pe.OPTIONAL_HEADER.SizeOfInitializedData + raw_size)
    struct.pack_into("<I", out, 0xD0, align(NEW_RVA + max(len(section), raw_size), 0x1000))
    for _name, (old, new, offsets, stack_disp) in POINTERS.items():
        found, start = [], 0
        while (start := original.find(struct.pack("<I", old), start)) >= 0:
            found.append(start)
            start += 1
        require(found == sorted(offsets), "Original pointer occurrence set")
        for offset in offsets:
            require(original[offset - 4:offset] == bytes([0xC7, 0x44, 0x24, stack_disp]), "QRC pointer MOV encoding")
            struct.pack_into("<I", out, offset, new)
    struct.pack_into("<I", out, 0xD8, pefile.PE(data=bytes(out)).generate_checksum())
    return bytes(out), {
        "original_qrc_reconstructed_exactly": True,
        "section": {"name": ".qrcupd", "rva": NEW_RVA, "raw_offset": NEW_RAW,
                    "virtual_size": len(section), "raw_size": raw_size, "characteristics": "0x40000040"},
        "pointer_patches": [{"array": name, "old": old, "new": new, "offsets": list(offsets)}
                            for name, (old, new, offsets, _disp) in POINTERS.items()],
        "display_label_edits": LABEL_EDITS,
        "settings_decompressed_size": len(settings_text),
        "settings_decompressed_sha256": sha(settings_text),
    }


def local_dependencies(directory):
    """Record all supplied DLLs/plugins; never load DLLs or execute the EXE."""
    directory = Path(directory)
    source = directory / "Profoto_DFU-app.exe"
    files = sorted(directory.rglob("*.dll"), key=lambda path: path.relative_to(directory).as_posix().lower())
    available = {path.name.lower(): path for path in files}
    records = []
    for path in [source] + files:
        blob = path.read_bytes()
        pe = pefile.PE(data=blob)
        imports = sorted({item.dll.decode("ascii") for item in getattr(pe, "DIRECTORY_ENTRY_IMPORT", [])}, key=str.lower)
        records.append({"path": path.relative_to(directory).as_posix(), "size": len(blob), "sha256": sha(blob),
                        "machine": hex(pe.FILE_HEADER.Machine), "imports": imports,
                        "local_imports": [available[name.lower()].relative_to(directory).as_posix() for name in imports if name.lower() in available],
                        "external_imports": [name for name in imports if name.lower() not in available]})
    return records


def main():
    require(not sys.flags.optimize, "Run Python without -O/-OO")
    import argparse
    import verify_gui
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--original-exe", type=Path, required=True)
    parser.add_argument("--bin", dest="binary", type=Path, required=True)
    parser.add_argument("--dfu", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True,
                        help="New output EXE; an existing file is never overwritten")
    args = parser.parse_args()
    original, binary, dfu = [p.read_bytes() for p in (args.original_exe, args.binary, args.dfu)]
    output, details = build_image(original, binary, dfu)
    verified = verify_gui.verify_image(original, binary, dfu, output)
    negative = verify_gui.negative_controls(original, binary, dfu, output)
    require(len(negative) == 8, "Eight negative controls required")
    require(len(output) == GUI_SIZE and sha(output) == GUI_SHA, "Frozen GUI hash/size")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("xb") as stream:
        stream.write(output)
    print(json.dumps({"status": "PASS", "release": RELEASE, "size": len(output), "sha256": sha(output),
                      "negative_controls": negative, "verification": verified,
                      "updater_executed": False, "usb_accessed": False}, indent=2))


if __name__ == "__main__":
    main()
