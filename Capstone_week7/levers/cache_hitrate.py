import argparse
import asyncio
import json
from pathlib import Path
from api.config import Settings
from api.service import TriageService
from api.providers.stub import StubModelProvider

FIXTURE = Path(__file__).resolve().parents[1]/'tests/fixtures/triage.json'

def workload():
    rows = json.loads(FIXTURE.read_text())
    return rows+rows[:30]+rows[:30]

async def check():
    service = TriageService(Settings(cache_enabled=True),StubModelProvider(delay=0))
    for row in workload():
        result = await service.process(row['message'])
        if result.urgency != row['urgency']:
            raise AssertionError('quality contract regression')
    return service.metrics()

if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--threshold',type=float,default=.55)
    args=parser.parse_args()
    if not 0 <= args.threshold <= 1:
        parser.error('threshold must be between 0 and 1')
    metrics=asyncio.run(check())
    print(json.dumps(metrics,indent=2))
    raise SystemExit(0 if metrics['cache_hit_rate'] >= args.threshold else 1)
