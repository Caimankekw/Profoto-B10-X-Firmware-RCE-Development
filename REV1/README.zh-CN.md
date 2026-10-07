# REV1 开发代码

[English](README.md) | [简体中文](README.zh-CN.md)

固件元数据：`D3-RC1`，ABOUT 保留原来的 `D3` 显示。基于 D3 增加 `SETTINGS → ADVANCED → RECHARGE CTRL`，选择 `NON-X / X`。

## 实现

- 保留真实机型和 250 / 500 Ws 家族，只替换回电策略选择。
- 无有效记录时，非 X 型号默认 NON-X，X 型号默认 X。
- X 策略仍受原造型灯 / DIM 条件限制；选中 X 不保证所有场景使用增强系数。
- 命令 `0x1032` 发送选择，在原参数装载流程中生效。
- EEPROM 独立记录位于 `0x3E0`，包含 magic、版本、反码及 CRC，并写后读回。
- 保留 NORMAL / FREEZE 放电表及原目标电压。

| 源码 | 职责 |
| --- | --- |
| [build_recharge.py](source/build_recharge.py) | 输入校验、补丁集成、功率板嵌入和 DFU 封装 |
| [config_codegen.py](source/config_codegen.py) | 主控设置、持久化、协议和菜单辅助代码 |
| [pb_patch.py](source/pb_patch.py) | 功率板命令解析与回电选择 |
| [ui_assets.py](source/ui_assets.py) | 从 D3 位图生成菜单资源 |

## 构建与标识

推荐 Python 3.11，在仓库根目录执行：

```powershell
python -m pip install -r requirements.txt
python build.py
```

根目录依赖固定为 `capstone==5.0.9`、`keystone-engine==0.9.2`、`Pillow==11.3.0`。输出 `REV1/build/RC1.bin`、`RC1.dfu`、`powerboard.bin` 和补丁记录。主控已嵌入功率板；单独的功率板 BIN 仅供开发核验，不能当作主控固件刷入。构建不访问 USB。

主控 682,596 字节。构建须逐字节复现已有发布镜像，固定 SHA-256：

```text
BIN  7661a83958caf5cd62a477575a8ffe8a6be9d0153ef076b5d7bf2e5850df3a0e
DFU  c8088fafa8d224d203c023442f0157050800169ded67282e62088bc833b1bcbe
PB   ce94c00388cdf755d4c343d8eeab5e517096ae8a81974efa09f67d175d6eb000
```

根目录构建还检查 DFU CRC 和功率板嵌入字节。保留原保护代码不能证明非 X 硬件采用 X 策略的电气余量；光量、色温和电气表现仍须实测。

## Windows 更新包

在 [REV1 + REV5 合并 Release](https://github.com/Caimankekw/Profoto-B10-X-Firmware-RCE-Development/releases/tag/rev1-rev5-20261007) 下载 `Profoto-B10-REV1-Custom-Updater.exe`。它封装了供此自定义固件使用的原厂风格 Windows 更新器，无需 Python；不是 Profoto 官方发版，也不代表获得官方签名。使用方法见更新包内说明。
