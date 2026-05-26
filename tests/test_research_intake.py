import json
from pathlib import Path

from aimesh.research import approve_research_draft, study_research_note


def test_study_research_note_builds_draft_module(tmp_path: Path):
    note_path = tmp_path / "sticker_pricing_notes.md"
    note_path.write_text(
        """# Sticker Pricing Notes

source: workshop pricing handbook
checked: 2026-05-26

```aimesh-rules
{
  "module_id": "printing_stickers_basic",
  "setup_eur": 14.0,
  "materials": {
    "vinyl": {"rate_per_cm2": 0.014},
    "paper": {"rate_per_cm2": 0.009}
  },
  "lamination_rate_per_cm2": 0.006,
  "tests": [
    {
      "text": "Quote 100 stickers, 50mm x 30mm, vinyl, laminated",
      "expected_total_eur": 44.0
    }
  ]
}
```
""",
        encoding="utf-8",
    )
    draft_path = tmp_path / "draft.json"

    draft = study_research_note(note_path, draft_path)

    assert draft["status"] == "draft_waiting_for_teacher_approval"
    assert draft["module_id"] == "printing_stickers_basic"
    assert draft["source_refs"] == ["workshop pricing handbook"]
    assert draft["checked"] == "2026-05-26"
    assert draft["tests"][0]["passed"] is True
    assert draft_path.exists()


def test_approve_research_draft_activates_rules(tmp_path: Path):
    draft_path = tmp_path / "draft.json"
    rules_path = tmp_path / "rules.json"
    draft_path.write_text(
        json.dumps(
            {
                "status": "draft_waiting_for_teacher_approval",
                "module_id": "printing_stickers_basic",
                "rules": {
                    "setup_eur": 14.0,
                    "materials": {"vinyl": {"rate_per_cm2": 0.014}},
                    "lamination_rate_per_cm2": 0.006,
                    "source": "research_note",
                },
                "tests": [{"passed": True}],
            }
        ),
        encoding="utf-8",
    )

    approved = approve_research_draft(draft_path, rules_path)

    assert approved["status"] == "approved"
    assert approved["rules_path"] == str(rules_path)
    assert json.loads(rules_path.read_text(encoding="utf-8"))["setup_eur"] == 14.0
