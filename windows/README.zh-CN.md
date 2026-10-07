# REV5 Windows 安装包源码

[English](README.md) | [简体中文](README.zh-CN.md)

Copyright 2026 Caimankekw。SPDX-License-Identifier: AGPL-3.0-only。见 [LICENSE](../LICENSE) 与 [许可范围](../NOTICE.md)。AGPL 仅覆盖原创自定义代码；厂商 EXE、固件、Qt、驱动及其他第三方组件保留各自原许可。

本目录公开本分支的 GUI 资源补丁、静态校验、便携 ZIP 与 NSIS 安装器构建源码。不含厂商二进制，不自动下载输入。先运行仓库固件构建；默认读取 `REV5/build/RC5.bin` 和 `.dfu`。GUI 标题为 `RC5 CUSTOM`，固件标识为 `RC5`，ABOUT 显示 `RC5`。

## 必需输入

- Python 3.9 以上及根目录构建依赖；另外执行 `python -m pip install -r windows/requirements.txt`，版本为 `pefile==2024.8.26`。
- 用户自行提供完整解出的原厂 D3 Windows 更新器 **Profoto_DFU-app** 目录：包括原 EXE、DLL、Qt 插件与驱动的全部 30 个文件。不能使用已经修改过的自定义更新器目录。
- 原厂 `license_3rd_party.txt` 与 `Profoto-FW-Trouble-Shooting-FAQ.pdf` 所在目录。
- 完整 [NSIS 3.13](https://sourceforge.net/projects/nsis/files/NSIS%203/3.13/) 目录，以及 [7-Zip 26.04 x64](https://github.com/ip7z/7zip/releases/tag/26.04) 的 `7z.exe` 和同目录的 `7z.dll`。

[input_manifest.json](input_manifest.json) 固定了全部原厂运行文件、两个文档和工具指纹，不完整或字节不同的输入会被拒绝。原厂 EXE 为 2,874,880 字节，SHA-256 为 `4fe18a566843afde2bb1b3b4e8600495d9d010afeab1e1902519022fa3356fa5`。

## 构建

从仓库根目录运行 PowerShell，将示例路径改为实际输入：

```powershell
python build.py
python -m pip install -r windows/requirements.txt
python windows/build_package.py `
  --runtime "C:\inputs\D3\Profoto_DFU-app" `
  --vendor-docs "C:\inputs\D3" `
  --nsis-dir "C:\tools\nsis-3.13" `
  --seven-zip "C:\tools\7zip\7z.exe"
```

默认输出到新建的 `windows/build/<UTC时间戳>/`。可用 `--output` 指定尚不存在的目录；脚本不会删除或覆盖旧目录。可用 `--bin` 和 `--dfu` 指定固件文件，但仍必须匹配冻结哈希。源码不依赖开发者本机路径、其他开发版本或其他分支。

输出包含完整更新器目录、便携 ZIP、自解压安装器、日志、SHA256SUMS 和 `package_verification.json`。GUI 只修改审计白名单内的资源指针、PE 字段并附加资源节，其他原厂更新代码保持原字节。验证包含固件哈希和 DFU CRC/地址/长度、PE/QRC 修改白名单、八项损坏注入、30 个运行文件（29 个不变）、DLL 依赖、ZIP 往返及 7-Zip 静态解包后的安装器内容。构建仅运行用户提供的 NSIS 编译器和解包工具；不会运行安装器、更新器、驱动脚本或访问 USB。

单独构建 GUI 可运行 `build_gui.py --original-exe ... --bin ... --dfu ... --output ...`；独立校验使用 `verify_gui.py --original-exe ... --bin ... --dfu ... --gui ...`。

## 冻结产物

| 产物 | 字节数 | SHA-256 |
| --- | ---: | --- |
| RC5.bin | 691644 | `ad8b5ff203bd1d7426f66666124432f154c00bc46c31878d660ff0e0ea506ea8` |
| RC5.dfu | 691953 | `c6c2343921b302c2ce45e9bf06ffa5e66d591700f59dd0218388327c24d57f4f` |
| Profoto_DFU-app.exe | 4463104 | `19d5e4b6857e5ec82ab4cce8fa3ba2e54e13b9b323a31c91fe7bf57f36d4e685` |

固件和 GUI 必须逐字节复现。外层安装器、ZIP 的元数据或时间戳可能与已发布附件不同；这里验证解包内容，不保证外层 EXE 哈希完全复现。离线通过不等于实测 Qt 启动、刷灯、电气余量或光学表现。安装器在用户目录解压，展示原创代码 AGPL 范围，并提供打开更新器的选项；不会自动安装驱动或自动刷写。

包内文档在 [templates](templates/)，NSIS 源码为 [installer.nsi](installer.nsi)。安装包复制仓库根 LICENSE；厂商与 NSIS 许可从显式提供的输入复制。
