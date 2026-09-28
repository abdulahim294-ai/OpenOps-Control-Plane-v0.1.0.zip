# API

The reference API uses JSON and runs on Python's standard-library HTTP server.

- `GET /health`
- `POST /runs`
- `GET /runs`
- `GET /runs/{id}`
- `GET /runs/{id}/audit`
- `POST /runs/{id}/approve`
- `POST /runs/{id}/reject`
- `POST /runs/{id}/cancel`
- `POST /runs/{id}/retry`
- `POST /dry-runs`

`Idempotency-Key` may be supplied as a header. Payloads over 1 MiB are rejected. The local actor is supplied through `X-Actor`; this is not authentication.

Errors use `{ "error": { "code": "...", "message": "..." } }`.
