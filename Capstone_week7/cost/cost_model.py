"""USD scenario calculator. All defaults are illustrative, not provider quotes."""
import argparse
import json
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict

class Assumptions(BaseModel):
    model_config = ConfigDict(extra='forbid', allow_inf_nan=False)
    input_per_million: float = Field(ge=0)
    output_per_million: float = Field(ge=0)
    input_tokens: int = Field(ge=0)
    output_tokens: int = Field(ge=0)
    monthly_requests: int = Field(gt=0)
    infra_monthly: float = Field(ge=0)
    ops_hours: float = Field(ge=0)
    ops_hourly: float = Field(ge=0)
    selfhost_gpu_monthly: float = Field(ge=0)
    selfhost_ops_hours: float = Field(ge=0)
    selfhost_storage_monthly: float = Field(ge=0)
    selfhost_variable: float = Field(ge=0)

def load(path=None):
    return Assumptions.model_validate_json(Path(path or Path(__file__).with_name('assumptions.json')).read_text())

def token_cost(a):
    return (a.input_tokens*a.input_per_million + a.output_tokens*a.output_per_million)/1e6

def calculate(a, volume=None, hit_rate=0):
    n = a.monthly_requests if volume is None else volume
    if n <= 0 or not 0 <= hit_rate <= 1:
        raise ValueError('positive volume and hit rate in [0, 1] required')
    variable = n*(1-hit_rate)*token_cost(a)
    fixed = a.infra_monthly + a.ops_hours*a.ops_hourly
    return dict(requests=n, hit_rate=hit_rate, tokens_usd=variable,
                infra_usd=a.infra_monthly, people_usd=a.ops_hours*a.ops_hourly,
                monthly_usd=variable+fixed, per_request_usd=(variable+fixed)/n,
                per_1000_usd=(variable+fixed)*1000/n,
                avoided_token_usd=n*hit_rate*token_cost(a))

def break_even(a, hit_rate=0):
    if not 0 <= hit_rate < 1:
        raise ValueError('hit rate must be in [0, 1)')
    extra_fixed = (a.selfhost_gpu_monthly+a.selfhost_storage_monthly
                   +a.selfhost_ops_hours*a.ops_hourly
                   -a.infra_monthly-a.ops_hours*a.ops_hourly)
    margin = (1-hit_rate)*(token_cost(a)-a.selfhost_variable)
    return max(0, extra_fixed/margin) if margin > 0 else None

if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--assumptions')
    args=parser.parse_args()
    a=load(args.assumptions)
    print(json.dumps({'classification':'MODELLED illustrative USD assumptions',
        'scenarios':[calculate(a,n,h) for n in (a.monthly_requests,a.monthly_requests*10)
                     for h in (0,0.6)],
        'break_even_requests':break_even(a),
        'break_even_with_cache':break_even(a,0.6)},indent=2))
