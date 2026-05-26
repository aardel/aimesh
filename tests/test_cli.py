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


def test_quote_cli_runs_local_skill():
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "aimesh",
            "quote",
            "Quote 100 stickers, 50mm x 30mm, vinyl, laminated",
            "--rules",
            "missing-rules.json",
        ],
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0
    assert "Run skill: quote_stickers" in result.stdout
    assert "Estimated price: EUR 42.00" in result.stdout
    assert "No cloud. No peer. Smallest capable node won." in result.stdout


def test_quote_cli_uses_approved_research_rules():
    subprocess.run(
        [
            sys.executable,
            "-m",
            "aimesh",
            "study",
            "examples/research/sticker_pricing_notes.md",
        ],
        text=True,
        capture_output=True,
        check=False,
    )
    subprocess.run(
        [
            sys.executable,
            "-m",
            "aimesh",
            "approve-module",
            "printing_stickers_basic",
        ],
        text=True,
        capture_output=True,
        check=False,
    )

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "aimesh",
            "quote",
            "Quote 100 stickers, 50mm x 30mm, vinyl, laminated",
        ],
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0
    assert "Estimated price: EUR 44.00" in result.stdout
    assert "research_note" in result.stdout


def test_learn_cli_compiles_teacher_examples():
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "aimesh",
            "learn-stickers",
        ],
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0
    assert "Teacher examples loaded: 5" in result.stdout
    assert "Compiled local rule table" in result.stdout
    assert "The user became the teacher." in result.stdout


def test_study_and_approve_cli_turn_research_into_active_rules():
    study = subprocess.run(
        [
            sys.executable,
            "-m",
            "aimesh",
            "study",
            "examples/research/sticker_pricing_notes.md",
        ],
        text=True,
        capture_output=True,
        check=False,
    )

    assert study.returncode == 0
    assert "Research studied: sticker_pricing_notes.md" in study.stdout
    assert "Draft module: printing_stickers_basic" in study.stdout
    assert "Waiting for teacher approval." in study.stdout

    approve = subprocess.run(
        [
            sys.executable,
            "-m",
            "aimesh",
            "approve-module",
            "printing_stickers_basic",
        ],
        text=True,
        capture_output=True,
        check=False,
    )

    assert approve.returncode == 0
    assert "Approved module: printing_stickers_basic" in approve.stdout
    assert "Research rules are now active locally." in approve.stdout
