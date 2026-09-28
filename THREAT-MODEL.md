# Threat model

Assets: execution authority, action parameters, audit records, identity/approval decisions.

Trust boundaries: proposer → API; API → policy/risk; approval identity → execution; execution → external adapter; service → storage.

Threats: malicious proposer, replayed request, unauthorized approval, malformed payload, adapter failure, storage corruption, log leakage, and compromised host.

Mitigations in 0.1.0: explicit state machine, persisted unique idempotency key, deterministic policy, approval tied to execution state, input-size limit, parameterized SQL, no shell execution, structured audit events.

Residual risk: host compromise, database tampering, identity spoofing in local mode, and arbitrary third-party side-effect semantics.
