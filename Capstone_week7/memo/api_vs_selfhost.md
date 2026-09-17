# Decision memo — API-hosted versus self-hosted inference
**Audience:** Finance and engineering sponsor · **Date:** 17 September 2026
**Decision:** choose a managed API for a future controlled pilot; retain the free
stub for this assessed demonstration. No live API or GPU comparison was performed.

The workload is a small educational symptom-routing API. This project evaluates
economics and deployment mechanics, not diagnostic competence. Clinical release
requires a separate safety evaluation and governance decision. Baseline demand is
100,000 incoming requests/month; the stress scenario is a sustained million/month.
Both are planning assumptions. Exact caching achieved 60% on an artificial fixture;
that proportion must be measured on consented representative traffic before use in
a financial forecast. For sensitive deployment, cache sharing needs tenant/session
boundaries and a reviewed data retention policy.

## Alternatives and operational consequences

| Dimension | Managed API | Self-hosted open-source model |
|---|---|---|
| Economics | Variable input/output tokens, plus application hosting and operations | Reserved GPU capacity, storage and more operations, plus variable costs |
| Utilisation | Pay per processed item; low utilisation avoids idle GPU expense | Idle hardware still costs; batching and sustained utilisation matter |
| Scaling | Provider quotas and rate limits; application still needs admission control | Capacity procurement, replication, scheduling and warm-up are our responsibility |
| Availability | Depend on provider and network; monitor limits and outages | Own hardware failures, failover and redundancy; one GPU is not high availability |
| Latency | Network and provider queueing; measure actual tails | Potential local latency control, but saturation and cold starts hurt tails |
| Privacy/security | Review vendor retention, residency and access terms | More infrastructure control, but responsibility for isolation, patching and deletion |
| Observability | Record usage, cost and latency without patient-text logs | Also monitor GPU memory/utilisation, scheduler queues and serving health |
| Maintenance/upgrades | Provider handles serving; pin versions and regression-test changes | Own serving stack, vulnerabilities, drivers, model licensing and upgrade testing |
| People burden | Estimated 4 hours/month | Estimated 16 hours/month; on-call and model operations can exceed this |

No throughput, quality or latency equivalence between the alternatives is assumed.
An open model must meet the same independently reviewed quality target before a
price comparison can justify switching. Model licensing and residency checks are
future selection work, not claims of compliance in this demo.

## Break-even, with visible assumptions

All figures below are **MODELLED/ESTIMATED USD**, not invoices or current vendor
quotes. Reproduce with `python -m cost.cost_model`; change `cost/assumptions.json`.
Input 450 tokens at illustrative $0.15/million and output 180 at $0.60/million yield
`v_api = $0.0001755` per processed item. API fixed monthly cost is `$30 + 4×$25 = $130`.
Self-host fixed monthly cost is estimated `$850 GPU + $50 storage/observability +
16×$25 operations = $1,300`, plus `$0.00005` per processed item. These GPU figures
are scenario allowances inspired by classwork, **not a machine quotation or benchmark**.

Let N be incoming requests/month and h be the same cache hit rate on both options:

```
API(N)  = 130  + N × (1-h) × 0.0001755
Self(N) = 1300 + N × (1-h) × 0.00005
N*      = (1300-130) / ((1-h) × (0.0001755-0.00005))
```

At h=0, the estimated crossing is **9.32 million requests/month**.
At h=0.60, it rises to **23.31 million incoming requests/month**. Caching improves
both options, so it must not be credited only to the API side. A single GPU's
capacity at either volume is unknown; adding GPUs or high availability moves the
crossing upward. If self-host variable cost meets/exceeds API cost, this model has
no positive-volume crossing. Batching has no assumed token discount.

| Monthly traffic | API, no cache | API, 60% hits | Self-host, no cache | Self-host, 60% hits |
|---:|---:|---:|---:|---:|
| 100,000 | $147.55 | $137.02 | $1,305 | $1,302 |
| 1,000,000 | $305.50 | $200.20 | $1,350 | $1,320 |

At baseline, people time dominates token costs. Removing operations would make the
comparison artificially favourable. The sensitivity script changes tokens and
people allocations one at a time. Higher output length or API pricing lowers the
crossing; cheaper GPU capacity and better utilisation may also lower it. More
on-call, redundancy, slower generation or low utilisation raise it. Actual cache
hit rate and safe reuse constraints are important unknowns.

## Recommendation and conditions

**Go for the local educational demo; conditional go for a tightly bounded API
pilot; no-go for clinical use or a GPU commitment today.** Before a pilot: obtain
dated rates, a small capped live-provider fixture test, privacy approval, reviewed
clinical labels, durable shared spend reservations and an owner for alert response.
Set token/request limits, timeouts and zero or bounded retries before enabling paid
calls. The current stub-only implementation deliberately cannot spend on inference.

Revisit self-hosting when measured sustained demand approaches the revised crossing,
when privacy constraints require it, or when provider reliability/quality is
unacceptable. Require a GPU pilot measuring output quality, p95 latency, throughput,
utilisation and failure recovery under representative traffic. A lower spreadsheet
number alone is insufficient to justify operating a model fleet.
