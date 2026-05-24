# Module Spec

A module manifest is a JSON document describing a small block of domain
knowledge.

Current prototype fields:

- `module_id`
- `name`
- `version`
- `capabilities`
- `intents`
- `required_fields`
- `safety_level`
- `sources`

Modules do not execute code yet. They advertise capability and shape future
workflow behavior.
