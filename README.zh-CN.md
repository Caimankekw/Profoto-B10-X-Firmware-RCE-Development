# Profoto B10 固件逆向

[English](README.md) | [简体中文](README.zh-CN.md)

自定义固件开发者：[Caimankekw](https://github.com/Caimankekw)（REV1 / REV5）。原厂组件版权归原权利人所有。

`main` 分支保存原始 B10 REV-D3 固件的逆向代码、分析说明与查看工具。入口为 [D3 逆向说明](D3/README.zh-CN.md)和[恢复的汇编切片](D3/source/)。

恢复的名称、注释与伪代码属于逆向研究结果，不是厂商原始 C 源码；目前是部分还原，不是完整反编译或可直接构建的原固件源码。

## 分支

| 分支 | 内容 |
| --- | --- |
| `main` | D3 逆向与查看工具，不带固件二进制或开发补丁 |
| [REV1](https://github.com/Caimankekw/Profoto-B10-X-Firmware-RCE-Development/tree/REV1) | 独立基于 D3 的 NON-X / X 回电选择开发代码，固件元数据为 `D3-RC1` |
| [REV5](https://github.com/Caimankekw/Profoto-B10-X-Firmware-RCE-Development/tree/REV5) | 独立基于 D3 的 NON-X / X / BOOST、ECO 与 HSS 适配开发代码，固件标识为 `RC5` |

每个开发分支均包含自己的构建入口与必要 D3 原始输入，不需要中间开发版本。在 `main` 上运行查看工具的输入取得方式见 [D3 固件输入说明](D3/README.zh-CN.md#固件输入与分支)。

## Windows 更新

两个自定义 Windows 更新包放在同一个 [REV1 + REV5 Release](https://github.com/Caimankekw/Profoto-B10-X-Firmware-RCE-Development/releases/tag/rev1-rev5-20261007)：`Profoto-B10-REV1-Custom-Updater.exe` 与 `Profoto-B10-REV5-Custom-Updater.exe`。更新包使用原厂风格的 Windows 更新器界面，属于自定义固件，不是 Profoto 官方发版，也不代表获得官方签名。使用方法见对应更新包内的 README。

代码及镜像校验不能证明电气余量、实际回电时间、曝光一致性或色温准确性。原固件及其资源归原权利人所有。

## 许可协议

原创代码及说明采用 [AGPL-3.0-only](LICENSE)，开发者为 **Caimankekw**。原厂固件、恢复的原始机器码及第三方组件保留各自权利，不由本项目重新授权；具体范围见 [NOTICE](NOTICE.md)。Windows 自定义更新器及安装器的构建源码位于对应开发分支的 `windows/`。
