import asyncio
import json
import logging
from api.spend import SpendGuard
from fastapi import FastAPI, HTTPException
from api.config import Settings
from api.models import TriageRequest, TriageResponse
from api.providers.stub import StubModelProvider

def create_app(settings=None, provider=None):
    settings = settings or Settings.from_env()
    provider = provider or StubModelProvider()
    app = FastAPI(title='Week 7 educational triage economics demo')
    app.state.provider = provider
    guard = SpendGuard(settings.spend_ceiling, settings.spend_window)
    app.state.guard = guard

    @app.get('/health')
    async def health():
        return {'status': 'ok', 'provider': 'stub', 'medical_use': False}

    @app.post('/triage', response_model=TriageResponse)
    async def triage(request: TriageRequest):
        try:
            guard.reserve(settings.reservation_per_item)
            logging.getLogger("capstone").info(json.dumps({"event":"provider_request","items":1}))
            results = await asyncio.wait_for(provider.process_batch([request.message]),
                                             settings.provider_timeout)
            if len(results) != 1:
                raise ValueError('provider result count mismatch')
            return results[0]
        except Exception:
            raise HTTPException(503, 'Demo provider unavailable; seek qualified care.') from None
    return app

app = create_app()
