from __future__ import annotations

import re
import json
from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True)
class StickerQuoteRequest:
    quantity: int
    width_mm: int
    height_mm: int
    material: str
    laminated: bool = False


@dataclass(frozen=True)
class SkillQuote:
    skill_name: str
    total_eur: float
    currency: str = "EUR"
    inputs: dict[str, object] = field(default_factory=dict)
    reason: str = ""


def parse_sticker_quote(text: str) -> StickerQuoteRequest:
    quantity_match = re.search(r"\b(\d+)\b", text, re.IGNORECASE)
    size_match = re.search(
        r"\b(\d+)\s*mm\s*[xX]\s*(\d+)\s*mm\b",
        text,
        re.IGNORECASE,
    )
    material = _find_material(text)

    if not quantity_match:
        raise ValueError("Sticker quote needs a quantity.")
    if not size_match:
        raise ValueError("Sticker quote needs a size like 50mm x 30mm.")
    if not material:
        raise ValueError("Sticker quote needs a material.")

    return StickerQuoteRequest(
        quantity=int(quantity_match.group(1)),
        width_mm=int(size_match.group(1)),
        height_mm=int(size_match.group(2)),
        material=material,
        laminated=bool(re.search(r"\blaminated|lamination\b", text, re.IGNORECASE)),
    )


def quote_stickers(
    quantity: int,
    width_mm: int,
    height_mm: int,
    material: str,
    laminated: bool = False,
    rules_path: str | Path | None = None,
    rules: dict[str, object] | None = None,
) -> SkillQuote:
    rules = rules or _load_rules(rules_path)
    area_cm2 = (width_mm * height_mm) / 100
    material_rate = _material_rate(material, rules)
    setup_eur = float(rules.get("setup_eur", 12.0))
    print_eur = quantity * area_cm2 * material_rate
    lamination_rate = float(rules.get("lamination_rate_per_cm2", 0.008))
    lamination_eur = quantity * area_cm2 * lamination_rate if laminated else 0.0
    total_eur = round(setup_eur + print_eur + lamination_eur, 2)

    reason_parts = [
        f"setup EUR {setup_eur:.2f}",
        f"{quantity} stickers",
        f"{width_mm}mm x {height_mm}mm",
        material,
    ]
    if laminated:
        reason_parts.append("lamination")
    if rules.get("source"):
        reason_parts.append(str(rules["source"]))

    return SkillQuote(
        skill_name="quote_stickers",
        total_eur=total_eur,
        inputs={
            "quantity": quantity,
            "width_mm": width_mm,
            "height_mm": height_mm,
            "material": material,
            "laminated": laminated,
        },
        reason="Calculated from " + ", ".join(reason_parts) + ".",
    )


def _find_material(text: str) -> str:
    known_materials = ["vinyl", "paper", "polyester"]
    lowered = text.lower()
    for material in known_materials:
        if material in lowered:
            return material
    return ""


def _load_rules(rules_path: str | Path | None) -> dict[str, object]:
    if rules_path:
        return json.loads(Path(rules_path).read_text(encoding="utf-8"))
    return {
        "setup_eur": 12.0,
        "materials": {
            "paper": {"rate_per_cm2": 0.010},
            "vinyl": {"rate_per_cm2": 0.012},
            "polyester": {"rate_per_cm2": 0.016},
        },
        "lamination_rate_per_cm2": 0.008,
    }


def _material_rate(material: str, rules: dict[str, object]) -> float:
    rates = rules.get("materials", {})
    try:
        material_rule = rates[material.lower()]  # type: ignore[index]
        return float(material_rule["rate_per_cm2"])
    except (KeyError, TypeError) as exc:
        raise ValueError(f"Unsupported sticker material: {material}") from exc
