# Operations

## Local run

`openops serve` starts on `127.0.0.1:8080` by default. Set `OPENOPS_DB` in your environment and adapt the CLI/API wiring if deploying beyond a local development environment.

## Operational boundaries

Use a reverse proxy/TLS, real authentication, authorization, request limits, external secret management, centralized logs, and a durable audit sink before exposing this reference implementation to an untrusted network.

## Roadmap

- PostgreSQL repository
- distributed idempotency/locking
- RBAC/OIDC
- OPA policy adapter
- OpenTelemetry
- signed execution plans
- webhook adapters
- Slack/GitHub/n8n/Temporal adapters
- tamper-resistant audit sink
