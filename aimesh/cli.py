from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from pathlib import Path

from .learning import compile_sticker_pricing_rules
from .loaders import load_capability_card, load_modules, load_peer_cards
from .models import MeshRequest
from .research import approve_research_draft, study_research_note
from .router import route
from .skills.printing import parse_sticker_quote, quote_stickers


PROJECT_ROOT = Path(__file__).resolve().parents[1]
EXAMPLES_ROOT = PROJECT_ROOT / "examples"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="aimesh")
    subparsers = parser.add_subparsers(dest="command", required=True)

    demo_parser = subparsers.add_parser("demo", help="Run the local AI Mesh routing demo.")
    demo_parser.add_argument("--json", action="store_true", help="Print the raw route decision.")

    route_parser = subparsers.add_parser("route", help="Route a structured request.")
    route_parser.add_argument("--capability", required=True)
    route_parser.add_argument("--question", required=True)
    route_parser.add_argument("--json", action="store_true", help="Print the raw route decision.")

    quote_parser = subparsers.add_parser("quote", help="Run the local sticker quote skill.")
    quote_parser.add_argument("text", help="Sticker quote request.")
    quote_parser.add_argument(
        "--rules",
        default=str(EXAMPLES_ROOT / "compiled" / "sticker_pricing_rules.json"),
        help="Compiled pricing rules JSON.",
    )

    subparsers.add_parser(
        "learn-stickers",
        help="Compile sticker pricing rules from teacher examples.",
    )

    study_parser = subparsers.add_parser("study", help="Study a research note into a draft module.")
    study_parser.add_argument("source", help="Local path or URL to study.")

    approve_parser = subparsers.add_parser("approve-module", help="Approve a studied draft module.")
    approve_parser.add_argument("module_id", help="Draft module id to approve.")

    args = parser.parse_args(argv)

    if args.command == "demo":
        return run_demo(json_output=args.json)
    if args.command == "route":
        return run_route(args.capability, args.question, json_output=args.json)
    if args.command == "quote":
        return run_quote(args.text, rules_path=args.rules)
    if args.command == "learn-stickers":
        return run_learn_stickers()
    if args.command == "study":
        return run_study(args.source)
    if args.command == "approve-module":
        return run_approve_module(args.module_id)

    parser.error("Unknown command")
    return 2


def run_demo(json_output: bool = False) -> int:
    return run_route(
        "printing.stickers.basic",
        "Can the local node quote a simple sticker job?",
        json_output=json_output,
    )


def run_route(capability: str, question: str, json_output: bool = False) -> int:
    local_card = load_capability_card(EXAMPLES_ROOT / "local_node" / "capability_card.json")
    peer_cards = load_peer_cards(EXAMPLES_ROOT / "peer_nodes")
    modules = load_modules(EXAMPLES_ROOT / "modules")
    request = MeshRequest(
        capability_needed=capability,
        question=question,
        user_private_context={"demo_note": "This must stay local."},
    )
    decision = route(request, local_card, peer_cards, modules)
    if json_output:
        print(json.dumps(asdict(decision), indent=2))
    else:
        print(_format_story(local_card.node_id, request, decision))
    return 0


def run_quote(text: str, rules_path: str | Path | None = None) -> int:
    request = parse_sticker_quote(text)
    quote = quote_stickers(
        quantity=request.quantity,
        width_mm=request.width_mm,
        height_mm=request.height_mm,
        material=request.material,
        laminated=request.laminated,
        rules_path=rules_path if Path(rules_path).exists() else None,
    )
    print(_format_quote_story(text, quote))
    return 0


def run_learn_stickers() -> int:
    examples_path = EXAMPLES_ROOT / "training" / "sticker_pricing_examples.json"
    rules_path = EXAMPLES_ROOT / "compiled" / "sticker_pricing_rules.json"
    rules = compile_sticker_pricing_rules(examples_path, rules_path)
    print(_format_learning_story(examples_path, rules_path, rules))
    return 0


