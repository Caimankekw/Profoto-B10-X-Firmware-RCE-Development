#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# Copyright 2026 Caimankekw
"""Read-only PE/QRC/DFU verification and in-memory negative controls for RC1 GUI."""
from __future__ import annotations

import json
from pathlib import Path
import struct
import sys
import zlib

sys.dont_write_bytecode = True
import build_gui as build


def check(condition, message):
    if not condition:
        raise ValueError(message)


def parse_resources(blob, tree_va, names_va, data_va):
    """Traverse the resource tree independently of the builder's four leaf list."""
    pe = build.pefile.PE(data=blob)
    image_base = pe.OPTIONAL_HEADER.ImageBase
    tree, names, data = [pe.get_offset_from_rva(address - image_base) for address in (tree_va, names_va, data_va)]
    seen, result = set(), {}

    def walk(index, parent):
        check(index not in seen and index < 100, "QRC cycle or unreasonable node index")
        seen.add(index)
        offset = tree + 14 * index
        check(offset + 14 <= len(blob), "QRC node bounds")
        name_offset, flags = struct.unpack_from(">IH", blob, offset)
        check(names + name_offset + 6 <= len(blob), "QRC name prefix bounds")
        name_size = struct.unpack_from(">H", blob, names + name_offset)[0]
        check(names + name_offset + 6 + 2 * name_size <= len(blob), "QRC name bounds")
        name = blob[names + name_offset + 6:names + name_offset + 6 + 2 * name_size].decode("utf-16-be") if index else ""
        path = parent + name
        if flags & 2:
            count, first = struct.unpack_from(">II", blob, offset + 6)
            check(count <= 100, "QRC child count")
            for child in range(first, first + count):
                walk(child, path + ("/" if name else ""))
        else:
            country, language, record_offset = struct.unpack_from(">HHI", blob, offset + 6)
            record = data + record_offset
            check(record + 4 <= len(blob), "QRC record length bounds")
            size = struct.unpack_from(">I", blob, record)[0]
            check(record + 4 + size <= len(blob), "QRC payload bounds")
            check(path not in result, "Duplicate QRC path")
            result[path] = {"payload": blob[record + 4:record + 4 + size], "flags": flags,
                            "country": country, "language": language, "node": index,
                            "record_offset": record_offset, "payload_file_offset": record + 4}

    walk(0, "")
    return result


def unpack_settings(payload):
    decoded = zlib.decompress(payload[4:])
    check(struct.unpack_from(">I", payload)[0] == len(decoded), "Settings qCompress size")
    return decoded, json.loads(decoded, strict=False)


