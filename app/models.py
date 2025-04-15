import re
from typing import List, Annotated
from pydantic import BaseModel, Field, StringConstraints, BeforeValidator
from datetime import date, time
from decimal import Decimal

# Regex patterns from the API spec
RETAILER_PATTERN = r"^[\w\s\-&]+$"
DECIMAL_PRICE_PATTERN = r"^\d+\.\d{2}$"
SHORT_DESC_PATTERN = r"^[\w\s\-]+$"


class Item(BaseModel):
    shortDescription: Annotated[str, StringConstraints(pattern=SHORT_DESC_PATTERN)] = Field(..., description="The Short Product Description for the item.", example="Mountain Dew 12PK")
    price: Annotated[str, StringConstraints(pattern=DECIMAL_PRICE_PATTERN)] = Field(..., description="The total price paid for this item.", example="6.49")

    @property
    def price_decimal(self) -> Decimal:
        """Get the price as a Decimal for calculations."""
        return Decimal(self.price)

class Receipt(BaseModel):
    retailer: Annotated[str, StringConstraints(pattern=RETAILER_PATTERN)] = Field(..., description="The name of the retailer or store the receipt is from.", example="M&M Corner Market")
    purchaseDate: date = Field(..., description="The date of the purchase", example="2022-01-01")
    purchaseTime: time = Field(..., description="The time of the purchase 24-hour time expected.", example="13:01")
    items: List[Item] = Field(..., min_length=1, description="List of items purchased.")
    total: Annotated[str, StringConstraints(pattern=DECIMAL_PRICE_PATTERN)] = Field(..., description="Purchase total", example="6.49")

    @property
    def total_decimal(self) -> Decimal:
        """Get the total as a Decimal for calculations."""
        return Decimal(self.total)

class ProcessResponse(BaseModel):
    id: str = Field(..., description="The ID assigned to the receipt.", example="adb6b560-0eef-42bc-9d16-df48f30e89b2")

class PointsResponse(BaseModel):
    points: int = Field(..., description="The number of points awarded.", example=100)
