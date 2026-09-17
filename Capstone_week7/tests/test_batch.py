import asyncio
import pytest
from fastapi.testclient import TestClient
from api.config import Settings
from api.main import create_app
from api.service import TriageService
from api.providers.stub import StubModelProvider
from levers.batch_worker import BatchQueue, QueueUnavailable

def test_batch_bounds_mapping_and_partial_window():
    async def run():
        calls=[]
        async def process(messages):
            calls.append(messages)
            return [m.upper() for m in messages]
        q=BatchQueue(process,max_batch=3,max_wait=.01)
        try:
            assert await asyncio.gather(*(q.submit(str(i)) for i in range(7)))==list('0123456')
            assert [len(c) for c in calls]==[3,3,1]
            assert await q.submit('word')=='WORD'
        finally:
            await q.close()
    asyncio.run(run())

def test_failure_and_recovery():
    async def run():
        async def process(messages):
            if 'fail' in messages: raise ValueError('failed')
            if 'short' in messages: return []
            return messages
        q=BatchQueue(process)
        try:
            for message in ('fail','short'):
                results=await asyncio.gather(q.submit(message),q.submit('ok'),return_exceptions=True)
                assert all(isinstance(x,ValueError) for x in results)
            assert await q.submit('ok')=='ok'
        finally: await q.close()
    asyncio.run(run())

def test_overload_timeout_and_shutdown():
    async def run():
        started=asyncio.Event()
        release=asyncio.Event()
        async def process(messages):
            started.set()
            await release.wait()
            return messages
        q=BatchQueue(process,max_batch=1,capacity=1,timeout=.2)
        first=asyncio.create_task(q.submit('a'))
        await started.wait()
        second=asyncio.create_task(q.submit('b'))
        await asyncio.sleep(0)
        with pytest.raises(QueueUnavailable): await q.submit('c')
        await q.close()
        result=await asyncio.gather(first,second,return_exceptions=True)
        assert all(isinstance(x,QueueUnavailable) for x in result)
        with pytest.raises(QueueUnavailable): await q.submit('closed')
        q=BatchQueue(process,max_batch=1,timeout=.01)
        try:
            with pytest.raises(TimeoutError): await q.submit('timeout')
        finally: await q.close()
    asyncio.run(run())

def test_batch_spend_admission_and_no_cache_on_failure():
    async def run():
        service=TriageService(Settings(batch_enabled=True,spend_ceiling=.0001755))
        try:
            result=await asyncio.gather(service.process('a'),service.process('b'),return_exceptions=True)
            assert all(isinstance(x,Exception) for x in result)
            assert service.provider.calls==0
            assert not service.cache.rows
        finally: await service.close()
    asyncio.run(run())

def test_api_batch_timeout():
    with TestClient(create_app(Settings(batch_enabled=True,provider_timeout=.001),StubModelProvider(.1))) as c:
        assert c.post('/triage',json={'message':'hello'}).status_code==503
        assert c.get('/metrics').json()['batch_failures']==1
