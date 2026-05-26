import json
from pathlib import Path

import pytest

from aimesh.learning import compile_sticker_pricing_rules
from aimesh.skills.printing import quote_stickers


def test_compile_sticker_pricing_rules_from_teacher_examples(tmp_path: Path):
    examples_path = tmp_path / "teacher_examples.json"
    examples_path.write_text(
        json.dumps(
            {
                "examples": [
                    {
                        "quantity": 100,
                        "width_mm": 50,
                        "height_mm": 30,
                        "material": "vinyl",
                        "laminated": True,
                        "total_eur": 42.0,
                    },
                    {
                        "quantity": 100,
                        "width_mm": 50,
                        "height_mm": 30,
                        "material": "vinyl",
                        "laminated": False,
                        "total_eur": 30.0,
                    },
                    {
                        "quantity": 100,
                        "width_mm": 50,
                        "height_mm": 30,
                        "material": "paper",
                        "laminated": False,
                        "total_eur": 27.0,
                    },
                    {
                        "quantity": 100,
                        "width_mm": 50,
                        "height_mm": 30,
                        "material": "polyester",
                        "laminated": False,
                        "total_eur": 36.0,
                    },
                ]
            }
        ),
        encoding="utf-8",
    )
    rules_path = tmp_path / "compiled_rules.json"

    rules = compile_sticker_pricing_rules(examples_path, rules_path)

    assert rules["setup_eur"] == pytest.approx(12.0)
    assert rules["materials"]["vinyl"]["rate_per_cm2"] == pytest.approx(0.012)
    assert rules["materials"]["paper"]["rate_per_cm2"] == pytest.approx(0.010)
    assert rules["materials"]["polyester"]["rate_per_cm2"] == pytest.approx(0.016)
    assert rules["lamination_rate_per_cm2"] == pytest.approx(0.008)
    assert rules_path.exists()


def test_quote_stickers_can_use_compiled_teacher_rules(tmp_path: Path):
    rules_path = tmp_path / "compiled_rules.json"
    rules_path.write_text(
        json.dumps(
            {
                "setup_eur": 10.0,
                "materials": {"vinyl": {"rate_per_cm2": 0.020}},
                "lamination_rate_per_cm2": 0.010,
                "source": "teacher_examples",
            }
        ),
        encoding="utf-8",
    )

    quote = quote_stickers(
        quantity=100,
        width_mm=50,
        height_mm=30,
        material="vinyl",
        laminated=True,
        rules_path=rules_path,
    )

    assert quote.total_eur == pytest.approx(55.0)
    assert "teacher_examples" in quote.reason
