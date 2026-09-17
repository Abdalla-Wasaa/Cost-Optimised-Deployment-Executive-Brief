from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from api.config import Settings
from api.models import TriageRequest, TriageResponse
from api.service import TriageService

def create_app(settings=None, provider=None):
    settings = settings or Settings.from_env()
    service = TriageService(settings, provider)
    @asynccontextmanager
    async def lifespan(app):
        yield
        await service.close()

    app = FastAPI(title='Week 7 educational triage economics demo', lifespan=lifespan)
    app.state.service = service
    app.state.provider = service.provider
    app.state.guard = service.guard

    @app.get('/health')
    async def health():
        return {'status':'ok','provider':'stub','medical_use':False}

    @app.get('/metrics')
    async def metrics():
        return service.metrics()

    @app.post('/triage', response_model=TriageResponse)
    async def triage(request: TriageRequest):
        try:
            return await service.process(request.message)
        except Exception:
            raise HTTPException(503, 'Demo provider unavailable; seek qualified care.') from None
    return app

app = create_app()
