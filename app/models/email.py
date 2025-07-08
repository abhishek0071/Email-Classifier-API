from pydantic import BaseModel, Field
from typing import Optional  

class EmailIn(BaseModel):
    subject: Optional[str] = Field(
    default=None,
    example="Claim payout",
    description="Optional. Leave blank if no separate subject."
   )
    body: str = Field(..., example="Congratulations! You have won...")

class EmailOut(BaseModel):
    label: str
    model_name: str            # ← finalised name
    latency_ms: float