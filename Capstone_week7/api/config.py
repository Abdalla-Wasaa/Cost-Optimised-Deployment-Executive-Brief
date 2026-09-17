import os
from pydantic import BaseModel, Field

class Settings(BaseModel):
    provider: str = 'stub'
    provider_timeout: float = Field(default=2, gt=0, le=30)

    @classmethod
    def from_env(cls):
        settings = cls(provider=os.getenv('PROVIDER', 'stub'),
                       provider_timeout=os.getenv('PROVIDER_TIMEOUT', '2'))
        if settings.provider != 'stub':
            raise ValueError('Only the free stub provider is implemented')
        return settings
