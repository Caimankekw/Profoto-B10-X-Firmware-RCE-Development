# REV5 开发代码

[English](README.md) | [简体中文](README.zh-CN.md)

自定义固件开发者：[Caimankekw](https://github.com/Caimankekw)（REV1 / REV5）。原厂组件版权归原权利人所有。

固件标识：`RC5`，直接基于 D3 构建；固件元数据与 ABOUT 均显示 `RC5`。

## 实现

- RECHARGE CTRL：NON-X / X / BOOST，主屏显示选择值。
- FLASH MODE：NORMAL / FREEZE / ECO，主屏显示模式提示。
- ECO 普通闪光及 HSS 使用 470 V 目标，保留相关反馈和边界控制。
- BOOST / ECO 仅对 500 Ws Plus 型号开放。
- BOOST 使用 K375 / T445 / C20，增强限于满足条件的主充电段，保留软启动、尾段及保护条件。
- 设置记录版本为 4，保留旧记录迁移及旧 BOOST 回落到 X 的行为。

主屏显示选择值，不能确认某次回电正处于增强段。缩时 20% 是设计目标，不是实测承诺。

| 源码 | 职责 |
| --- | --- |
| [build_recharge.py](source/build_recharge.py) | 从 D3 集成补丁，生成命名版 RC5 |
| [config_codegen.py](source/config_codegen.py) | 回电 / ECO 设置、型号限制、迁移、协议和 UI |
| [pb_patch.py](source/pb_patch.py) | 回电状态机、BOOST 条件和目标电压 |
| [eco_guard.py](source/eco_guard.py) | ECO 的 HSS 参考与标定保护钩子 |
| [ui_assets.py](source/ui_assets.py) | 菜单与主屏位图 |

## 构建与标识

推荐 Python 3.11，在仓库根目录执行：

```powershell
python -m pip install -r requirements.txt
python build.py
```

根目录依赖固定为 `capstone==5.0.9`、`keystone-engine==0.9.2`、`Pillow==11.3.0`。输出 `REV5/build/RC5.bin`、`RC5.dfu`、`powerboard.bin` 和补丁记录。构建先校验命名前的控制镜像，再仅修改两个版本字段及 ABOUT 为 RC5，并重算 DFU CRC；不访问 USB。

主控 691,644 字节；功率板 55,996 字节，ID 为 `b0e69569`。构建须逐字节复现已有命名版发布镜像：

```text
BIN  ad8b5ff203bd1d7426f66666124432f154c00bc46c31878d660ff0e0ea506ea8
DFU  c6c2343921b302c2ce45e9bf06ffa5e66d591700f59dd0218388327c24d57f4f
PB   be56734b508ef577fa5c4c257499e3a65ef06003aa4d7c8d526cccaf09a85fac
```

根目录构建还检查 DFU CRC 和功率板嵌入字节。功率板 BIN 仅供核验，不能当作主控固件刷入。光量、色温、HSS 均匀性和电气稳定性仍须实测。

## Windows 更新包

在 [REV1 + REV5 合并 Release](https://github.com/Caimankekw/Profoto-B10-X-Firmware-RCE-Development/releases/tag/rev1-rev5-20261007) 下载 `Profoto-B10-REV5-Custom-Updater.exe`。它封装了供此自定义固件使用的原厂风格 Windows 更新器，无需 Python；不是 Profoto 官方发版，也不代表获得官方签名。使用方法见更新包内说明。

## 许可协议

原创代码及说明采用 [AGPL-3.0-only](../LICENSE)，开发者为 **Caimankekw**。原厂固件、恢复的原始机器码及第三方组件保留各自权利，不由本项目重新授权；具体范围见 [NOTICE](../NOTICE.md)。Windows 自定义更新器及安装器的构建源码位于对应开发分支的 `windows/`。
