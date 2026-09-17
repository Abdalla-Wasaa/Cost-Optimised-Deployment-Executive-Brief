# Staged measurement protocol
A: baseline without cache. B: same workload with exact cache. C will add batching
only after A/B are recorded. Run `python -m scripts.measure`. Raw A/B artifact:
`evidence/cache_measurements.json`. Cold service per configuration; 100 requests
in waves of ten, fixed 20ms synthetic provider delay. Timings include ASGI request
validation/serialization, exclude TCP, Docker and external model latency. Nearest
rank p50/p95; throughput is requests / total wall time including wave scheduling.
No warm-up, no tuning, no discarded requests; hardware timing will vary.

40 unique inputs then 60 repeats yield exactly 60% hits with sufficient TTL/capacity.
Quality checks expected urgency, advice and disclaimer for every result. These
prove optimisation contract preservation only, not clinical safety. Cost/1k is
modelled at 100k/month using cost/assumptions.json, including $130 fixed costs.
Actual provider spend is zero. Cache eviction/expiry/concurrent duplicates reduce
hits in real use. There is no cross-request single-flight suppression.
