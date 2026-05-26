# Skill Compiler

Repeated knowledge should become executable skill.

Planned flow:

```text
examples -> extracted rules -> workflow -> tests -> compiled skill
```

Example future skill:

```python
quote_stickers(quantity, width_mm, height_mm, material, laminated=False)
```

Current prototype skill:

```bash
python -m aimesh learn-stickers
python -m aimesh quote "Quote 100 stickers, 50mm x 30mm, vinyl, laminated"
```

This compiles sticker pricing examples into a local rule table, then runs the
local `quote_stickers` skill from `aimesh.skills.printing`. It is deliberately
small, but it proves the principle:

```text
teacher examples -> local rules -> tested function -> local execution
```
