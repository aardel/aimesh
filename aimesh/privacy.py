from __future__ import annotations

from dataclasses import replace

from .models import MeshRequest


def strip_private_context(request: MeshRequest) -> MeshRequest:
    return replace(
        request,
        user_private_context={},
        privacy_level="personal_context_removed",
    )
