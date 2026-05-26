# AI Mesh Roadmap

## Milestone 1: First Local Node

- Load a local capability card from JSON.
- Load module manifests from JSON.
- Load peer capability cards from JSON.
- Route structured requests to the smallest capable node.
- Strip private context before peer routing.
- Provide a simple CLI.
- Cover behavior with tests.

## Milestone 2: Module Shape

- Expand the module manifest format.
- Add schema validation.
- Add beginner-readable module examples.
- Add module tests.
- Prove teacher examples can compile into a local rule table.

## Milestone 2A: Teacher Examples To Local Rules

- Load sticker pricing examples from JSON.
- Compile simple pricing rules from examples.
- Save an inspectable local rule table.
- Use the rule table in `quote_stickers`.
- Show the proof in the one-command Steve demo.

## Milestone 2B: Research Notes To Approved Modules

- Study a sourced local research note.
- Extract draft rules and tests.
- Require approval before activation.
- Activate approved research as local rules.
- Keep source refs and checked dates with the compiled rules.

## Milestone 3: Vacuum Bag Memory

- Implement active, warm, compressed, archived, and forgotten memory states.
- Add source-linked compressed memory bags.
- Add rehydration policy checks.

## Milestone 4: Skill Compiler

- Convert repeated examples into tested executable skills.
- Start with simple pricing and workflow examples.

## Milestone 5: Peer Protocol

- Define local peer request and response formats.
- Add trust and safety labels.
- Add multi-peer comparison for risky topics.
