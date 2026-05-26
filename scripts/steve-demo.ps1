$ErrorActionPreference = "Stop"

$repoUrl = "https://github.com/aardel/aimesh.git"
$repoName = "Ai Mesh"

function Get-AIMeshRoot {
    if ($PSScriptRoot) {
        $scriptRoot = Resolve-Path -LiteralPath $PSScriptRoot
        $fromScript = Resolve-Path -LiteralPath (Join-Path $scriptRoot "..")
        if (Test-Path -LiteralPath (Join-Path $fromScript "pyproject.toml")) {
            return $fromScript.Path
        }
    }

    $candidates = @()
    if ($env:OneDrive) {
        $candidates += (Join-Path $env:OneDrive "Documents\$repoName")
    }
    $candidates += (Join-Path $HOME "Documents\$repoName")
    $candidates += (Join-Path $HOME "aimesh")

    foreach ($candidate in $candidates) {
        if (Test-Path -LiteralPath (Join-Path $candidate "pyproject.toml")) {
            return (Resolve-Path -LiteralPath $candidate).Path
        }
    }

    $target = $candidates[0]
    $parent = Split-Path -Parent $target
    if (-not (Test-Path -LiteralPath $parent)) {
        New-Item -ItemType Directory -Path $parent | Out-Null
    }

    Write-Host "AI Mesh repo not found. Cloning to: $target"
    git clone $repoUrl $target
    return (Resolve-Path -LiteralPath $target).Path
}

$projectRoot = Get-AIMeshRoot
Set-Location -LiteralPath $projectRoot

Write-Host ""
Write-Host "AI Mesh prototype bench"
Write-Host "Repo: $projectRoot"
Write-Host ""

$python = Join-Path $projectRoot ".venv\Scripts\python.exe"

if ((Test-Path -LiteralPath ".venv") -and -not (Test-Path -LiteralPath $python)) {
    Write-Host "Removing incomplete Python environment..."
    Remove-Item -LiteralPath ".venv" -Recurse -Force
}

if (-not (Test-Path -LiteralPath $python)) {
    Write-Host "Creating local Python environment..."
    py -m venv .venv
}

Write-Host "Installing AI Mesh from the repo..."
& $python -m pip --disable-pip-version-check install -q -e ".[dev]"
if ($LASTEXITCODE -ne 0) {
    throw "Could not install AI Mesh into the repo environment."
}

$activePython = $null
if ($env:VIRTUAL_ENV) {
    $candidatePython = Join-Path $env:VIRTUAL_ENV "Scripts\python.exe"
    if ((Test-Path -LiteralPath $candidatePython) -and ($candidatePython -ne $python)) {
        $activePython = $candidatePython
        & $activePython -c "import aimesh" 2>$null
        if ($LASTEXITCODE -eq 0) {
            Write-Host "Active shell environment already has AI Mesh."
        }
        else {
            Write-Host "Installing AI Mesh into the active shell environment..."
            & $activePython -m pip --disable-pip-version-check install -q --no-deps -e "."
            if ($LASTEXITCODE -ne 0) {
                throw "Could not install AI Mesh into the active shell environment."
            }
        }
    }
}

Write-Host ""
Write-Host "Demo 1: local smallest-capable-node routing"
& $python -m aimesh demo

Write-Host ""
Write-Host "Demo 2: peer routing with private context stripped"
& $python -m aimesh route --capability painting.oil_cleaning.basic --question "How do I clean this?"

Write-Host ""
Write-Host "Demo 3: module knowledge becomes local execution"
& $python -m aimesh quote "Quote 100 stickers, 50mm x 30mm, vinyl, laminated"

Write-Host ""
Write-Host "Verification"
& $python -m pytest
if ($LASTEXITCODE -ne 0) {
    throw "AI Mesh verification failed."
}

if ($activePython) {
    Write-Host ""
    Write-Host "After this launcher, your current shell can run:"
    Write-Host '  python -m aimesh quote "Quote 100 stickers, 50mm x 30mm, vinyl, laminated"'
}
