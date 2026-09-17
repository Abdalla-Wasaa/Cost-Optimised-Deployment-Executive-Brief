# Reproducible cost model (USD; MODELLED, not billed)
Run `python -m cost.cost_model` and `python -m cost.sensitivity` from Capstone_week7.
Override the complete JSON with `--assumptions path.json`. Invalid negative rates,
non-finite values and invalid volumes are rejected. No secrets belong in this file.

| Assumption | Value | Provenance / status |
|---|---:|---|
| Input / output per million tokens | $0.15 / $0.60 | Illustrative classroom rates from wk7/monday; not a current vendor quote |
| Input / output tokens per model item | 450 / 180 | Synthetic planning shape from classwork; not observed tokenizer usage |
| Baseline traffic / sustained 10x month | 100,000 / 1,000,000 | Chosen planning scenarios, no production traffic |
| Hosting, logs and egress allowance | $30/month | Estimated small service allowance, not a cloud quote |
| Operations | 4 hours/month × $25 | Estimated staffing allocation, not salary data |
| GPU / storage / self-host people | $850 / $50 / 16h × $25 | Estimated classwork-inspired scenario; no GPU provisioned |
| Self-host variable cost per processed item | $0.00005 | Estimated energy/egress proxy; no benchmark |

Input cost = 450 × 0.15 / 1e6 = $0.0000675.
Output cost = 180 × 0.60 / 1e6 = $0.000108.
Model item cost v = $0.0001755. Fixed cost F = 30 + 4 × 25 = $130/month.
For incoming requests N and cache hit fraction h:
`monthly = F + N × (1-h) × v`; `unit = monthly/N`; `per_1k = 1000×unit`.
The cache saves tokens only on hits. Batching receives **no token discount**.

| Traffic/month | Cache | Monthly total | Cost/request | Cost/1,000 |
|---:|---:|---:|---:|---:|
| 100,000 | 0% | $147.55 | $0.0014755 | $1.4755 |
| 100,000 | 60% | $137.02 | $0.0013702 | $1.3702 |
| 1,000,000 | 0% | $305.50 | $0.0003055 | $0.3055 |
| 1,000,000 | 60% | $200.20 | $0.0002002 | $0.2002 |

Baseline avoided token cost is $10.53/month (7.14% fully loaded); spike saving
$105.30/month (34.47%). Fixture repetition does not predict production cache hits.
A 10x spike here means a full month at 10x volume; a one-day spike costs less.
Fixed infrastructure is held constant to isolate traffic; this is not a capacity
claim. Scale-out, taxes, FX, network overages, retries, security reviews and higher
support demands require a revised allowance. Zero retries in the implemented demo.
Sensitivity varies one assumption at a time, including people time; no uncertainty
interval is claimed. Replace rates with dated vendor quotes before any spending.
