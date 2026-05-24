from __future__ import annotations

from .models import CapabilityCard, MeshRequest, MeshResponse


class AIMeshNode:
    def __init__(self, capability_card: CapabilityCard):
        self.capability_card = capability_card

    @property
    def node_id(self) -> str:
        return self.capability_card.node_id

    def can_handle(self, capability: str) -> bool:
        return capability in self.capability_card.capabilities

    def handle(self, request: MeshRequest) -> MeshResponse:
        if not self.can_handle(request.capability_needed):
            return MeshResponse(
                status="cannot_handle",
                handler_id=self.node_id,
                capability=request.capability_needed,
                answer="This node does not advertise the requested capability.",
            )

        return MeshResponse(
            status="handled",
            handler_id=self.node_id,
            capability=request.capability_needed,
            answer="Prototype node accepted the request. Domain answer generation comes later.",
        )
