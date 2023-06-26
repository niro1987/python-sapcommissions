import unittest
from dataclasses import dataclass, field
from datetime import date, datetime
from typing import ClassVar, List

from sapcommissions.resources import _decode, _encode, _Resource


@dataclass
class DummyResource(_Resource):
    _endpoint_name: ClassVar[str] = "test"
    id: str = field(metadata={"id": True})
    name: str = field(default=None)
    items: List[str] = field(default_factory=list)
    expands: bool = field(default=None, metadata={"expand": True})


class TestResourceMethods(unittest.TestCase):
    def setUp(self):
        self.resource_dict = {
            "id": "123",
            "name": "Test Resource",
            "items": ["item1", "item2"],
            "expands": False,
        }
        self.resource: DummyResource = DummyResource.from_dict(self.resource_dict)

    def test_name_property(self):
        self.assertEqual(DummyResource._name, "test")

    def test_seq_attr_property(self):
        self.assertIsNone(DummyResource._seq_attr)

    def test_seq_property(self):
        self.assertIsNone(self.resource._seq)

    def test_id_attr_property(self):
        self.assertEqual(DummyResource._id_attr, "id")

    def test_id_property(self):
        self.assertEqual(self.resource._id, "123")

    def test_expands_property(self):
        self.assertEqual(DummyResource._expands, ("expands",))

    def test_from_dict_method(self):
        self.assertIsInstance(self.resource, DummyResource)
        self.assertEqual(self.resource.id, "123")
        self.assertEqual(self.resource.name, "Test Resource")
        self.assertEqual(self.resource.items, ["item1", "item2"])
        self.assertEqual(self.resource.expands, False)

    def test_to_dict_method(self):
        expected_dict = {
            "id": "123",
            "name": "Test Resource",
            "items": ["item1", "item2"],
            "expands": False,
        }
        self.assertEqual(self.resource.to_dict(), expected_dict)


class TestEncodeDecode(unittest.TestCase):
    def test_decode_datetime(self):
        dt_str = "2000-01-02T03:04:05.000-06:00"
        decoded_dt = _decode(dt_str, datetime)
        self.assertEqual(decoded_dt, datetime.fromisoformat(dt_str))

    def test_encode_datetime(self):
        dt = datetime(2000, 1, 2, 3, 4, 5)
        encoded_dt = _encode(dt, datetime)
        self.assertEqual(encoded_dt, "2000-01-02T03:04:05")

    def test_decode_date(self):
        date_str = "2000-01-02T03:04:05.000-06:00"
        decoded_date = _decode(date_str, date)
        self.assertEqual(decoded_date, datetime.fromisoformat(date_str).date())

    def test_encode_date(self):
        dt = date(2000, 1, 2)
        encoded_dt = _encode(dt, date)
        self.assertEqual(encoded_dt, "2000-01-02")

    def test_decode_none(self):
        decoded_none = _decode(None, str)
        self.assertIs(decoded_none, None)

    def test_encode_none(self):
        encoded_none = _encode(None, str)
        self.assertIs(encoded_none, None)

    def test_decode_string(self):
        test_str = "SPAM"
        decoded_str = _decode(test_str, str)
        self.assertEqual(decoded_str, "SPAM")

    def test_encode_string(self):
        test_str = "SPAM"
        encoded_str = _encode(test_str, str)
        self.assertEqual(encoded_str, "SPAM")

    def test_decode_int(self):
        test_int = 1
        decoded_int = _decode(test_int, int)
        self.assertEqual(decoded_int, 1)

    def test_decode_str_int(self):
        test_int_str = "1"
        decoded_int_str = _decode(test_int_str, int)
        self.assertEqual(decoded_int_str, 1)

    def test_encode_int(self):
        test_int = 1
        encoded_int = _encode(test_int, int)
        self.assertEqual(encoded_int, 1)

    def test_decode_list_str(self):
        test_list = ["SPAM", "EGGS"]
        decoded_list = _decode(test_list, list[str])
        self.assertListEqual(decoded_list, test_list)

    def test_decode_list_error(self):
        test_list = ["SPAM", "EGGS"]
        with self.assertRaises(TypeError):
            _decode(test_list, list[str, int])
        with self.assertRaises(TypeError):
            _decode(test_list, list)
        with self.assertRaises(TypeError):
            _decode(test_list, str)

    def test_decode_unions(self):
        test_value = 1
        with self.assertRaises(NotImplementedError):
            _decode(test_value, int | dict)


if __name__ == "__main__":
    unittest.main()
