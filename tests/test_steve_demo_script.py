from pathlib import Path


def test_steve_demo_script_uses_repo_root_not_current_directory():
    script = Path("scripts/steve-demo.ps1").read_text(encoding="utf-8")

    assert "Set-Location -LiteralPath $projectRoot" in script
    assert 'Join-Path $projectRoot ".venv\\Scripts\\python.exe"' in script
    assert 'Remove-Item -LiteralPath ".venv" -Recurse -Force' in script
    assert '& $python -m pip --disable-pip-version-check install -q -e ".[dev]"' in script
    assert 'throw "Could not install AI Mesh into the repo environment."' in script
    assert 'Join-Path $env:VIRTUAL_ENV "Scripts\\python.exe"' in script
    assert "Push-Location -LiteralPath $env:TEMP" in script
    assert '$previousErrorActionPreference = $ErrorActionPreference' in script
    assert '$ErrorActionPreference = "Continue"' in script
    assert '& $activePython -c "import aimesh" 2>$null' in script
    assert "$activeImportExitCode = $LASTEXITCODE" in script
    assert "$ErrorActionPreference = $previousErrorActionPreference" in script
    assert "Pop-Location" in script
    assert "Active shell environment already has AI Mesh." in script
    assert "Installing AI Mesh into the active shell environment" in script
    assert '& $activePython -m pip --disable-pip-version-check install -q --no-deps -e "." *> $null' in script
    assert "$activeInstallExitCode = $LASTEXITCODE" in script
    assert "Active shell environment could not be updated. Use the repo Python command shown below." in script
    assert "Follow-up command that works from any folder:" in script
    assert "Your active shell Python can also run:" in script
    assert "& $python -m aimesh demo" in script
    assert "& $python -m aimesh quote" in script
    assert "& $python -m pytest" in script
    assert '$pytestTemp = Join-Path $env:TEMP "aimesh-pytest-$PID"' in script
    assert "& $python -m pytest --basetemp $pytestTemp" in script
