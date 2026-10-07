"""RC5 packed recharge/ECO configuration helpers; no writes past cfg+67."""
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
import json
from keystone import Ks, KS_ARCH_ARM, KS_MODE_THUMB
CFG=0x200019A4
RECORD_ADDR=0x3E0
MAGIC=0x32484352
OLD_MAGIC=0x31484352
RECORD_VERSION=4
MARKER=0x53
INVALID=255

def imm(reg,value):
    return f'movw {reg}, #{value & 65535}\nmovt {reg}, #{value >> 16}'

def build(base=0x08099400):
    offsets={'rc_get':0,'rc_get_packed':0x40,'rc_is_plus':0xA0,'rc_normalize':0xD0,
        'rc_validate_record':0x180,'rc_load':0x280,'rc_save':0x380,'rc_send':0x580,
        'rc_commit':0x600,'rc_set':0x680,'eco_get':0x720,'eco_set':0x760,
        'flash_set_hook':0x840,'flash_cycle':0x8E0,'rc_boot_hook':0x980,
        'rc_restore_hook':0x9A0,'rc_sync_hook':0x9C0,'rc_factory_hook':0xA00,
        'flash_send':0xA40}
    sym={k:base+v for k,v in offsets.items()}
    asm={}
    asm['rc_get']=f'''
        push {{r4,lr}}
        bl {sym['rc_get_packed']}
        and r0,r0,#3
        pop {{r4,pc}}
    '''
    asm['rc_get_packed']=f'''
        push {{r4,lr}}
        {imm('r1',CFG)}
        ldrb r2,[r1,#0x66]
        cmp r2,#0x53
        bne fallback
        ldrb r0,[r1,#0x65]
        bl {sym['rc_normalize']}
        pop {{r4,pc}}
    fallback:
        bl 0x08004e08
        pop {{r4,pc}}
    '''
    asm['rc_is_plus']=f'''
        {imm('r1',CFG)}
        ldrb r1,[r1,#0x3c]
        cmp r1,#0x8d
        beq yes
        cmp r1,#0x8f
        beq yes
        movs r0,#0
        bx lr
    yes:
        movs r0,#1
        bx lr
    '''
    asm['rc_normalize']=f'''
        push {{r4,lr}}
        mov r4,r0
        cmp r4,#6
        bhi fallback
        and r1,r4,#3
        cmp r1,#3
        beq fallback
        cmp r4,#1
        bls accepted
        bl {sym['rc_is_plus']}
        cmp r0,#0
        beq fallback
    accepted:
        {imm('r1',CFG)}
        ldrb r1,[r1,#0x25]
        cmp r1,#0
        beq done
        bic r4,r4,#4
    done:
        mov r0,r4
        pop {{r4,pc}}
    fallback:
        bl 0x08004e08
        pop {{r4,pc}}
    '''
    asm['rc_validate_record']=f'''
        push {{r4,lr}}
        mov r4,r0
        ldr r0,[r4]
        {imm('r1',MAGIC)}
        cmp r0,r1
        beq version_rch2
        {imm('r1',OLD_MAGIC)}
        cmp r0,r1
        bne invalid
        ldrb r0,[r4,#4]
        cmp r0,#1
        bne invalid
        ldrb r0,[r4,#5]
        cmp r0,#1
        bhi invalid
        b fields
    version_rch2:
        ldrb r0,[r4,#4]
        cmp r0,#2
        beq packed_rch2
        cmp r0,#3
        beq packed_rch2
        cmp r0,#{RECORD_VERSION}
        bne invalid
    packed_rch2:
        ldrb r0,[r4,#5]
        cmp r0,#6
        bhi invalid
        and r1,r0,#3
        cmp r1,#3
        beq invalid
    fields:
        ldrb r1,[r4,#6]
        eor r0,r0,#255
        cmp r0,r1
        bne invalid
        ldrb r0,[r4,#7]
        cmp r0,#0
        bne invalid
        ldr r0,[r4,#8]
        cmp r0,#0
        bne invalid
        {imm('r0',0x7fffffff)}
        mov r1,r4
        movs r2,#12
        bl 0x08000708
        ldr r1,[r4,#12]
        cmp r0,r1
        bne invalid
        ldrb r0,[r4,#5]
        pop {{r4,pc}}
    invalid:
        movs r0,#255
        pop {{r4,pc}}
    '''
    asm['rc_load']=f'''
        push {{r4,r5,r6,lr}}
        sub sp,#16
        bl 0x08004e08
        mov r4,r0
        movw r0,#{RECORD_ADDR}
        mov r1,sp
        movs r2,#16
        bl 0x080162d4
        cmp r0,#1
        bne accept
        mov r0,sp
        bl {sym['rc_validate_record']}
        cmp r0,#255
        beq accept
        mov r5,r0
        mov r1,sp
        ldrb r1,[r1,#4]
        cmp r1,#2
        beq migrate_loaded
        cmp r1,#3
        bne normalize_loaded
    migrate_loaded:
        and r1,r5,#3
        cmp r1,#2
        bne normalize_loaded
        bl {sym['rc_is_plus']}
        cmp r0,#0
        beq normalize_loaded
        bic r5,r5,#3
        orr r5,r5,#1
    normalize_loaded:
        mov r0,r5
        bl {sym['rc_normalize']}
        mov r4,r0
    accept:
        {imm('r1',CFG)}
        strb r4,[r1,#0x65]
        movs r0,#0
        strb r0,[r1,#0x67]
        movs r0,#0x53
        strb r0,[r1,#0x66]
        mov r0,r4
        add sp,#16
        pop {{r4,r5,r6,pc}}
    '''
    asm['rc_save']=f'''
        push {{r4,r5,r6,lr}}
        sub sp,#32
        mov r4,r0
        bl {sym['rc_normalize']}
        cmp r0,r4
        bne failure
        {imm('r0',MAGIC)}
        str r0,[sp]
        movs r0,#0
        str r0,[sp,#4]
        str r0,[sp,#8]
        movs r0,#{RECORD_VERSION}
        mov r1,sp
        strb r0,[r1,#4]
        strb r4,[r1,#5]
        eor r0,r4,#255
        strb r0,[r1,#6]
        {imm('r0',0x7fffffff)}
        movs r2,#12
        bl 0x08000708
        str r0,[sp,#12]
        movw r0,#{RECORD_ADDR}
        mov r1,sp
        movs r2,#16
        bl 0x080161b0
        cmp r0,#1
        bne failure
        movs r0,#10
        bl 0x080214d4
        movw r0,#{RECORD_ADDR}
        add r1,sp,#16
        movs r2,#16
        bl 0x080162d4
        cmp r0,#1
        bne failure
        mov r1,sp
        add r2,sp,#16
        movs r3,#4
    compare:
        ldr r0,[r1],#4
        ldr r4,[r2],#4
        cmp r0,r4
        bne failure
        subs r3,r3,#1
        bne compare
        movs r0,#1
        b exit_save
    failure:
        movs r0,#0
    exit_save:
        add sp,#32
        pop {{r4,r5,r6,pc}}
    '''
    asm['rc_send']=f'''
        push {{r4,lr}}
        sub sp,#8
        bl {sym['rc_get_packed']}
        mov r1,sp
        strb r0,[r1,#2]
        movw r0,#0x1033
        strh r0,[r1]
        mov r0,sp
        movs r1,#3
        bl 0x0800af38
        add sp,#8
        pop {{r4,pc}}
    '''
    asm['rc_commit']=f'''
        push {{r4,lr}}
        mov r4,r0
        {imm('r1',CFG)}
        strb r4,[r1,#0x65]
        movs r0,#0x53
        strb r0,[r1,#0x66]
        bl 0x0800bb50
        cmp r0,#0
        beq save_set
        bl {sym['rc_send']}
    save_set:
        mov r0,r4
        bl {sym['rc_save']}
        {imm('r1',CFG)}
        eor r2,r0,#1
        strb r2,[r1,#0x67]
        pop {{r4,pc}}
    '''
    asm['rc_set']=f'''
        push {{r4,r5,r6,lr}}
        cmp r0,#2
        bhi invalid_set
        mov r4,r0
        cmp r4,#2
        bne valid
        bl {sym['rc_is_plus']}
        cmp r0,#0
        beq invalid_set
    valid:
        bl {sym['rc_get_packed']}
        and r0,r0,#4
        orr r0,r0,r4
        bl {sym['rc_commit']}
        pop {{r4,r5,r6,pc}}
    invalid_set:
        movs r0,#0
        pop {{r4,r5,r6,pc}}
    '''
    asm['eco_get']=f'''
        push {{r4,lr}}
        bl {sym['rc_get_packed']}
        ubfx r0,r0,#2,#1
        pop {{r4,pc}}
    '''
    asm['eco_set']=f'''
        push {{r4,r5,r6,lr}}
        cmp r0,#1
        bhi invalid_eco
        mov r4,r0
        bl {sym['rc_is_plus']}
        cmp r0,#0
        beq invalid_eco
        bl {sym['rc_get_packed']}
        mov r5,r0
        ubfx r1,r5,#2,#1
        cmp r1,r4
        beq unchanged
        bic r5,r5,#4
        cmp r4,#0
        beq commit
        orr r5,r5,#4
        {imm('r1',CFG)}
        movs r0,#0
        strb r0,[r1,#0x25]
        bl 0x0800bb50
        cmp r0,#0
        beq commit
        {imm('r0',0x0800af39)}
        movs r1,#0
        bl 0x08013360
    commit:
        mov r0,r5
        bl {sym['rc_commit']}
        pop {{r4,r5,r6,pc}}
    unchanged:
        {imm('r1',CFG)}
        ldrb r0,[r1,#0x67]
        eor r0,r0,#1
        pop {{r4,r5,r6,pc}}
    invalid_eco:
        movs r0,#0
        pop {{r4,r5,r6,pc}}
    '''
    asm['flash_set_hook']=f'''
        push {{r4,r5,r6,lr}}
        movs r4,#0
        cmp r0,#0
        beq normalized
        movs r4,#1
    normalized:
        bl {sym['rc_get_packed']}
        mov r5,r0
        {imm('r1',CFG)}
        ldrb r2,[r1,#0x66]
        cmp r2,#0x53
        bne write_native
        ldrb r2,[r1,#0x65]
        tst r2,#4
        beq write_native
        orr r5,r5,#4
    write_native:
        strb r4,[r1,#0x25]
        tst r5,#4
        beq done
        bic r0,r5,#4
        bl {sym['rc_commit']}
        bl {sym['flash_send']}
    done:
        mov r0,r4
        pop {{r4,r5,r6,pc}}
    '''
    asm['flash_cycle']=f'''
        push {{r4,lr}}
        bl {sym['rc_is_plus']}
        cmp r0,#0
        beq toggle
        bl {sym['eco_get']}
        cmp r0,#0
        beq maybe_freeze
        movs r0,#0
        bl {sym['eco_set']}
        b result
    maybe_freeze:
        bl 0x08004f34
        cmp r0,#0
        beq toggle
        movs r0,#1
        bl {sym['eco_set']}
        b result
    toggle:
        bl 0x08004f34
        eor r0,r0,#1
        bl {sym['flash_set_hook']}
        bl {sym['flash_send']}
    result:
        bl 0x08004f34
        pop {{r4,pc}}
    '''
    asm['rc_boot_hook']='''
        push {r4,lr}
        bl 0x08004dd0
        pop {r4,pc}
    '''
    asm['rc_restore_hook']=f'''
        push {{r4,lr}}
        bl {sym['rc_load']}
        bl 0x080130e0
        pop {{r4,pc}}
    '''
    asm['rc_sync_hook']=f'''
        push {{r4,lr}}
        bl {sym['rc_send']}
        {imm('r0',0x0800af39)}
        bl 0x080138f8
        pop {{r4,pc}}
    '''
    asm['rc_factory_hook']=f'''
        push {{r4,lr}}
        bl 0x0801ae30
        bl 0x08004e08
        bl {sym['rc_commit']}
        pop {{r4,pc}}
    '''
    asm['flash_send']=f'''
        push {{r4,lr}}
        bl 0x0800bb50
        cmp r0,#0
        beq done
        bl 0x08004f34
        mov r1,r0
        {imm('r0',0x0800af39)}
        bl 0x08013360
    done:
        pop {{r4,pc}}
    '''
    ks=Ks(KS_ARCH_ARM,KS_MODE_THUMB)
    chunks=[]
    slots=list(sym)
    end=base+0xA80
    for index,name in enumerate(slots):
        address=sym[name]
        machine=bytes(ks.asm(asm[name],address)[0])
        boundary=sym[slots[index+1]] if index+1<len(slots) else end
        assert address+len(machine)<=boundary,(name,len(machine),hex(boundary))
        chunks.append({'name':name,'address':address,'data':machine,'asm':asm[name]})
    patches=[]
    for address,name,original,mnemonic in [
        (0x0801AF74,'rc_boot_hook','e9f72cff','bl'),
        (0x0801B26A,'rc_restore_hook','f7f739ff','bl'),
        (0x0800BC9E,'rc_sync_hook','07f02bfe','bl'),
        (0x08019B70,'rc_factory_hook','01f05ef9','bl'),
        (0x08004F4C,'flash_set_hook','80b483b0','b.w')]:
        machine=bytes(ks.asm(f'{mnemonic} {sym[name]}',address)[0])
        assert len(machine)==4
        patches.append({'address':address,'data':machine,'original':bytes.fromhex(original),'name':name})
    return {'symbols':sym,'chunks':chunks,'patches':patches,'end':end}

if __name__=='__main__':
    result=build()
    binary=(ROOT / 'D3/firmware/B10_REV_D3.bin').read_bytes()
    for p in result['patches']:
        off=p['address']-0x08000000
        assert binary[off:off+4]==p['original'],p
    manifest={'symbols':result['symbols'],'end':result['end'],
        'chunks':[{k:(v.hex() if isinstance(v,bytes) else v) for k,v in c.items()} for c in result['chunks']],
        'patches':[{k:(v.hex() if isinstance(v,bytes) else v) for k,v in c.items()} for c in result['patches']]}
    out = Path(__file__).resolve().parent.parent / 'build'
    out.mkdir(parents=True, exist_ok=True)
    (out/'config_generated.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
    print(json.dumps({'symbols':result['symbols'],'lengths':{c['name']:len(c['data']) for c in result['chunks']},'end':hex(result['end'])},indent=2))
