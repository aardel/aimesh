# Sticker Pricing Notes

source: workshop pricing handbook
checked: 2026-05-26

This is a small controlled research note used by the prototype. It stands in for
the "school book" layer: material the system studies before the teacher approves
it for local use.

```aimesh-rules
{
  "module_id": "printing_stickers_basic",
  "setup_eur": 14.0,
  "materials": {
    "paper": {"rate_per_cm2": 0.009},
    "polyester": {"rate_per_cm2": 0.015},
    "vinyl": {"rate_per_cm2": 0.014}
  },
  "lamination_rate_per_cm2": 0.006,
  "tests": [
    {
      "text": "Quote 100 stickers, 50mm x 30mm, vinyl, laminated",
      "expected_total_eur": 44.0
    },
    {
      "text": "Quote 100 stickers, 50mm x 30mm, paper",
      "expected_total_eur": 27.5
    }
  ]
}
```
