from ninja import Schema, ModelSchema, FilterSchema, Field
from datetime import datetime
from typing import Optional, List, Self
from pydantic import model_validator

from discount.models import DiscountCode,PriceRule

class PriceRuleIn(Schema):
    title: str
    target_type: str
    target_selection: str
    allocation_method: str
    value_type: str
    value: float

class PriceRuleOut(Schema):
    id: int
    title: str
    target_type: str
    target_selection: str
    allocation_method: str
    value_type: str
    value: int
    customer_segment_prerequisite: Optional[str] = ''
    prerequisite_quantity_range: Optional[int] = None
    prerequisite_shipping_price_range: Optional[float] = None
    prerequisite_subtotal_range: Optional[float] = None
    prerequisite_to_entitlement_quantity_ratio: Optional[int] = None
    prerequisite_to_entitlement_purchase: Optional[int] = None
    starts_at: datetime
    ends_at: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True

class PriceRuleResp(Schema):
    price_rule: PriceRuleOut


class DiscountCodeIn(Schema):
    price_rule_id: int
    code: str
    usage_count: Optional[int] = 0
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class DiscountCodeOut(Schema):
    id: int
    price_rule_id: int
    code: str
    usage_count: int = 0
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True

class DiscountCodeResp(Schema):
    discount_code: DiscountCodeOut
