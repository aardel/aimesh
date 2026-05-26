from __future__ import annotations

import json
import re
import urllib.request
from pathlib import Path
from typing import Any

from .skills.printing import parse_sticker_quote, quote_stickers


def study_research_note(source: str | Path, draft_path: str | Path) -> dict[str, Any]:
    text, source_name = _read_source(source)
    rule_block = _extract_rule_block(text)
    source_refs = _extract_values(text, "source")
    checked = _extract_first_value(text, "checked")

    tests = [_run_quote_test(test, rule_block) for test in rule_block.get("tests", [])]
    draft = {
        "status": "draft_waiting_for_teacher_approval",
        "module_id": rule_block["module_id"],
        "source_name": source_name,
        "source_refs": source_refs,
        "checked": checked,
        "rules": {
            "setup_eur": rule_block["setup_eur"],
            "materials": rule_block["materials"],
            "lamination_rate_per_cm2": rule_block["lamination_rate_per_cm2"],
            "source": "research_note",
            "source_refs": source_refs,
            "checked": checked,
        },
        "tests": tests,
    }

    Path(draft_path).parent.mkdir(parents=True, exist_ok=True)
    Path(draft_path).write_text(json.dumps(draft, indent=2), encoding="utf-8")
    return draft


def approve_research_draft(
    draft_path: str | Path,
    rules_path: str | Path,
) -> dict[str, Any]:
    draft = json.loads(Path(draft_path).read_text(encoding="utf-8"))
    if draft.get("status") != "draft_waiting_for_teacher_approval":
        raise ValueError("Research draft is not waiting for approval.")
    if not all(test.get("passed") for test in draft.get("tests", [])):
        raise ValueError("Research draft tests must pass before approval.")

    Path(rules_path).parent.mkdir(parents=True, exist_ok=True)
    Path(rules_path).write_text(json.dumps(draft["rules"], indent=2), encoding="utf-8")
    return {
        "status": "approved",
        "module_id": draft["module_id"],
        "rules_path": str(rules_path),
    }


def _read_source(source: str | Path) -> tuple[str, str]:
    source_text = str(source)
    if source_text.startswith(("http://", "https://")):
        with urllib.request.urlopen(source_text, timeout=10) as response:
            return response.read().decode("utf-8"), source_text
    path = Path(source)
    return path.read_text(encoding="utf-8"), path.name


def _extract_rule_block(text: str) -> dict[str, Any]:
    match = re.search(r"```aimesh-rules\s*(.*?)```", text, re.DOTALL)
    if not match:
        raise ValueError("Research note needs an aimesh-rules block.")
    return json.loads(match.group(1))


def _extract_values(text: str, key: str) -> list[str]:
    values = []
    for line in text.splitlines():
        if line.lower().startswith(f"{key}:"):
            values.append(line.split(":", 1)[1].strip())
    return values


def _extract_first_value(text: str, key: str) -> str:
    values = _extract_values(text, key)
    return values[0] if values else ""


def _run_quote_test(test: dict[str, Any], rules: dict[str, Any]) -> dict[str, Any]:
    request = parse_sticker_quote(test["text"])
    quote = quote_stickers(
        quantity=request.quantity,
        width_mm=request.width_mm,
        height_mm=request.height_mm,
        material=request.material,
        laminated=request.laminated,
        rules=rules,
    )
    expected = float(test["expected_total_eur"])
    return {
        "text": test["text"],
        "expected_total_eur": expected,
        "actual_total_eur": quote.total_eur,
        "passed": quote.total_eur == expected,
    }
