"""Controlled staged ASGI benchmark; no network, paid tokens or clinical validation."""
import argparse
import asyncio
import hashlib
import json
import math
import platform
import time
from datetime import datetime, timezone
from pathlib import Path
import httpx
from api.config import Settings
from api.main import create_app
from levers.cache_hitrate import workload, FIXTURE
from cost.cost_model import load, calculate, token_cost

async def measure(name, cache, batch=False):
    app=create_app(Settings(cache_enabled=cache, batch_enabled=batch))
    rows=workload()
    latencies=[]
    quality=0
    async with app.router.lifespan_context(app):
        async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app),base_url='http://demo') as client:
            async def request(row):
                start=time.perf_counter()
                response=await client.post('/triage',json={'message':row['message']})
                latencies.append((time.perf_counter()-start)*1000)
                assert response.status_code==200, response.text
                result=response.json()
                expected_advice=('Seek immediate emergency assistance.' if row['urgency']=='emergency' else
                                 'This demo cannot assess your symptoms. Contact a qualified clinician.')
                assert result['advice']==expected_advice
                assert 'not medical advice' in result['disclaimer']
                return int(result['urgency']==row['urgency'])
            start=time.perf_counter()
            for offset in range(0,len(rows),10):
                quality+=sum(await asyncio.gather(*(request(row) for row in rows[offset:offset+10])))
            elapsed=time.perf_counter()-start
    m=app.state.service.metrics()
    latencies.sort()
    a=load()
    return {'configuration':name,'requests':len(rows),**m,'quality_correct':quality,
            'p50_ms':latencies[math.ceil(len(rows)*.50)-1],
            'p95_ms':latencies[math.ceil(len(rows)*.95)-1],
            'throughput_rps':len(rows)/elapsed,'elapsed_seconds':elapsed,
            'modelled_token_cost_per_1000':1000*m['provider_items']/len(rows)*token_cost(a),
            'modelled_fully_loaded_per_1000':calculate(a,hit_rate=m['cache_hit_rate'])['per_1000_usd'],
            'latencies_ms_sorted':latencies}

async def main(output):
    results=[await measure('A baseline',False),await measure('B cache',True),
             await measure('C cache + batching',True,True)]
    report={'classification':'MEASURED locally with deterministic STUB; costs MODELLED',
            'timestamp_utc':datetime.now(timezone.utc).isoformat(),
            'python':platform.python_version(),'platform':platform.platform(),
            'fixture_sha256':hashlib.sha256(FIXTURE.read_bytes()).hexdigest(),
            'concurrency':10,'stub_fixed_delay_ms':20,'results':results}
    Path(output).write_text(json.dumps(report,indent=2)+'\n')
    for row in results:
        print(json.dumps({k:v for k,v in row.items() if k!='latencies_ms_sorted'}))
    assert all(row['quality_correct']==row['requests'] for row in results)

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',default='evidence/measurements.json')
    asyncio.run(main(parser.parse_args().output))
