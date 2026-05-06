# Ren'Py Android Build Script for MAS (Monika After Story)
#
# 用法：
#   .\build-android.ps1                      # 默认设置构建
#   .\build-android.ps1 -Bundle              # 生成 .aab bundle
#   .\build-android.ps1 -OutputDir "./dist"  # 指定输出目录
#   .\build-android.ps1 -Bundle -OutputDir "./dist" -Install
#   .\build-android.ps1 -Proxy "127.0.0.1:7890"  # 指定构建代理
#   .\build-android.ps1 -NoProxy             # 禁用默认代理
#

param(
    [string]$RenPySDK = "J:\Renpy\renpy-8.2.3-sdk",
    [string]$ProjectBase = "J:\MAS\MonikaModDev-zhCN\Monika After Story",
    [string]$DDLCBase = "J:\MAS\MonikaModDev-zhCN\.DDLC_BASE",
    [string]$OutputDir = "",
    [string]$Proxy = "localhost:7890",
    [switch]$NoProxy = $false,
    [switch]$Bundle = $false,
    [switch]$Install = $false,
    [switch]$Launch = $false,
    [switch]$Verbose = $false,
    [switch]$KeepTemp = $false,
    [switch]$NoConfirm = $false
)

# 颜色输出函数
function Write-Success {
    param([string]$Message)
    Write-Host "✓ $Message" -ForegroundColor Green
}

function Write-Error-Custom {
    param([string]$Message)
    Write-Host "✗ $Message" -ForegroundColor Red
}

function Write-Info {
    param([string]$Message)
    Write-Host "ℹ $Message" -ForegroundColor Cyan
}

function Write-Warning-Custom {
    param([string]$Message)
    Write-Host "⚠ $Message" -ForegroundColor Yellow
}

function Get-NormalizedProxyUri {
    param([string]$ProxyValue)

    if ([string]::IsNullOrWhiteSpace($ProxyValue)) {
        throw "代理地址不能为空；如需禁用代理，请使用 -NoProxy"
    }

    if ($ProxyValue -notmatch '^[a-zA-Z][a-zA-Z0-9+.-]*://') {
        $ProxyValue = "http://$ProxyValue"
    }

    try {
        $proxyUri = [System.Uri]$ProxyValue
    } catch {
        throw "代理地址格式无效: $ProxyValue"
    }

    if (-not $proxyUri.Host -or $proxyUri.Port -le 0) {
        throw "代理地址必须包含 host 和 port: $ProxyValue"
    }

    return $proxyUri
}

function Enable-BuildProxy {
    param([string]$ProxyValue)

    $proxyUri = Get-NormalizedProxyUri -ProxyValue $ProxyValue
    $proxyUrl = $proxyUri.AbsoluteUri.TrimEnd('/')
    $proxyHost = $proxyUri.Host
    $proxyPort = $proxyUri.Port
    $proxyOptions = "-Dhttp.proxyHost=$proxyHost -Dhttp.proxyPort=$proxyPort -Dhttps.proxyHost=$proxyHost -Dhttps.proxyPort=$proxyPort"

    $keys = @(
        "HTTP_PROXY",
        "HTTPS_PROXY",
        "ALL_PROXY",
        "GRADLE_OPTS",
        "JAVA_TOOL_OPTIONS"
    )

    $backup = @{}
    foreach ($key in $keys) {
        $backup[$key] = [Environment]::GetEnvironmentVariable($key, "Process")
    }

    [Environment]::SetEnvironmentVariable("HTTP_PROXY", $proxyUrl, "Process")
    [Environment]::SetEnvironmentVariable("HTTPS_PROXY", $proxyUrl, "Process")
    [Environment]::SetEnvironmentVariable("ALL_PROXY", $proxyUrl, "Process")

    $existingGradleOpts = [Environment]::GetEnvironmentVariable("GRADLE_OPTS", "Process")
    $existingJavaToolOptions = [Environment]::GetEnvironmentVariable("JAVA_TOOL_OPTIONS", "Process")
    [Environment]::SetEnvironmentVariable("GRADLE_OPTS", "$existingGradleOpts $proxyOptions".Trim(), "Process")
    [Environment]::SetEnvironmentVariable("JAVA_TOOL_OPTIONS", "$existingJavaToolOptions $proxyOptions".Trim(), "Process")

    Write-Info "已启用构建代理: $proxyUrl"
    return $backup
}

function Restore-BuildProxy {
    param([hashtable]$Backup)

    if (-not $Backup) {
        return
    }

    foreach ($key in $Backup.Keys) {
        if ($null -eq $Backup[$key]) {
            Remove-Item -Path "Env:\$key" -ErrorAction SilentlyContinue
        } else {
            [Environment]::SetEnvironmentVariable($key, $Backup[$key], "Process")
        }
    }

    Write-Info "已恢复构建前的代理环境变量"
}

