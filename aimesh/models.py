from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class CapabilityCard:
    node_id: str
    capabilities: list[str]
    query_modes: list[str] = field(default_factory=lambda: ["answer_only"])
    stores_queries: bool = False
    max_block_size_mb: int = 10
    trust: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ModuleManifest:
    module_id: str
    name: str
    version: str
    capabilities: list[str]
    intents: list[str] = field(default_factory=list)
    required_fields: list[str] = field(default_factory=list)
    safety_level: str = "unknown"
    sources: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class MeshRequest:
    capability_needed: str
    question: str
    request_id: str = "local-request"
    privacy_level: str = "local_private_context_present"
    response_format: str = "structured_answer"
    user_private_context: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class MeshResponse:
    status: str
    handler_id: str
    capability: str
    answer: str
    privacy_level: str = "local_only"


@dataclass(frozen=True)
class RouteDecision:
    handler_type: str
    handler_id: str
    capability: str
    reason: str
    module_id: str = ""
