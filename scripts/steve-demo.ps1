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
        Push-Location -LiteralPath $env:TEMP
        $previousErrorActionPreference = $ErrorActionPreference
        $ErrorActionPreference = "Continue"
        & $activePython -c "import aimesh" 2>$null
        $activeImportExitCode = $LASTEXITCODE
        $ErrorActionPreference = $previousErrorActionPreference
        Pop-Location
        if ($activeImportExitCode -eq 0) {
            Write-Host "Active shell environment already has AI Mesh."
        }
        else {
            Write-Host "Installing AI Mesh into the active shell environment..."
            $previousErrorActionPreference = $ErrorActionPreference
            $ErrorActionPreference = "Continue"
            & $activePython -m pip --disable-pip-version-check install -q --no-deps -e "." *> $null
            $activeInstallExitCode = $LASTEXITCODE
            $ErrorActionPreference = $previousErrorActionPreference
            if ($activeInstallExitCode -ne 0) {
                Write-Host "Active shell environment could not be updated. Use the repo Python command shown below."
                $activePython = $null
            }
        }
    }
}

Write-Host ""
Write-Host "Demo 1: user examples become local rules"
& $python -m aimesh learn-stickers

Write-Host ""
Write-Host "Demo 2: local smallest-capable-node routing"
& $python -m aimesh demo

Write-Host ""
Write-Host "Demo 3: peer routing with private context stripped"
& $python -m aimesh route --capability painting.oil_cleaning.basic --question "How do I clean this?"

Write-Host ""
Write-Host "Demo 4: learned rules become local execution"
& $python -m aimesh quote "Quote 100 stickers, 50mm x 30mm, vinyl, laminated"

Write-Host ""
Write-Host "Verification"
$pytestTemp = Join-Path $env:TEMP "aimesh-pytest-$PID"
& $python -m pytest --basetemp $pytestTemp
if ($LASTEXITCODE -ne 0) {
    throw "AI Mesh verification failed."
}

Write-Host ""
Write-Host "Follow-up command that works from any folder:"
Write-Host "  & `"$python`" -m aimesh quote `"Quote 100 stickers, 50mm x 30mm, vinyl, laminated`""
if ($activePython) {
    Write-Host ""
    Write-Host "Your active shell Python can also run:"
    Write-Host '  python -m aimesh quote "Quote 100 stickers, 50mm x 30mm, vinyl, laminated"'
}
