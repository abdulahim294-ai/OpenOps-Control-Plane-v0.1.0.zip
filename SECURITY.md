# Security

OpenOps is a reference implementation, not a security certification. Threats considered include command injection (no shell execution is provided), SQL injection (parameterized SQLite statements), authorization bypass (approval state is checked), replay/duplicate execution (persisted idempotency key), payload abuse (1 MiB API limit), and secret leakage (no secret fields are logged by the reference implementation).

The local `X-Actor` header must never be treated as authentication on an exposed deployment. Add authenticated identity and authorization before network exposure.

Report vulnerabilities privately to the repository maintainers once a project contact is established; no public security email is invented in this release.
