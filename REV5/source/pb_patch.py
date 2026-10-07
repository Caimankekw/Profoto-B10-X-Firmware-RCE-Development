# SPDX-License-Identifier: AGPL-3.0-only
# Copyright (C) 2026 Caimankekw.
"""RC5 experimental BOOST policy for the exact B10 D3 power board.

No USB access or file writes. Uses the original B10 timer and HAL constants.
"""
import hashlib
import struct
from keystone import Ks, KS_ARCH_ARM, KS_MODE_THUMB

BASE = 0x08000000
CTX = 0x100003f8
STATE = 0x10000740
ORIGINAL_LENGTH = 0xc610
ORIGINAL_SHA256 = '6f8778d89a4d10ddc13b7726ff76814643accd3b37ad9743eb192faebb6a74b6'

# Four-byte battery snapshot at +8; deferred start/top-up flags at +12/+13.
# The remaining reserved bytes are untouched by this module.
RAM_END = STATE + 0x20
SLOTS = {
    'selector': (0xc610, 0x80), 'parser': (0xc690, 0x100),
    'cycle_begin': (0xc790, 0x100), 'effective_p': (0xc890, 0x200),
    'parameter_p': (0xca90, 0x80), 'monitor': (0xcb10, 0x100),
    'active_tick': (0xcc10, 0x180), 'stop_threshold': (0xcd90, 0x80),
    'restart_threshold': (0xce10, 0x80), 'target': (0xce90, 0x100),
    'policy': (0xcf90, 0x80),
    'comp_0': (0xd010, 0x80), 'comp_1': (0xd090, 0x80),
    'comp_2': (0xd110, 0x80), 'comp_3': (0xd190, 0x80),
    'hss_voltage_ref': (0xd210, 0x80), 'hss_tail_threshold': (0xd290, 0x80),
    'hold_restart': (0xd610, 0x100),
    'start_enable': (0xd710, 0x100),
    'boost_update': (0xd810, 0x200),
    'resume_paused': (0xda10, 0x200),
}


