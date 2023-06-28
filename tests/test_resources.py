"""Tests for the sapcommissions.resources module."""
from __future__ import annotations

import unittest
from dataclasses import dataclass, field
from datetime import date, datetime
from typing import ClassVar

from sapcommissions.resources import _deserialize, _Resource, _serialize


@dataclass
class DummyResource(_Resource):
    _endpoint_name: ClassVar[str] = "test"
    id: str = field(metadata={"id": True})
    name: str = field(default=None)
    items: list[str] = field(default_factory=list)
    expands: dict = field(default=None)


class TestResourceMethods(unittest.TestCase):
    def setUp(self):
        self.resource_dict = {
            "id": "123",
            "name": "Test Resource",
            "items": ["item1", "item2"],
        }
        self.resource: DummyResource = DummyResource.from_dict(self.resource_dict)

    def test_name_property(self):
        self.assertEqual(DummyResource._name, "test")

    def test_seq_attr_property(self):
        self.assertIsNone(DummyResource._seqAttr)

    def test_seq_property(self):
        self.assertIsNone(self.resource._seq)

    def test_id_attr_property(self):
        self.assertEqual(DummyResource._idAttr, "id")

    def test_id_property(self):
        self.assertEqual(self.resource._id, "123")

    def test_expands_property(self):
        self.assertEqual(
            DummyResource._expands,
            ("items", "expands"),
        )

    def test_from_dict_method(self):
        self.assertIsInstance(self.resource, DummyResource)
        self.assertEqual(self.resource.id, "123")
        self.assertEqual(self.resource.name, "Test Resource")
        self.assertEqual(self.resource.items, ["item1", "item2"])
        self.assertEqual(self.resource.expands, None)

    def test_to_dict_method(self):
        expected_dict = {
            "id": "123",
            "name": "Test Resource",
            "items": ["item1", "item2"],
        }
        self.assertEqual(self.resource.to_dict(), expected_dict)


class TestEncodeDecode(unittest.TestCase):
    def test_decode_datetime(self):
        dt_str = "2000-01-02T03:04:05.000-06:00"
        decoded_dt = _deserialize(dt_str, datetime)
        self.assertEqual(decoded_dt, datetime.fromisoformat(dt_str))

    def test_encode_datetime(self):
        dt = datetime(2000, 1, 2, 3, 4, 5)
        encoded_dt = _serialize(dt, datetime)
        self.assertEqual(encoded_dt, "2000-01-02T03:04:05")

    def test_decode_date(self):
        date_str = "2000-01-02T03:04:05.000-06:00"
        decoded_date = _deserialize(date_str, date)
        self.assertEqual(decoded_date, datetime.fromisoformat(date_str).date())

    def test_encode_date(self):
        dt = date(2000, 1, 2)
        encoded_dt = _serialize(dt, date)
        self.assertEqual(encoded_dt, "2000-01-02")

    def test_decode_none(self):
        decoded_none = _deserialize(None, str)
        self.assertIs(decoded_none, None)

    def test_encode_none(self):
        encoded_none = _serialize(None, str)
        self.assertIs(encoded_none, None)

    def test_decode_string(self):
        test_str = "SPAM"
        decoded_str = _deserialize(test_str, str)
        self.assertEqual(decoded_str, "SPAM")

    def test_encode_string(self):
        test_str = "SPAM"
        encoded_str = _serialize(test_str, str)
        self.assertEqual(encoded_str, "SPAM")

    def test_decode_int(self):
        test_int = 1
        decoded_int = _deserialize(test_int, int)
        self.assertEqual(decoded_int, 1)

    def test_decode_str_int(self):
        test_int_str = "1"
        decoded_int_str = _deserialize(test_int_str, int)
        self.assertEqual(decoded_int_str, 1)

    def test_encode_int(self):
        test_int = 1
        encoded_int = _serialize(test_int, int)
        self.assertEqual(encoded_int, 1)

    def test_decode_list_str(self):
        test_list = ["SPAM", "EGGS"]
        decoded_list = _deserialize(test_list, list[str])
        self.assertListEqual(decoded_list, test_list)

    def test_decode_list_error(self):
        test_list = ["SPAM", "EGGS"]
        with self.assertRaises(TypeError):
            _deserialize(test_list, list[str, int])
        with self.assertRaises(TypeError):
            _deserialize(test_list, list)
        with self.assertRaises(TypeError):
            _deserialize(test_list, str)

    def test_decode_unions(self):
        test_value = 1
        with self.assertRaises(NotImplementedError):
            _deserialize(test_value, int | dict)


if __name__ == "__main__":
    unittest.main()
