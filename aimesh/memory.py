from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class VacuumBag:
    bag_id: str
    summary: str
    important_rules: list[str] = field(default_factory=list)
    key_examples: list[str] = field(default_factory=list)
    source_refs: list[str] = field(default_factory=list)
    last_used: str = ""
    confidence: float = 0.0
    rehydration_steps: list[str] = field(default_factory=list)
    expiry_policy: str = "ask_before_using_after_12_months"
