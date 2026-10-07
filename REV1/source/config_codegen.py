# SPDX-License-Identifier: AGPL-3.0-only
# Copyright (C) 2026 Caimankekw.
"""Generate D3 RECHARGE CTRL main-side Thumb helpers, without patching firmware.

Ownership: config_* files only. Import build() in the integrated patch builder.
All code is AAPCS, uses existing PB queue and EEPROM mutex APIs. Mode 0=NON-X,
mode 1=X. cfg+0x67 is 0=normal/default, 1=save failed (RAM active), not PB acknowledgement.
"""
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
import json

from keystone import Ks, KS_ARCH_ARM, KS_MODE_THUMB

CFG = 0x200019A4
RECORD_ADDR = 0x3E0
MAGIC = 0x31484352  # little-endian RCH1


def imm(reg, value):
    return f"movw {reg}, #{value & 0xffff}\nmovt {reg}, #{value >> 16}"


def build(base=0x08099400):
    sym = {k: base + v for k, v in {
        "rc_get": 0x000,
        "rc_validate_record": 0x100,
        "rc_load": 0x200,
        "rc_save": 0x300,
        "rc_send": 0x500,
        "rc_set": 0x600,
        "rc_boot_hook": 0x700,
        "rc_sync_hook": 0x740,
        "rc_factory_hook": 0x780,
    }.items()}
    asm = {}
    asm["rc_get"] = f"""
        push {{r4, lr}}
        {imm('r1', CFG)}
        ldrb r0, [r1, #0x65]
        ldrb r2, [r1, #0x66]
        cmp r2, #0x52
        bne fallback
        cmp r0, #1
        bls done
    fallback:
        bl 0x08004e08
    done:
        pop {{r4, pc}}
    """
    # r0=16-byte buffer; result 0/1 valid mode, 2 invalid. Preserves r4-r11.
    asm["rc_validate_record"] = f"""
        push {{r4, lr}}
        mov r4, r0
        ldr r0, [r4]
        {imm('r1', MAGIC)}
        cmp r0, r1
        bne invalid
        ldrb r0, [r4, #4]
        cmp r0, #1
        bne invalid
        ldrb r0, [r4, #5]
        cmp r0, #1
        bhi invalid
        ldrb r1, [r4, #6]
        eor r0, r0, #255
        cmp r0, r1
        bne invalid
        ldrb r0, [r4, #7]
        cmp r0, #0
        bne invalid
        ldr r0, [r4, #8]
        cmp r0, #0
        bne invalid
        {imm('r0', 0x7fffffff)}
        mov r1, r4
        movs r2, #12
        bl 0x08000708
        ldr r1, [r4, #12]
        cmp r0, r1
        bne invalid
        ldrb r0, [r4, #5]
        pop {{r4, pc}}
    invalid:
        movs r0, #2
        pop {{r4, pc}}
    """
    # Uses no uninitialised buffer if read fails; read return must be exactly 1.
    asm["rc_load"] = f"""
        push {{r4, r5, r6, lr}}
        sub sp, #16
        bl 0x08004e08
        mov r4, r0
        movs r5, #0
        movw r0, #{RECORD_ADDR}
        mov r1, sp
        movs r2, #16
        bl 0x080162d4
        cmp r0, #1
        bne accept
        mov r0, sp
        bl {sym['rc_validate_record']}
        cmp r0, #1
        bhi accept
        mov r4, r0
    accept:
        {imm('r1', CFG)}
        strb r4, [r1, #0x65]
        strb r5, [r1, #0x67]
        movs r0, #0x52
        strb r0, [r1, #0x66]
        mov r0, r4
        add sp, #16
        pop {{r4, r5, r6, pc}}
    """
    # r0=mode. Returns 1 iff write succeeds and a full 16-byte readback matches.
    # One 10-tick RTOS delay gives the external memory a write-cycle interval.
    # No repeated EEPROM writes on failure. Factory original settings untouched.
    asm["rc_save"] = f"""
        push {{r4, r5, r6, lr}}
        sub sp, #32
        cmp r0, #1
        bhi failure
        mov r4, r0
        {imm('r0', MAGIC)}
        str r0, [sp]
        movs r0, #0
        str r0, [sp, #4]
        str r0, [sp, #8]
        movs r0, #1
        mov r1, sp
        strb r0, [r1, #4]
        strb r4, [r1, #5]
        eor r0, r4, #255
        strb r0, [r1, #6]
        {imm('r0', 0x7fffffff)}
        movs r2, #12
        bl 0x08000708
        str r0, [sp, #12]
        movw r0, #{RECORD_ADDR}
        mov r1, sp
        movs r2, #16
        bl 0x080161b0
        cmp r0, #1
        bne failure
        movs r0, #10
        bl 0x080214d4
        movw r0, #{RECORD_ADDR}
        add r1, sp, #16
        movs r2, #16
        bl 0x080162d4
        cmp r0, #1
        bne failure
        mov r1, sp
        add r2, sp, #16
        movs r3, #4
    compare:
        ldr r0, [r1], #4
        ldr r4, [r2], #4
        cmp r0, r4
        bne failure
        subs r3, r3, #1
        bne compare
        movs r0, #1
        b exit_save
    failure:
        movs r0, #0
    exit_save:
        add sp, #32
        pop {{r4, r5, r6, pc}}
    """
    # Existing queue copies stack packet as all stock send helpers do.
    asm["rc_send"] = f"""
        push {{r4, lr}}
        sub sp, #8
        bl {sym['rc_get']}
        mov r1, sp
        strb r0, [r1, #2]
        movw r0, #0x1032
        strh r0, [r1]
        mov r0, sp
        movs r1, #3
        bl 0x0800af38
        add sp, #8
        pop {{r4, pc}}
    """
    # Returns persistence status. On storage failure RAM+PB still use selected
    # mode until reboot; caller should not claim persistent success from mode.
    asm["rc_set"] = f"""
        push {{r4, lr}}
        cmp r0, #1
        bhi invalid_set
        mov r4, r0
        {imm('r1', CFG)}
        strb r4, [r1, #0x65]
        movs r0, #0x52
        strb r0, [r1, #0x66]
        bl 0x0800bb50
        cmp r0, #0
        beq save_set
        bl {sym['rc_send']}
    save_set:
        mov r0, r4
        bl {sym['rc_save']}
        {imm('r1', CFG)}
        eor r2, r0, #1
        strb r2, [r1, #0x67]
        pop {{r4, pc}}
    invalid_set:
        movs r0, #0
        pop {{r4, pc}}
    """
    asm["rc_boot_hook"] = f"""
        push {{r4, lr}}
        bl 0x08004dd0
        bl {sym['rc_load']}
        pop {{r4, pc}}
    """
    asm["rc_sync_hook"] = f"""
        push {{r4, lr}}
        bl {sym['rc_send']}
        {imm('r0', 0x0800af39)}
        bl 0x080138f8
        pop {{r4, pc}}
    """
    asm["rc_factory_hook"] = f"""
        push {{r4, lr}}
        bl 0x0801ae30
        bl 0x08004e08
        bl {sym['rc_set']}
        pop {{r4, pc}}
    """
    ks = Ks(KS_ARCH_ARM, KS_MODE_THUMB)
    chunks = []
    slots = list(sym)
    for index, name in enumerate(slots):
        address = sym[name]
        machine, _ = ks.asm(asm[name], address)
        machine = bytes(machine)
        boundary = sym[slots[index + 1]] if index + 1 < len(slots) else base + 0x800
        assert address + len(machine) <= boundary, (name, len(machine))
        chunks.append({"name": name, "address": address, "data": machine, "asm": asm[name]})
    patches = []
    for address, name, original in [
        (0x0801AF74, "rc_boot_hook", "e9f72cff"),
        (0x0800BC9E, "rc_sync_hook", "07f02bfe"),
        (0x08019B70, "rc_factory_hook", "01f05ef9"),
    ]:
        machine, _ = ks.asm(f"bl {sym[name]}", address)
        assert len(machine) == 4
        patches.append({"address": address, "data": bytes(machine), "original": bytes.fromhex(original), "name": name})
    return {"symbols": sym, "chunks": chunks, "patches": patches, "end": base + 0x800}


if __name__ == "__main__":
    result = build()
    binary = (ROOT / "D3/firmware/B10_REV_D3.bin").read_bytes()
    for p in result["patches"]:
        off = p["address"] - 0x08000000
        assert binary[off:off+4] == p["original"], p
    manifest = {"symbols": result["symbols"], "end": result["end"],
                "chunks": [{k: (v.hex() if isinstance(v, bytes) else v) for k, v in c.items()} for c in result["chunks"]],
                "patches": [{k: (v.hex() if isinstance(v, bytes) else v) for k, v in c.items()} for c in result["patches"]]}
    out = Path(__file__).resolve().parent.parent / "build"
    out.mkdir(parents=True, exist_ok=True)
    output = out / "config_generated.json"
    output.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(json.dumps({"symbols": result["symbols"], "lengths": {c['name']: len(c['data']) for c in result['chunks']}, "patches_verified": len(result['patches'])}, indent=2))
