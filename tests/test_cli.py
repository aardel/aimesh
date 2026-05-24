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
    assert "AI Mesh local node" in result.stdout
    assert "Smallest capable node found locally." in result.stdout
    assert "local-demo-node" in result.stdout
    assert "printing.stickers.basic" in result.stdout


def test_peer_route_cli_explains_privacy_stripping():
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "aimesh",
            "route",
            "--capability",
            "painting.oil_cleaning.basic",
            "--question",
            "How do I clean this?",
        ],
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0
    assert "Local node cannot handle this request." in result.stdout
    assert "Private context removed before peer routing." in result.stdout
    assert "peer-painting-node" in result.stdout


def test_route_cli_can_emit_json():
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "aimesh",
            "route",
            "--capability",
            "printing.stickers.basic",
            "--question",
            "Quote stickers",
            "--json",
        ],
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0
    assert '"handler_type": "local"' in result.stdout