def sources(symbols):
    def a(name): return hex(symbols[name])
    out = {}
    out['policy'] = '''
        ldr r1, =0x10000740
        ldrb r2, [r1, #4]
        cmp r2, #0
        ite eq
        ldrbeq r0, [r1]
        ldrbne r0, [r1, #2]
        cmp r0, #3
        bne done
        ldr r1, =0x100003f8
        ldrb.w r1, [r1, #0x64]
        cmp r1, #0x8d
        it ne
        movne r0, #0
    done:
        bx lr
        .align 2
    '''
    # Caller has already pushed r4-r6. Original LR was not saved, so this hook
    # saves it itself before calling a helper; original r0/r2/r3 must survive.
    out['selector'] = f'''
        push {{r0, r2, r3, lr}}
        bl #{a('policy')}
        cmp r0, #0
        beq physical
        cmp r0, #3
        ite eq
        moveq r1, #1
        subne r1, r0, #1
        b chosen
    physical:
        ldr r1, =0x100003f8
        ldrb.w r1, [r1, #0x89]
    chosen:
        pop {{r0, r2, r3, lr}}
        b.w #0x08009154
        .align 2
    '''
    out['parser'] = '''
        movw r3, #0x1033
        cmp r4, r3
        beq packed
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
        movs r3, #0
        strb r3, [r2, #1]
        b accept
    packed:
        cmp r5, #4
        bne reject
        ldrb r3, [r1, #3]
        cmp r3, #6
        bhi reject
        and r2, r3, #3
        cmp r2, #3
        beq reject
        cmp r3, #1
        bls store
        ldr r2, =0x100003f8
        ldrb.w r2, [r2, #0x64]
        cmp r2, #0x8d
        bne reject
    store:
        and r2, r3, #3
        adds r2, #1
        ldr r0, =0x10000740
        strb r2, [r0]
        lsrs r3, r3, #2
        strb r3, [r0, #1]
    accept:
        b.w #0x0800020e
    original:
        movw r3, #0x1031
        b.w #0x080001f8
    reject:
        b.w #0x080009ca
        .align 2
    '''
    # Qualified charge start, after the unchanged battery >11999mV branch.
    # Explicitly preserve the floating-point working set around the injection.
    out['cycle_begin'] = '''
        push {r0-r3, r12, lr}
        vpush {d0-d1}
        ldr r0, =0x10000740
        ldrb r3, [r0, #3]
        ldrb r1, [r0]
        strb r1, [r0, #2]
        ldrb r1, [r0, #1]
        strb r1, [r0, #3]
        cmp r3, #0
        beq no_ready_change
        cmp r1, #0
        bne no_ready_change
        ldr r2, =0x48000818
        ldr r3, =0x00080000
        str r3, [r2]
    no_ready_change:
        movs r1, #1
        strb r1, [r0, #4]
        movs r1, #0
        strb r1, [r0, #6]
        strb r1, [r0, #12]
        strb r1, [r0, #13]
        vldr s0, [r6, #0x60]
        ldr r2, =0x42200000
        vmov s1, r2
        vcmpe.f32 s0, s1
        vmrs APSR_nzcv, fpscr
        it mi
        movmi r1, #1
        strb r1, [r0, #5]
        vldr s0, [r6, #0x5c]
        ldr r2, =0x447a0000
        vmov s1, r2
        vmul.f32 s0, s0, s1
        vcvt.u32.f32 s0, s0
        vmov r1, s0
        movw r2, #13000
        cmp r1, r2
        it lo
        movlo r1, r2
        movw r2, #17000
        cmp r1, r2
        it hi
        movhi r1, r2
        str r1, [r0, #8]
        movs r1, #0
        strb r1, [r0, #14]
        strb r1, [r0, #15]
        ldrb.w r1, [r6, #0x64]
        cmp r1, #0x8d
        bne qualification_done
        ldrb r1, [r0, #2]
        cmp r1, #3
        bne qualification_done
        ldr r1, [r6, #0x28]
        cmp r1, #100
        bne qualification_done
        ldrb.w r1, [r6, #0x44]
        cmp r1, #0
        bne qualification_done
        movs r1, #1
        strb r1, [r0, #14]
    qualification_done:
        vpop {d0-d1}
        pop {r0-r3, r12, lr}
        ldrd r2, r3, [r5]
        b.w #0x080094e6
        .align 2
    '''
    # Return voltage target as IEEE754 in r0; no float register changes.
    # ECO applies to native NORMAL and HSS; FREEZE keeps its original 500 V.
    out['target'] = '''
        ldr r1, =0x10000740
        ldrb r2, [r1, #4]
        cmp r2, #0
        ite eq
        ldrbeq r2, [r1, #1]
        ldrbne r2, [r1, #3]
        cmp r2, #0
        beq normal
        ldr r1, =0x100003f8
        ldrb.w r2, [r1, #0x64]
        cmp r2, #0x8d
        bne normal
        ldrb.w r2, [r1, #0x38]
        cmp r2, #0
        bne normal
        ldr r0, =0x43eb0000
        bx lr
    normal:
        ldr r0, =0x43fa0000
        bx lr
        .align 2
    '''
    # Percentage always obeys the original thermal controller. RC5 changes K/T
    # only at a qualified, original complete parameter-load call, never here.
    # Stop/READY are still based on actual 500/470 V, never an early-ready flag.
    out['effective_p'] = f'''
        push {{r4-r7, lr}}
        vpush {{d0-d1}}
        ldr r4, =0x100003f8
        ldr r5, =0x10000740
        ldr r6, [r4, #0x28]
        bl #{a('policy')}
        cmp r0, #3
        bne legacy
        bl #{a('boost_update')}
        bl #{a('target')}
        vmov s1, r0
        vldr s0, [r4, #0x60]
        vcmpe.f32 s0, s1
        vmrs APSR_nzcv, fpscr
        bge zero
        movs r7, #100
        b limit
    zero:
        movs r7, #0
    limit:
        cmp r6, r7
        it hi
        movhi r6, r7
    legacy:
        mov r0, r6
        strb r0, [r5, #7]
        vpop {{d0-d1}}
        pop {{r4-r7, pc}}
        .align 2
    '''
    out['parameter_p'] = f'''
        push {{r0-r3, r12, lr}}
        bl #{a('boost_update')}
        cmp r0, #0
        beq no_enhancement
        ldr r2, [r5]
        movw r0, #310
        cmp r2, r0
        bne no_enhancement
        movw r2, #375
        str r2, [r5]
        movw r4, #445
        ldr r0, =0x10000740
        movs r2, #1
        strb r2, [r0, #15]
    no_enhancement:
        bl #{a('effective_p')}
        mov r6, r0
        pop {{r0-r3, r12, lr}}
        ldr r2, [r5]
        b.w #0x08009178
        .align 2
    '''
    # Return whether the original 09148 load may choose 375/445. This helper
    # never raises K; runtime calls can only cancel the one-cycle eligibility
    # or restore the appropriate stock K before ARR is calculated. TIM2 and
    # EGR are never written, so an enhanced cycle retains T445 when derating.
    out['boost_update'] = f'''
        push {{r4-r7, lr}}
        vpush {{d0-d1}}
        ldr r4, =0x100003f8
        ldr r5, =0x10000740
        ldrb.w r0, [r4, #0x64]
        cmp r0, #0x8d
        bne unavailable
        ldrb r0, [r5, #4]
        cmp r0, #1
        bne unavailable
        ldrb r0, [r5, #2]
        cmp r0, #3
        bne unavailable
        ldrb r0, [r5, #14]
        cmp r0, #1
        bne stock
        ldr r0, [r4, #0x28]
        cmp r0, #100
        bne cancel
        ldrb.w r0, [r4, #0x44]
        cmp r0, #0
        bne cancel
        ldrb r0, [r5, #13]
        cmp r0, #0
        bne cancel
        bl #{a('target')}
        vmov s1, r0
        vmov.f32 s2, #10.0
        vsub.f32 s1, s1, s2
        vldr s0, [r4, #0x60]
        vcmpe.f32 s0, s1
        vmrs APSR_nzcv, fpscr
        bvs cancel
        bge cancel
        vmov.f32 s1, #30.0
        vcmpe.f32 s0, s1
        vmrs APSR_nzcv, fpscr
        bpl in_window
        ldrb r0, [r5, #15]
        cmp r0, #0
        bne cancel
        b stock
    in_window:
        movs r0, #1
        b finish
    cancel:
        movs r0, #0
        strb r0, [r5, #14]
    stock:
        movs r0, #0
        strb r0, [r5, #15]
        movw r6, #310
        ldrb.w r0, [r4, #0x44]
        cmp r0, #0
        beq restore_k
        ldrb.w r0, [r4, #0x45]
        cmp r0, #0
        bne restore_k
        movw r6, #273
    restore_k:
        ldr r7, =0x10000218
        ldr r0, [r7]
        cmp r0, r6
        beq unavailable
        str r6, [r7]
    unavailable:
        movs r0, #0
    finish:
        vpop {{d0-d1}}
        pop {{r4-r7, pc}}
        .align 2
    '''
    # State 4 wrapper runs after the existing ADC and all early stop interlocks.
    # It does not touch TIM2 period and leaves the original <30V soft-start intact.
    out['active_tick'] = f'''
        push {{r0-r3, r12, lr}}
        vpush {{d0-d1}}
        ldr r1, =0x10000740
        ldrb r1, [r1, #3]
        cmp r1, #0
        beq ready_checked
        bl #{a('target')}
        ldr r1, =0x43fa0000
        cmp r0, r1
        bne ready_checked
        vmov s1, r0
        ldr r0, =0x100003f8
        vldr s0, [r0, #0x60]
        vcmpe.f32 s0, s1
        vmrs APSR_nzcv, fpscr
        bge ready_checked
        ldr r0, =0x48000818
        ldr r1, =0x00080000
        str r1, [r0]
    ready_checked:
        bl #{a('policy')}
        cmp r0, #3
        bne done
        bl #{a('effective_p')}
        cmp r0, #0
        beq zero_power
        ldr r1, =0x10000740
        mrs r12, primask
        cpsid i
        ldr r3, =0x40014000
        ldr r2, =0x10000700
        ldrb r2, [r2]
        cmp r2, #0
        bne restore_irq
        ldr r2, =0x10000218
        ldr r2, [r2]
        mul r2, r2, r0
        movs r3, #100
        udiv r2, r2, r3
        ldrb r0, [r1, #13]
        cmp r0, #0
        beq budget_ready
        cmp r2, #160
        it hi
        movhi r2, #160
    budget_ready:
        uxth r2, r2
        ldr r3, =0x40014000
        ldr r0, [r3, #0x34]
        add r2, r2, r0
        str r2, [r3, #0x2c]
        b restore_irq
    zero_power:
        ldr r1, =0x10000740
        mrs r12, primask
        cpsid i
        ldr r3, =0x40000000
        ldr r0, [r3]
        bic r0, r0, #1
        str r0, [r3]
        ldr r0, [r3, #0x0c]
        bic r0, r0, #1
        str r0, [r3, #0x0c]
        ldr r3, =0x40014000
        ldr r0, [r3, #8]
        bic r0, r0, #7
        str r0, [r3, #8]
        movs r0, #1
        strb r0, [r1, #6]
    restore_irq:
        msr primask, r12
    done:
        vpop {{d0-d1}}
        pop {{r0-r3, r12, lr}}
        b.w #0x080093d8
        .align 2
    '''
    # Rebuild the small W calculation using the effective percentage, without
    # writing over the temperature controller's own ctx+28 output.
    out['monitor'] = f'''
        push {{r0, r2, r3, lr}}
        bl #{a('resume_paused')}
        bl #{a('policy')}
        cmp r0, #3
        bne legacy
        bl #{a('effective_p')}
        cmp r0, #1
        bls slow
        movw r1, #20000
        udiv r1, r1, r0
        movw r0, #1000
        cmp r1, r0
        it hi
        movhi r1, r0
        b finish
    slow:
        movw r1, #1000
    finish:
        pop {{r0, r2, r3, lr}}
        b.w #0x08009460
    legacy:
        pop {{r0, r2, r3, lr}}
        ldr r3, [r6, #0x28]
        cmp r3, #1
        b.w #0x0800943e
        .align 2
    '''
    # Called at 0943a, after this tick's stock soft-start ARR/CCR writes (or
    # its stock 30 V transition). Synchronize timer preloads only after TIM15
    # has naturally finished its OPM pulse. Never force-clear its CEN while
    # PWM2 may be high; otherwise leave the chain stopped until the next tick.
    out['resume_paused'] = f'''
        push {{r4-r7, lr}}
        ldr r4, =0x10000740
        ldr r0, =0x1000000c
        ldrb r0, [r0]
        cmp r0, #4
        bne done
        ldrb r0, [r4, #6]
        cmp r0, #1
        bne done
        bl #{a('policy')}
        cmp r0, #3
        bne done
        bl #{a('effective_p')}
        cmp r0, #0
        beq done
        mrs r7, primask
        cpsid i
        ldr r5, =0x40014000
        ldr r6, =0x40000000
        ldr r0, [r5]
        tst r0, #1
        bne restore_irq
        ldr r0, [r5, #8]
        tst r0, #7
        bne restore_irq
        ldr r0, [r6]
        tst r0, #1
        bne restore_irq
        ldr r0, [r6, #0x0c]
        tst r0, #1
        bne restore_irq
        ldrb r0, [r4, #12]
        cmp r0, #0
        beq sync_tim15
        ldr r0, [r6, #0x14]
        orr r0, r0, #1
        str r0, [r6, #0x14]
    sync_tim15:
        ldr r0, [r5, #0x14]
        orr r0, r0, #1
        str r0, [r5, #0x14]
        ldrb r0, [r4, #12]
        cmp r0, #0
        beq enable_chain
        ldr r1, =0x48000418
        movw r0, #0x8000
        str r0, [r1]
    enable_chain:
        ldr r0, [r5, #8]
        bic r0, r0, #7
        orr r0, r0, #6
        str r0, [r5, #8]
        ldr r0, [r6, #0x0c]
        orr r0, r0, #1
        str r0, [r6, #0x0c]
        ldr r0, [r6]
        orr r0, r0, #1
        str r0, [r6]
        movs r0, #0
        strb r0, [r4, #6]
        strb r0, [r4, #12]
    restore_irq:
        msr primask, r7
    done:
        pop {{r4-r7, pc}}
        .align 2
    '''
    out['stop_threshold'] = f'''
        push {{r0-r3, r12, lr}}
        bl #{a('target')}
        vmov s15, r0
        ldr r1, =0x43eb0000
        cmp r0, r1
        beq adapted
        bl #{a('policy')}
        cmp r0, #3
        beq adapted
        pop {{r0-r3, r12, lr}}
        b.w #0x080093e0
    adapted:
        vcmpe.f32 s14, s15
        vmrs APSR_nzcv, fpscr
        bge stop
        pop {{r0-r3, r12, lr}}
        b.w #0x080093ec
    stop:
        pop {{r0-r3, r12, lr}}
        b.w #0x0800966c
        .align 2
    '''
    out['restart_threshold'] = f'''
        push {{r0-r3, r12, lr}}
        bl #{a('target')}
        ldr r1, =0x43eb0000
        cmp r0, r1
        beq eco
        bl #{a('policy')}
        cmp r0, #3
        beq adapted
        ldr r0, =0x43f98000
        vmov s15, r0
        pop {{r0-r3, r12, lr}}
        b.w #0x080094a6
    adapted:
        ldr r0, =0x43f98000
        b finish
    eco:
        ldr r0, =0x43ea8000
    finish:
        vmov s15, r0
        vcmpe.f32 s14, s15
        vmrs APSR_nzcv, fpscr
        bvs hold
        blt restart
    hold:
        pop {{r0-r3, r12, lr}}
        b.w #0x08009302
    restart:
        pop {{r0-r3, r12, lr}}
        b.w #0x080094b2
        .align 2
    '''
    # A NORMAL->FREEZE target increase can begin from state3 rather than state2.
    # Drop READY before enabling the old top-up path; retain first-ready latch.
    # Stock top-up branches directly into 0956e and bypasses start_enable, so
    # BOOST must enforce its zero budget here as well. Deferred initial setup
    # is distinct from an already initialized top-up and retains its flag.
    out['hold_restart'] = f'''
        push {{r0-r3, r12, lr}}
        ldr r1, =0x10000740
        ldrb r1, [r1, #3]
        cmp r1, #0
        beq check_budget
        bl #{a('target')}
        ldr r1, =0x43fa0000
        cmp r0, r1
        bne check_budget
        ldr r0, =0x48000818
        ldr r1, =0x00080000
        str r1, [r0]
    check_budget:
        bl #{a('policy')}
        cmp r0, #3
        bne done
        ldr r1, =0x10000740
        movs r0, #1
        strb r0, [r1, #13]
        bl #{a('effective_p')}
        cmp r0, #0
        beq zero_budget
        ldr r2, =0x10000218
        ldr r2, [r2]
        mul r2, r2, r0
        movs r3, #100
        udiv r2, r2, r3
        cmp r2, #160
        it hi
        movhi r2, #160
        uxth r2, r2
        ldr r3, =0x40014000
        ldr r0, [r3, #0x34]
        add r2, r2, r0
        mrs r12, primask
        cpsid i
        str r2, [r3, #0x2c]
        msr primask, r12
    zero_budget:
        mrs r12, primask
        cpsid i
        ldr r3, =0x40000000
        ldr r0, [r3]
        bic r0, r0, #1
        str r0, [r3]
        ldr r0, [r3, #0x0c]
        bic r0, r0, #1
        str r0, [r3, #0x0c]
        ldr r3, =0x40014000
        ldr r0, [r3, #8]
        bic r0, r0, #7
        str r0, [r3, #8]
        ldr r1, =0x10000740
        movs r0, #1
        strb r0, [r1, #6]
        movs r0, #4
        strb r0, [r7]
        msr primask, r12
        pop {{r0-r3, r12, lr}}
        str r2, [r4, #8]
        b.w #0x08009302
    done:
        pop {{r0-r3, r12, lr}}
        ldr r0, =0x40014000
        str r2, [r4, #8]
        b.w #0x080094bc
        .align 2
    '''
    # A zero request must never run the stock unconditional enable sequence.
    # Leave state4 paused; its ordinary stop/progress/interlock logic still runs.
    out['start_enable'] = f'''
        push {{r0-r3, r12, lr}}
        bl #{a('policy')}
        cmp r0, #3
        bne enable
        bl #{a('effective_p')}
        cmp r0, #0
        bne enable
        mrs r12, primask
        cpsid i
        ldr r3, =0x40000000
        ldr r0, [r3]
        bic r0, r0, #1
        str r0, [r3]
        ldr r0, [r3, #0x0c]
        bic r0, r0, #1
        str r0, [r3, #0x0c]
        ldr r3, =0x40014000
        ldr r0, [r3, #8]
        bic r0, r0, #7
        str r0, [r3, #8]
        ldr r3, =0x10000740
        movs r0, #1
        strb r0, [r3, #6]
        strb r0, [r3, #12]
        movs r0, #4
        strb r0, [r7]
        msr primask, r12
        pop {{r0-r3, r12, lr}}
        b.w #0x08009302
    enable:
        pop {{r0-r3, r12, lr}}
        mov.w r0, #0x40000000
        b.w #0x08009554
        .align 2
    '''
    for name, end in zip(('comp_0', 'comp_1', 'comp_2', 'comp_3'),
                         (0x080024f2, 0x08006458, 0x08006e3e, 0x08006e74)):
        out[name] = f'''
            push {{r0-r3, r12, lr}}
            mrs r0, apsr
            push {{r0, r4}}
            bl #{a('target')}
            vmov s15, r0
            pop {{r0, r4}}
            msr APSR_nzcvq, r0
            pop {{r0-r3, r12, lr}}
            b.w #{end:#x}
            .align 2
        '''
    return out


