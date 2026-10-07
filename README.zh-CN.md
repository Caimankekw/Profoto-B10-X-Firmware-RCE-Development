# B10 REV5 开发

[English](README.md) | [简体中文](README.zh-CN.md)

自定义固件开发者：[Caimankekw](https://github.com/Caimankekw)（REV1 / REV5）。原厂组件版权归原权利人所有。

本分支为独立基于 D3 的 REV5 开发工程。提供 RECHARGE CTRL 下的 `NON-X / X / BOOST`、主屏挡位提示，以及 ECO 与 HSS 适配。固件元数据与 ABOUT 显示 `RC5`。BOOST 和 ECO 仅对 500 Ws Plus 型号开放。

| 目录 | 内容 |
| --- | --- |
| [D3](D3/README.zh-CN.md) | 原固件逆向、查看工具及必要构建输入 |
| [REV5](REV5/README.zh-CN.md) | 补丁源码、实现说明与固定发布哈希 |
| [Windows](windows/README.zh-CN.md) | 自定义更新器、安装器构建源码及输入指纹 |

这是二进制补丁工程，不是厂商完整 C 源码或官方更新；直接从 D3 构建，不需要中间开发版本。

## 构建

推荐 Python 3.11，在仓库根目录运行：

```powershell
python -m pip install -r requirements.txt
python build.py
```

依赖固定为 `capstone==5.0.9`、`keystone-engine==0.9.2`、`Pillow==11.3.0`。产物位于 `REV5/build/`：`RC5.bin`、`RC5.dfu`、`powerboard.bin` 与补丁记录。主控镜像已嵌入功率板镜像，不能把独立功率板 BIN 当作主控固件刷入。

构建核验固定 SHA-256、内嵌功率板字节与 DFU CRC，逐字节复现已有命名版 RC5 发布镜像。构建不访问 USB，也不刷写灯具。

## Windows 更新包与其他分支

REV5 自定义 Windows 更新包 `Profoto-B10-REV5-Custom-Updater.exe` 与 REV1 一起放在[同一个 Release](https://github.com/Caimankekw/Profoto-B10-X-Firmware-RCE-Development/releases/tag/rev1-rev5-20261007)。它使用原厂风格的更新器界面，无需 Python；不是 Profoto 官方发版，也不代表获得官方签名。使用方法见包内 README。

仅查看 D3 逆向请进入 [main](https://github.com/Caimankekw/Profoto-B10-X-Firmware-RCE-Development/tree/main)；NON-X / X 开发请进入 [REV1](https://github.com/Caimankekw/Profoto-B10-X-Firmware-RCE-Development/tree/REV1)。

回电缩时 20% 是设计目标，不是实测承诺。主屏选择值不能证明当前正处于增强充电段。镜像校验不替代电气、温升、曝光、HSS 均匀性和色温实测。原固件及其资源归原权利人所有。

## 许可协议

原创代码及说明采用 [AGPL-3.0-only](LICENSE)，开发者为 **Caimankekw**。原厂固件、恢复的原始机器码及第三方组件保留各自权利，不由本项目重新授权；具体范围见 [NOTICE](NOTICE.md)。Windows 自定义更新器及安装器的构建源码位于对应开发分支的 `windows/`。
