# REV5 Windows 固件更新器

简体中文 | [English](README.md)

开发者：[Caimankekw](https://github.com/Caimankekw)

**这是自定义实验固件，不是 Profoto 官方发布。** 本包复用原厂 D3 Qt 更新界面及完整运行库。自定义安装器和更新器均没有 Authenticode 签名，不宣称厂商签名或认可。

RECHARGE CTRL 提供 NON-X / X / BOOST；Plus 型号还提供 ECO（470 V，包含 HSS），主屏显示回电档位。BOOST/ECO 仍仅对 500 Ws Plus 开放。回电缩时 20% 是开发目标，不是实测保证。

使用独立命名的 RC5 固件，在这里以 REV5 发布。更新器和灯内 ABOUT 显示 RC5。迁移旧设置时，旧 BOOST 选择会转为 X；如需 BOOST，请更新后手动选择。

## 协议与源码

Caimankekw 原创的自定义开发与封装代码采用 **AGPL-3.0-only**。完整协议见 [LICENSE](LICENSE)，适用范围见双语 [NOTICE.md](NOTICE.md)。原厂固件、原厂更新器/运行库及第三方组件仍遵循各自原有条款；本包不会将这些组件重新许可为 AGPL。

源码：[REV5 分支](https://github.com/Caimankekw/Profoto-B10-X-Firmware-RCE-Development/tree/REV5) · [Windows 更新器补丁及封装源码](https://github.com/Caimankekw/Profoto-B10-X-Firmware-RCE-Development/tree/REV5/windows)。

## 更新步骤

1. 运行 `Profoto-B10-REV5-Custom-Updater.exe`。它解压到 `%LOCALAPPDATA%\Profoto-B10-Custom\REV5` 下的用户目录，不请求管理员权限；完成页可打开更新器。不会自动安装驱动或自动刷写。
2. 关灯、取下电池，再通过 USB 连接一台目标灯具。遵循原厂更新器的提示；确认设备和目标固件版本后，手动点击更新。
3. 保持 USB 连接，等待更新器完成写入和整幅镜像读回比较。
4. 断开 USB、装回电池并开机。若首次启动执行内部功率板更新，保持供电直到完成。

再次运行可使用解压目录中的 `REV5.cmd`。保留完整 `app` 文件夹，无需 Python。若使用便携 ZIP，先完整解压再运行命令文件。

原厂 PC 端检查的是共享的 B10/B10X 家族（0x8C），不能独立区分 Plus 与非 Plus；固件内部的型号条件保持原样。本包只用于其支持的 B10 家族硬件，不用于其他产品。

## 驱动及流程

已有驱动正常工作时应继续使用。新电脑无法识别设备时，查阅附带原厂故障排查 PDF。原驱动保留在 `app/driver_package`；确需手动安装时，应以管理员命令行进入 **app 目录**，执行 `driver_package\install_driver.cmd`。安装器不会执行该脚本。

GUI 保留原厂设备枚举、型号/版本判断、写入/读回及 leave/重连流程；不包含独立 Python 工具的写前完整备份、已知镜像白名单或失败事务恢复功能。已安装相同固件时沿用原厂不重复更新的行为。不发布任何私人设备备份、OTP 转储或序列号。

## 校验及边界

已完成离线校验：固件哈希与 DfuSe CRC/地址/长度、PE 资源指针和修改白名单、全部 30 个运行文件（29 个字节不变）、每版 GUI 八项损坏注入检查、ZIP 往返和安装器静态解包核对。封装期间没有运行更新器或安装器、安装驱动、访问 USB 或灯具；这些结果不等于真实 Windows/Qt 启动或实机刷写结果。封装也未新增验证光量、色温、温升余量或 HSS 均匀性。

固件 BIN SHA-256：`ad8b5ff203bd1d7426f66666124432f154c00bc46c31878d660ff0e0ea506ea8`  
固件 DFU SHA-256：`c6c2343921b302c2ce45e9bf06ffa5e66d591700f59dd0218388327c24d57f4f`

`package_manifest.json` 和 `SHA256SUMS.txt` 标识实际解压文件。保留的原厂依赖许可及故障排查 PDF 不代表厂商认证自定义固件。外层解压器使用未修改的 NSIS 3.13 组件，许可见 `NSIS-COPYING.txt`，源码可从 [NSIS 项目](https://sourceforge.net/projects/nsis/files/NSIS%203/3.13/) 获取。
