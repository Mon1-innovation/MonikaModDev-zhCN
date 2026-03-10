# Wrapper script that automatically runs the build without confirmation
# Outputs to ./dists directory in project root
$projectRoot = Split-Path (Split-Path $PSScriptRoot -Parent) -Parent
$outputDir = Join-Path $projectRoot "dists"
& "J:\MAS\MonikaModDev-zhCN\utils\build-android.ps1" -NoConfirm -OutputDir $outputDir


