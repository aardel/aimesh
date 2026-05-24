from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from pathlib import Path

from .loaders import load_capability_card, load_modules, load_peer_cards
from .models import MeshRequest
from .router import route


PROJECT_ROOT = Path(__file__).resolve().parents[1]
EXAMPLES_ROOT = PROJECT_ROOT / "examples"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="aimesh")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("demo", help="Run the local AI Mesh routing demo.")

    route_parser = subparsers.add_parser("route", help="Route a structured request.")
    route_parser.add_argument("--capability", required=True)
    route_parser.add_argument("--question", required=True)

    args = parser.parse_args(argv)

    if args.command == "demo":
        return run_demo()
    if args.command == "route":
        return run_route(args.capability, args.question)

    parser.error("Unknown command")
    return 2


def run_demo() -> int:
    return run_route(
        "printing.stickers.basic",
        "Can the local node quote a simple sticker job?",
    )


def run_route(capability: str, question: str) -> int:
    local_card = load_capability_card(EXAMPLES_ROOT / "local_node" / "capability_card.json")
    peer_cards = load_peer_cards(EXAMPLES_ROOT / "peer_nodes")
    modules = load_modules(EXAMPLES_ROOT / "modules")
    request = MeshRequest(
        capability_needed=capability,
        question=question,
        user_private_context={"demo_note": "This must stay local."},
    )
    decision = route(request, local_card, peer_cards, modules)
    print(json.dumps(asdict(decision), indent=2))
    return 0
