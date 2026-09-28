# OpenOps Control Plane

**Control the actions your automations are allowed to execute.**

OpenOps is an open-source reference implementation for putting a deterministic control layer between automation/AI proposals and side effects. It evaluates policy and risk, gates sensitive actions on human approval, persists idempotency, executes through action adapters, and records an audit trail.

> **Status: 0.1.0 reference implementation.** Local-first, SQLite-backed, single-process. It is not a claim of universal production readiness or tamper-proof auditing.

## Architecture

```text
AI / Automation Reasoning
          |
    Action Proposal
          v
+-----------------------+
| OpenOps Control Plane |
+-----------------------+
   | policy -> risk
   | approval
   | idempotency
   v
Deterministic Execution
          |
    Action Adapter
          |
   Audit / Evidence
```

## Quick demo

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
python -m unittest discover -s tests
python -m openops.cli.main demo
```

The demo uses only local deterministic actions and no credentials.

## What is implemented

| Capability | 0.1.0 |
|---|---|
| Deterministic policy evaluation | Yes |
| Transparent risk assessment | Yes |
| Human approval/rejection | Yes |
| Persisted SQLite idempotency | Yes |
| Dry-run | Yes |
| Action adapter boundary | Yes |
| Safe built-in actions | Yes |
| State machine + illegal transition checks | Yes |
| Structured audit events | Yes |
| CLI | Yes |
| HTTP API | Yes |
| Webhook signature adapter | Roadmap |
| RBAC/OIDC | Roadmap |
| PostgreSQL/distributed workers | Roadmap |

## API example

```http
POST /runs
Idempotency-Key: deploy-demo-1
Content-Type: application/json

{"action":"send-notification","environment":"production","actor":"agent","payload":{"destination":"demo@example.invalid","message":"review me"}}
```

A production request is returned in `AWAITING_APPROVAL`; approval is a separate operation.

## Audit example

```json
{"event":"APPROVED","actor":"operator","metadata":{"approver":"operator"}}
```

## Security model

Authentication, authorization, policy, and execution are deliberately separate concepts. The reference server uses an actor header as a simple local identity input; it is **not** an authentication system. See `SECURITY.md` and `THREAT-MODEL.md`.

## Limitations

SQLite and this single-process server do not provide distributed locking, immutable audit storage, high availability, or a production identity system. External side effects are intentionally limited to safe local simulations. Exactly-once execution of arbitrary external systems cannot be guaranteed by this control plane alone; adapters must cooperate with idempotency semantics.

## Research

See `docs/RESEARCH.md`, `docs/ECOSYSTEM.md`, and `docs/VIDEO_RESOURCES.md`.

## Roadmap

See `docs/DECISIONS.md` and the roadmap section in `docs/OPERATIONS.md`.

## Contributing

See `CONTRIBUTING.md`.
