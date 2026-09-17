import os
from pydantic import BaseModel, Field

class Settings(BaseModel):
    provider: str = 'stub'
    cache_enabled: bool = True
    cache_ttl: float = Field(default=600, gt=0, allow_inf_nan=False)
    cache_capacity: int = Field(default=1024, ge=1, le=100000)
    spend_ceiling: float = Field(default=1, ge=0, allow_inf_nan=False)
    spend_window: float = Field(default=3600, gt=0, allow_inf_nan=False)
    reservation_per_item: float = Field(default=0.0001755, gt=0, allow_inf_nan=False)
    provider_timeout: float = Field(default=2, gt=0, le=30)

    @classmethod
    def from_env(cls):
        settings = cls(provider=os.getenv('PROVIDER', 'stub'),
                       cache_enabled=os.getenv('CACHE_ENABLED','true'),
                       cache_ttl=os.getenv('CACHE_TTL_SECONDS','600'),
                       cache_capacity=os.getenv('CACHE_CAPACITY','1024'),
                       provider_timeout=os.getenv('PROVIDER_TIMEOUT', '2'),
                       spend_ceiling=os.getenv('SPEND_CEILING_USD', '1'),
                       spend_window=os.getenv('SPEND_WINDOW_SECONDS', '3600'),
                       reservation_per_item=os.getenv('RESERVATION_PER_ITEM_USD', '0.0001755'))
        if settings.provider != 'stub':
            raise ValueError('Only the free stub provider is implemented')
        return settings
