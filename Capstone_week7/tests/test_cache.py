import asyncio
import subprocess
import sys
from fastapi.testclient import TestClient
from api.main import create_app
from api.models import TriageResponse
from levers.cache_triage import ExactCache, cache_key
from levers.cache_hitrate import check

def test_miss_hit_and_metrics():
    with TestClient(create_app()) as c:
        assert c.post('/triage',json={'message':'headache'}).json()['cache']=='MISS'
        assert c.post('/triage',json={'message':' headache '}).json()['cache']=='HIT'
        metrics=c.get('/metrics').json()
        assert metrics['cache_hit_rate']==.5
        assert metrics['provider_calls']==1

def test_normalization_is_conservative():
    assert cache_key(' chest pain ')==cache_key('chest pain')
    for text in ('no chest pain','Chest pain','chest  pain','chest pains'):
        assert cache_key(text)!=cache_key('chest pain')

def test_ttl_capacity_copy():
    now=[0]
    c=ExactCache(ttl=5,capacity=1,clock=lambda:now[0])
    assert c.hit_rate==0
    v=TriageResponse(urgency='review',advice='demo')
    c.put('a',v)
    c.get('a').advice='mutated'
    assert c.get('a').advice=='demo'
    now[0]=5
    assert c.get('a') is None
    c.put('a',v);c.put('b',v)
    assert c.get('a') is None

def test_fixture_and_exit_gate():
    assert asyncio.run(check())['cache_hit_rate']==.6
    for threshold,code in [('.55',0),('.61',1)]:
        result=subprocess.run([sys.executable,'-m','levers.cache_hitrate','--threshold',threshold],capture_output=True)
        assert result.returncode==code
