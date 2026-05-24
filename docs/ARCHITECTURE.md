# Architecture

AI Mesh starts with a small local node.

The first prototype has four moving parts:

- `CapabilityCard`: what a node can handle
- `ModuleManifest`: what local knowledge modules advertise
- `MeshRequest`: the structured user request
- `RouteDecision`: the selected handler

Routing order:

1. compiled local skill later
2. active local module
3. warm or compressed memory later
4. trusted peer node
5. larger local model later
6. cloud fallback later, only if necessary

Only steps 2, 4, and no-match exist in the first prototype.