# 复制目录函数（递归，覆盖模式，排除不必要的文件）
function Copy-DirectoryRecursive {
    param(
        [string]$Source,
        [string]$Destination,
        [string]$ExcludePattern = $null
    )

    if (-not (Test-Path $Source)) {
        Write-Warning-Custom "源路径不存在: $Source"
        return
    }

    if (-not (Test-Path $Destination)) {
        New-Item -ItemType Directory -Path $Destination -Force | Out-Null
    }

    Get-ChildItem -Path $Source -Recurse | ForEach-Object {
        $relativePath = $_.FullName.Substring($Source.Length).TrimStart('\')
        $targetPath = Join-Path $Destination $relativePath

        # 排除特定模式和编译文件
        if ($ExcludePattern -and $_.Name -match $ExcludePattern) {
            return
        }

        # 排除 __pycache__ 目录
        if ($_.PSIsContainer -and $_.Name -eq "__pycache__") {
            return
        }

        # 排除 .pyc 和 .pyo 文件
        if (-not $_.PSIsContainer -and ($_.Name -match '\.pyc$|\.pyo$')) {
            return
        }

        # 排除 .rpyc 文件（Ren'Py 编译文件）
        if (-not $_.PSIsContainer -and $_.Name -match '\.rpyc$') {
            return
        }

        if ($_.PSIsContainer) {
            if (-not (Test-Path $targetPath)) {
                New-Item -ItemType Directory -Path $targetPath -Force | Out-Null
            }
        } else {
            $targetDir = Split-Path $targetPath -Parent
            if (-not (Test-Path $targetDir)) {
                New-Item -ItemType Directory -Path $targetDir -Force | Out-Null
            }
            Copy-Item -Path $_.FullName -Destination $targetPath -Force
        }
    }
}

# 设置默认输出目录（如果未指定）
if (-not $OutputDir) {
    $projectRoot = Split-Path $ProjectBase -Parent
    $OutputDir = Join-Path $projectRoot "dists"
    Write-Info "未指定输出目录，使用默认值: $OutputDir"
}

# 验证路径
Write-Info "验证配置..."

if (-not (Test-Path $RenPySDK)) {
    Write-Error-Custom "Ren'Py SDK 路径不存在: $RenPySDK"
    exit 1
}

if (-not (Test-Path $ProjectBase)) {
    Write-Error-Custom "项目路径不存在: $ProjectBase"
    exit 1
}

if (-not (Test-Path $DDLCBase)) {
    Write-Error-Custom "DDLC Base 路径不存在: $DDLCBase"
    exit 1
}

Write-Success "Ren'Py SDK 路径: $RenPySDK"
Write-Success "项目路径: $ProjectBase"
Write-Success "DDLC Base 路径: $DDLCBase"

# 检查 Python 或 renpy.py
$pythonExe = Join-Path $RenPySDK "lib\py3-windows-x86_64\python.exe"
$renpyPy = Join-Path $RenPySDK "renpy.py"
$renpyExe = Join-Path $RenPySDK "renpy.exe"

if (-not (Test-Path $pythonExe)) {
    Write-Warning-Custom "Python 可执行文件未找到: $pythonExe"
    if (Test-Path $renpyExe) {
        Write-Info "将尝试使用 renpy.exe"
    }
}

# 验证项目配置文件
$projectJson = Join-Path $ProjectBase "project.json"
if (-not (Test-Path $projectJson)) {
    Write-Error-Custom "找不到 project.json: $projectJson"
    exit 1
}

Write-Success "找到 project.json"

# 创建临时构建目录（必须在所有操作之前）
Write-Info "准备临时构建环境..."
$tempBuildDir = Join-Path (Get-Location) ".build_temp"

# 清理旧的临时目录
if (Test-Path $tempBuildDir) {
    Write-Warning-Custom "清理旧的临时目录..."
    Remove-Item -Path $tempBuildDir -Recurse -Force
}

# 创建新的临时目录
New-Item -ItemType Directory -Path $tempBuildDir -Force | Out-Null
Write-Success "临时构建目录已创建: $tempBuildDir"

# 1. 复制 DDLC Base 文件到临时目录
Write-Info "复制 DDLC Base 文件..."
Copy-DirectoryRecursive -Source $DDLCBase -Destination $tempBuildDir -ExcludePattern '\.gitkeep'
Write-Success "DDLC Base 文件已复制"

# 清理临时目录中的问题 .pyc 和 __pycache__（预防性）
Write-Info "清理潜在的 .pyc 文件冲突..."
$sitePackages = Join-Path $tempBuildDir "lib\python*\site-packages"
Get-ChildItem -Path $tempBuildDir -Recurse -Filter "__pycache__" -Directory -ErrorAction SilentlyContinue | ForEach-Object {
    Remove-Item -Path $_.FullName -Recurse -Force -ErrorAction SilentlyContinue
}
Get-ChildItem -Path $tempBuildDir -Recurse -Filter "*.pyc" -ErrorAction SilentlyContinue | Remove-Item -Force -ErrorAction SilentlyContinue
Write-Success "已清理 .pyc 文件"

# 2. 复制 Monika After Story 文件（覆盖重复项）
Write-Info "复制 Monika After Story 文件（覆盖重复项）..."
Copy-DirectoryRecursive -Source $ProjectBase -Destination $tempBuildDir
Write-Success "Monika After Story 文件已复制"

# 再次清理（确保没有重复的 .pyc）
Write-Info "最终清理 .pyc 文件..."
Get-ChildItem -Path $tempBuildDir -Recurse -Filter "__pycache__" -Directory -ErrorAction SilentlyContinue | ForEach-Object {
    Remove-Item -Path $_.FullName -Recurse -Force -ErrorAction SilentlyContinue
}
Get-ChildItem -Path $tempBuildDir -Recurse -Filter "*.pyc" -ErrorAction SilentlyContinue | Remove-Item -Force -ErrorAction SilentlyContinue
Write-Success ".pyc 文件已清理"

# 验证临时目录中的关键文件
$gameDir = Join-Path $tempBuildDir "game"
if (-not (Test-Path $gameDir)) {
    Write-Error-Custom "临时构建目录中找不到 game 文件夹！"
    Remove-Item -Path $tempBuildDir -Recurse -Force
    exit 1
}

# 使用临时目录作为构建路径
$buildProjectPath = $tempBuildDir
Write-Info "使用临时目录进行构建: $buildProjectPath"

# 构建命令
Write-Info "准备构建命令..."

# 转换路径为正斜杠（Ren'Py期望的格式）
$ProjectBaseForwarded = $buildProjectPath -replace '\\', '/'

# 基础命令
if (Test-Path $pythonExe) {
    $buildCmd = & {
        Write-Host "$pythonExe $renpyPy launcher android_build `"$ProjectBaseForwarded`""
    }
} else {
    $buildCmd = & {
        Write-Host "$renpyExe launcher android_build `"$ProjectBaseForwarded`""
    }
}

# 添加选项
$cmdArgs = @("launcher", "android_build", $ProjectBaseForwarded)

if ($OutputDir) {
    $OutputDirForwarded = $OutputDir -replace '\\', '/'
    $cmdArgs += "--destination"
    $cmdArgs += $OutputDirForwarded
    Write-Info "输出目录: $OutputDir"
}

if ($Bundle) {
    $cmdArgs += "--bundle"
    Write-Info "将生成 .aab bundle（而不是 .apk）"
} else {
    Write-Info "将生成 .apk 文件"
}

if ($Install) {
    $cmdArgs += "--install"
    Write-Info "构建后将安装到连接的设备"
}

if ($Launch) {
    $cmdArgs += "--launch"
    Write-Info "构建后将在设备上启动游戏"
}

if ($NoProxy) {
    Write-Info "构建代理: 已禁用"
} else {
    try {
        $proxyPreview = Get-NormalizedProxyUri -ProxyValue $Proxy
        Write-Info "构建代理: $($proxyPreview.AbsoluteUri.TrimEnd('/'))"
    } catch {
        Write-Error-Custom $_
        exit 1
    }
}

# 显示完整命令
Write-Info "完整命令:"
if (Test-Path $pythonExe) {
    Write-Host "  & `"$pythonExe`" `"$renpyPy`" $($cmdArgs -join ' ')" -ForegroundColor Yellow
} else {
    Write-Host "  & `"$renpyExe`" $($cmdArgs -join ' ')" -ForegroundColor Yellow
}

# 确认
Write-Host ""
if ($NoConfirm) {
    Write-Info "跳过确认（-NoConfirm 已启用）"
    $confirm = "y"
} else {
    $confirm = Read-Host "是否继续构建? (y/n)"
}
if ($confirm -ne "y") {
    Write-Warning-Custom "构建已取消"
    # 清理已创建的临时目录
    if (Test-Path $tempBuildDir) {
        Remove-Item -Path $tempBuildDir -Recurse -Force
    }
    exit 0
}

# 执行构建
Write-Info "开始构建 Android 版本..."

# 清理 SDK 生成的旧 APK 文件
Write-Info "清理 SDK 中的旧 APK 文件..."
$sdkApkDir = Join-Path $RenPySDK "rapt\bin"
if (Test-Path $sdkApkDir) {
    Get-ChildItem -Path $sdkApkDir -Filter "*.apk" -ErrorAction SilentlyContinue | Remove-Item -Force -ErrorAction SilentlyContinue
    Write-Success "SDK 中的旧 APK 文件已清理"
}

# 清理 Ren'Py SDK 的临时目录（避免 .pyc 文件冲突）
Write-Info "清理 SDK 临时文件..."
$sdkTmpDir = Join-Path $RenPySDK "tmp"
if (Test-Path $sdkTmpDir) {
    Remove-Item -Path $sdkTmpDir -Recurse -Force -ErrorAction SilentlyContinue
}

# 清理 Ren'Py SDK 的 PIL 目录中的所有 .pyc 文件（防止 eliminate_pycache 冲突）
Write-Info "清理 SDK PIL 目录中的 .pyc 文件..."
$pilPath = Join-Path $RenPySDK "lib\python*\site-packages\PIL"
$pilDirs = @(
    (Join-Path $RenPySDK "lib\python3.9\site-packages\PIL"),
    (Join-Path $RenPySDK "lib\python3.10\site-packages\PIL"),
    (Join-Path $RenPySDK "lib\python3.11\site-packages\PIL")
)

foreach ($dir in $pilDirs) {
    if (Test-Path $dir) {
        # 删除根目录下所有 .pyc 文件
        Get-ChildItem -Path $dir -Filter "*.pyc" -ErrorAction SilentlyContinue | Remove-Item -Force -ErrorAction SilentlyContinue
        # 删除 __pycache__ 目录
        $pycacheDir = Join-Path $dir "__pycache__"
        if (Test-Path $pycacheDir) {
            Remove-Item -Path $pycacheDir -Recurse -Force -ErrorAction SilentlyContinue
        }
    }
}
Write-Success "SDK PIL 目录已清理"

Write-Host "---" -ForegroundColor Gray

$proxyEnvBackup = $null
$pushedRenPyLocation = $false

try {
    if ($NoProxy) {
        Write-Info "跳过构建代理设置"
    } else {
        $proxyEnvBackup = Enable-BuildProxy -ProxyValue $Proxy
    }

    # 从 Ren'Py SDK 目录运行命令
    Push-Location $RenPySDK
    $pushedRenPyLocation = $true

    if (Test-Path $pythonExe) {
        & "$pythonExe" "$renpyPy" @cmdArgs
    } else {
        & "$renpyExe" @cmdArgs
    }

    $buildExitCode = $LASTEXITCODE

    Pop-Location
    $pushedRenPyLocation = $false

    if ($buildExitCode -eq 0) {
        Write-Success "Android 构建完成！"

        # 从 SDK 输出目录复制 APK 到目标目录
        $sdkApkDir = Join-Path $RenPySDK "rapt\bin"
        $generatedApks = Get-ChildItem -Path $sdkApkDir -Filter "*.apk" -ErrorAction SilentlyContinue

        if ($generatedApks) {
            Write-Info "发现生成的 APK 文件，准备复制..."

            # 确保输出目录存在
            if (-not (Test-Path $OutputDir)) {
                New-Item -ItemType Directory -Path $OutputDir -Force | Out-Null
            }

            # 复制所有 APK 到输出目录
            $generatedApks | ForEach-Object {
                $destPath = Join-Path $OutputDir $_.Name
                Copy-Item -Path $_.FullName -Destination $destPath -Force
                Write-Success "APK 已复制: $destPath"
            }
        } else {
            Write-Warning-Custom "未在 SDK 目录中发现生成的 APK 文件"
        }

        if ($OutputDir -and (Test-Path $OutputDir)) {
            Write-Info "输出目录内容:"
            Get-ChildItem $OutputDir -Filter "*.apk" -ErrorAction SilentlyContinue | ForEach-Object {
                Write-Success "文件: $($_.FullName) ($('{0:N0}' -f ($_.Length/1MB)) MB)"
            }
        }
    } else {
        Write-Error-Custom "构建失败，错误代码: $buildExitCode"
    }

    # 清理临时构建目录
    if ($buildExitCode -eq 0 -or $KeepTemp -eq $false) {
        Write-Info "清理临时构建目录..."
        if (Test-Path $tempBuildDir) {
            Remove-Item -Path $tempBuildDir -Recurse -Force -ErrorAction SilentlyContinue
            Write-Success "临时目录已清理"
        }
    }

    if ($buildExitCode -ne 0) {
        exit $buildExitCode
    }
} catch {
    Write-Error-Custom "执行构建时出错: $_"
    exit 1
} finally {
    if ($pushedRenPyLocation) {
        Pop-Location
    }

    Restore-BuildProxy -Backup $proxyEnvBackup
}

Write-Host "---" -ForegroundColor Gray
Write-Success "构建流程结束"
