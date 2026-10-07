# Experimental Firmware Disclaimer and Risk Notice

[English](DISCLAIMER.md) | [简体中文](DISCLAIMER.zh-CN.md)

Developer: **Caimankekw**  
Applicable versions: **REV1 (D3-RC1), REV5 (RC5), and their accompanying update tools, Windows installers, and development materials**  
Document date: 7 October 2026

**This project provides unofficial, experimental custom firmware. Flashing and using it may cause a device to become unable to start, hardware damage, data loss, and other losses. Abnormal charging, discharging, or battery behavior may also pose risks to personal safety and property. Decide whether to use it only after understanding its scope, update procedure, and recovery requirements.**

## 1. Project status and relationship with the manufacturer

The custom modifications and development tools in this project are provided by Caimankekw. They are not official Profoto firmware releases and do not imply Profoto certification, authorization, endorsement, official signing, or a quality guarantee. Reusing the original updater interface, file formats, runtime libraries, or resources does not change the project's unofficial, experimental status.

Rights in Profoto and related product names, trademarks, original firmware, and third-party components belong to their respective rights holders. Neither this notice nor the project's open-source license grants additional rights in third-party intellectual property or additional redistribution rights.

## 2. Scope and verification limits

Refer to the README and Release notes for the selected version, and check the device model, hardware requirements, and firmware version. Successful USB identification, completed writing, or a normally displayed menu does not mean compatibility has been verified across all hardware batches and usage scenarios. The 250 Ws and 500 Ws models must not be treated as having the same hardware specifications.

REV1 provides NON-X / X recharge-policy selection. REV5 adds BOOST, ECO, and related HSS adaptations; BOOST / ECO are limited to the 500 Ws Plus models identified in its documentation. These features must not be interpreted as converting a device into another model or obtaining that model's rated performance.

Rebuilding from source, hashes, CRCs, resource checks, flash readback, or limited hardware testing establish results only within the scope of each check. They do not constitute whole-device safety certification, proof of long-term reliability, or complete optical calibration. Successful readback of the main-controller image does not establish that the internal power-board update and operation of the complete device have also been verified.

## 3. Flashing, recovery, and data risks

An interrupted flash, device or driver differences, abnormal power supply, version mismatches, and software defects may cause startup failure, update failure, corrupted settings or other data, and may require professional repair or component replacement, or leave the device unrecoverable.

The supplied Windows updater does not automatically provide a complete pre-flash backup of the device, nor does it guarantee one-click recovery after a failure. Before flashing, record important settings and understand recovery methods appropriate for the target device. When the internal power board is updated on the first startup, maintain power as instructed. Reverting to original manufacturer firmware does not guarantee restoration of every original state and cannot undo hardware damage that has already occurred.

## 4. Recharge and flash-performance risks

Switching between NON-X / X policies and using enhanced BOOST recharging may change the load and temperature rise of the battery, charging circuit, and power components. Retaining existing protection logic does not establish electrical margin, component service life, or effective protection under every fault condition when operating with enhanced settings. Abnormal conditions may cause overheating or component or battery damage; severe cases may present hazards such as fire, burns, or electric shock.

Light output, color temperature, flash duration, and exposure uniformity in ECO, NORMAL, FREEZE, and HSS may vary with hardware, battery, temperature, triggering method, and shooting conditions. ECO's 470 V value is a software target, not a guarantee of actual voltage or residual stored energy at any given moment. The ECO name also does not indicate completed safety certification.

BOOST's “20% reduction in recycle time” is a development target, not a commitment to minimum performance, performance on every flash, or sustained continuous operation. The level shown on the home screen is a setting state; it cannot by itself establish that a particular recharge cycle is using enhanced parameters. Examples, comparisons, or feedback from individual devices do not guarantee the same results on other devices.

## 5. Recommendations for use and handling abnormal behavior

Begin with limited testing in a controlled environment. Do not rely on an insufficiently verified device as the sole provision for a critical shoot, and avoid unattended testing or continuous high-load testing. Follow the original device's environmental, cooling, battery, and operating requirements; the availability of enhanced options in this project is not a reason to disregard the device's rated operating conditions.

If abnormal heat, odors, sounds, repeated errors, abnormal flashes, or battery behavior occur, stop triggering and using the device. Follow the device's instructions to handle the situation while prioritizing personal safety, and contact qualified repair personnel when necessary. Do not disassemble the device or touch internal high-voltage circuitry to investigate a firmware problem. Switching off the device, disconnecting USB, or removing the battery does not establish that internal capacitors have safely discharged.

The above information is a risk notice and operating advice. It does not impose additional restrictions on rights granted by the open-source license, nor is it a complete repair or safety procedure.

## 6. Warranties, support, and limitation of liability

**To the maximum extent permitted by applicable law, and unless expressly committed otherwise in writing, this project is provided “as is,” without express or implied warranties, including warranties of merchantability, fitness for a particular purpose, freedom from defects, compatibility, reliability, performance, or recoverability.**

Within the scope described above, the developer and others lawfully involved in modifying or providing this project are not liable for losses arising from its use or inability to use it, including damage to equipment or other property, repair or replacement costs, lost data or settings, failed shoots, business interruption, lost revenue or profits, and other direct, indirect, incidental, or consequential losses. This does not exclude liability required by applicable law or otherwise assumed by written agreement.

Unless required by law or otherwise agreed in writing, publishing code, providing downloads, answering questions, or publishing test results does not constitute a commitment to ongoing maintenance, fixes within a specified time, remote device recovery, refunds, or compensation. Using third-party firmware may affect manufacturer warranty or repair handling. The actual position depends on the original warranty terms, the cause of the fault, and applicable law; this notice alone must not be taken to mean that a warranty is necessarily void.

## 7. Preservation of statutory rights

**This notice does not exclude, limit, or waive any warranty, liability, or user right that applicable law does not permit to be excluded, limited, or waived. This includes, where applicable, non-excludable consumer rights and liability for personal injury, intentional misconduct, gross negligence, or other matters for which liability cannot lawfully be excluded.**

Where a provision cannot lawfully apply, applicable law prevails. Downloading, installing, clicking to continue, or using this project must not be interpreted as a waiver of rights that cannot lawfully be waived, nor does it mean the developer can exclude all liability.

## 8. Relationship with the open-source license

Caimankekw's original development code and documentation are licensed under **AGPL-3.0-only**. See [LICENSE](LICENSE) for the complete terms and [NOTICE.md](NOTICE.md) for the scope of original manufacturer and third-party materials. Sections 15–17 of the AGPL set out its warranty disclaimer and limitation-of-liability provisions; see also the [standard AGPL-3.0-only text](https://spdx.org/licenses/AGPL-3.0-only.html).

This notice supplements the project-specific risk information. It does not modify, replace, or reduce the rights granted by the AGPL, and does not add license restrictions such as a prohibition on commercial use. The applicable LICENSE governs open-source licensing matters. Mandatory provisions of applicable law remain in force in all cases.
