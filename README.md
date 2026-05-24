# AI Mesh

Local-first, peer-to-peer modular AI for self-learning personal intelligence.

AI Mesh is not a normal chatbot app. It is an experiment in a smaller local AI
architecture built around:

- a small communication and routing core
- inspectable knowledge modules
- compressed memory lifecycle
- trusted peer specialist nodes
- compiled skills for repeated work
- cloud fallback only when truly needed later

This repo currently contains the first prototype: a local node that can load JSON
capability cards and module manifests, route a structured request, and avoid
sharing private request context with peers.

## Quick Start

### Windows PowerShell

```powershell
py -m venv .venv
.venv\Scripts\activate
pip install -e ".[dev]"
python -m aimesh demo
pytest
```

### macOS / Linux

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
python -m aimesh demo
pytest
```

## CLI

Run the demo route:

```bash
python -m aimesh demo
```

Example output:

```text
AI Mesh local node: local-demo-node

Request:
  Capability needed: printing.stickers.basic
  Question: Can the local node quote a simple sticker job?

Decision:
  Handle locally with local-demo-node.
  Use module: printing_stickers_basic

Why:
  Smallest capable node found locally.
```

Route a specific capability request:

```bash
python -m aimesh route --capability painting.oil_cleaning.basic --question "How do I clean this?"
```

This shows the first peer-routing proof:

```text
Decision:
  Local node cannot handle this request.
  Private context removed before peer routing.
  Route to peer: peer-painting-node
```

For the raw structured decision:

```bash
python -m aimesh route --capability printing.stickers.basic --question "Quote stickers" --json
```

## Current Prototype

The router follows the smallest capable node rule:

1. local node capability
2. trusted peer capability
3. no handler

The project is intentionally plain Python and JSON for now. No cloud APIs, model
inference, vector databases, heavyweight frameworks, or networking are included
in this first milestone.
