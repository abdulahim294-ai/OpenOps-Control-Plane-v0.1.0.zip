# Ecosystem comparison

| System | Primary purpose | Policy | Approval | Idempotency | Audit | Execution | AI-agent focus |
|---|---|---|---|---|---|---|---|
| OpenOps | Automation control plane | Built-in deterministic | Built-in | Built-in persisted reference implementation | Built-in | Action adapters | Explicit boundary |
| n8n | Workflow automation | Workflow/node controls | Human review for selected AI tools | Workflow-dependent | Execution history | Workflow engine | Strong AI workflow features |
| Temporal | Durable execution | Application-defined | Application-defined | Application/external-service patterns | Event history | Durable workflows/activities | General-purpose |
| Airflow | Batch/data workflows | Task/DAG/application patterns | Operational controls | Task design dependent | Task/run metadata | Scheduler/executor | Not primary |
| OPA | Policy engine | Declarative Rego | Not primary | Not primary | Not primary | Not primary | General policy enforcement |
| Kyverno | Kubernetes policy | Declarative Kubernetes policy | Policy/admission workflows | Not primary | Kubernetes ecosystem | Not primary | Not primary |
| GitHub Actions | CI/CD automation | Repository/org controls | Environments/reviews | Workflow dependent | Run logs | CI runners | Not primary |

Sources: OPA documentation (https://www.openpolicyagent.org/docs), n8n HITL documentation (https://docs.n8n.io/build/integrate-ai/ai-examples/human-in-the-loop-for-tools), Temporal documentation (https://docs.temporal.io/), and Airflow documentation (https://airflow.apache.org/docs/).

OpenOps is intentionally not a replacement for these systems. It is a control-plane boundary that can sit in front of or beside them.
