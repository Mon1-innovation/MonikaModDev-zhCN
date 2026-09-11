param(
    [string]$ScriptPath = (Join-Path $PSScriptRoot "generate-translations.ps1")
)

$ErrorActionPreference = "Stop"

function Assert-Contains {
    param(
        [string]$Content,
        [string]$Pattern,
        [string]$Message
    )

    if ($Content -notmatch [regex]::Escape($Pattern)) {
        throw $Message
    }
}

if (-not (Test-Path -LiteralPath $ScriptPath)) {
    throw "Missing script: $ScriptPath"
}

$content = Get-Content -LiteralPath $ScriptPath -Raw

Assert-Contains $content ".translation_temp" "Script should use a dedicated temporary merged project directory."
Assert-Contains $content "Copy-DirectoryRecursive" "Script should merge DDLC base and MAS project files."
Assert-Contains $content "zz_mas_cli_translation.rpy" "Script should install the Ren'Py launcher CLI patch."
Assert-Contains $content "mas_generate_translations" "Script should call the patched launcher translation command."
Assert-Contains $content "MAS_GENERATE_TRANSLATIONS" "Script should mark the inner Ren'Py process as translation generation."
Assert-Contains $content "00mas_translation_generation.rpy" "Script should add a temporary bootstrap before MAS splash archive checks."
Assert-Contains $content "launcher" "Script should invoke Ren'Py through the launcher project."
Assert-Contains $content "game\tl" "Script should copy generated translation files back to the real project."

Write-Host "generate-translations.ps1 static checks passed."
