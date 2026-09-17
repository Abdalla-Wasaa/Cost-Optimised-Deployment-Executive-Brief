import pytest
from fastapi.testclient import TestClient
from api.config import Settings
from api.main import create_app
from api.spend import SpendGuard, SpendExceeded
from cost.cost_model import load, calculate, token_cost, break_even

def test_economics():
    a=load()
    assert token_cost(a) == pytest.approx(0.0001755)
    assert calculate(a)['monthly_usd'] == pytest.approx(147.55)
    assert calculate(a,1000000)['monthly_usd'] == pytest.approx(305.5)
    assert calculate(a,hit_rate=.6)['monthly_usd'] == pytest.approx(137.02)
    assert break_even(a) == pytest.approx(1170/.0001255)
    with pytest.raises(ValueError): calculate(a,0)
    with pytest.raises(ValueError): calculate(a,hit_rate=2)

def test_reservation_and_reset():
    now=[0]
    g=SpendGuard(.2,10,clock=lambda:now[0])
    g.reserve(.1); g.reserve(.1)
    with pytest.raises(SpendExceeded): g.reserve(.01)
    now[0]=10
    g.reserve(.2)
    assert float(g.used)==.2

def test_guard_blocks_provider():
    with TestClient(create_app(Settings(spend_ceiling=0))) as c:
        assert c.post('/triage',json={'message':'hello'}).status_code==503
        assert c.app.state.provider.calls==0
