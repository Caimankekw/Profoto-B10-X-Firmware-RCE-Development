# SPDX-License-Identifier: AGPL-3.0-only
# Copyright (C) 2026 Caimankekw.
"""B10 RC5 target-relative HSS hooks.

Normal and HSS remain at the selected ECO voltage. ADC scaling, PWM bounds, feedback, timing
and absolute low-voltage checks remain original. ECO never writes the stock
persisted HSS auto-calibration. No files or hardware are accessed here.
"""

HOOKS = (
    (0x080058CC, 'hss_voltage_ref', '9fed9c8a'),
    (0x08005A94, 'hss_tail_threshold', 'dfed357a'),
    (0x08005E22, 'hss_calibration_guard', '0eaa0423'),
)


def build_guard_sources(symbols, state=0x10000740):
    """Return (assembly_sources, hooks, additional_symbols).

    symbols['target'] returns float32 bits for exactly 470 or 500 in r0,
    clobbers r0-r3/APSR only. VLDR hooks preserve every register except the
    destination s16/s15. The calibration hook skips ECO self-learning and
    preserves original registers on the 500 V path. No new RAM is required.
    """
    extra = {'hss_voltage_ref': symbols.get('hss_voltage_ref', 0x0800D210),
             'hss_tail_threshold': symbols.get('hss_tail_threshold', 0x0800D290),
             'hss_calibration_guard': symbols.get('hss_calibration_guard', 0x0800D310)}
    target = symbols['target']

    def body(dest, resume, subtract_six=False, actual_entry_voltage=False):
        adjust = 'sub.w r0, r0, #0x30000' if subtract_six else ''
        move = f'vmov {dest}, r0'
        if actual_entry_voltage:
            move = '''
                ldr r1, =0x43eb0000
                cmp r0, r1
                beq actual
                vmov s16, r0
                b moved
            actual:
                vmov.f32 s16, s19
            moved:
            '''
        # Both targets have float32 exponent 8; six volts is exactly 0x30000
        # adjacent representations, yielding 464.0 or 494.0 without rounding.
        return f'''
            push.w {{r0-r3, r12, lr}}
            mrs r3, APSR
            push {{r2, r3}}
            bl #0x{target:08x}
            {adjust}
            {move}
            pop {{r2, r3}}
            msr APSR_nzcvq, r3
            pop.w {{r0-r3, r12, lr}}
            b.w #0x{resume:08x}
            .align 2
        '''

    sources = {
        'hss_voltage_ref': body('s16', 0x080058D0, actual_entry_voltage=True),
        'hss_tail_threshold': body('s15', 0x08005A98, True),
        'hss_calibration_guard': f'''
            push.w {{r0-r3, r12, lr}}
            mrs r3, APSR
            push {{r2, r3}}
            bl #0x{target:08x}
            ldr r1, =0x43eb0000
            cmp r0, r1
            beq eco
            pop {{r2, r3}}
            msr APSR_nzcvq, r3
            pop.w {{r0-r3, r12, lr}}
            add r2, sp, #0x38
            movs r3, #4
            b.w #0x08005e26
        eco:
            pop {{r2, r3}}
            msr APSR_nzcvq, r3
            pop.w {{r0-r3, r12, lr}}
            b.w #0x08005b1a
            .align 2
        ''',
    }
    return sources, list(HOOKS), extra
