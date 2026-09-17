# Verification record — 2026-09-17

## Local checks
- Fresh temporary Python 3.12 virtual environment installed requirements.txt.
- 16 pytest tests passed in 0.98s; full output: tests.txt. Two upstream TestClient
  deprecation warnings, no test failures. Dependency snapshot: environment.txt.
- Cache gate: 60 hits, 40 misses, 60%; default 55% exits 0, 61% exits 1 (tested).
- Three staged ASGI configurations: 100 requests each, 100/100 contract matches,
  zero errors. Final raw samples: measurements.json. Earlier independent cache
  sweep and pre-logging batch sweep retained, clearly named.
- Cost calculation and sensitivity outputs: cost_model.json and sensitivity.json.
- Docker Compose configuration parsed successfully.
- Image capstone-week7:1.0.0 built locally (image ID 736c14c13c46).
- Installed Compose build path crashed in buildx integration; direct docker build
  succeeded using its legacy fallback. No build tooling was modified.
- Published port 8000 was occupied. Used `docker compose -p capstone-week7-review
  -f deploy/docker-compose.cost.yml run --no-deps -d --name
  capstone-week7-review-smoke triage`, which publishes no host port.
- Inside that container GET /health returned status ok/provider stub; repeated
  synthetic triage returned MISS then HIT; metrics showed 2 requests, 1 provider
  item, hit rate 0.5 and modelled reserved cost 0.0001755 USD.
- Docker inspect reported `healthy demo true`: healthy, user demo, read-only root.
- Container JSON logs included cache MISS, provider_batch items=1 and cache HIT,
  without message text. The test container and project network were removed after
  validation. No unrelated service was stopped.
- Executive PDF generated using optional ReportLab export, one page; visually reviewed.

Tests using TestClient initially stalled in the restricted execution sandbox;
network-enabled execution passed. CI uses normal GitHub runners. No hidden live
provider fallback, cloud credentials, clinical data or paid inference was used.

## Evidence boundaries
MEASURED: local timing/counts, contract checks, Docker build and isolated API checks.
STUBBED: all inference outputs and the fixed 20ms synthetic call overhead.
MODELLED: token costs, full costs, avoided dollars and traffic scenarios.
ESTIMATED: staffing/hosting/GPU allowances, self-host variable cost and break-even.
NOT PERFORMED: cloud deployment/alert receipt, real model or GPU benchmarks,
production capacity study, clinical quality evaluation or external security audit.

GitHub statuses and review links are in PR_NOTES.md. Configured CI is not described
as passing until an actual remote run succeeds. Secret review checks staged paths
and known credential formats without printing matching values; it cannot certify
that no possible secret format exists. No .env, virtual environment or classwork
files are part of this repository.
