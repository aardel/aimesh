from pathlib import Path


def test_steve_demo_script_uses_repo_root_not_current_directory():
    script = Path("scripts/steve-demo.ps1").read_text(encoding="utf-8")

    assert "Set-Location -LiteralPath $projectRoot" in script
    assert 'Join-Path $projectRoot ".venv\\Scripts\\python.exe"' in script
    assert 'Remove-Item -LiteralPath ".venv" -Recurse -Force' in script
    assert '& $python -m pip --disable-pip-version-check install -q -e ".[dev]"' in script
    assert 'throw "Could not install AI Mesh into the repo environment."' in script
    assert 'Join-Path $env:VIRTUAL_ENV "Scripts\\python.exe"' in script
    assert '& $activePython -c "import aimesh" 2>$null' in script
    assert "Active shell environment already has AI Mesh." in script
    assert "Installing AI Mesh into the active shell environment" in script
    assert '& $activePython -m pip --disable-pip-version-check install -q --no-deps -e "."' in script
    assert 'throw "Could not install AI Mesh into the active shell environment."' in script
    assert "After this launcher, your current shell can run:" in script
    assert "& $python -m aimesh demo" in script
    assert "& $python -m aimesh quote" in script
    assert "& $python -m pytest" in script
