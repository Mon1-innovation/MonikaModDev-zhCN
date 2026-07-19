# Android 构建脚本使用指南

这是一个 PowerShell 脚本，用于自动化 Monika After Story (MAS) 中文版本的 Android 构建流程。

## 前置要求

1. **DDLC Base 本体文件**
   - 将原始DDLC本体文件放在 `.DDLC_BASE/` 目录
   - 这些文件会被加入 `.gitignore` 不提交到版本控制
   - 构建时会自动与MAS文件合并

2. **Ren'Py SDK 8.2.3** 或更高版本
   - 默认路径: `J:\Renpy\renpy-8.2.3-sdk`
   - 如果路径不同，需要在命令中指定

3. **Android SDK 配置**
   - 必须通过 Ren'Py 启动器安装 Android SDK
   - 生成过密钥库 (keystore)
   - 在项目中配置过 Android 设置

4. **PowerShell 5.0+**
   - Windows 10/11 内置 PowerShell

## 快速开始

### 第一步：准备 DDLC 本体文件

1. 获取原始 DOKI DOKI Literature Club 的完整文件副本
2. 将其复制到 `.DDLC_BASE/` 目录

或者使用以下命令复制：
```powershell
# 从源文件复制到 .DDLC_BASE
Copy-Item -Path "E:\YourDDLCFolder\*" -Destination ".\.DDLC_BASE" -Recurse -Force
```

### 第二步：运行构建脚本

在项目目录中打开 PowerShell，执行：

```powershell
cd J:\MAS\MonikaModDev-zhCN\utils
.\build-android.ps1
```

脚本会：
1. ✓ 验证配置文件和路径
2. ✓ 创建临时构建目录
3. ✓ 合并 DDLC 本体和 MAS 文件（MAS 优先）
4. ✓ 显示完整的构建命令
5. ✓ 询问是否继续 (输入 `y` 确认)
6. ✓ 执行 Android 构建
7. ✓ 清理临时文件

### 常用命令

#### 1. 生成 .aab Bundle（推荐用于 Google Play）

```powershell
.\build-android.ps1 -Bundle
```

#### 2. 指定输出目录

```powershell
.\build-android.ps1 -OutputDir "D:\MAS-Build\output"
```

#### 3. 构建后自动安装到设备

```powershell
.\build-android.ps1 -Install
```

需要连接 Android 设备并启用 USB 调试。

#### 4. 构建并立即启动（需要连接设备）

```powershell
.\build-android.ps1 -Launch
```

这个选项包含了 `-Install`。

#### 5. 组合使用

```powershell
.\build-android.ps1 -Bundle -OutputDir "D:\output" -Install
```

## 参数说明

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `-RenPySDK` | 字符串 | `J:\Renpy\renpy-8.2.3-sdk` | Ren'Py SDK 路径 |
| `-ProjectBase` | 字符串 | `J:\MAS\MonikaModDev-zhCN\Monika After Story` | 项目基础路径 |
| `-DDLCBase` | 字符串 | `J:\MAS\MonikaModDev-zhCN\.DDLC_BASE` | DDLC 本体文件路径 |
| `-OutputDir` | 字符串 | 空（使用默认值） | 输出目录路径 |
| `-Bundle` | 开关 | 关闭 | 生成 .aab bundle（否则生成 .apk） |
| `-Install` | 开关 | 关闭 | 构建后安装到连接的设备 |
| `-Launch` | 开关 | 关闭 | 构建后启动游戏（包含 Install） |
| `-KeepTemp` | 开关 | 关闭 | 保留临时构建目录（用于调试） |
| `-Verbose` | 开关 | 关闭 | 显示详细信息 |

## 执行权限问题

如果遇到 "执行策略不允许运行此脚本" 的错误，可以：

### 方案 1：临时运行脚本（推荐）

```powershell
powershell -ExecutionPolicy Bypass -File .\build-android.ps1
```

### 方案 2：使用 -Command 参数

```powershell
powershell -ExecutionPolicy Bypass -Command ".\build-android.ps1 -Bundle"
```

### 方案 3：一次性修改执行策略（不推荐）

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## 工作原理

该脚本使用以下流程来构建 Android 版本：

1. **验证配置**：检查所有必需的路径和文件

2. **准备临时构建环境**：
   - 在当前目录创建 `.build_temp` 临时目录
   - 从 `.DDLC_BASE` 复制原始DDLC文件到临时目录
   - 从 `Monika After Story` 复制MAS文件到临时目录（覆盖重复项）
   - 这样确保MAS的修改优先于原始DDLC文件

3. **执行构建**：
   - 使用Ren'Py CLI从临时目录构建Android版本
   - 生成 `.apk` 或 `.aab` 文件

4. **清理**：
   - 构建完成后自动删除临时目录（保持工作目录整洁）
   - 可以使用 `-KeepTemp` 选项保留临时目录用于调试

## 文件优先级

当 `.DDLC_BASE` 和 `Monika After Story` 中有重名文件时：
- **Monika After Story 中的文件优先** ✓
- 这确保MAS的所有修改都能被使用

## 关于 .DDLC_BASE 目录

- `.DDLC_BASE` 目录中的所有文件都被加入 `.gitignore`
- 仅 `.gitkeep` 文件被版本控制，用来保持空目录
- 您需要手动将DDLC本体文件复制到该目录

```
.DDLC_BASE/
├── .gitkeep
├── game/
│   ├── *.rpy
│   └── ...
├── lib/
├── renpy/
└── ...
```

## 输出文件

构建完成后，输出文件默认位置为：
```
<当前目录>/MonikaAfterStory-<Version>-dists/
```

## 故障排除

### 1. "Ren'Py SDK 路径不存在"
- 检查 Ren'Py SDK 实际安装位置
- 更正脚本中的 `-RenPySDK` 参数

### 2. "找不到 project.json"
- 确保项目路径正确
- 确保 `Monika After Story/project.json` 存在

### 3. "构建失败"
- 检查 Ren'Py 启动器中 Android 配置是否完整
- 查看输出中的错误信息
- 确保 Android SDK 已正确安装

### 4. 安装或启动失败
- 确保 Android 设备已连接
- 启用 USB 调试模式
- 检查 ADB 驱动程序是否正确安装

## 相关文档

- [Ren'Py CLI 文档](https://www.renpy.org/doc/html/cli.html)
- [Ren'Py Android 打包指南](https://www.renpy.org/doc/html/android-packaging.html)

## 示例工作流

### 第一次设置

```bash
# 1. 将 DDLC 本体文件复制到 .DDLC_BASE/
#    (手动操作或使用脚本复制)

# 2. 创建 .gitkeep 来保持目录（已由脚本自动完成）

# 3. 首次构建
.\build-android.ps1
```

### 日常构建

```bash
# 基本构建
.\build-android.ps1

# 为 Google Play 生成 bundle
.\build-android.ps1 -Bundle -OutputDir ".\release"

# 本地测试
.\build-android.ps1 -Install -OutputDir ".\debug"

# 完整构建并启动
.\build-android.ps1 -Bundle -Launch -OutputDir ".\release"

# 调试：保留临时目录查看最终组合文件
.\build-android.ps1 -KeepTemp
```
