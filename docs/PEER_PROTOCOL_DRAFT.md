# Peer Protocol Draft

Peer requests should be minimal and privacy-filtered.

Example shape:

```json
{
  "request_id": "req_001",
  "domain": "painting",
  "capability_needed": "painting.oil_cleaning.basic",
  "question": "How do I safely clean an old oil painting?",
  "privacy_level": "personal_context_removed",
  "response_format": "structured_answer"
}
```

The first prototype does not include networking. It only routes against local
JSON peer capability cards.
