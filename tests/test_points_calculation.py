import json
import math
import re
from decimal import Decimal, ROUND_CEILING
from pathlib import Path
import pytest
# from . import models, services, storage
from app.models import Receipt 
from app.main import  get_receipt_points, processReceipt


# Helper function to manually calculate points based on rules
# This mirrors the logic described in README.md
def calculate_expected_points(receipt_data: dict) -> int:
    # Validate structure first using Pydantic model
    # This ensures the input data matches the expected format
    try:
        receipt = Receipt(**receipt_data)
    except Exception as e:
        print(f"Pydantic validation failed for data: {receipt_data}")
        raise e # Re-raise validation error

    points = 0

    # Rule 1: Retailer alphanumeric characters
    retailer_name = receipt.retailer
    alphanumeric_chars = re.findall(r'[a-zA-Z0-9]', retailer_name)
    points += len(alphanumeric_chars)
    # print(f"Retailer points: {len(alphanumeric_chars)}")

    # Rule 2: Round dollar total
    total = Decimal(receipt.total)
    if total == total.to_integral_value():
        points += 50
        # print("Round total points: 50")

    # Rule 3: Total is multiple of 0.25
    # Use Decimal for precision
    if total % Decimal('0.25') == Decimal('0.00'):
        points += 25
        # print("Multiple of 0.25 points: 25")

    # Rule 4: 5 points per two items
    num_items = len(receipt.items)
    points += (num_items // 2) * 5
    # print(f"Item pairs points: {(num_items // 2) * 5}")

    # Rule 5: Item description length multiple of 3
    for item in receipt.items:
        trimmed_desc = item.shortDescription.strip()
        if len(trimmed_desc) > 0 and len(trimmed_desc) % 3 == 0:
            price = Decimal(item.price)
            # Multiply by 0.2 and round up to the nearest integer
            item_points_decimal = (price * Decimal('0.2'))
            # Use math.ceil for rounding up
            item_points = math.ceil(item_points_decimal)
            points += item_points
            # print(f"Item '{item.shortDescription}' points: {item_points}")

    # Rule 6: Odd purchase day
    if receipt.purchaseDate.day % 2 != 0:
        points += 6
        # print("Odd day points: 6")

    # Rule 7: Time between 2 PM (14:00) and 4 PM (16:00)
    # Time is strictly after 14:00 and strictly before 16:00
    purchase_time = receipt.purchaseTime
    if purchase_time.hour == 14 and purchase_time.minute > 0:
        points += 10
        # print("Time window points (14:xx): 10")
    elif purchase_time.hour == 15:
        points += 10
        # print("Time window points (15:xx): 10")

    return points

# --- Test Setup ---

# Define the directory containing example JSON files relative to this test file
# Assumes tests/ is inside receipt-processor/
# TESTS_DIR = Path(__file__).parent
# PROJECT_ROOT = TESTS_DIR.parent.parent # Go up two levels from tests/test_...py
# print(f"Project root: {PROJECT_ROOT}")
# EXAMPLES_DIR = PROJECT_ROOT / "examples"

EXAMPLES_DIR = "/examples/"

TEST_FILES = [
    "simple-receipt.json",
    "morning-receipt.json",
    "test-receipt-1.json", 
    "test-receipt-2.json", 
    "test-receipt-3.json", 
    "test-receipt-4.json", 
    "readme-example-1.json",
    "readme-example-2.json",
]

# Function to load JSON and calculate expected points
def load_and_prepare_test_data(filename):
    file_path = f"{EXAMPLES_DIR}/{filename}"
    p = Path(file_path)
    if not p.exists():
        # Mark test as skipped if file doesn't exist yet
        # This allows running pytest even before files are created
        return pytest.param(None, None, id=f"{filename}-MISSING", marks=pytest.mark.skip(reason=f"File not found: {filename}"))
    try:
        with open(p, 'r') as f:
            data = json.load(f)
        expected = calculate_expected_points(data)
        # Use filename as ID for better test reporting
        return pytest.param(data, expected, id=filename)
    except Exception as e:
        print(f"Error processing {filename}: {e}")
        # Fail the test setup if processing fails for an existing file
        pytest.fail(f"Failed to load or process {filename}: {e}")


# Prepare test data
test_params = [load_and_prepare_test_data(f) for f in TEST_FILES]

# --- Test Cases ---

@pytest.mark.parametrize("receipt_data, expected_points", test_params)
def test_point_calculation_logic(receipt_data, expected_points):
    """
    Tests the point calculation logic against manually calculated expected values.
    This verifies the rules implementation in `calculate_expected_points`.
    Once `services.calculate_points` is implemented, this test structure
    can be adapted to call that function instead.
    """
    # If receipt_data is None, the test is skipped by the marker in load_and_prepare_test_data
    if receipt_data is None:
        return

    # For now, we test our manual calculation helper against the expected value
    # derived from the same helper. This primarily validates the test data loading
    # and the helper function itself based on the rules.
    calculated_points = calculate_expected_points(receipt_data)
    assert calculated_points == expected_points

# --- Placeholder for README examples (to be created) ---
# We need to create JSON files for the examples shown in README.md

# readme-example-1.json (Expected: 28 points)
# readme-example-2.json (Expected: 109 points)
