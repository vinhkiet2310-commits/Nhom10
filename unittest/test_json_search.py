"""Functional and authorization tests for recursive JSON search."""

import unittest

from policy import POLICY
from recursive_json_search import json_search
from test_data import data, key1, key2


class json_search_test(unittest.TestCase):
    def test_search_found(self):
        """Find a configured field when called by an authorized role."""
        self.assertEqual(
            json_search(key1, data, role="admin"),
            ["Network Device 10.10.20.82 Is Unreachable From Controller"],
        )

    def test_search_not_found(self):
        """Return an empty list when the key does not occur in the data."""
        self.assertEqual(json_search(key2, data), [])

    def test_is_a_list(self):
        """Return search matches in a list, including list-valued fields."""
        matches = json_search("suggestedActions", data, role="viewer")

        self.assertIsInstance(matches, list)
        self.assertEqual(len(matches), 1)
        self.assertEqual(len(matches[0]), 3)

    def test_search_aggregates_nested_matches(self):
        """Collect matching values from all nested dictionaries and lists."""
        self.assertEqual(
            json_search("id", data),
            [
                "AWcvsjx864kVeDHDi2gB",
                "a7633ae5-d3c9-4aea-837d-c3ad5b19c802",
            ],
        )

    def test_api_key_is_limited_to_admin(self):
        """Only admin can retrieve apiKey; missing and unauthorized roles deny."""
        expected = ["SNMP-COMMUNITY-STRING-7f3a9c"]

        self.assertEqual(json_search("apiKey", data, role="admin"), expected)
        self.assertEqual(json_search("apiKey", data, role="operator"), [])
        self.assertEqual(json_search("apiKey", data, role="viewer"), [])
        self.assertEqual(json_search("apiKey", data), [])
        self.assertEqual(json_search("apiKey", data, role="unknown"), [])

    def test_management_ip_allows_operator_but_not_viewer(self):
        """Allow admin and operator, but deny viewer, for management IPs."""
        expected = ["10.10.20.21"]

        self.assertEqual(
            json_search("managementIpAddress", data, role="admin"), expected
        )
        self.assertEqual(
            json_search("managementIpAddress", data, role="operator"), expected
        )
        self.assertEqual(json_search("managementIpAddress", data, role="viewer"), [])
        self.assertEqual(json_search("managementIpAddress", data), [])
        self.assertEqual(
            json_search("managementIpAddress", data, role="unknown"), []
        )

    def test_issue_summary_allows_each_configured_role(self):
        """Allow every role configured for issueSummary and deny other roles."""
        expected = ["Network Device 10.10.20.82 Is Unreachable From Controller"]

        for role in POLICY["issueSummary"]:
            with self.subTest(role=role):
                self.assertEqual(json_search("issueSummary", data, role=role), expected)

        self.assertEqual(json_search("issueSummary", data), [])
        self.assertEqual(json_search("issueSummary", data, role="unknown"), [])


if __name__ == "__main__":
    unittest.main()
