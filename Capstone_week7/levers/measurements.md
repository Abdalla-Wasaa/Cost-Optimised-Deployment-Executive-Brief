# Staged measurement protocol
A: baseline without cache. B: same workload with exact cache. C adds batching after the original A/B run was recorded. Run `python -m scripts.measure` for the final A/B/C sweep. Raw A/B artifact:
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

## Final staged run

MEASURED locally with deterministic stub; all dollar columns MODELLED.

| Configuration | Requests | Provider calls / items | Hit rate | Full cost/1k | p50 ms | p95 ms | Requests/s | Quality |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| A baseline | 100 | 100 / 100 | 0% | $1.4755 | 21.78 | 24.45 | 373.2 | 100/100 |
| B cache | 100 | 40 / 40 | 60% | $1.3702 | 0.62 | 25.33 | 629.6 | 100/100 |
| C cache + batching | 100 | 4 / 40 | 60% | $1.3702 | 0.84 | 25.53 | 679.7 | 100/100 |

Raw sorted samples, timestamp, Python version, host and fixture SHA-256 are in
`evidence/measurements.json`. The previous independently recorded A/B run remains
in `evidence/cache_measurements.json`; neither run was selected for better timing.

A→B isolates cache: 60 fewer processed items, 60% modelled token saving, 7.14%
fully loaded saving at 100k/month. B→C isolates batching: transport calls fall
40→4 but processed items stay 40 and modelled dollar cost stays unchanged.
This is transport consolidation, not evidence of a provider bulk-price discount.
Observed timings are short local samples, not statistically established speedups.
The stub models a fixed 20ms call overhead, not GPU compute; baseline allows ten
concurrent calls, whereas batching has one worker. Real provider throughput may
respond differently. No paid calls, GPU throughput or production capacity measured.

Max batch=10, window=5ms, waiting queue=100, request timeout=3s, provider timeout=2s.
The window limits collection time once a worker can service a batch; queued work
may wait behind earlier batches. The total request timeout bounds that delay.
Sparse requests pay the collection window; full batches flush immediately. A batch
failure fails all its callers; the worker continues with subsequent batches. No
retries. Failed results never enter cache. Requests cancelled before processing are
skipped; in-flight work may finish and remains reserved. Shutdown fails pending
futures. The queue is volatile, not a durable clinical job system. Both levers use
bounded in-memory storage; no Redis is required or implicitly contacted.

Demo SLO: p95 ≤100ms and success ≥99% for this 100-request ASGI fixture window.
p95 means 95% of requests complete at or below that latency; it is not the mean.
A 1% error budget permits one failed request in this 100-request window, but this
quality gate is stricter and requires all fixture results to pass. All configurations
met this local objective. A live service SLO needs a representative sustained test.

The final sweep was rerun after enabling INFO JSON event output; the earlier sweep
is preserved in `evidence/measurements_pre_logging.json`. This is an instrumentation
change, so the table uses the final run rather than comparing timings across builds.
