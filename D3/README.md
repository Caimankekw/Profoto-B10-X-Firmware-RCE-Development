# B10 REV-D3 firmware reverse engineering

[English](README.md) | [简体中文](README.zh-CN.md)

This directory covers the original REV-D3 firmware: recovered code and analysis, plus tools for inspecting machine code and bitmaps on demand. Function names and pseudocode were reconstructed from the binary. **They are not the manufacturer's original C source, and the firmware has not been completely decompiled.**

Evidence levels: **confirmed** means that image bytes, instructions, actual call chains, or resource mappings can be checked directly; **inferred** means a physical purpose interpreted from control behavior. Register counts are not measurements of current, light output, color temperature, or recycle time.

## Firmware inputs and branches

The `main` branch contains reverse-engineered source, documentation, and inspection tools only. It does not include BIN/DFU firmware or development build inputs. The [REV1](https://github.com/Caimankekw/Profoto-B10-X-Firmware-RCE-Development/tree/REV1/D3/firmware) and [REV5](https://github.com/Caimankekw/Profoto-B10-X-Firmware-RCE-Development/tree/REV5/D3/firmware) branches include the same required D3 inputs under `D3/firmware/`.

To run the tools from a checkout of `main`, obtain those inputs from either development branch. For example, from the repository root:

```powershell
git fetch origin REV1
git restore --source=origin/REV1 --worktree -- D3/firmware/B10_REV_D3.bin D3/firmware/B10_REV_D3.dfu
python -m pip install capstone==5.0.9 Pillow==11.3.0
```

On a development branch, the inputs are already present; install that branch's root `requirements.txt` instead. The original firmware and its resources remain the property of their respective rights holders.

## Recovered code

These files are linear-disassembly excerpts from original D3 machine code, with recovered symbols/comments to aid reading. They do not contain development-version patches and are not complete functions or a buildable assembly project. `charge_state_machine.asm` and `pulse_builder.asm` end with a truncated Thumb-2 instruction shown as `.byte`; consult a full D3 disassembly when following those boundaries.

| File | Contents |
| --- | --- |
| [charge_state_machine.asm](source/charge_state_machine.asm) | Recharge state machine |
| [powerboard_parameter_builder.asm](source/powerboard_parameter_builder.asm) | Flash/discharge parameter and recipe construction |
| [powerboard_mode_parser.asm](source/powerboard_mode_parser.asm) | Power-board mode protocol parser |
| [pulse_builder.asm](source/pulse_builder.asm) | Ordinary discharge event construction |
| [pulse_executor.asm](source/pulse_executor.asm) | Flash-event and GPIO / HRTIM execution |

## Images and addresses

| Item | Original value |
| --- | --- |
| Main-controller BIN | `firmware/B10_REV_D3.bin`, 627,548 bytes (`0x9935C`) |
| Main-controller SHA-256 | `105de29fd444d22755e676c6474eb32f6f32e37ad333b8d232d49948e228b305` |
| Main-controller vectors | SP=`0x10010000`, Reset=`0x0802C759` (Thumb bit included) |
| Firmware metadata | B10 / D3, build `2023-06-07T14:29:32+02:00`, Git `1b07e2d4` |
| Embedded power board | Main BIN half-open interval `[0x8B670, 0x97C80)`, 50,704 bytes, identifier `08a7ad77` |
| Power-board SHA-256 | `6f8778d89a4d10ddc13b7726ff76814643accd3b37ad9743eb192faebb6a74b6` |
| Power-board vectors | SP=`0x10001000`, Reset=`0x0800AC85` (Thumb bit included) |
| DfuSe | `firmware/B10_REV_D3.dfu`, 627,857 bytes; one target and one element; payload equals the BIN |

Below, **M:** denotes the main controller and **P:** the power board. Each image is independently mapped at `0x08000000`. A P address corresponds to main BIN offset `0x8B670 + P address − 0x08000000`; it must not be located as a main-controller address. The power board's Thumb-2, VFP, HRTIM, and peripheral layout are consistent with the STM32F334 family; the exact chip suffix is unconfirmed.

## Main module index

| Module | Contents | Verifiable entry points |
| --- | --- | --- |
| Model identification | ADC hardware classification, OTP X field, model display | M:`08004DD0`, `08004CD0`, `08019A4E` |
| Flash configuration | Sending energy level, NORMAL/FREEZE, and synchronization configuration to the power board | M:`0800BC0C`, `08013360` |
| Ordinary discharge | Recipe lookup, event construction, GPIO/HRTIM execution | P:`080068D4` → `0800705C` → `08005EF4` |
| Recharging | High-voltage sampling, soft start, charging hysteresis, voltage-rise monitoring | P:`080092D4`; parameter selection `08009148` |
| Thermal control | Four NTC channels, recharge derating, overtemperature flags, cooling outputs | P:`080078C8`, `080071B8`, `080077E8` |
| Battery | Voltage filtering, charge-level hysteresis, undervoltage/overvoltage handling | P:`08004C4C` |
| Modeling light | On/off, brightness/color temperature, dual-color channels, load and thermal coordination | M:`0801B668`; P:`08007F6C` |
| Air / Bluetooth | Wireless packets, channels/groups, synchronization, app settings | M:`080065AC`, `08006A20`, `0800A830` |
| UI / sound | Input, display model, drawing, refresh, audible signals | M:`08017718`, `0801ADA0`, `0800F020`, `0801E494` |
| Storage / update | Configuration persistence, USB, logs, internal-module updates | M:`08012350`, `08014534`, `080148F0`, `08013C68` |

The main-controller tasks above have actual RTOS task-creation calls. Static bitmaps also include standby, auto-off, factory-reset, and service-test pages. A resource's presence does not mean every model or ordinary user can access that page. TTL, HSS, wireless subimages, and factory calibration are not fully recovered.

## Models and recharge control

**Confirmed: one D3 image supports four models.** The main controller reads the OTP X field, then samples ADC channel 10, requiring five consecutive classifications to agree.

| Main-controller model code | Model | Power-board base model |
| --- | --- | --- |
| `0x8C` | B10 | `0x8C` |
| `0x8D` | B10 Plus | `0x8D` |
| `0x8F` | B10X Plus | `0x8D`, with a separate X flag |
| `0x90` | B10X | `0x8C`, with a separate X flag |

Power-board context `ctx=0x100003F8`: `+0x64` is the base model; `+0x89` is the X flag. Main-controller X detection at M:`08004E08` → M:`0800C46C` sends command `0x1031`. P:`080001F4` receives it, sets the X flag, and reloads the thermal table.

Ordinary recharge parameters at P:`08009148` are shown below. `p=ctx+0x28` is the thermal-budget percentage.

```c
enhanced = (ctx.x == 1) && (ctx.ready_dim != 0 || ctx.light_on == 0);
// Plus: K/T/C = enhanced ? 310/380/20 : 273/343/20
// B10:  K/T/C = enhanced ? 230/300/20 : 210/280/20
// Unknown-model fallback: 50/280/180
TIM15_CCR1 = C;
TIM15_ARR = TIM15_CCR1 + (uint16_t)((K * p) / 100);
q = TIM2_CCR1;
if ((uint32_t)(q + T) > 71)
    TIM2_ARR = (uint32_t)(T - TIM2_CCR1);  // Original code reads CCR1 again.
else
    TIM2_ARR = 72;
```

`ready_dim` is the READY SIGNAL DIM setting (P:`ctx+0x45`); `light_on` is the modeling-light switch (`+0x44`). Thus X Plus falls back to `273/343/20` with the modeling light on and DIM off. It uses `310/380/20` only when the modeling light is off or DIM is on.

**Confirmed:** TIM15=`0x40014000`; it is not the flash-event timer TIM16. TIM2 and TIM15 both enable one-pulse mode and preload. The TIM2 update interrupt at P:`0800920C` also depends on PA15 input. The unsigned branch above cannot be simplified to `max(72, T−CCR1)`, and a larger ARR cannot be described as a higher PWM frequency. TIM2 `CCER=0x12` leaves CC1E disabled; reading CCR1 is not evidence of a proven current-capture feedback loop.

**Inferred:** the interlock between X parameters and the modeling light coordinates a shared supply load. The code does not prove that both generations have identical power hardware, and the K/T ratio cannot directly predict a measured recycle-speed improvement.

### High voltage, thermal control, and battery

P:`080092D4` is serviced at intervals of approximately 5 ms at the fastest; the timebase comes from a 72 MHz configuration and SysTick `LOAD=71999`. ADC2 channel 4 is converted as `raw×3/4095×199.44444`. Its processed value is `0.1×current converted sample + 0.9×previous raw converted sample`, **not a recursive IIR filter**.

| State | Recovered behavior |
| --- | --- |
| 0 / 1 | Disable recharge output and enter idle / idle |
| 2 | Converted battery millivolts must be `>11999`; use the shared soft start when high voltage is `<30`, otherwise load ordinary parameters |
| 4 | Main charging; stop and enter state 3 at high voltage `>500`; also check voltage-rise progress |
| 3 | Hold; restart charging at high voltage `<499` |
| 5 | Enter state 2 once a stored delay expires |

State names are interpretations; values and branches are directly verifiable. 500/499 are software-converted thresholds, with strong evidence that they represent capacitor high voltage. They are not equivalent to all trigger-permission or READY criteria. The voltage-rise monitoring window is `p<=1 ? 1000 : min(1000, floor(20000/p))` ms. Protection is entered if the voltage has increased by less than one software voltage unit after that window; this is not a fixed recycle time.

Four NTC readings are converted to degrees Celsius. Recharge uses the minimum allowed percentage across the four channels. The X path changes only thermal slot 1 (ADC1 channel 4): derating start/end move from `65/75°C` to `73/83°C`, and the charging-stop threshold moves from `80°C` to `88°C`. Related tables are P:`0800BE00` and `0800BE70`. Other channels can still impose an earlier limit. The physical sensor location is unknown; these thresholds must not be treated as ambient temperature or a whole-unit temperature rating.

Battery ADC1 channel 2 uses `raw×3/4095×6.17647` and `0.2×new + 0.8×previous filtered value`. `>18.0` enters protection; `<12.0` is an undervoltage candidate, with recovery at `>12.1`; undervoltage also needs stable confirmation. Battery ADC is not refreshed during recharge state 4 or for 512 ms after leaving that state, so this path does not monitor battery sag in real time while recharging.

## NORMAL / FREEZE discharge

Main-controller configuration `0x200019A4+0x25` is written to power-board `ctx+0x38` via command `0x0016`: 0 is NORMAL; nonzero is FREEZE. The ordinary chain is **mode/effective energy → ROM recipe → event compiler → executor**. There is not a separate independently coded algorithm for every power setting.

| Table | Plus (including X Plus) | Non-Plus | Record format |
| --- | --- | --- | --- |
| NORMAL | P:`0800B410` | P:`0800B8C0` | 100×12 bytes: initial segment a, tail length b, duty code d (third field read as u8) |
| FREEZE | P:`0800B0F0` | P:`0800B280` | 100×4 bytes: cutoff time T |

The index is `clamp(E,1,100)−1`. The nominal panel level is `E/10`, but runtime energy can first receive voltage or other compensation, so the panel setting is not always the direct ROM index. P:`080068D4` does not read the X flag on the ordinary lookup path; both Plus models therefore share the discharge tables.

```text
NORMAL: read (a,b,d), PWM width = floor(2357*d/256)
  b>0: action3 @ a switches to PWM; action5 @ a+b ends it; append action5 @ a+b+1
  b=0: action5 @ a ends it; append action5 @ a+1
FREEZE: read T, set tail length to 0; use the same event compiler to generate end events
```

Compiler P:`0800705C` writes 12-byte events (action@+0, time@+4, width@+8). The two arrays are `0x100002C8` (trigger) and `0x100002FC` (gate). Executor P:`08005EF4` controls PA8 GPIO/HRTIM.

The nominal TIM16 event-count unit is `7/72 µs≈0.097222 µs`; the executor polls for `CNT>event time` before acting. HRTIM has period 2357, compare start 96, and a final width clamp of 2261, giving a nominal carrier frequency of about 30.55 kHz. **a is not the entire initial optical pulse measured from ignition: PA8 is already high before TIM16 starts, with trigger/phase conditions preceding it.** These programmed times are not optical t0.1 values.

For example, the nominal Plus 5.0 NORMAL recipe is `(341,4250,114)`, and the FREEZE cutoff is 1152. NORMAL tail length is zero from 9.7 upward; at 10.0 both modes use cutoff 64500. Changing the initial segment, PWM tail length, and width changes current timing; the original table can be interpreted as a calibrated compromise between light output and spectrum. **No direct mapping from target Kelvin to waveform was found, and no spectral feedback loop was established. These integers alone cannot determine actual color temperature.**

Original diagnostic commands `0x1008/0x1009/0x100A` set the initial segment, tail length, and duty, then set override flag `0x100002A6`. The receiver does not clamp times. Changing mode does not clear the override; power-board reset is a confirmed clearing path. These commands are not an ordinary user interface for color-temperature adjustment.

## Storage, protocol, and USB updates

Main-controller runtime configuration begins at `0x200019A4`: model at `+0x3C`, mode at `+0x25`, DIM at `+0x31`, and modeling-light switch at `+0x0C`. StorageTask and factory-reset code exist. These RAM offsets must not be treated as an EEPROM file layout. OTP contains identity information and is separate from user configuration.

Confirmed main-controller → power-board commands: `0x0012` energy, `0x0016` mode, `0x0018` DIM, `0x001F` modeling light, and `0x1031` X initialization. The power-board protocol parser starts at P:`08000190`; the main-controller send entry is M:`0800AF38`.

The original Windows updater uses dfu-util and USB `0483:DF11`, reads OTP `0x1FFF7800:512` and main-controller firmware information `0x08000000:2048`, checks the product family, writes the image, and reads it back for verification. Product family `0x8C` does not independently distinguish Plus, X, and non-Plus. Main-controller M:`0800B614` uses embedded address `0x0808B670` and length `0xC610` to update the power board. Successful PC verification of the main controller is not an independent readback of the power board.

## Inspecting machine code on demand

After obtaining the inputs and dependencies described above, run from the repository root:

```powershell
python D3/disassemble.py --output-dir local_disassembly
python D3/disassemble.py --image powerboard --start 0x08009148 --end 0x0800920C --output-dir charge_slice
```

The script first checks the original BIN and embedded power-board hashes, then produces disassembly only in the selected output directory. It does not access USB. It performs linear decoding: **data and literal pools may also appear as instructions**. It does not automatically recover function boundaries or original C source. Main-controller output skips the embedded power board, which is decoded separately at its own correct load address. Existing files with the same names are not overwritten. The repository does not include full pre-generated disassembly, bitmaps, or per-level data exports.

## License / 许可

Original code and documentation are licensed under [AGPL-3.0-only](../LICENSE), by **Caimankekw**. Original firmware, recovered original machine code, and third-party components retain their respective rights and are not relicensed by this project; see [NOTICE](../NOTICE.md) for the scope. Custom Windows updater and installer build source is available in `windows/` on the corresponding development branch.
