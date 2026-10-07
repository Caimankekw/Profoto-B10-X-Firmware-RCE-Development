# SPDX-License-Identifier: AGPL-3.0-only
# Copyright (C) 2026 Caimankekw.
"""Reproducible binary patch build. Never opens USB or runs an updater.

Only accepts the exactly identified official B10 REV-D3 inputs. All mutations
are applied to copies and recorded, including newly allocated code/data.
"""
from pathlib import Path
import hashlib
import json
import struct
import zlib

HERE = Path(__file__).resolve().parent
ROOT = Path(__file__).resolve().parents[2]
from keystone import Ks, KS_ARCH_ARM, KS_MODE_THUMB
from capstone import Cs, CS_ARCH_ARM, CS_MODE_THUMB, CS_MODE_MCLASS
import config_codegen
from pb_patch import build_powerboard
from ui_assets import build_assets

BASE = 0x08000000
ORIGINAL_SHA = '105de29fd444d22755e676c6474eb32f6f32e37ad333b8d232d49948e228b305'
OUT = HERE.parent / 'build'
MAIN_NAME = 'RC5.bin'
DFU_NAME = 'RC5.dfu'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def aligned(value, align=4):
    return (value + align - 1) & -align


def imm(reg, value):
    return f'movw {reg}, #{value & 65535}\nmovt {reg}, #{value >> 16}'


def make_dfu(payload, template):
    assert template[:6] == b'DfuSe\x01' and template[10] == 1
    head = bytearray(template[:293])
    struct.pack_into('<I', head, 6, 293 + len(payload))
    struct.pack_into('<I', head, 277, len(payload) + 8)
    struct.pack_into('<I', head, 289, len(payload))
    result = head + payload + template[-16:-4]
    result += struct.pack('<I', zlib.crc32(result) ^ 0xffffffff)
    assert result[293:-16] == payload
    return bytes(result)


