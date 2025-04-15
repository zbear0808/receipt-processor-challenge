from .models import Receipt, Item
import math
from decimal import Decimal
from datetime import time

def alphanumeric_rule(receipt: Receipt) -> int:
    """
    One point for every alphanumeric character in the retailer name.

    Args:
        receipt: the `Receipt` object containing details.

    Returns:
        points: int
    """
    return sum(c.isalnum() for c in receipt.retailer)

def roundDollarRule(receipt: Receipt) -> int:
    """
    50 points if the total is a round dollar amount with no cents, otherwise 0.

    Args:
        receipt: the `Receipt` object containing details.

    Returns:
        points: int
    """
    return 50 if receipt.total_decimal % 1 == 0 else 0

def roundQuarterRule(receipt: Receipt) -> int:
    """
    25 points if the total is a multiple of 0.25, otherwise 0.

    Args:
        receipt: the `Receipt` object containing details.

    Returns:
        points: int
    """
    return 25 if receipt.total_decimal % Decimal('0.25') == 0 else 0

def itemCountRule(receipt: Receipt) -> int:
    """
    5 points for every two items on the receipt.
    Args:
        receipt: the `Receipt` object containing details.

    Returns:
        points: int
    """
    return (len(receipt.items) // 2) * 5

def descriptionLengthRule(item: Item) -> int:
    """
    If the trimmed length of the item description is a multiple of 3, multiply the price by 0.2 and round up to the nearest integer. The result is the number of points earned.
    Args:
        item: Item with shortDescription and price.
    Returns:
        points: int
        """
    if len(item.shortDescription.strip()) % 3 == 0:
        return math.ceil(item.price_decimal * Decimal('0.2')) 
    else:
         return 0

def oddPurchaseDateRule(receipt: Receipt) -> int:
    """
    6 points if the day in the purchase date is odd.

    Args:
        receipt: the `Receipt` object containing details.

    Returns:
        points: int
    """
    return 6 * (receipt.purchaseDate.day % 2 == 1)

def purchaseTimeRule(receipt: Receipt) -> int:
    """
    10 points if the time of purchase is after 2:00pm and before 4:00pm.

    Args:
        receipt: the `Receipt` object containing details.

    Returns:
        points: int
    """
    return 10 * (time(14, 0) <= receipt.purchaseTime <= time(16, 0))


def calculateAllItemRules(receipt: Receipt) -> int:
    """
    Calculates points based on any item rules.

    Args:
        receipt: The `Receipt` object containing details.

    Returns:
        points: `int` total points based on any item rules.
    """
    return sum(rule(item) for rule in item_rules for item in receipt.items)

item_rules = [descriptionLengthRule, ]
receipt_rule_fns = [alphanumeric_rule, roundDollarRule, roundQuarterRule, itemCountRule, oddPurchaseDateRule, purchaseTimeRule]


def calculatePoints(receipt: Receipt) -> int:
    """
    Calculates the points awarded for a given receipt.

    Placeholder implementation: This function currently returns 0 points.
    Replace this with the actual points calculation logic based on the rules.

    Args:
        receipt: the `Receipt` object containing details.

    Returns:
        The calculated points
    """
    points = sum(rule(receipt) for rule in receipt_rule_fns)
    points += calculateAllItemRules(receipt)
    return points
