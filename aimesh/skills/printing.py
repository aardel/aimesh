from __future__ import annotations

import re
from dataclasses import dataclass, field


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
) -> SkillQuote:
    area_cm2 = (width_mm * height_mm) / 100
    material_rate = _material_rate(material)
    setup_eur = 12.0
    print_eur = quantity * area_cm2 * material_rate
    lamination_eur = quantity * area_cm2 * 0.008 if laminated else 0.0
    total_eur = round(setup_eur + print_eur + lamination_eur, 2)

    reason_parts = [
        f"setup EUR {setup_eur:.2f}",
        f"{quantity} stickers",
        f"{width_mm}mm x {height_mm}mm",
        material,
    ]
    if laminated:
        reason_parts.append("lamination")

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


def _material_rate(material: str) -> float:
    rates = {
        "paper": 0.010,
        "vinyl": 0.012,
        "polyester": 0.016,
    }
    try:
        return rates[material.lower()]
    except KeyError as exc:
        raise ValueError(f"Unsupported sticker material: {material}") from exc
