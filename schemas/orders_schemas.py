
from pydantic import BaseModel, Field


class CreateOrder(BaseModel):

    driver_id: int
    warehouser_id: int
    customer_loc_id: int


class UpdateOrder(BaseModel):
    id: int
    status: int = Field(..., lt=3)
    driver_id: int
    warehouser_id: int
    customer_loc_id: int

