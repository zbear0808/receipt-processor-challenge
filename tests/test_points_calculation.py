import json
import unittest
import asyncio
from pathlib import Path
from app.models import Receipt
from app.main import get_receipt_points, processReceipt


EXAMPLES_DIR = Path("tests/examples")

TEST_FILES = {
    "simple-receipt.json": 31,
    "morning-receipt.json": 15,
    "test-receipt-1.json": 97,
    "test-receipt-2.json": 52,
    "test-receipt-3.json": 20,
    "test-receipt-4.json": 70,
    "readme-example-1.json": 28,
    "readme-example-2.json": 109
}


class TestPointCalculation(unittest.TestCase):

    def _load_json_data(self, filename):
        """Helper to load JSON data from the examples directory."""
        file_path = EXAMPLES_DIR / filename
        if not file_path.exists():
            self.fail(f"Test data file not found: {file_path}")
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            self.fail(f"Error loading or parsing {filename}: {e}")
    
    def test_points_calculation(self):
        out = {}
        for filename in TEST_FILES:
            data = self._load_json_data(filename)
            receipt = Receipt(**data)
            process_response = asyncio.run(processReceipt(receipt))
            receipt_id = process_response.id
            points_response = asyncio.run(get_receipt_points(receipt_id))
            points = points_response.points
            out[filename] = points
        self.assertEqual(out, TEST_FILES, f"Points calculation mismatch: {out}")

if __name__ == '__main__':
    unittest.main()
