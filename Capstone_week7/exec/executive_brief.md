# Week 7 executive brief: control cost before scaling

**Decision requested:** approve an educational demo and a gated API pilot plan.  
**No-go:** clinical use or a self-hosted GPU purchase without further evidence.

The service turns a short symptom message into a structured demo urgency response.
It is **not medical advice**. This project demonstrates cost controls and reliable
software behaviour using a free deterministic substitute for an AI model.

| Monthly planning scenario | Before optimisation | With 60% exact-cache hits |
|---|---:|---:|
| 100,000 requests | $147.55 total; $1.4755/1,000 | $137.02 total; $1.3702/1,000 |
| Sustained 10×: 1,000,000 requests | $305.50 total; $0.3055/1,000 | $200.20 total; $0.2002/1,000 |

**These are modelled costs, not bills.** They include $30/month hosting and four
operations hours at $25/hour. Token rates, message lengths, traffic and staffing
are visible assumptions. The artificial fixture's 60% hit rate is not a demand forecast.

**Lever 1 — exact caching:** reuse an identical message's response for up to ten
minutes. In the measured 100-request fixture, model items fell from 100 to 40.
This models 60% token savings, but only **7.14% total savings at baseline** because
staffing and hosting remain. Keys preserve wording and punctuation; no semantic
matching is used.

**Lever 2 — batching:** group up to ten waiting requests. After caching, measured
provider calls fell from 40 to 4; model items stayed at 40. **No additional dollar
saving is claimed.** Small queues may add waiting time. It is a transport efficiency
result from the stub, not a paid-provider discount or GPU benchmark.

**Performance and quality:** the recorded local sweep completed 100/100 contract
checks in every configuration. p95 was 24.45ms baseline, 25.33ms cached, and 25.53ms
cached plus batching. p95 means 95 out of 100 requests completed within that time.
The demo objective is p95 ≤100ms; these short stub timings do not predict live AI
latency. Quality here means preserving expected synthetic responses, not proving
clinical safety.

**Primary risk:** a cheap response may still be clinically wrong. Mitigation:
keep the service educational; require clinician-reviewed evaluation and privacy
approval before any patient use. In-memory caching and queues are bounded but
volatile. Real deployments need tenant isolation, durable spend accounting and
reviewed retention; this demonstration uses no patient data.

**Budget protection:** a simulated $1/hour application guard refuses model work
when its reservation ceiling is exhausted. AWS budget examples alert at 80% actual
and 100% forecast of $250/month; alerts do not stop spend and have not been deployed.
External API invoices and people time require separate reconciliation. Unoptimised
10× traffic exceeds the overall $250 planning envelope.

**API versus self-host:** prefer API for a controlled pilot. The estimated cost
crossing is 9.32m requests/month without caching, 23.31m with equal 60% caching on
both sides. GPU capacity and model quality are untested; baseline demand is far
below either scenario. See the memo for the equation and staffing assumptions.

**Conditions to proceed:** verify current prices and realistic demand; independently
validate quality; set live request/token/spend limits; prove alert receipt and shared
spend enforcement; assign a budget owner. No paid-provider experiment or cloud
production deployment has occurred. Evidence: `levers/measurements.md`,
`cost/cost_model.md`, `memo/api_vs_selfhost.md` and `evidence/EVIDENCE_CHECKLIST.md`.
