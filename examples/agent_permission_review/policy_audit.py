"""Static review of a fictional AI-agent tool policy.

This educational example inspects declared permissions only. It does not
connect to an agent, inspect runtime behaviour, read credentials, or enforce
security controls.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

BROAD_PERMISSIONS = {"*", "all", "admin", "root", "system:*"}


def validate_policy(policy: Any) -> dict[str, Any]:
    if not isinstance(policy, dict):
        raise ValueError("policy must be a JSON object")

    tools = policy.get("tools")
    if not isinstance(tools, list):
        raise ValueError("tools must be a list")

    for index, tool in enumerate(tools):
        if not isinstance(tool, dict):
            raise ValueError(f"tools[{index}] must be an object")
        if not isinstance(tool.get("name"), str) or not tool["name"].strip():
            raise ValueError(f"tools[{index}].name must be a non-empty string")
        permissions = tool.get("permissions", [])
        if not isinstance(permissions, list) or not all(
            isinstance(value, str) for value in permissions
        ):
            raise ValueError(f"tools[{index}].permissions must be a list of strings")
        for field in (
            "reads_sensitive_data",
            "sends_external_data",
            "accesses_secrets",
            "requires_human_approval",
        ):
            if field in tool and not isinstance(tool[field], bool):
                raise ValueError(f"tools[{index}].{field} must be a boolean")

    if "audit_logging_enabled" in policy and not isinstance(
        policy["audit_logging_enabled"], bool
    ):
        raise ValueError("audit_logging_enabled must be a boolean")

    return policy


def _finding(
    severity: str,
    rule: str,
    tool: str,
    issue: str,
    recommendation: str,
) -> dict[str, str]:
    return {
        "severity": severity,
        "rule": rule,
        "tool": tool,
        "issue": issue,
        "recommendation": recommendation,
    }


def audit_policy(policy: Any) -> dict[str, Any]:
    """Return deterministic findings for a declared, synthetic tool policy."""
    policy = validate_policy(policy)
    findings: list[dict[str, str]] = []

    if policy.get("audit_logging_enabled", True) is False:
        findings.append(
            _finding(
                "MEDIUM",
                "audit_logging_disabled",
                "(policy)",
                "Tool activity logging is declared as disabled.",
                "Enable appropriate audit records and review access regularly.",
            )
        )

    for tool in policy["tools"]:
        name = tool["name"]
        permissions = {value.strip().lower() for value in tool.get("permissions", [])}
        approval = tool.get("requires_human_approval", False)

        if permissions & BROAD_PERMISSIONS or any(
            permission.endswith(":*") for permission in permissions
        ):
            findings.append(
                _finding(
                    "HIGH",
                    "broad_permission",
                    name,
                    "The tool declares wildcard or administrator-level access.",
                    "Replace broad access with the smallest task-specific permission set.",
                )
            )

        if tool.get("accesses_secrets", False):
            findings.append(
                _finding(
                    "HIGH",
                    "agent_can_read_secrets",
                    name,
                    "The tool is declared as able to read secrets or credentials.",
                    "Keep raw secrets outside agent-readable context; use a controlled secret broker.",
                )
            )

        if (
            tool.get("sends_external_data", False)
            and tool.get("reads_sensitive_data", False)
            and not approval
        ):
            findings.append(
                _finding(
                    "HIGH",
                    "sensitive_external_send_without_approval",
                    name,
                    "Sensitive data can be sent externally without a human approval gate.",
                    "Require a human to review the exact destination and payload before sending.",
                )
            )

        has_write = any(
            permission in {"write", "delete"}
            or permission.endswith((":write", ":delete"))
            for permission in permissions
        )
        if has_write and not approval:
            findings.append(
                _finding(
                    "HIGH",
                    "write_without_approval",
                    name,
                    "The tool declares write or delete access without human approval.",
                    "Use read-only access by default and gate consequential changes.",
                )
            )

    severity_order = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}
    findings.sort(
        key=lambda item: (
            severity_order[item["severity"]],
            item["tool"],
            item["rule"],
        )
    )
    highest = findings[0]["severity"] if findings else "NONE"
    return {
        "agent_name": policy.get("agent_name", "unnamed-demo-agent"),
        "finding_count": len(findings),
        "highest_severity": highest,
        "findings": findings,
        "limitations": [
            "This checks declared configuration only, not effective runtime permissions.",
            "It cannot prove that secrets are absent from files, prompts, logs or provider systems.",
            "It is not a security audit, penetration test or policy enforcement mechanism.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Review a fictional AI-agent tool policy (static, read-only)."
    )
    parser.add_argument("policy", type=Path, help="Path to a JSON policy file")
    parser.add_argument(
        "--output",
        type=Path,
        help="Optional path for a JSON report; otherwise print to stdout",
    )
    args = parser.parse_args()

    try:
        policy = json.loads(args.policy.read_text(encoding="utf-8"))
        report = audit_policy(policy)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        parser.error(str(exc))

    rendered = json.dumps(report, indent=2, ensure_ascii=False)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered + "\n", encoding="utf-8")
    else:
        print(rendered)

    return 1 if report["highest_severity"] == "HIGH" else 0


if __name__ == "__main__":
    raise SystemExit(main())
