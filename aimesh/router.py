from __future__ import annotations

from .models import CapabilityCard, MeshRequest, ModuleManifest, RouteDecision
from .privacy import strip_private_context


def route(
    request: MeshRequest,
    local_card: CapabilityCard,
    peer_cards: list[CapabilityCard],
    modules: list[ModuleManifest],
) -> RouteDecision:
    capability = request.capability_needed
    module = _find_module(capability, modules)

    if capability in local_card.capabilities:
        return RouteDecision(
            handler_type="local",
            handler_id=local_card.node_id,
            capability=capability,
            module_id=module.module_id if module else "",
            reason="Local node advertises this capability.",
        )

    peer_request = strip_private_context(request)
    for peer_card in peer_cards:
        if peer_request.capability_needed in peer_card.capabilities:
            return RouteDecision(
                handler_type="peer",
                handler_id=peer_card.node_id,
                capability=capability,
                reason="Trusted peer advertises this capability after privacy stripping.",
            )

    return RouteDecision(
        handler_type="none",
        handler_id="",
        capability=capability,
        reason="No local or peer capability matched the request.",
    )


def _find_module(
    capability: str,
    modules: list[ModuleManifest],
) -> ModuleManifest | None:
    for module in modules:
        if capability in module.capabilities:
            return module
    return None
