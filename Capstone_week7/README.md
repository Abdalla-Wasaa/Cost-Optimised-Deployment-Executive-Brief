# Week 7 Capstone — Cost-Optimised Deployment & Executive Brief
Educational demo only, not medical advice. No credentials or paid provider needed.

From `Capstone_week7`: `python -m pip install -r requirements.txt`,
`python -m pytest -q`, then `python -m uvicorn api.main:app`.
POST `/triage` with `{"message":"headache"}`; GET `/health` checks the service.

Implementation progresses through five focused branches: foundation, economics and
controls, cache, batch, and decision packet. All project work is isolated here.
