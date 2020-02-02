import unittest

from api.models import Store


class ModelTest(unittest.TestCase):
    def test_equals(self):
        store1 = Store(name="test name",
                       postcode="test code")

        store2 = Store(name="test name",
                       postcode="test code")
        # id gets assigned after being persisted
        self.assertIsNone(store1.id)
        self.assertIsNone(store2.id)

        self.assertEqual(store1.name, store2.name)
        self.assertEqual(store1.postcode, store2.postcode)

        self.assertIsNone(store1.latitude)
        self.assertIsNone(store1.longitude)
        self.assertEqual(store1.latitude, store2.latitude)
        self.assertEqual(store1.longitude, store2.longitude)

    def test_to_dict(self):
        store1 = Store(id=1321321, name="test name", postcode="test code").to_dict()
        self.assertNotIn("id", store1)

    def test_to_verbose_dict(self):
        store1 = Store(id=1321321,
                       name="test name",
                       postcode="test code",
                       longitude=231,
                       latitude=231).to_verbose_dict()
        self.assertIn("longitude", store1)
        self.assertIn("latitude", store1)

    def test_repr(self):
        store1 = Store(id=1321321, name="test name", postcode="test code")
        self.assertIsNotNone(store1.__rerp__)
