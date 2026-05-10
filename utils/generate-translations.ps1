# Ren'Py translation generation script for MAS (Monika After Story).
#
# Usage:
#   .\generate-translations.ps1
#   .\generate-translations.ps1 -Language chinese2
#   .\generate-translations.ps1 -KeepSourceText
#   .\generate-translations.ps1 -StringsOnly
#
# Ren'Py's launcher does not expose its "Generate Translations" workflow as a
# command in this SDK, so this script installs a small launcher-side command
# patch and then calls it non-interactively.

param(
    [string]$RenPySDK = "J:\Renpy\renpy-8.2.3-sdk",
    [string]$ProjectBase = "J:\MAS\MonikaModDev-zhCN\Monika After Story",
    [string]$DDLCBase = "J:\MAS\MonikaModDev-zhCN\.DDLC_BASE",
    [string]$Language = "chinese",
    [switch]$KeepSourceText = $false,
    [switch]$StringsOnly = $false,
    [switch]$NoTodo = $false,
    [switch]$KeepTemp = $false
)

$ErrorActionPreference = "Stop"
$pushedRenPyLocation = $false

function Write-Success {
    param([string]$Message)
    Write-Host "[OK] $Message" -ForegroundColor Green
}

function Write-Error-Custom {
    param([string]$Message)
    Write-Host "[ERROR] $Message" -ForegroundColor Red
}

function Write-Info {
    param([string]$Message)
    Write-Host "[INFO] $Message" -ForegroundColor Cyan
}

function Write-Warning-Custom {
    param([string]$Message)
    Write-Host "[WARN] $Message" -ForegroundColor Yellow
}