def run_study(source: str) -> int:
    draft_path = EXAMPLES_ROOT / "drafts" / "printing_stickers_basic.research_draft.json"
    draft = study_research_note(source, draft_path)
    print(_format_study_story(Path(source).name, draft_path, draft))
    return 0


def run_approve_module(module_id: str) -> int:
    draft_path = EXAMPLES_ROOT / "drafts" / f"{module_id}.research_draft.json"
    rules_path = EXAMPLES_ROOT / "compiled" / "sticker_pricing_rules.json"
    approval = approve_research_draft(draft_path, rules_path)
    print(_format_approval_story(approval))
    return 0


def _format_story(local_node_id: str, request: MeshRequest, decision) -> str:
    lines = [
        f"AI Mesh local node: {local_node_id}",
        "",
        "Request:",
        f"  Capability needed: {request.capability_needed}",
        f"  Question: {request.question}",
        "",
        "Decision:",
    ]

    if decision.handler_type == "local":
        lines.append(f"  Handle locally with {decision.handler_id}.")
        if decision.module_id:
            lines.append(f"  Use module: {decision.module_id}")
        lines.extend(
            [
                "",
                "Why:",
                "  Smallest capable node found locally.",
            ]
        )
    elif decision.handler_type == "peer":
        lines.extend(
            [
                "  Local node cannot handle this request.",
                "  Private context removed before peer routing.",
                f"  Route to peer: {decision.handler_id}",
                "",
                "Why:",
                "  A trusted peer advertises the needed capability.",
            ]
        )
    else:
        lines.extend(
            [
                "  No capable local or peer node found.",
                "",
                "Why:",
                "  No capability card matched this request.",
            ]
        )

    return "\n".join(lines)


def _format_quote_story(text: str, quote) -> str:
    return "\n".join(
        [
            "AI Mesh local node: local-demo-node",
            "",
            "User:",
            f"  {text}",
            "",
            "Decision:",
            "  Handle locally.",
            "  Use module: printing_stickers_basic",
            f"  Run skill: {quote.skill_name}",
            "",
            "Result:",
            f"  Estimated price: {quote.currency} {quote.total_eur:.2f}",
            f"  Reason: {quote.reason}",
            "",
            "Why this matters:",
            "  Repeated knowledge became local execution.",
            "  No cloud. No peer. Smallest capable node won.",
        ]
    )


def _format_learning_story(examples_path: Path, rules_path: Path, rules) -> str:
    return "\n".join(
        [
            "AI Mesh Night School: sticker pricing",
            "",
            f"Teacher examples loaded: {rules['example_count']}",
            f"Source: {examples_path}",
            "",
            "Compiled local rule table:",
            f"  setup_eur: {rules['setup_eur']:.2f}",
            f"  materials: {', '.join(rules['materials'].keys())}",
            f"  lamination_rate_per_cm2: {rules['lamination_rate_per_cm2']:.3f}",
            f"Output: {rules_path}",
            "",
            "Why this matters:",
            "  The user became the teacher.",
            "  Examples became local rules.",
            "  Local rules became execution.",
        ]
    )


def _format_study_story(source_name: str, draft_path: Path, draft) -> str:
    passed = sum(1 for test in draft["tests"] if test["passed"])
    total = len(draft["tests"])
    return "\n".join(
        [
            f"Research studied: {source_name}",
            "",
            f"Draft module: {draft['module_id']}",
            f"Sources: {', '.join(draft['source_refs'])}",
            f"Checked: {draft['checked']}",
            f"Tests: {passed}/{total} passed",
            f"Draft saved: {draft_path}",
            "",
            "Waiting for teacher approval.",
        ]
    )


def _format_approval_story(approval) -> str:
    return "\n".join(
        [
            f"Approved module: {approval['module_id']}",
            f"Rules activated: {approval['rules_path']}",
            "",
            "Research rules are now active locally.",
            "Book knowledge became an approved local skill.",
        ]
    )
