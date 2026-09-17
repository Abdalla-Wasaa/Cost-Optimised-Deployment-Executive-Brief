from typing import Literal
from pydantic import BaseModel, Field, field_validator, ConfigDict

DISCLAIMER = 'Educational demonstration only; not medical advice or a diagnosis.'

class TriageRequest(BaseModel):
    model_config = ConfigDict(extra='forbid')
    message: str = Field(min_length=1, max_length=1000)

    @field_validator('message')
    @classmethod
    def nonblank(cls, value):
        if not value.strip():
            raise ValueError('message must contain text')
        return value

class TriageResponse(BaseModel):
    urgency: Literal['emergency', 'review']
    advice: str
    disclaimer: str = DISCLAIMER
    provider: str = 'stub-v1'
    cache: Literal['DISABLED', 'MISS', 'HIT'] = 'DISABLED'