def verify_image(original, binary, dfu, output):
    build.validate_inputs(original, binary, dfu)
    source = build.pefile.PE(data=original)
    target = build.pefile.PE(data=output)
    check(target.verify_checksum(), "PE checksum")
    check(target.FILE_HEADER.NumberOfSections == 10, "New PE section count")
    check(target.OPTIONAL_HEADER.AddressOfEntryPoint == source.OPTIONAL_HEADER.AddressOfEntryPoint, "PE entrypoint")
    check(target.OPTIONAL_HEADER.ImageBase == source.OPTIONAL_HEADER.ImageBase, "PE image base")
    check(target.OPTIONAL_HEADER.DllCharacteristics == source.OPTIONAL_HEADER.DllCharacteristics, "PE loader characteristics")
    check(target.FILE_HEADER.Characteristics == source.FILE_HEADER.Characteristics, "PE COFF characteristics")
    check(target.OPTIONAL_HEADER.SizeOfHeaders == source.OPTIONAL_HEADER.SizeOfHeaders == 0x400, "PE header size")
    check(target.get_overlay_data_start_offset() is None, "No PE overlay")
    for old, new in zip(source.sections, target.sections[:9]):
        check(old.__pack__() == new.__pack__(), "Existing PE section header changed")
    for old, new in zip(source.OPTIONAL_HEADER.DATA_DIRECTORY, target.OPTIONAL_HEADER.DATA_DIRECTORY):
        check((old.VirtualAddress, old.Size) == (new.VirtualAddress, new.Size), "PE data directory changed")
    section = target.sections[-1]
    check(section.Name == b".qrcupd\0" and section.VirtualAddress == 0x2C5000 and section.PointerToRawData == len(original), "New PE section location")
    check(section.Characteristics == 0x40000040, "New section must be read-only initialized data")
    check(section.PointerToRelocations == section.PointerToLinenumbers == section.NumberOfRelocations == section.NumberOfLinenumbers == 0, "New section auxiliary pointers")
    check(section.SizeOfRawData == build.align(section.Misc_VirtualSize, 0x200), "New section raw alignment")
    check(len(output) == section.PointerToRawData + section.SizeOfRawData, "New file size")
    check(target.OPTIONAL_HEADER.SizeOfImage == build.align(section.VirtualAddress + max(section.Misc_VirtualSize, section.SizeOfRawData), 0x1000), "New PE image size")
    check(target.OPTIONAL_HEADER.SizeOfInitializedData == source.OPTIONAL_HEADER.SizeOfInitializedData + section.SizeOfRawData, "New PE initialized size")
    check(not any(output[section.PointerToRawData + section.Misc_VirtualSize:]), "New section tail padding")
    for address_name, size_name in [("PointerToRawData", "SizeOfRawData"), ("VirtualAddress", "Misc_VirtualSize")]:
        ranges = sorted((getattr(s, address_name), getattr(s, address_name) + getattr(s, size_name)) for s in target.sections if getattr(s, size_name))
        check(all(end <= next_start for (_start, end), (next_start, _next_end) in zip(ranges, ranges[1:])), "PE section overlap")
    allowed = [(0x86, 2), (0xA0, 4), (0xD0, 4), (0xD8, 4), (0x2E0, 40)]
    patches = []
    for name, (old, new, offsets, displacement) in build.POINTERS.items():
        for offset in offsets:
            check(struct.unpack_from("<I", original, offset)[0] == old, "Original pointer precondition")
            check(output[offset - 4:offset] == bytes((0xC7, 0x44, 0x24, displacement)), "Pointer instruction encoding")
            check(struct.unpack_from("<I", output, offset)[0] == new, "New resource registration pointer")
            allowed.append((offset, 4))
            patches.append({"array": name, "file_offset": hex(offset), "va": hex(new)})
    allowed_bytes = {position for start, length in allowed for position in range(start, start + length)}
    changed = [i for i, (old, new) in enumerate(zip(original, output)) if old != new]
    check(all(index in allowed_bytes for index in changed), "Change outside PE bookkeeping and 12 pointers")
    masked_old, masked_new = bytearray(original), bytearray(output[:len(original)])
    for start, length in allowed:
        masked_old[start:start + length] = bytes(length)
        masked_new[start:start + length] = bytes(length)
    check(masked_old == masked_new, "Entire original executable preserved outside whitelist")
    for start, length in [(build.TREE_FILE, build.TREE_LEN), (build.NAMES_FILE, build.NAMES_LEN), (build.DATA_FILE, build.DATA_LEN)]:
        check(output[start:start + length] == original[start:start + length], "Old QRC arrays unchanged")
    old_resources = parse_resources(original, 0x504880, 0x5048E0, 0x504980)
    new_resources = parse_resources(output, 0x6C5000, 0x6C5060, 0x6C5100)
    check(new_resources.keys() == old_resources.keys(), "QRC resource paths")
    expected_payloads = {"resources/firmware.bin": binary, "resources/firmware.dfu": dfu}
    resource_records = []
    for path, resource in new_resources.items():
        old = old_resources[path]
        check(all(resource[k] == old[k] for k in ("flags", "country", "language", "node")), "QRC flags, locale and node ordering")
        if path in expected_payloads:
            check(resource["payload"] == expected_payloads[path], "Embedded RC1 payload mismatch")
        elif path.endswith("background.jpg"):
            check(resource["payload"] == old["payload"], "Background must remain original")
        elif path.endswith("settings_GUI.json"):
            old_text, old_obj = unpack_settings(old["payload"])
            new_text, new_obj = unpack_settings(resource["payload"])
            expected_text = old_text.replace(b"Firmware upgrade", build.LABEL_EDITS[0]["new"].encode("ascii"), 1).replace(
                b"Follow the steps below\\nto upgrade your product.", b"EXPERIMENTAL firmware.\\nFollow the steps below.", 1)
            check(new_text == expected_text, "Settings changes limited to two exact display strings")
            check(new_obj == json.loads(expected_text, strict=False), "Settings parse")
            check(old_obj.keys() == new_obj.keys() == {"labels", "circles"}, "Settings structure")
        else:
            raise ValueError("Unexpected QRC resource")
        resource_records.append({"path": path, "length": len(resource["payload"]), "sha256": build.sha(resource["payload"]),
                                 "payload_file_offset": hex(resource["payload_file_offset"]), "flags": resource["flags"]})
    check(build.parse_dfuse(new_resources["resources/firmware.dfu"]["payload"]) == new_resources["resources/firmware.bin"]["payload"], "Embedded DFU payload")
    # Independent array reconstruction from traversed final records: also catches
    # unreferenced bytes, gaps and unintended QRC layout changes.
    tree_expected = bytearray(original[build.TREE_FILE:build.TREE_FILE + build.TREE_LEN])
    data_expected = bytearray()
    for path in sorted(old_resources, key=lambda p: old_resources[p]["record_offset"]):
        resource = new_resources[path]
        check(resource["record_offset"] == len(data_expected), "QRC data record order/contiguity")
        struct.pack_into(">I", tree_expected, resource["node"] * 14 + 10, len(data_expected))
        data_expected.extend(struct.pack(">I", len(resource["payload"])))
        data_expected.extend(resource["payload"])
    raw = section.PointerToRawData
    check(output[raw:raw + 84] == tree_expected, "QRC tree structure")
    check(not any(output[raw + 84:raw + 0x60]) and not any(output[raw + 0xFE:raw + 0x100]), "QRC internal padding")
    check(output[raw + 0x60:raw + 0xFE] == original[build.NAMES_FILE:build.NAMES_FILE + build.NAMES_LEN], "QRC names array")
    check(output[raw + 0x100:raw + section.Misc_VirtualSize] == data_expected, "QRC data complete reconstruction")
    for tree, names, data in ((0x430080, 0x4300C0, 0x430140), (0x441480, 0x4414C0, 0x441500)):
        check(parse_resources(original, tree, names, data) == parse_resources(output, tree, names, data), "Original font/dfu-util resource group")
    return {"result": "PASS", "size": len(output), "sha256": build.sha(output), "pe_checksum": hex(target.OPTIONAL_HEADER.CheckSum),
            "original_changed_byte_count": len(changed), "allowed_original_byte_count": len(allowed_bytes),
            "original_masked_sha256": build.sha(masked_old), "pointer_count": len(patches), "pointers": patches,
            "resources": resource_records, "metadata": {"revision": build.REVISION, "family": "0x8c", "identical_copies": True},
            "dfu": {"payload_size": len(binary), "address": "0x08000000", "alt": 0, "targets": 1, "elements": 1, "crc_valid": True}}


