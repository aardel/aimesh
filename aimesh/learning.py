from __future__ import annotations

import json
from pathlib import Path
from typing import Any


DEFAULT_SETUP_EUR = 12.0


def compile_sticker_pricing_rules(
    examples_path: str | Path,
    rules_path: str | Path,
) -> dict[str, Any]:
    examples = _load_examples(examples_path)
    material_rates: dict[str, float] = {}
    lamination_rates: list[float] = []

    for example in examples:
        area_cm2 = _area_cm2(example)
        material = str(example["material"]).lower()
        total_eur = float(example["total_eur"])
        base_rate = (total_eur - DEFAULT_SETUP_EUR) / (
            int(example["quantity"]) * area_cm2
        )

        if example.get("laminated"):
            unlaminated_rate = _find_unlaminated_rate(material, examples)
            if unlaminated_rate is not None:
                material_rates[material] = unlaminated_rate
                lamination_rates.append(round(base_rate - unlaminated_rate, 6))
            else:
                material_rates[material] = round(base_rate, 6)
        else:
            material_rates[material] = round(base_rate, 6)

    rules = {
        "setup_eur": DEFAULT_SETUP_EUR,
        "materials": {
            material: {"rate_per_cm2": rate}
            for material, rate in sorted(material_rates.items())
        },
        "lamination_rate_per_cm2": round(_average(lamination_rates), 6),
        "source": "teacher_examples",
        "example_count": len(examples),
    }

    Path(rules_path).parent.mkdir(parents=True, exist_ok=True)
    Path(rules_path).write_text(json.dumps(rules, indent=2), encoding="utf-8")
    return rules


def _load_examples(examples_path: str | Path) -> list[dict[str, Any]]:
    data = json.loads(Path(examples_path).read_text(encoding="utf-8"))
    examples = data.get("examples", [])
    if not examples:
        raise ValueError("No teacher examples found.")
    return examples


def _area_cm2(example: dict[str, Any]) -> float:
    return (int(example["width_mm"]) * int(example["height_mm"])) / 100


def _find_unlaminated_rate(
    material: str,
    examples: list[dict[str, Any]],
) -> float | None:
    for example in examples:
        if str(example["material"]).lower() == material and not example.get("laminated"):
            return round(
                (float(example["total_eur"]) - DEFAULT_SETUP_EUR)
                / (int(example["quantity"]) * _area_cm2(example)),
                6,
            )
    return None


def _average(values: list[float]) -> float:
    if not values:
        return 0.0
    return sum(values) / len(values)
