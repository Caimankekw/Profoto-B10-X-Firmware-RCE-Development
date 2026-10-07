# B10 REV1 开发

[English](README.md) | [简体中文](README.zh-CN.md)

自定义固件开发者：[Caimankekw](https://github.com/Caimankekw)（REV1 / REV5）。原厂组件版权归原权利人所有。

本分支为独立基于 D3 的 REV1 开发工程。新增 `SETTINGS → ADVANCED → RECHARGE CTRL`，选择 `NON-X / X`，保留 250 / 500 Ws 型号家族。固件元数据为 `D3-RC1`；ABOUT 保留原来的 `D3` 显示。

| 目录 | 内容 |
| --- | --- |
| [D3](D3/README.zh-CN.md) | 原固件逆向、查看工具及必要构建输入 |
| [REV1](REV1/README.zh-CN.md) | 补丁源码、实现说明与固定发布哈希 |
| [Windows](windows/README.zh-CN.md) | 自定义更新器、安装器构建源码及输入指纹 |

这是二进制补丁工程，不是厂商完整 C 源码或官方更新；本分支不依赖其他开发版本。

## 构建

推荐 Python 3.11，在仓库根目录运行：

```powershell
python -m pip install -r requirements.txt
python build.py
```

依赖固定为 `capstone==5.0.9`、`keystone-engine==0.9.2`、`Pillow==11.3.0`。产物位于 `REV1/build/`：`RC1.bin`、`RC1.dfu`、`powerboard.bin` 与补丁记录。主控镜像已嵌入功率板镜像，不能把独立功率板 BIN 当作主控固件刷入。

构建核验固定 SHA-256、内嵌功率板字节与 DFU CRC，逐字节复现已有 REV1 发布镜像。构建不访问 USB，也不刷写灯具。

## Windows 更新包与其他分支

REV1 自定义 Windows 更新包 `Profoto-B10-REV1-Custom-Updater.exe` 与 REV5 一起放在[同一个 Release](https://github.com/Caimankekw/Profoto-B10-X-Firmware-RCE-Development/releases/tag/rev1-rev5-20261007)。它使用原厂风格的更新器界面，无需 Python；不是 Profoto 官方发版，也不代表获得官方签名。使用方法见包内 README。

仅查看 D3 逆向请进入 [main](https://github.com/Caimankekw/Profoto-B10-X-Firmware-RCE-Development/tree/main)；BOOST / ECO 开发请进入 [REV5](https://github.com/Caimankekw/Profoto-B10-X-Firmware-RCE-Development/tree/REV5)。

保留原保护代码不能证明非 X 硬件采用 X 策略的电气余量。镜像校验不替代电气、温升、曝光和色温实测。原固件及其资源归原权利人所有。

## 许可协议

原创代码及说明采用 [AGPL-3.0-only](LICENSE)，开发者为 **Caimankekw**。原厂固件、恢复的原始机器码及第三方组件保留各自权利，不由本项目重新授权；具体范围见 [NOTICE](NOTICE.md)。Windows 自定义更新器及安装器的构建源码位于对应开发分支的 `windows/`。