def negative_controls(original, binary, dfu, output):
    results = []

    def reject(name, action, expected_message):
        try:
            action()
        except ValueError as error:
            check(expected_message in str(error), "Negative control rejected for an unrelated reason: " + name)
            results.append({"name": name, "result": "REJECTED", "reason": str(error)})
        else:
            raise ValueError("Negative control accepted: " + name)

    bad_original = bytearray(original)
    bad_original[0x1000] ^= 1
    reject("changed original EXE", lambda: build.build_image(bytes(bad_original), binary, dfu), "Pinned original EXE")
    bad_binary = bytearray(binary)
    bad_binary[-1] ^= 1
    reject("changed RC1 BIN", lambda: build.build_image(original, bytes(bad_binary), dfu), "Pinned RC1 BIN")
    bad_dfu = bytearray(dfu)
    bad_dfu[-1] ^= 1
    reject("changed RC1 DFU input", lambda: build.build_image(original, binary, bytes(bad_dfu)), "Pinned RC1 DFU")
    reject("DFU CRC corruption", lambda: build.parse_dfuse(bytes(bad_dfu)), "DFU CRC")
    bad_address = bytearray(dfu)
    struct.pack_into("<I", bad_address, 285, 0x08001000)
    struct.pack_into("<I", bad_address, len(bad_address) - 4, zlib.crc32(bad_address[:-4]) ^ 0xFFFFFFFF)
    reject("DFU wrong address with valid CRC", lambda: build.parse_dfuse(bytes(bad_address)), "DFU element address")

    def pe_mutation(offset, value):
        modified = bytearray(output)
        modified[offset:offset + len(value)] = value
        struct.pack_into("<I", modified, 0xD8, build.pefile.PE(data=bytes(modified)).generate_checksum())
        return bytes(modified)

    reject("missing constructor data-pointer update", lambda: verify_image(original, binary, dfu,
           pe_mutation(0x2A7B7, struct.pack("<I", 0x504980))), "New resource registration pointer")
    reject("unapproved original code edit with valid PE checksum", lambda: verify_image(original, binary, dfu,
           pe_mutation(0x1000, bytes((output[0x1000] ^ 1,)))), "Change outside")
    resources = parse_resources(output, 0x6C5000, 0x6C5060, 0x6C5100)
    offset = resources["resources/firmware.dfu"]["payload_file_offset"] + 1000
    reject("embedded DFU corruption with valid PE checksum", lambda: verify_image(original, binary, dfu,
           pe_mutation(offset, bytes((output[offset] ^ 1,)))), "Embedded RC1 payload mismatch")
    return results


def main():
    check(not sys.flags.optimize, "Run Python without -O/-OO")
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--original-exe", type=Path, required=True)
    parser.add_argument("--bin", dest="binary", type=Path, required=True)
    parser.add_argument("--dfu", type=Path, required=True)
    parser.add_argument("--gui", type=Path, required=True)
    args = parser.parse_args()
    original, binary, dfu, output = [p.read_bytes() for p in
                                    (args.original_exe, args.binary, args.dfu, args.gui)]
    result = verify_image(original, binary, dfu, output)
    negative = negative_controls(original, binary, dfu, output)
    check(len(negative) == 8, "Eight negative controls required")
    check(len(output) == build.GUI_SIZE and build.sha(output) == build.GUI_SHA, "Frozen GUI hash/size")
    print(json.dumps({"status": "PASS", "release": build.RELEASE, "verification": result,
                      "negative_controls": negative, "updater_executed": False, "usb_accessed": False}, indent=2))


if __name__ == "__main__":
    main()
