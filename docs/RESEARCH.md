# Research

Research was used to constrain the project rather than to justify broad security claims.

1. **OWASP AI Agent Security Cheat Sheet** — 2026, https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet.html. Describes prompt injection, tool abuse/privilege escalation, and data exfiltration risks; supports the explicit agent-to-proposal boundary. 
2. **n8n: Human-in-the-loop for AI tool calls** — current documentation, https://docs.n8n.io/build/integrate-ai/ai-examples/human-in-the-loop-for-tools. Demonstrates selective approval gates for side-effecting AI tools; supports OpenOps treating approval as a first-class control rather than a UI-only feature.
3. **AWS Durable Execution: Idempotency and retries** — current documentation, https://docs.aws.amazon.com/durable-execution/patterns/best-practices/idempotency/. Explains why retries can repeat side effects and why idempotency is required for retry-safe operations.
4. **Apache Airflow Best Practices** — current documentation, https://airflow.apache.org/docs/apache-airflow/stable/best-practices.html. Explicitly recommends designing retried tasks to produce the same outcome and warns about duplicate database writes.
5. **Temporal Activity Definition** — current documentation, https://docs.temporal.io/encyclopedia/activities. Explains that retryable activities can execute more than once and that external services commonly enforce idempotency keys.
6. **Open Policy Agent documentation** — current documentation, https://www.openpolicyagent.org/docs. Establishes a mature pattern of separating policy decision-making from enforcement and using structured input for declarative policy.

## Findings

- AI agents increase the importance of controlling tool authority rather than trusting model intent.
- Human approval is most useful when it gates the actual parameters that will be executed.
- Retries and duplicate delivery are normal distributed-systems behavior; side effects therefore need explicit idempotency semantics.
- Policy should be deterministic and explainable, while enforcement remains in the application/execution layer.
- Auditability is evidence collection, not proof of tamper resistance.

## Scope boundary

OpenOps does not attempt to solve prompt injection, identity, arbitrary sandboxing, immutable compliance storage, or exactly-once semantics for third-party systems in 0.1.0. It provides extension points and documents those boundaries.
