import json
import unittest

from api import create_app
from api.models import db
from config import TestingConfig


class TestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = create_app(TestingConfig)
        cls.app.debug = True

    def setUp(self):
        with self.app.app_context():
            self.client = self.app.test_client()
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    # Health Check
    def test_health_check(self):
        result = self.client.get("/health_check")
        self.assertEqual(result.status_code, 200)


    # Add Store
    def test_add_store(self):
        header = {"Content-type": "application/json"}
        store = {
            "name": "Test",
            "postcode": "Test"
        }
        result = self.client.post("/add_store",
                                  headers=header,
                                  data=json.dumps(store))
        self.assertEqual(result.status_code, 201)
        self.assertIn("Location", result.headers)

    def test_add_store_invalid_payload(self):
        header = {"Content-type": "application/json"}
        store = {
            "name": "Test",
        }
        result = self.client.post(
            "/add_store",
            headers=header,
            data=json.dumps(store))
        self.assertEqual(result.status_code, 400)


    # Get Store
    def test_get_store_not_exists(self):
        result = self.client.get("/store/1321313")
        self.assertEqual(result.status_code, 404)

    def test_get_store_exists(self):
        store = {
            "name": "Test",
            "postcode": "Test"
        }
        self.client.post("/add_store",
                         headers={"Content-type": "application/json"},
                         data=json.dumps(store))

        # When I posted before, the store has been created with ID 1
        result = self.client.get("/store/1")
        self.assertEqual(result.status_code, 200)


    # Get stores in order
    def test_stores_in_order(self):
        store1 = {
            "name": "Test1",
            "postcode": "Test"
        }
        store2 = {
            "name": "Test2",
            "postcode": "Test"
        }
        self.client.post("/add_store",
                         headers={"Content-type": "application/json"},
                         data=json.dumps(store1))
        
        self.client.post("/add_store",
                         headers={"Content-type": "application/json"},
                         data=json.dumps(store2))


        result = self.client.get("/stores_in_order")
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.json[0]["name"], "Test1")
        self.assertEqual(result.json[1]["name"], "Test2")
        
        
    def test_stores_in_order_empty(self):
        result = self.client.get("/stores_in_order")
        self.assertEqual(result.status_code, 404)
        self.assertEqual(result.json, None)
    

    # Get Coords
    def test_get_coords_empty(self):
        result = self.client.get("/get_coords")
        self.assertEqual(result.status_code, 404)
        
    def test_get_stores_in_radius_without_params(self):
        result = self.client.get("/whats_in_radius/xxx")
        self.assertEqual(result.status_code, 404)


    # Get Radius
    def test_get_stores_in_radius_big_radius(self):
        result = self.client.get("/whats_in_radius/NW33DE/999")
        self.assertEqual(result.status_code, 404)

    def test_get_stores_in_radius_flow(self):
        """Coordinates will be added after calling get_coords endpoint"""
        payload = {
            "name": "St_Albans",
            "postcode": "AL1 2RJ"
        }
        self.client.post("/add_store",
                         headers={"Content-type": "application/json"},
                         data=json.dumps(payload))
        self.client.get("/get_coords")
        result = self.client.get("/whats_in_radius/AL12RJ/0")
        self.assertEqual(result.status_code, 200)


    def test_get_stores_in_radius_flow_ii(self):
        payload = {
            "name": "St_Albans",
            "postcode": "AL1 2RJ"
        }
        far_away_postcode = "NW14LJ"
        self.client.post("/add_store",
                         headers={"Content-type": "application/json"},
                         data=json.dumps(payload))
        self.client.get("/get_coords")
        result = self.client.get(f"/whats_in_radius/{far_away_postcode}/1")
        self.assertEqual(result.status_code, 404)
        

