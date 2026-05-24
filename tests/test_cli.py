import subprocess
import sys


def test_demo_cli_runs():
    result = subprocess.run(
        [sys.executable, "-m", "aimesh", "demo"],
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0
    assert "local-demo-node" in result.stdout
    assert "printing.stickers.basic" in result.stdout
