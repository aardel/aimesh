from aimesh.models import CapabilityCard, MeshRequest
from aimesh.node import AIMeshNode


def test_node_can_handle_known_capability():
    node = AIMeshNode(
        CapabilityCard(
            node_id="local-demo-node",
            capabilities=["printing.stickers.basic"],
        )
    )

    assert node.can_handle("printing.stickers.basic") is True
    assert node.can_handle("painting.oil_cleaning.basic") is False


def test_node_returns_structured_response_for_known_capability():
    node = AIMeshNode(
        CapabilityCard(
            node_id="local-demo-node",
            capabilities=["printing.stickers.basic"],
        )
    )

    response = node.handle(
        MeshRequest(
            capability_needed="printing.stickers.basic",
            question="Quote 100 stickers",
        )
    )

    assert response.status == "handled"
    assert response.handler_id == "local-demo-node"
    assert response.capability == "printing.stickers.basic"
