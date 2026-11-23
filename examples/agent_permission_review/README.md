# AI Agent Permission Review

A small, dependency-free Python example that checks a **fictional** agent tool policy for several high-risk permission patterns.

## What it checks

- Wildcard or administrator-level permissions.
- Tools declared as able to read secrets.
- External sending of sensitive data without human approval.
- Write/delete permissions without human approval.
- Whether audit logging is declared disabled.

The included policy is fictional. It intentionally contains several unsafe settings so the report has findings to explain.

## Run it

From the repository root:

```bash
python examples/agent_permission_review/policy_audit.py examples/agent_permission_review/sample_policy.json
```

The command prints a JSON report. It returns exit code `1` when a HIGH finding exists and `0` otherwise. To save a report:

```bash
python examples/agent_permission_review/policy_audit.py examples/agent_permission_review/sample_policy.json --output reports/agent_policy_review.json
```

Run the unit tests:

```bash
python -m unittest tests.test_agent_permission_review -v
```

## Design boundary

This is a static review of declared configuration, not a live agent inspection. It does not connect to APIs, execute tools, read secret values, inspect prompts or prove effective permissions. It does not fix policy settings or make operational decisions. Real deployments require identity, access-control, logging, data-protection and security review by the responsible organisation.

All names and records are synthetic. The example uses only the Python standard library.
