# Deshitification local agent inventory
# Read-only: lists relevant project files and checks Python/Playwright availability.
# It does not read credentials, browser profiles, environment files, or file contents.

$ErrorActionPreference = "SilentlyContinue"
$Root = "C:\Deshitification"

if (-not (Test-Path -LiteralPath $Root -PathType Container)) {
    Write-Host "PROJECT_FOLDER_NOT_FOUND: $Root" -ForegroundColor Yellow
    exit 2
}

$Excluded = @(".git", ".venv", "venv", "__pycache__", "node_modules", ".pytest_cache")
$Extensions = @(".py", ".ps1", ".bat", ".cmd", ".js", ".mjs", ".json", ".toml", ".yaml", ".yml")
$Names = @("requirements.txt", "pyproject.toml", "Pipfile", "package.json", "playwright.config.js", "playwright.config.ts")

Write-Output "DESHITIFICATION LOCAL INVENTORY"
Write-Output "Root: $Root"
Write-Output "Checked: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss zzz')"
Write-Output ""

Write-Output "=== RELEVANT PROJECT FILES ==="
Get-ChildItem -LiteralPath $Root -File -Recurse -Force |
    Where-Object {
        $relative = $_.FullName.Substring($Root.Length).TrimStart('\')
        $parts = $relative -split '[\\/]'
        ($parts | Where-Object { $Excluded -contains $_ }).Count -eq 0 -and
        ($Extensions -contains $_.Extension.ToLowerInvariant() -or $Names -contains $_.Name)
    } |
    Sort-Object FullName |
    ForEach-Object {
        $relative = $_.FullName.Substring($Root.Length).TrimStart('\')
        "{0}  [{1} bytes]" -f $relative, $_.Length
    }

Write-Output ""
Write-Output "=== PYTHON ==="
$python = Get-Command python -ErrorAction SilentlyContinue
if ($python) {
    & python --version 2>&1
    Write-Output "Python command: $($python.Source)"
} else {
    Write-Output "Python command not found on PATH"
}

Write-Output ""
Write-Output "=== PLAYWRIGHT ==="
if ($python) {
    & python -m pip show playwright 2>&1 | Select-Object -First 8
    if ($LASTEXITCODE -ne 0) { Write-Output "Playwright Python package not detected in this Python environment." }
} else {
    Write-Output "Skipped: Python unavailable."
}

Write-Output ""
Write-Output "=== BROWSER EXECUTABLES (PATH ONLY) ==="
foreach ($browser in @("msedge", "chrome", "chromium")) {
    $cmd = Get-Command $browser -ErrorAction SilentlyContinue
    if ($cmd) { "$browser : $($cmd.Source)" } else { "$browser : not found on PATH" }
}

Write-Output ""
Write-Output "=== END ==="