function Copy-DirectoryRecursive {
    param(
        [string]$Source,
        [string]$Destination,
        [string]$ExcludePattern = $null
    )

    if (-not (Test-Path -LiteralPath $Source)) {
        Write-Warning-Custom "Source path does not exist: $Source"
        return
    }

    if (-not (Test-Path -LiteralPath $Destination)) {
        New-Item -ItemType Directory -Path $Destination -Force | Out-Null
    }

    Get-ChildItem -LiteralPath $Source -Recurse | ForEach-Object {
        $relativePath = $_.FullName.Substring($Source.Length).TrimStart('\')
        $targetPath = Join-Path $Destination $relativePath

        if ($ExcludePattern -and $_.Name -match $ExcludePattern) {
            return
        }

        if ($_.PSIsContainer -and $_.Name -eq "__pycache__") {
            return
        }

        if (-not $_.PSIsContainer -and ($_.Name -match '\.pyc$|\.pyo$|\.rpyc$')) {
            return
        }

        if ($_.PSIsContainer) {
            if (-not (Test-Path -LiteralPath $targetPath)) {
                New-Item -ItemType Directory -Path $targetPath -Force | Out-Null
            }
        } else {
            $targetDir = Split-Path $targetPath -Parent
            if (-not (Test-Path -LiteralPath $targetDir)) {
                New-Item -ItemType Directory -Path $targetDir -Force | Out-Null
            }
            Copy-Item -LiteralPath $_.FullName -Destination $targetPath -Force
        }
    }
}

function Install-LauncherTranslationPatch {
    param([string]$SdkPath)

    $launcherGameDir = Join-Path $SdkPath "launcher\game"
    if (-not (Test-Path -LiteralPath $launcherGameDir)) {
        throw "Ren'Py launcher game directory not found: $launcherGameDir"
    }

    $patchPath = Join-Path $launcherGameDir "zz_mas_cli_translation.rpy"
    $patchContent = @'
# MAS_GENERATE_TRANSLATIONS_PATCH_V2
# Installed by MonikaModDev-zhCN/utils/generate-translations.ps1.
# This adds a non-interactive launcher command that forwards to the project's
# built-in translation generator.

init python:
    import os
    import subprocess
    import sys

    def mas_generate_translations_command():
        ap = renpy.arguments.ArgumentParser(description="Generates or updates project translations through the launcher.")
        ap.add_argument("source_project", help="The merged project directory to scan.")
        ap.add_argument("language", help="The language to generate translations for.")
        ap.add_argument("--empty", action="store_true", help="Generate empty strings instead of copying source text.")
        ap.add_argument("--strings-only", action="store_true", help="Only translate strings, not dialogue.")
        ap.add_argument("--no-todo", action="store_true", help="Do not add TODO update markers.")
        args = ap.parse_args()

        translate_args = [ "translate", args.language ]

        if args.empty:
            translate_args.append("--empty")

        if args.strings_only:
            translate_args.append("--strings-only")

        if args.no_todo:
            translate_args.append("--no-todo")

        cmd = [ sys.executable, sys.argv[0], args.source_project ]
        cmd.extend(translate_args)

        environ = dict(os.environ)
        environ["RENPY_LAUNCHER_LANGUAGE"] = _preferences.language or "english"
        environ["MAS_GENERATE_TRANSLATIONS"] = "1"

        if hasattr(sys, "renpy_executable"):
            environ = { k : v for k, v in environ.items() if not k.startswith("PYTHON") }

        encoded_environ = { }
        for k, v in environ.items():
            if v is not None:
                encoded_environ[renpy.fsencode(k)] = renpy.fsencode(v)

        returncode = subprocess.call([ renpy.fsencode(i) for i in cmd ], env=encoded_environ)

        if returncode:
            raise Exception("Translation generation failed with exit code {}.".format(returncode))

        return False

    renpy.arguments.register_command("mas_generate_translations", mas_generate_translations_command)
'@

    $needsWrite = $true
    if (Test-Path -LiteralPath $patchPath) {
        $existing = Get-Content -LiteralPath $patchPath -Raw
        $needsWrite = ($existing -ne $patchContent)
    }

    if ($needsWrite) {
        Set-Content -LiteralPath $patchPath -Value $patchContent -Encoding UTF8
        Write-Success "Launcher CLI patch installed: $patchPath"
    } else {
        Write-Success "Launcher CLI patch already installed: $patchPath"
    }
}

try {
    if ($Language -notmatch '^\w+$') {
        throw "Language should only contain ASCII letters, digits, and underscores: $Language"
    }

    Write-Info "Validating paths..."

    if (-not (Test-Path -LiteralPath $RenPySDK)) {
        throw "Ren'Py SDK path does not exist: $RenPySDK"
    }

    if (-not (Test-Path -LiteralPath $ProjectBase)) {
        throw "Project path does not exist: $ProjectBase"
    }

    if (-not (Test-Path -LiteralPath $DDLCBase)) {
        throw "DDLC base path does not exist: $DDLCBase"
    }

    $pythonExe = Join-Path $RenPySDK "lib\py3-windows-x86_64\python.exe"
    $renpyPy = Join-Path $RenPySDK "renpy.py"
    $renpyExe = Join-Path $RenPySDK "renpy.exe"

    if ((-not (Test-Path -LiteralPath $pythonExe)) -and (-not (Test-Path -LiteralPath $renpyExe))) {
        throw "Neither Ren'Py Python nor renpy.exe was found under: $RenPySDK"
    }

    $projectJson = Join-Path $ProjectBase "project.json"
    if (-not (Test-Path -LiteralPath $projectJson)) {
        throw "project.json not found: $projectJson"
    }

    Write-Success "Ren'Py SDK path: $RenPySDK"
    Write-Success "Project path: $ProjectBase"
    Write-Success "DDLC base path: $DDLCBase"
    Write-Success "Language: $Language"

    Install-LauncherTranslationPatch -SdkPath $RenPySDK

    $projectRoot = Split-Path $ProjectBase -Parent
    $tempBuildDir = Join-Path $projectRoot ".translation_temp"

    Write-Info "Preparing temporary merged project: $tempBuildDir"

    if (Test-Path -LiteralPath $tempBuildDir) {
        Write-Warning-Custom "Removing old temporary translation directory..."
        Remove-Item -LiteralPath $tempBuildDir -Recurse -Force
    }

    New-Item -ItemType Directory -Path $tempBuildDir -Force | Out-Null

    Write-Info "Copying DDLC base files..."
    Copy-DirectoryRecursive -Source $DDLCBase -Destination $tempBuildDir -ExcludePattern '\.gitkeep'
    Write-Success "DDLC base files copied"

    Write-Info "Copying Monika After Story files over DDLC base..."
    Copy-DirectoryRecursive -Source $ProjectBase -Destination $tempBuildDir
    Write-Success "Project files copied"

    Write-Info "Cleaning compiled Python/Ren'Py cache files from the temporary project..."
    Get-ChildItem -LiteralPath $tempBuildDir -Recurse -Filter "__pycache__" -Directory -ErrorAction SilentlyContinue | ForEach-Object {
        Remove-Item -LiteralPath $_.FullName -Recurse -Force -ErrorAction SilentlyContinue
    }
    Get-ChildItem -LiteralPath $tempBuildDir -Recurse -Include "*.pyc","*.pyo","*.rpyc" -File -ErrorAction SilentlyContinue | Remove-Item -Force -ErrorAction SilentlyContinue
    Write-Success "Temporary cache files cleaned"

    $gameDir = Join-Path $tempBuildDir "game"
    if (-not (Test-Path -LiteralPath $gameDir)) {
        throw "Temporary merged project does not contain a game directory: $gameDir"
    }

    $translationBootstrapPath = Join-Path $gameDir "00mas_translation_generation.rpy"
    $translationBootstrapContent = @'
# Created by utils/generate-translations.ps1 in the temporary project only.
# MAS checks for DDLC archives during desktop startup. Android builds skip that
# check, but translation generation runs in desktop mode, so mark the archives
# present only for this non-interactive translation process.
init -101 python:
    import os

    if os.environ.get("MAS_GENERATE_TRANSLATIONS") == "1":
        for archive in ("audio", "images", "fonts"):
            if archive not in config.archives:
                config.archives.append(archive)
'@
    Set-Content -LiteralPath $translationBootstrapPath -Value $translationBootstrapContent -Encoding UTF8
    Write-Success "Temporary translation bootstrap added: $translationBootstrapPath"

    $sourceProject = $tempBuildDir -replace '\\', '/'
    $cmdArgs = @("launcher", "mas_generate_translations", $sourceProject, $Language)

    if (-not $KeepSourceText) {
        $cmdArgs += "--empty"
        Write-Info "Generated translation strings will be empty."
    } else {
        Write-Info "Generated translation strings will keep source text."
    }

    if ($StringsOnly) {
        $cmdArgs += "--strings-only"
        Write-Info "Only string translations will be generated."
    }

    if ($NoTodo) {
        $cmdArgs += "--no-todo"
        Write-Info "TODO update markers will be omitted."
    }

    Write-Info "Running Ren'Py translation generation command:"
    if (Test-Path -LiteralPath $pythonExe) {
        Write-Host "  & `"$pythonExe`" `"$renpyPy`" $($cmdArgs -join ' ')" -ForegroundColor Yellow
    } else {
        Write-Host "  & `"$renpyExe`" $($cmdArgs -join ' ')" -ForegroundColor Yellow
    }

    Push-Location $RenPySDK
    $script:pushedRenPyLocation = $true

    if (Test-Path -LiteralPath $pythonExe) {
        & "$pythonExe" "$renpyPy" @cmdArgs
    } else {
        & "$renpyExe" @cmdArgs
    }

    $translationExitCode = $LASTEXITCODE
    Pop-Location
    $script:pushedRenPyLocation = $false

    if ($translationExitCode -ne 0) {
        throw "Translation generation failed with exit code: $translationExitCode"
    }

    $tlRoot = "game\tl"
    $generatedLanguageDir = Join-Path (Join-Path $tempBuildDir $tlRoot) $Language
    $targetLanguageDir = Join-Path (Join-Path $ProjectBase $tlRoot) $Language

    if (-not (Test-Path -LiteralPath $generatedLanguageDir)) {
        throw "Generated translation directory was not found: $generatedLanguageDir"
    }

    Write-Info "Copying generated translation files back to the real project..."
    Copy-DirectoryRecursive -Source $generatedLanguageDir -Destination $targetLanguageDir
    Write-Success "Translations copied to: $targetLanguageDir"

    $rpyCount = (Get-ChildItem -LiteralPath $targetLanguageDir -Recurse -Filter "*.rpy" -File -ErrorAction SilentlyContinue | Measure-Object).Count
    Write-Success "Generated/updated $rpyCount translation files for '$Language'."

    if (-not $KeepTemp) {
        Write-Info "Cleaning temporary translation directory..."
        Remove-Item -LiteralPath $tempBuildDir -Recurse -Force -ErrorAction SilentlyContinue
        Write-Success "Temporary directory cleaned"
    } else {
        Write-Warning-Custom "Temporary directory kept: $tempBuildDir"
    }
} catch {
    Write-Error-Custom $_
    exit 1
} finally {
    if ($script:pushedRenPyLocation) {
        Pop-Location
        $script:pushedRenPyLocation = $false
    }
}
