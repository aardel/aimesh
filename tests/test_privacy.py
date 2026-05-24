from aimesh.models import MeshRequest
from aimesh.privacy import strip_private_context


def test_strip_private_context_removes_private_payload():
    request = MeshRequest(
        capability_needed="painting.oil_cleaning.basic",
        question="How do I clean this?",
        user_private_context={"customer": "Secret Customer"},
    )

    stripped = strip_private_context(request)

    assert stripped.user_private_context == {}
    assert stripped.capability_needed == request.capability_needed
    assert stripped.privacy_level == "personal_context_removed"
