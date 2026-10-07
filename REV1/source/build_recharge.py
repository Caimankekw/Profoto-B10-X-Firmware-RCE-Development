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
MAIN_NAME = 'RC1.bin'
DFU_NAME = 'RC1.dfu'


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
    ui_base = cfg['end']  # 0x08099c00
    ui_addresses = {'label': ui_base, 'value': ui_base+0x40, 'click': ui_base+0x140}
    asset_base = ui_base + 0x200
    assets, asset_info = build_assets(asset_base)
    pb_source_address = aligned(asset_base + len(assets), 0x100)

    # A deterministic development identifier, not an image-wide checksum.
    pb_unsigned, _ = build_powerboard(pb_original)
    pb_id = sha(b'RECHARGE CTRL RC1 powerboard\0'+pb_unsigned)[:8]
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
        done:
            b.w 0x080199a2
        """,
        'click': f"""
            bl {cfg['symbols']['rc_get']}
            eor r0, r0, #1
            bl {cfg['symbols']['rc_set']}
            b.w 0x0801893e
        """,
    }
    ui_chunks = []
    for name, source in ui_sources.items():
        address = ui_addresses[name]
        code = asm(source, address)
        boundary = {'label': ui_base+0x40, 'value': ui_base+0x140, 'click': asset_base}[name]
        assert address+len(code) <= boundary
        allocate(address, code, 'UI '+name)
        ui_chunks.append(dict(name='ui_'+name, address=address, data=code, asm=source))
    patch(0x08017e80, bytes.fromhex('0a23'), bytes.fromhex('0923'), 'ADVANCED item count 9 -> 10')
    for address, name, old in [(0x080191b4,'label',0x080191e5),
                                (0x08019738,'value',0x080197f5),
                                (0x08018870,'click',0x0801893d)]:
        patch(address, struct.pack('<I', ui_addresses[name]|1), struct.pack('<I',old), 'slot10 '+name)
    allocate(asset_base, assets, 'five native compressed bitmap resources')
    allocate(pb_source_address, bytes(pb_data), 'relocated extended powerboard image')
    patch(0x0800b6a8, struct.pack('<I',pb_source_address), struct.pack('<I',0x0808b670), 'PB source relocation')
    patch(0x0800b6a4, struct.pack('<I',len(pb_data)), struct.pack('<I',len(pb_original)), 'PB length, four-byte aligned')
    patch(0x0800b804, struct.pack('<I',int(pb_id,16)), struct.pack('<I',0x08a7ad77), 'PB expected protocol build ID')

    # Preserve product-family/name and exact metadata layout. Distinguish test
    # revision in both copies so the boot-time equality check remains true.
    revision = b'D3-RC1\0'.ljust(32,b'\0')
    for metadata in (0x080001ac, 0x080980a4):
        patch(metadata+0x28, revision, b'D3\0'.ljust(32,b'\0'), 'explicit development revision')
    assert data[0x1ac:0x2f8] == data[0x980a4:0x981f0]
    # Old embedded PB is retained but no longer referenced by the programmer.
    assert data[0x8b670:0x97c80] == pb_original
    assert data[:0x1ac] == original[:0x1ac]
    dfu = make_dfu(bytes(data), template)
    # These pins also detect changed assembler or image-resampling behavior.
    expected = {MAIN_NAME: '7661a83958caf5cd62a477575a8ffe8a6be9d0153ef076b5d7bf2e5850df3a0e',
                DFU_NAME: 'c8088fafa8d224d203c023442f0157050800169ded67282e62088bc833b1bcbe',
                'powerboard.bin': 'ce94c00388cdf755d4c343d8eeab5e517096ae8a81974efa09f67d175d6eb000'}
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
    manifest = dict(schema=1, release='REV1', revision='D3-RC1',
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
