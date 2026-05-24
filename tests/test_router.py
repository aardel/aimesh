from aimesh.models import CapabilityCard, MeshRequest, ModuleManifest
from aimesh.router import route


def test_router_selects_local_node_first():
    decision = route(
        MeshRequest(
            capability_needed="printing.stickers.basic",
            question="Quote stickers",
        ),
        local_card=CapabilityCard(
            node_id="local-demo-node",
            capabilities=["printing.stickers.basic"],
        ),
        peer_cards=[
            CapabilityCard(
                node_id="peer-printing-node",
                capabilities=["printing.stickers.basic"],
            )
        ],
        modules=[],
    )

    assert decision.handler_type == "local"
    assert decision.handler_id == "local-demo-node"


def test_router_selects_peer_when_local_cannot_handle():
    decision = route(
        MeshRequest(
            capability_needed="painting.oil_cleaning.basic",
            question="How do I clean this?",
        ),
        local_card=CapabilityCard(
            node_id="local-demo-node",
            capabilities=["printing.stickers.basic"],
        ),
        peer_cards=[
            CapabilityCard(
                node_id="peer-painting-node",
                capabilities=["painting.oil_cleaning.basic"],
            )
        ],
        modules=[],
    )

    assert decision.handler_type == "peer"
    assert decision.handler_id == "peer-painting-node"


def test_router_returns_none_when_no_capability_exists():
    decision = route(
        MeshRequest(
            capability_needed="painting.oil_cleaning.basic",
            question="How do I clean this?",
        ),
        local_card=CapabilityCard(
            node_id="local-demo-node",
            capabilities=["printing.stickers.basic"],
        ),
        peer_cards=[],
        modules=[],
    )

    assert decision.handler_type == "none"
    assert decision.handler_id == ""


def test_router_includes_matching_local_module():
    decision = route(
        MeshRequest(
            capability_needed="printing.stickers.basic",
            question="Quote stickers",
        ),
        local_card=CapabilityCard(
            node_id="local-demo-node",
            capabilities=["printing.stickers.basic"],
        ),
        peer_cards=[],
        modules=[
            ModuleManifest(
                module_id="printing_stickers_basic",
                name="Printing Stickers Basic",
                version="0.1.0",
                capabilities=["printing.stickers.basic"],
            )
        ],
    )

    assert decision.handler_type == "local"
    assert decision.module_id == "printing_stickers_basic"