def build():
    original = (ROOT / 'D3/firmware/B10_REV_D3.bin').read_bytes()
    template = (ROOT / 'D3/firmware/B10_REV_D3.dfu').read_bytes()
    pb_original = original[0x8b670:0x97c80]
    if sha(original) != ORIGINAL_SHA:
        raise ValueError('Only the byte-exact official D3 base is supported')
    assert len(original) == 0x9935c and original[0x8b670:0x97c80] == pb_original
    ks = Ks(KS_ARCH_ARM, KS_MODE_THUMB)
    asm = lambda source, at: bytes(ks.asm(source, at)[0])
    cfg = config_codegen.build(0x08099400)
    ui_base = cfg['end']
    ui_addresses = {'label': ui_base, 'value': ui_base+0x40, 'click': ui_base+0x140,
                    'flash_value': ui_base+0x200, 'flash_click': ui_base+0x280,
                    'flash_shortcut': ui_base+0x2c0, 'home_mode': ui_base+0x300,
                    'home_profile': ui_base+0x400}
    asset_base = ui_base + 0x500
    assets, asset_info = build_assets(asset_base)
    pb_source_address = aligned(asset_base + len(assets), 0x100)

    # A deterministic development identifier, not an image-wide checksum.
    pb_unsigned, _ = build_powerboard(pb_original)
    pb_id = sha(b'RECHARGE CTRL RC5 powerboard\0'+pb_unsigned)[:8]
    pb_data, pb_manifest = build_powerboard(pb_original, version_id=pb_id)
    pb_data = bytearray(pb_data)
    assert struct.unpack_from('<I', pb_data, 0x10a8)[0] == 0x08a7ad77
    struct.pack_into('<I', pb_data, 0x10a8, int(pb_id, 16))
    pb_manifest['modifications'].append(dict(address='0x080010a8', offset='0x10a8',
        old='77ada708', new=struct.pack('<I', int(pb_id, 16)).hex()))
    pb_manifest['sha256'] = sha(pb_data)
    final_end = aligned(pb_source_address-BASE + len(pb_data))
    assert final_end <= 0xc0000
    data = bytearray(original + b'\xff'*(final_end-len(original)))
    changes = []
    allocations = []

    def patch(address, replacement, expected=None, description=''):
        off = address-BASE
        old = bytes(data[off:off+len(replacement)])
        if len(old) != len(replacement) or (expected is not None and old != expected):
            raise ValueError(f'Preimage guard failed at {address:#x}: {description}')
        data[off:off+len(replacement)] = replacement
        changes.append(dict(address=hex(address), offset=hex(off), size=len(replacement),
                            description=description, old=old.hex(), new=replacement.hex()))

    def allocate(address, replacement, description):
        assert address >= BASE+len(original)
        for previous in allocations:
            assert address+len(replacement) <= previous['start'] or address >= previous['end']
        patch(address, replacement, b'\xff'*len(replacement), description)
        allocations.append(dict(start=address, end=address+len(replacement), description=description))

    for chunk in cfg['chunks']:
        allocate(chunk['address'], chunk['data'], chunk['name'])
    for item in cfg['patches']:
        patch(item['address'], item['data'], item['original'], item['name'])

    desc = {name: info['descriptor'] for name, info in asset_info.items()}
    ui_sources = {
        'label': imm('r3', desc['RECHARGE CTRL'])+'\nb.w 0x080191f0',
        'value': f"""
            bl {cfg['symbols']['rc_get']}
            {imm('r2', 0x20001a0b)}
            ldrb r2, [r2]
            cmp r0, #0
            beq nonx
            cmp r0, #2
            beq boost
            cmp r2, #1
            beq x_error
            {imm('r3', desc['X'])}
            b done
        x_error:
            {imm('r3', desc['X !'])}
            b done
        nonx:
            cmp r2, #1
            beq nonx_error
            {imm('r3', desc['NON-X'])}
            b done
        nonx_error:
            {imm('r3', desc['NON-X !'])}
            b done
        boost:
            cmp r2, #1
            beq boost_error
            {imm('r3', desc['BOOST'])}
            b done
        boost_error:
            {imm('r3', desc['BOOST !'])}
        done:
            b.w 0x080199a2
        """,
        'click': f"""
            bl {cfg['symbols']['rc_get']}
            adds r0, #1
            {imm('r1', 0x200019a4)}
            ldrb r1, [r1, #0x3c]
            cmp r1, #0x8d
            beq plus
            cmp r1, #0x8f
            beq plus
            cmp r0, #2
            blo apply
            movs r0, #0
            b apply
        plus:
            cmp r0, #3
            blo apply
            movs r0, #0
        apply:
            bl {cfg['symbols']['rc_set']}
            b.w 0x0801893e
        """,
        'flash_value': f"""
            bl {cfg['symbols']['eco_get']}
            cmp r0, #0
            beq native_mode
            {imm('r2', 0x20001a0b)}
            ldrb r2, [r2]
            cmp r2, #1
            beq eco_error
            {imm('r3', desc['ECO'])}
            b flash_done
        eco_error:
            {imm('r3', desc['ECO !'])}
            b flash_done
        native_mode:
            ldrb r3, [r7, #0x1d]
            cmp r3, #0
            beq normal
            {imm('r3', 0x0803acc0)}
            b flash_done
        normal:
            {imm('r3', 0x0803ab40)}
        flash_done:
            b.w 0x080199a2
        """,
        'flash_click': f"""
            bl {cfg['symbols']['flash_cycle']}
            b.w 0x080187e4
        """,
        'flash_shortcut': f"""
            bl {cfg['symbols']['flash_cycle']}
            b.w 0x0801b620
        """,
        'home_mode': f"""
            bl {ui_addresses['home_profile']}
            bl 0x08004f34
            cmp r0, #0
            bne native_home
            bl {cfg['symbols']['eco_get']}
            cmp r0, #0
            beq native_home
            ldr r2, [r7, #0x1c]
            ldr r4, [r7, #0x20]
            ldrb r3, [r7, #0x3f]
            str r3, [sp]
            ldr r0, [r7, #0xc]
            {imm('r1', 0x08034888)}
            mov r3, r4
            bl 0x0800f918
            ldr r2, [r7, #0x1c]
            ldr r4, [r7, #0x20]
            ldrb r3, [r7, #0x3f]
            str r3, [sp]
            movs r3, #1
            str r3, [sp, #4]
            ldr r0, [r7, #0xc]
            {imm('r1', desc['ECO_HOME'])}
            mov r3, r4
            bl 0x0800f768
            b.w 0x0800df90
        native_home:
            b.w 0x0800df3c
        """,
        'home_profile': f"""
            push {{r4, lr}}
            sub sp, #8
            bl {cfg['symbols']['rc_get']}
            {imm('r2', 0x20001a0b)}
            ldrb r2, [r2]
            cmp r0, #0
            beq profile_nonx
            cmp r0, #2
            beq profile_boost
            cmp r2, #1
            beq profile_x_error
            {imm('r1', desc['RECHARGE_HOME_X'])}
            b profile_draw
        profile_x_error:
            {imm('r1', desc['RECHARGE_HOME_X !'])}
            b profile_draw
        profile_nonx:
            cmp r2, #1
            beq profile_nonx_error
            {imm('r1', desc['RECHARGE_HOME_NON-X'])}
            b profile_draw
        profile_nonx_error:
            {imm('r1', desc['RECHARGE_HOME_NON-X !'])}
            b profile_draw
        profile_boost:
            cmp r2, #1
            beq profile_boost_error
            {imm('r1', desc['RECHARGE_HOME_BOOST'])}
            b profile_draw
        profile_boost_error:
            {imm('r1', desc['RECHARGE_HOME_BOOST !'])}
        profile_draw:
            ldr r2, [r7, #0x1c]
            adds r2, #26
            ldr r3, [r7, #0x20]
            ldrb r4, [r7, #0x3f]
            str r4, [sp]
            ldr r0, [r7, #0xc]
            bl 0x0800f918
            add sp, #8
            pop {{r4, pc}}
        """,
    }
    ui_chunks = []
    for name, source in ui_sources.items():
        address = ui_addresses[name]
        code = asm(source, address)
        boundary = {'label': ui_base+0x40, 'value': ui_base+0x140,
                    'click': ui_base+0x200, 'flash_value': ui_base+0x280,
                    'flash_click': ui_base+0x2c0, 'flash_shortcut': ui_base+0x300,
                    'home_mode': ui_base+0x400, 'home_profile': asset_base}[name]
        assert address+len(code) <= boundary
        allocate(address, code, 'UI '+name)
        ui_chunks.append(dict(name='ui_'+name, address=address, data=code, asm=source))
    patch(0x08017e80, bytes.fromhex('0a23'), bytes.fromhex('0923'), 'ADVANCED item count 9 -> 10')
    for address, name, old in [(0x080191b4,'label',0x080191e5),
                                (0x08019738,'value',0x080197f5),
                                (0x08018870,'click',0x0801893d)]:
        patch(address, struct.pack('<I', ui_addresses[name]|1), struct.pack('<I',old), 'slot10 '+name)
    # The original mode stays boolean throughout stock BLE/storage/PB paths.
    # These three UI sites render/cycle a synthetic ECO choice from RCH2.
    patch(0x080194dc, asm(f"b.w {ui_addresses['flash_value']}", 0x080194dc),
          bytes.fromhex('7b7f002b'), 'FLASH MODE display ECO overlay')
    patch(0x080187c2, asm(f"b.w {ui_addresses['flash_click']}", 0x080187c2),
          bytes.fromhex('ecf7b7fb'), 'FLASH MODE cycle via independent ECO setting')
    patch(0x0801b5fe, asm(f"b.w {ui_addresses['flash_shortcut']}", 0x0801b5fe),
          bytes.fromhex('e9f799fc'), 'flash mode shortcut cycle via independent ECO setting')
    # Keep the original FREEZE branch and all redraw scheduling. The caller
    # clears the whole framebuffer for every render, including ECO -> NORMAL.
    patch(0x0800df38, asm(f"b.w {ui_addresses['home_mode']}", 0x0800df38),
          bytes.fromhex('f6f7fcff'), 'home selected recharge profile plus preserved FREEZE / Plus ECO badge')
    allocate(asset_base, assets, 'native compressed menu bitmap resources')
    allocate(pb_source_address, bytes(pb_data), 'relocated extended powerboard image')
    patch(0x0800b6a8, struct.pack('<I',pb_source_address), struct.pack('<I',0x0808b670), 'PB source relocation')
    patch(0x0800b6a4, struct.pack('<I',len(pb_data)), struct.pack('<I',len(pb_original)), 'PB length, four-byte aligned')
    patch(0x0800b804, struct.pack('<I',int(pb_id,16)), struct.pack('<I',0x08a7ad77), 'PB expected protocol build ID')

    # Preserve product-family/name and exact metadata layout. Distinguish test
    # revision in both copies so the boot-time equality check remains true.
    revision = b'D3-RC5\0'.ljust(32,b'\0')
    for metadata in (0x080001ac, 0x080980a4):
        patch(metadata+0x28, revision, b'D3\0'.ljust(32,b'\0'), 'explicit development revision')
    assert data[0x1ac:0x2f8] == data[0x980a4:0x981f0]
    # Old embedded PB is retained but no longer referenced by the programmer.
    assert data[0x8b670:0x97c80] == pb_original
    assert data[:0x1ac] == original[:0x1ac]
    # Freeze the original development payload before applying display naming.
    assert sha(data) == '5c30e6f91ab65f54c344691136591db96a1b4adda1d24aa6d9c6e953680ce524'
    for address in (0x080001d4, 0x080980cc):
        patch(address, b'RC5\0'.ljust(32, b'\0'),
              b'D3-RC5\0'.ljust(32, b'\0'), 'release revision RC5')
    patch(0x08055530, b'RC5\0', b'D3\0\0', 'ABOUT revision RC5')
    assert data[0x1ac:0x2f8] == data[0x980a4:0x981f0]
    dfu = make_dfu(bytes(data), template)
    # These pins also detect changed assembler or image-resampling behavior.
    expected = {MAIN_NAME: 'ad8b5ff203bd1d7426f66666124432f154c00bc46c31878d660ff0e0ea506ea8',
                DFU_NAME: 'c6c2343921b302c2ce45e9bf06ffa5e66d591700f59dd0218388327c24d57f4f',
                'powerboard.bin': 'be56734b508ef577fa5c4c257499e3a65ef06003aa4d7c8d526cccaf09a85fac'}
    files_to_write = {MAIN_NAME: bytes(data), DFU_NAME: dfu,
                      'powerboard.bin': bytes(pb_data)}
    for name, contents in files_to_write.items():
        if sha(contents) != expected[name]:
            raise ValueError(f'Reproducibility check failed for {name}: {sha(contents)}')
    OUT.mkdir(parents=True, exist_ok=True)
    for name, contents in files_to_write.items():
        (OUT/name).write_bytes(contents)
    patch_map = dict(main_modifications=changes, allocations=allocations, powerboard=pb_manifest,
                     main_symbols=cfg['symbols'], ui_symbols=ui_addresses, bitmap_assets=asset_info)
    (OUT/'patch_map.json').write_text(json.dumps(patch_map,indent=2)+'\n',encoding='utf-8')
    manifest = dict(schema=1, release='REV5', revision='RC5',
        product_family=140,
        supported_model_ids={'B10':140,'B10Plus':141,'B10XPlus':143,'B10X':144},
        original_main_sha256=ORIGINAL_SHA, original_main_size=len(original),
        main_bin=MAIN_NAME, main_dfu=DFU_NAME, powerboard_bin='powerboard.bin',
        main_flash_address=BASE, powerboard_offset=pb_source_address-BASE,
        powerboard_size=len(pb_data), powerboard_build_id=pb_id,
        hardware_access=False,
        files={name:dict(sha256=sha(contents),size=len(contents))
               for name,contents in files_to_write.items()})
    (OUT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
    cs = Cs(CS_ARCH_ARM, CS_MODE_THUMB|CS_MODE_MCLASS)
    dis = []
    for chunk in cfg['chunks']+ui_chunks:
        dis.append('\n'+chunk['name'])
        dis.extend(f'{i.address:08x}: {i.bytes.hex():12} {i.mnemonic:9} {i.op_str}'
                   for i in cs.disasm(chunk['data'],chunk['address']))
    (OUT/'integrated_hooks.asm').write_text('\n'.join(dis)+'\n',encoding='utf-8')
    (OUT/'integrated_symbols.json').write_text(json.dumps(dict(config=cfg['symbols'],ui=ui_addresses,
        assets=asset_info,main_size=len(data),pb_offset=pb_source_address-BASE),indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(output=str(OUT),main_bytes=len(data),pb_bytes=len(pb_data),pb_id=pb_id,
        main_sha256=sha(data),dfu_sha256=sha(dfu),patches=len(changes),hardware_access=False),indent=2))
    return manifest


if __name__ == '__main__':
    build()
