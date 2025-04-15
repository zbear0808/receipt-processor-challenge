import unittest
import json
from datetime import date, time
from decimal import Decimal
from app.models import Receipt
from pydantic import ValidationError


class TestPydanticCoercion(unittest.TestCase):
    def test_valid_iso_format(self):
        json_string = """
        {
            "retailer": "Test Retailer",
            "purchaseDate": "2024-04-14",
            "purchaseTime": "14:30",
            "items": [
                {"shortDescription": "Item 1", "price": "10.00"}
            ],
            "total": "10.00"
        }
        """
        data = json.loads(json_string)
        receipt = Receipt(**data) 
        self.assertEqual(receipt.purchaseDate, date(2024, 4, 14))
        self.assertEqual(receipt.purchaseTime, time(14, 30))
        self.assertEqual(receipt.total_decimal, Decimal("10.00"))


    def test_invalid_format(self):
        json_string = """
        {
            "retailer": "Test Retailer",
            "purchaseDate": "2024-04-14",
            "purchaseTime": "14:30",
            "items": [
                {"shortDescription": "Item 1", "price": 10.00}
            ],
            "total": 10.00
        }
        """
        data = json.loads(json_string)
        with self.assertRaises(ValidationError):
            Receipt(**data) 


    def test_invalid_date_format(self):
        json_string = """
        {
            "retailer": "Test Retailer",
            "purchaseDate": "04/14/2024",
            "purchaseTime": "14:30",
            "items": [
                {"shortDescription": "Item 1", "price": "10.00"}
            ],
            "total": "10.00"
        }
        """
        data = json.loads(json_string)
        with self.assertRaises(ValueError):
            Receipt(**data)

    def test_invalid_time_format(self):
        json_string = """
        {
            "retailer": "Test Retailer",
            "purchaseDate": "2024-04-14",
            "purchaseTime": "14:30:61",
            "items": [
                {"shortDescription": "Item 1", "price": "10.00"}
            ],
            "total": "10.00"
        }
        """
        data = json.loads(json_string)
        with self.assertRaises(ValueError):
            Receipt(**data)

if __name__ == '__main__':
    unittest.main()