def build_powerboard(source, version_id=None, cave_offset=0xc610):
    if len(source) != ORIGINAL_LENGTH or hashlib.sha256(source).hexdigest() != ORIGINAL_SHA256:
        raise ValueError('RC5 only supports the exact original D3 powerboard')
    if cave_offset != 0xc610:
        raise ValueError('RC5 fixed guarded layout requires cave_offset=0xc610')
    symbols = {name: BASE + slot for name, (slot, _) in SLOTS.items()}
    ks = Ks(KS_ARCH_ARM, KS_MODE_THUMB)
    def asm(code, addr): return bytes(ks.asm('.cpu cortex-m4\n.fpu fpv4-sp-d16\n'+code, addr)[0])
    source_blocks = sources(symbols)
    # ECO guards are owned separately; absence must fail closed for the build.
    from eco_guard import build_guard_sources
    guard_sources, guard_hooks, extra_symbols = build_guard_sources(symbols, STATE)
    symbols.update(extra_symbols)
    source_blocks.update(guard_sources)
    chunks = []
    for name, code in source_blocks.items():
        address = symbols[name]
        try:
            raw = asm(code, address)
        except Exception as exc:
            raise ValueError(f'Cannot assemble {name}: {exc}') from exc
        maximum = SLOTS.get(name, (0, 0x200))[1]
        if len(raw) > maximum:
            raise ValueError(f'{name}: {len(raw)} bytes exceeds slot {maximum}')
        chunks.append(dict(name=name, address=address, bytes=raw))
    end = (max(c['address']-BASE+len(c['bytes']) for c in chunks)+3) & ~3
    if end > 0x10000:
        raise ValueError('PB exceeds 64 KiB')
    image = bytearray(source + b'\xff'*(end-len(source)))
    modifications = []
    def patch(address, new, old=None, kind='hook'):
        off = address-BASE
        previous = bytes(image[off:off+len(new)])
        if old is not None and previous != old:
            raise ValueError(f'Original-byte guard mismatch at {address:#x}')
        image[off:off+len(new)] = new
        modifications.append(dict(address=hex(address), offset=hex(off), old=previous.hex(), new=new.hex(), kind=kind))
    hooks = [
        (0x08009150, 'selector', '92f88910'),
        (0x080001f4, 'parser', '41f23103'),
        (0x080094e2, 'cycle_begin', 'd5e90023'),
        (0x08009174, 'parameter_p', '866a2a68'),
        (0x0800943a, 'monitor', 'b36a012b'),
        (0x080093dc, 'stop_threshold', 'dfed8e7a'),
        (0x080094a2, 'restart_threshold', 'dfed617a'),
        (0x080094b8, 'hold_restart', '5c48a260'),
        (0x08009550, 'start_enable', '4ff08040'),
        (0x080024ee, 'comp_0', 'dfed367a'),
        (0x08006454, 'comp_1', 'dfed0b7a'),
        (0x08006e3a, 'comp_2', 'dfed387a'),
        (0x08006e70, 'comp_3', 'dfed2a7a'),
    ]
    hooks.extend(guard_hooks)
    for addr, name, old in hooks:
        patch(addr, asm(f'b.w #{symbols[name]:#x}', addr), bytes.fromhex(old))
    patch(0x080093d0, struct.pack('<I', symbols['active_tick']|1), bytes.fromhex('d9930008'), 'dispatch')
    patch(0x0800acfc, struct.pack('<I', RAM_END), struct.pack('<I', STATE), 'bss')
    for chunk in chunks:
        patch(chunk['address'], chunk['bytes'], b'\xff'*len(chunk['bytes']), 'code')
    if version_id is not None:
        if isinstance(version_id, str): version_id = version_id.encode('ascii')
        if len(version_id) != 8 or any(c<0x20 or c>0x7e for c in version_id):
            raise ValueError('version_id must be 8 printable ASCII bytes')
        for address in (0x08000184, 0x0800c358):
            patch(address, version_id, b'08a7ad77', 'version')
    manifest = dict(original_sha256=ORIGINAL_SHA256, sha256=hashlib.sha256(image).hexdigest(),
        original_length=len(source), length=len(image), version_id=None if version_id is None else version_id.decode('ascii'),
        state_address=STATE, ram_end=RAM_END, bss_end=RAM_END,
        ram_state=dict(start=STATE, end=RAM_END, requested_selector=STATE,
            requested_eco=STATE+1, active_selector=STATE+2, active_eco=STATE+3,
            active_valid=STATE+4, initial_low=STATE+5, zero_paused=STATE+6,
            effective_percent=STATE+7, startup_battery_mv=STATE+8,
            startup_pending=STATE+12, topup_active=STATE+13,
            boost_allowed=STATE+14, boost_engaged=STATE+15), symbols=symbols,
        selector_address=symbols['selector'], parser_address=symbols['parser'],
        selector_size=next(len(c['bytes']) for c in chunks if c['name']=='selector'),
        parser_size=next(len(c['bytes']) for c in chunks if c['name']=='parser'),
        state_mapping={'0':'AUTO', '1':'NONX', '2':'X', '3':'BOOST'},
        boost_strategy=dict(
            revision=5, experimental=True, hardware_measured=False,
            guaranteed_recharge_improvement_percent=None,
            requested_time_reduction_percent_vs_original_x=20,
            target_recharge_seconds_from_2p2_baseline=1.76,
            model_only=dict(formula='(K*K/T)/(310*310/380)',
                proxy_ratio=(375*375/445)/(310*310/380),
                proxy_time_seconds=2.2/((375*375/445)/(310*310/380)),
                measured=False,
                limitations='Not a measured current, power or recharge-time relationship; soft start, tail, battery and losses are excluded.'),
            purpose='Conditional enhanced bulk recharge, conservative latched retirement and stopped-timer preload synchronization.',
            model_family=0x8d, profile_selector=3,
            stock_plus_x=dict(K=310,T=380,C=20),
            enhanced_plus=dict(K=375,T=445,C=20),
            arithmetic='T=K+70; original two-read unsigned TIM2 capture arithmetic is unchanged.',
            entry='Only original full parameter load 0x08009148 / guarded hook 0x08009174.',
            qualification=dict(active_valid=1,active_selector=3,cycle_allowed=1,
                original_selected_K=310,thermal_exact=100,led_request_exact=0,
                topup_active=0,voltage_min_inclusive=30,voltage_max_exclusive='target-10',
                finite_voltage=True,extra_battery_voltage_gate=False),
            target_volts=dict(normal=500,eco=470),tail_margin_volts=10,
            retirement=dict(latched_until_next_qualified_cycle=True,
                causes=['thermal!=100','LED request!=0','Vcap>=target-10','Vcap is NaN',
                        'topup','Vcap<30 after previously engaged'],
                restore_K='273 when LED on and DIM off, else 310; before computing ARR.',
                tim2_runtime_reload=False,retain_enhanced_T_until_next_full_parameter_load=True,
                exact_stock_x_after_retirement=False),
            soft_start='Original <30 V formula preserved; first 30 V transition can qualify despite soft flag still set.',
            maintenance=dict(restart_strictly_below='target-1',increment_cap=160,
                deferred_one_service=True),
            resume_preload_sync=dict(site='monitor at 0x0800943a after original soft parameter update',
                guards=['state4','zero_paused','positive effective percent','TIM15 CEN=0',
                        'TIM15 SMS=0','TIM2 CEN=0','TIM2 UIE=0'],
                normal_resume='TIM15 UG only',initial_deferred='TIM2 UG, TIM15 UG, PB15',
                active_pulse_handling='Wait for natural OPM completion; never force-clear TIM15 CEN.',
                asynchronous_external_triggers_fully_modeled=False),
            unchanged=['NON-X','X','250 Ws drive','ADC','physical thermal limits','fault interlocks',
                       'stop and READY','normal flash curves','HSS executor']),
        wire_mapping={'1032': {'0':'NONX','1':'X','2':'AUTO'},
                      '1033':'bits0..1: NONX=0/X=1/BOOST=2; bit2: ECO'},
        chunks=[dict(name=c['name'], address=c['address'], size=len(c['bytes'])) for c in chunks],
        hooks=[dict(address=addr, name=name, expected=old) for addr,name,old in hooks], modifications=modifications)
    return bytes(image), manifest
