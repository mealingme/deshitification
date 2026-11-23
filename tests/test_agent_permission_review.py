import unittest

from examples.agent_permission_review.policy_audit import audit_policy


class AgentPermissionReviewTests(unittest.TestCase):
    def test_sample_policy_flags_expected_high_risks(self):
        policy = {
            "agent_name": "fictional-agent",
            "audit_logging_enabled": True,
            "tools": [
                {
                    "name": "send_email",
                    "permissions": ["email:send"],
                    "reads_sensitive_data": True,
                    "sends_external_data": True,
                    "accesses_secrets": True,
                    "requires_human_approval": False,
                },
                {
                    "name": "update_order",
                    "permissions": ["orders:write"],
                    "requires_human_approval": False,
                },
                {
                    "name": "admin",
                    "permissions": ["*"],
                },
            ],
        }
        report = audit_policy(policy)
        rules = {finding["rule"] for finding in report["findings"]}
        self.assertEqual(report["highest_severity"], "HIGH")
        self.assertIn("agent_can_read_secrets", rules)
        self.assertIn("sensitive_external_send_without_approval", rules)
        self.assertIn("write_without_approval", rules)
        self.assertIn("broad_permission", rules)

    def test_approved_sensitive_external_send_is_not_flagged(self):
        policy = {
            "tools": [
                {
                    "name": "reviewed_send",
                    "permissions": ["email:send"],
                    "reads_sensitive_data": True,
                    "sends_external_data": True,
                    "requires_human_approval": True,
                }
            ]
        }
        report = audit_policy(policy)
        self.assertEqual(report["finding_count"], 0)
        self.assertEqual(report["highest_severity"], "NONE")

    def test_write_access_requires_approval(self):
        policy = {
            "tools": [
                {
                    "name": "change_record",
                    "permissions": ["orders:write"],
                    "requires_human_approval": False,
                }
            ]
        }
        report = audit_policy(policy)
        self.assertIn(
            "write_without_approval",
            {finding["rule"] for finding in report["findings"]},
        )

    def test_disabled_audit_logging_is_medium(self):
        report = audit_policy({"audit_logging_enabled": False, "tools": []})
        self.assertEqual(report["highest_severity"], "MEDIUM")
        self.assertEqual(report["findings"][0]["rule"], "audit_logging_disabled")

    def test_wildcard_permission_is_high(self):
        report = audit_policy(
            {"tools": [{"name": "all_access", "permissions": ["orders:*"]}]}
        )
        self.assertEqual(report["highest_severity"], "HIGH")
        self.assertEqual(report["findings"][0]["rule"], "broad_permission")

    def test_invalid_policy_shape_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "tools must be a list"):
            audit_policy({"tools": "not-a-list"})

    def test_invalid_permission_type_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "list of strings"):
            audit_policy(
                {"tools": [{"name": "bad", "permissions": ["orders:read", 7]}]}
            )


if __name__ == "__main__":
    unittest.main()
