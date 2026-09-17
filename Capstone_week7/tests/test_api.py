import asyncio
from fastapi.testclient import TestClient
from api.main import create_app
from api.providers.stub import StubModelProvider

def test_health_and_triage():
    with TestClient(create_app()) as c:
        assert c.get('/health').json()['medical_use'] is False
        result = c.post('/triage', json={'message': 'chest pain'})
        assert result.status_code == 200
        assert result.json()['urgency'] == 'emergency'
        assert 'not medical advice' in result.json()['disclaimer']

def test_validation():
    with TestClient(create_app()) as c:
        for body in ({}, {'message': ''}, {'message': '   '}, {'message': 'x'*1001},
                     {'message': 4}, {'message': 'hello', 'patient_id': 'secret'}):
            assert c.post('/triage', json=body).status_code == 422

def test_deterministic_stub():
    async def run():
        p = StubModelProvider(delay=0)
        assert await p.process_batch(['headache']) == await p.process_batch(['headache'])
    asyncio.run(run())

def test_failure():
    class Broken:
        async def process_batch(self, messages):
            raise RuntimeError('sensitive provider details')
    with TestClient(create_app(provider=Broken())) as c:
        r = c.post('/triage', json={'message': 'hello'})
        assert r.status_code == 503
        assert 'sensitive' not in r.text
