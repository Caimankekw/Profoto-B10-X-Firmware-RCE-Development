# License scope / 许可范围

## English

Copyright (C) 2026 Caimankekw.

Caimankekw's original development code, build and inspection tools, custom Windows packaging code, and original explanatory documentation are licensed under the GNU Affero General Public License, version 3 only (SPDX: AGPL-3.0-only). See LICENSE for the complete, unmodified license text. The software is supplied without warranty as described in that license.

The license grant covers only material for which the developer can grant rights. It does not relicense the following third-party material:

- Original Profoto firmware BIN/DFU files and original firmware bytes retained in generated patched images.
- Recovered original machine code in assembly excerpts, original firmware tables, fonts, bitmaps, or other extracted vendor resources. Original explanatory text and independently authored tools remain within the scope above.
- Original Profoto updater code and resources, Qt runtime libraries, dfu-util, driver packages, vendor manuals, or other third-party components included in Windows packages. Their original ownership and license notices remain applicable.
- NSIS and its unmodified runtime components, whose own licenses are retained in the packages.

No rights to these excluded materials or vendor trademarks are granted by this project's AGPL notice. No manufacturer approval or signing is implied. A generated updater or firmware image may contain both custom and excluded material; the entire combined binary is not represented as wholly authored by Caimankekw or wholly relicensed under AGPL.

Custom source is available at https://github.com/Caimankekw/Profoto-B10-X-Firmware-RCE-Development: main for D3 inspection tools and original analysis, REV1 and REV5 for their respective development projects, including windows/ for custom updater and installer build source. Release notes link the corresponding source commits. Third-party inputs are identified separately by their original notices and build instructions.

## 简体中文

版权所有 (C) 2026 Caimankekw。

Caimankekw 原创的开发代码、构建及检查工具、Windows 自定义打包代码和原创说明文档，采用 GNU Affero General Public License 第 3 版，且仅该版本（SPDX：AGPL-3.0-only）。完整、未经修改的许可证见 LICENSE；软件按该协议不提供担保。

该授权仅涵盖开发者有权许可的材料，不重新授权以下第三方内容：

- 原厂 Profoto BIN/DFU 固件，以及生成的补丁固件中保留的原厂字节。
- 汇编切片中恢复的原始机器码、原厂标定表、字体、位图及其他提取资源；原创解释文字及独立编写的工具仍适用上述授权。
- Windows 包中的原厂更新器代码及资源、Qt 运行库、dfu-util、驱动、原厂手册及其他第三方组件；其原有权利与许可声明继续适用。
- NSIS 及未经修改的运行组件；安装包保留其各自许可。

本项目的 AGPL 声明不授予上述排除内容或厂商商标的权利，也不代表厂商认可或签名。生成的更新器及固件可能混合包含自定义与原厂内容，不宣称整个二进制均由 Caimankekw 创作或已整体改为 AGPL。

自定义源码仓库：https://github.com/Caimankekw/Profoto-B10-X-Firmware-RCE-Development 。main 提供 D3 检查工具及原创分析；REV1、REV5 提供各自开发工程，windows/ 包含更新器和安装器构建源码。Release 说明链接对应源码提交；第三方输入由其原有声明和构建说明单独标识。
