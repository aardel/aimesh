from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .models import CapabilityCard, ModuleManifest


def _read_json(path: str | Path) -> dict[str, Any]:
    with Path(path).open("r", encoding="utf-8") as file:
        data = json.load(file)
    if not isinstance(data, dict):
        raise ValueError(f"Expected JSON object in {path}")
    return data


def load_capability_card(path: str | Path) -> CapabilityCard:
    data = _read_json(path)
    return CapabilityCard(
        node_id=data["node_id"],
        capabilities=list(data.get("capabilities", [])),
        query_modes=list(data.get("query_modes", ["answer_only"])),
        stores_queries=bool(data.get("stores_queries", False)),
        max_block_size_mb=int(data.get("max_block_size_mb", 10)),
        trust=dict(data.get("trust", {})),
    )


def load_module_manifest(path: str | Path) -> ModuleManifest:
    data = _read_json(path)
    return ModuleManifest(
        module_id=data["module_id"],
        name=data["name"],
        version=data["version"],
        capabilities=list(data.get("capabilities", [])),
        intents=list(data.get("intents", [])),
        required_fields=list(data.get("required_fields", [])),
        safety_level=data.get("safety_level", "unknown"),
        sources=list(data.get("sources", [])),
    )


def load_peer_cards(folder: str | Path) -> list[CapabilityCard]:
    folder_path = Path(folder)
    if not folder_path.exists():
        return []
    return [
        load_capability_card(path)
        for path in sorted(folder_path.glob("*.json"))
    ]


def load_modules(folder: str | Path) -> list[ModuleManifest]:
    folder_path = Path(folder)
    if not folder_path.exists():
        return []
    return [
        load_module_manifest(path)
        for path in sorted(folder_path.glob("*.json"))
    ]
