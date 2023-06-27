"""Tests for the sapcommissions module."""
import unittest
from dataclasses import asdict

from sapcommissions import Connection


class TestConnection(unittest.TestCase):
    """Tests for the Connection class."""

    def test_url(self):
        """Test the url attribute."""
        # Create a connection instance to test
        conn = Connection(
            tenant="spam", environment="eggs", username="user", password="pass"
        )

        # Check that the url property returns the expected value
        self.assertEqual(conn.url, "https://spam-eggs.callidusondemand.com")

    def test_api_url(self):
        """Test the apiUrl attribute."""
        # Create a connection instance to test
        conn = Connection(
            tenant="spam", environment="eggs", username="user", password="pass"
        )

        # Check that the api_url property returns the expected value
        self.assertEqual(conn.apiUrl, "https://spam-eggs.callidusondemand.com/api")

    def test_api_document(self):
        """Test the apiDocument attribute."""
        # Create a connection instance to test
        conn = Connection(
            tenant="spam", environment="eggs", username="user", password="pass"
        )

        # Check that the api_document property returns the expected value
        self.assertEqual(
            conn.apiDocument, "https://spam-eggs.callidusondemand.com/APIDocument"
        )

    def test_connection_dataclass(self):
        """Test the Connection dataclass."""
        # Check that the Connection dataclass is defined correctly
        conn_dict = {
            "tenant": "spam",
            "environment": "eggs",
            "username": "user",
            "password": "pass",
            "verifySsl": True,
        }

        # Check that the fields of the Connection instance match the values in conn_dict
        conn = Connection(**conn_dict)
        self.assertEqual(asdict(conn), conn_dict)

        # Check that the verify_ssl field defaults to True if not provided
        del conn_dict["verifySsl"]
        conn = Connection(**conn_dict)
        conn_dict["verifySsl"] = True  # Verify that verify_ssl defaults to True
        self.assertEqual(asdict(conn), conn_dict)

    def test_hidden_password(self):
        """Test the password visibility."""
        # Create a connection instance to test
        conn = Connection(
            tenant="spam", environment="eggs", username="foo", password="barbaz"
        )

        # Check that the password property is hidden from the string representation.
        self.assertNotIn("barbaz", str(conn))
        self.assertNotIn("barbaz", repr(conn))
