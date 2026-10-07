; SPDX-License-Identifier: AGPL-3.0-only
; Copyright 2026 Caimankekw
Unicode true
!include "MUI2.nsh"
Name "Profoto B10 REV5 Custom Firmware Updater"
OutFile "${OUTPUT_EXE}"
InstallDir "$LOCALAPPDATA\Profoto-B10-Custom\REV5"
RequestExecutionLevel user
SetCompressor /SOLID lzma
SetCompressorDictSize 32
CRCCheck on
BrandingText "Custom firmware by Caimankekw - not an official Profoto release"
VIProductVersion "5.0.0.0"
VIAddVersionKey /LANG=1033 "ProductName" "Profoto B10 REV5 Custom Firmware Updater"
VIAddVersionKey /LANG=1033 "CompanyName" "Caimankekw"
VIAddVersionKey /LANG=1033 "FileDescription" "Custom experimental firmware package; not an official release"
VIAddVersionKey /LANG=1033 "FileVersion" "5.0.0.0"
VIAddVersionKey /LANG=1033 "LegalCopyright" "Custom firmware development and packaging by Caimankekw; original components retain their notices"
!define MUI_WELCOMEPAGE_TITLE "REV5 custom firmware updater"
!define MUI_WELCOMEPAGE_TEXT "Developer: Caimankekw.$\r$\nThis is experimental custom firmware, not an official Profoto release.$\r$\n$\r$\nThis wizard extracts the complete updater to your user folder. It does not install drivers or flash a device automatically.$\r$\n$\r$\nRead README.md or README.zh-CN.md in the extracted folder before updating."
!define MUI_FINISHPAGE_RUN
!define MUI_FINISHPAGE_RUN_FUNCTION "LaunchUpdater"
!define MUI_FINISHPAGE_RUN_TEXT "Open REV5 custom firmware updater"
!define MUI_FINISHPAGE_TEXT "Developer: Caimankekw.$\r$\nExtraction is complete. Read the included English or Chinese README, then follow the updater's instructions. Updating firmware requires your explicit click in the updater."
!insertmacro MUI_PAGE_WELCOME
!define MUI_LICENSEPAGE_TEXT_TOP "AGPL-3.0-only covers Caimankekw's original custom code. Vendor and third-party components keep their original terms. Scope: NOTICE.md."
!define MUI_LICENSEPAGE_TEXT_BOTTOM "Read the license for the custom code. NOTICE.md contains the bilingual scope and source links."
!define MUI_LICENSEPAGE_BUTTON "Continue"
!insertmacro MUI_PAGE_LICENSE "${PACKAGE_DIR}\LICENSE"
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH
!insertmacro MUI_LANGUAGE "English"
!insertmacro MUI_LANGUAGE "SimpChinese"
Function .onInit
  !insertmacro MUI_LANGDLL_DISPLAY
FunctionEnd
Section "Extract updater"
  SetOutPath "$INSTDIR"
  File /r "${PACKAGE_DIR}\*.*"
SectionEnd
Function LaunchUpdater
  SetOutPath "$INSTDIR\app"
  Exec '"$INSTDIR\app\Profoto_DFU-app.exe"'
FunctionEnd
