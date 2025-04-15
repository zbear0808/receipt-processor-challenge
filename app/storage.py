from typing import Dict, Any, Optional
from .models import Receipt

# Simple in-memory storage
# Structure: { "receipt_id": {"receipt": ReceiptObject, "points": calculated_points} }
receipt_storage: Dict[str, Dict[str, Any]] = {}

def save_receipt(receipt_id: str, receipt: Receipt, points: int):
    """Saves the receipt details and calculated points."""
    receipt_storage[receipt_id] = {"receipt": receipt, "points": points}
    print(f"Receipt {receipt_id} saved. Storage size: {len(receipt_storage)}") 

def get_points(receipt_id: str) -> Optional[int]:
    """Retrieves the points for a given receipt ID."""
    data = receipt_storage.get(receipt_id)
    if data:
        return data.get("points")
    return None

def receipt_exists(receipt_id: str) -> bool:
    """Checks if a receipt ID exists in storage."""
    return receipt_id in receipt_storage
