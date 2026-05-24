from pathlib import Path

from aimesh.loaders import load_capability_card, load_module_manifest


def test_load_capability_card_reads_json(tmp_path: Path):
    card_path = tmp_path / "card.json"
    card_path.write_text(
        """{
          "node_id": "local-demo-node",
          "capabilities": ["printing.stickers.basic"],
          "query_modes": ["answer_only"],
          "stores_queries": false,
          "max_block_size_mb": 10,
          "trust": {"signed": false, "reputation": 0.5}
        }""",
        encoding="utf-8",
    )

    card = load_capability_card(card_path)

    assert card.node_id == "local-demo-node"
    assert card.capabilities == ["printing.stickers.basic"]
    assert card.max_block_size_mb == 10


def test_load_module_manifest_reads_json(tmp_path: Path):
    module_path = tmp_path / "module.json"
    module_path.write_text(
        """{
          "module_id": "printing_stickers_basic",
          "name": "Printing Stickers Basic",
          "version": "0.1.0",
          "capabilities": ["printing.stickers.basic"],
          "intents": ["quote_stickers"],
          "required_fields": ["quantity", "width_mm", "height_mm"],
          "safety_level": "low",
          "sources": ["founder examples"]
        }""",
        encoding="utf-8",
    )

    manifest = load_module_manifest(module_path)

    assert manifest.module_id == "printing_stickers_basic"
    assert manifest.capabilities == ["printing.stickers.basic"]
    assert manifest.required_fields == ["quantity", "width_mm", "height_mm"]
