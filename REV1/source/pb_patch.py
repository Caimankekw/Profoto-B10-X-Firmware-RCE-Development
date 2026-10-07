"""Minimal recharge-selector PB patch builder, with strict original-byte guards.

No files or hardware are written by this module. The parent build owns nesting,
main-board protocol, DFU/checksums, version coordination, and artifact delivery.
Requires the Keystone assembler Python package.
"""
import hashlib
import struct
from keystone import Ks, KS_ARCH_ARM, KS_MODE_THUMB

BASE=0x08000000
CTX=0x100003f8
STATE=0x10000740
ORIGINAL_LENGTH=0xc610
ORIGINAL_SHA256='6f8778d89a4d10ddc13b7726ff76814643accd3b37ad9743eb192faebb6a74b6'

SELECTOR_SOURCE='''
ldr r1, =0x10000740
ldrb r1, [r1]
subs r1, #1
cmp r1, #1
bls chosen
ldrb.w r1, [r2, #0x89]
chosen:
b.w #0x08009154
.align 2
'''
# External conditional-wide jumps are deliberately avoided: Keystone 0.9.2
# assembled an incorrect absolute target in validation. Local labels are sound.
PARSER_SOURCE='''
movw r3, #0x1032
cmp r4, r3
bne original
cmp r5, #4
bne reject
ldrb r3, [r1, #3]
cmp r3, #2
bhi reject
adds r3, #1
cmp r3, #3
it eq
moveq r3, #0
ldr r2, =0x10000740
strb r3, [r2]
b.w #0x0800020e
original:
movw r3, #0x1031
b.w #0x080001f8
reject:
b.w #0x080009ca
.align 2
'''

def build_powerboard(source: bytes, version_id=None, cave_offset=0xc610):
    """Return (patched_image, manifest). version_id is optional 8-byte ASCII.

    Existing physical model and X state are never rewritten. New command 1032
    wire 0/1/2 selects NONX/X/AUTO; state stores 1/2/0. Startup zero = AUTO.
    Parameters change on the next original 09148 invocation; this handler only
    stores the selection and goes through the original ACK path.
    """
    if len(source)!=ORIGINAL_LENGTH or hashlib.sha256(source).hexdigest()!=ORIGINAL_SHA256:
        raise ValueError('PB patch only supports the exact extracted D3 powerboard payload')
    if cave_offset<ORIGINAL_LENGTH or cave_offset%4:
        raise ValueError('Cave must be aligned and outside the original PB payload')
    selector_address=BASE+cave_offset
    parser_address=selector_address+0x20
    ks=Ks(KS_ARCH_ARM,KS_MODE_THUMB)
    def asm(code,address):return bytes(ks.asm(code,address)[0])
    selector=asm(SELECTOR_SOURCE,selector_address)
    parser=asm(PARSER_SOURCE,parser_address)
    if len(selector)>0x20:raise ValueError('Selector overlaps parser')
    end=(parser_address-BASE+len(parser)+3)&~3
    if end>0x10000:raise ValueError('PB patch exceeds 64 KiB address window')
    image=bytearray(source+b'\xff'*(end-len(source)))
    changes=[]
    def patch(address,new,expected=None):
        off=address-BASE
        old=bytes(image[off:off+len(new)])
        if expected is not None and old!=expected:
            raise ValueError(f'Original-byte guard failed at {address:#x}')
        image[off:off+len(new)]=new
        changes.append(dict(address=hex(address),offset=hex(off),old=old.hex(),new=new.hex()))
    patch(0x08009150,asm(f'b.w #{selector_address:#x}',0x08009150),bytes.fromhex('92f88910'))
    patch(0x080001f4,asm(f'b.w #{parser_address:#x}',0x080001f4),bytes.fromhex('41f23103'))
    patch(0x0800acfc,struct.pack('<I',STATE+4),struct.pack('<I',STATE))
    patch(selector_address,selector)
    patch(parser_address,parser)
    if version_id is not None:
        if isinstance(version_id,str):version_id=version_id.encode('ascii')
        if len(version_id)!=8 or any(c<0x20 or c>0x7e for c in version_id):
            raise ValueError('PB version must be exactly 8 printable ASCII bytes')
        for address in [0x08000184,0x0800c358]:patch(address,version_id,b'08a7ad77')
    return bytes(image),dict(original_sha256=ORIGINAL_SHA256,
        sha256=hashlib.sha256(image).hexdigest(),original_length=len(source),length=len(image),
        selector_address=selector_address,selector_size=len(selector),parser_address=parser_address,
        parser_size=len(parser),state_address=STATE,state_mapping={'0':'AUTO','1':'NONX','2':'X'},
        wire_mapping={'0':'NONX','1':'X','2':'AUTO'},version_id=None if version_id is None else version_id.decode('ascii'),
        modifications=changes)
