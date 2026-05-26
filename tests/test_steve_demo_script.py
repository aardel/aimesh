from pathlib import Path


def test_steve_demo_script_uses_repo_root_not_current_directory():
    script = Path("scripts/steve-demo.ps1").read_text(encoding="utf-8")

    assert "Set-Location -LiteralPath $projectRoot" in script
    assert 'Join-Path $projectRoot ".venv\\Scripts\\python.exe"' in script
    assert 'Remove-Item -LiteralPath ".venv" -Recurse -Force' in script
    assert '& $python -m pip --disable-pip-version-check install -q -e ".[dev]"' in script
    assert "& $python -m aimesh demo" in script
    assert "& $python -m aimesh quote" in script
    assert "& $python -m pytest" in script
