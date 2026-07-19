# Wrapper script that automatically runs the build without confirmation
# Outputs to ./dists directory in project root
$projectRoot = Split-Path $PSScriptRoot -Parent
$outputDir = Join-Path $projectRoot "dists"
$buildScript = Join-Path $PSScriptRoot "build-android.ps1"
$projectBase = Join-Path $projectRoot "Monika After Story"
$ddlcBase = Join-Path $projectRoot ".DDLC_BASE"

& $buildScript `
    -NoConfirm `
    -OutputDir $outputDir `
    -ProjectBase $projectBase `
    -DDLCBase $ddlcBase

