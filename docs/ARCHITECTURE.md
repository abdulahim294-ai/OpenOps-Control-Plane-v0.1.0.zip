# Architecture

The core service is intentionally small. `domain.py` defines stable domain objects and states. `policy` evaluates authorization-like business rules without performing side effects. `risk` produces a transparent factor list. `service.py` coordinates the state machine and adapters. `storage` persists executions and audit records. `actions` contains the side-effect boundary.

The reference implementation is single-process. SQLite's unique idempotency key is the durable duplicate guard. This is sufficient for a local reference implementation but not a distributed execution guarantee.
