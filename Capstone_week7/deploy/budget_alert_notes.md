# Budget controls: config-only cloud fallback
Cloud alert example: $250 monthly AWS tagged infrastructure budget; actual 80%
($200) and forecast 100%. Replace recipient, activate project cost-allocation tag,
apply equivalent tags on actual cloud resources (Compose labels do not do this).
Examples follow the [AWS create-budget reference](https://docs.aws.amazon.com/cli/latest/reference/budgets/create-budget.html)
and [CLI examples](https://docs.aws.amazon.com/cli/latest/userguide/cli_budgets_code_examples.html), consulted 2026-09-17.
No cloud resources or notification deliveries have been demonstrated.
External model bills and people time are outside this AWS budget: reconcile these
separately in a $250 overall planning envelope. Baseline $147.55 fits; unoptimised
10x $305.50 exceeds it. Cached 10x $200.20 fits only under the stated assumptions.

FinOps tags: project=capstone-week7, environment=demo, owner=capstone-maintainer,
cost-centre=education. Replace owner before deployment. At alert: named maintainer
checks billing and usage, pauses experiments, investigates failures, updates Finance;
forecast breach triggers a capacity/traffic review. Verify receipt with a controlled
notification test; budget alerts are delayed signals, not synchronous spending caps.

Application guard reserves simulated USD per item before provider invocation, with
$1/hour default and no retries. Refuses expensive work with HTTP 503 at exhaustion;
failed/timeout calls keep reservations. Cache hits need no reservation. This demo
only supports the free stub: reserved amounts are modelled, never actual spend.
Window resets after one hour; process restart resets state. One worker/replica only:
a real paid rollout needs durable shared atomic reservations, actual token ceilings,
usage reconciliation and account-level limits. Do not multiply replicas with this
local guard and claim a global cap. Unknown provider settings fail at startup.
