# Evidence checklist
All commands start in Capstone_week7 unless specified. Never use real patient text
in screenshots. Store screenshots here; none are fabricated by this submission.

| Evidence | Status | Exact action / expected result | Suggested screenshot |
|---|---|---|---|
| Tests | Local pass; see VERIFICATION.md | `python -m pytest -q` → all pass | tests.png |
| Cache regression | Measured 60% | `python -m levers.cache_hitrate` → exit 0; `python -m levers.cache_hitrate --threshold .61` → exit 1 | cache-gate.png |
| Staged experiment | Raw JSON committed | `python -m scripts.measure --output evidence/reproduction.json` → all quality checks pass; inspect call/item counts | staged-results.png |
| Cost and sensitivity | Modelled | `python -m cost.cost_model`; `python -m cost.sensitivity` | costs.png |
| API health | Local demo | `curl -fsS http://127.0.0.1:8000/health` → status ok, provider stub | health.png |
| Docker | See VERIFICATION.md | `docker compose -f deploy/docker-compose.cost.yml up --build -d --wait`; health command above | docker-health.png |
| Cache logs | Instrumented | POST identical fixture twice then `docker compose -f deploy/docker-compose.cost.yml logs --no-color` → MISS then HIT, no message text | cache-logs.png |
| AWS budget | CONFIG ONLY; manual | Replace notification email, set account ID, activate project tag, run command below; inspect budget and delivery | budget-config.png, alert-received.png |
| FinOps tags | Compose labels configured | Apply project/environment/owner/cost-centre tags to actual resources; activate billing allocation tag | resource-tags.png |
| GitHub CI/PRs | See PR_NOTES.md | At repository root `gh pr list --state all`; `gh run list --workflow capstone-ci.yml` | github-ci.png |
| Executive PDF | PDF generated and reviewed | Follow exec/PDF_INSTRUCTIONS.md; inspect one page | executive-brief.png |
| Live inference / GPU | NOT TESTED | Separate reviewed pilot required; no adapter or paid test command is provided | Do not imply this evidence exists |

## Cloud budget (manual account-specific action)

```bash
# Edit deploy/aws_budget_notifications.json with your real verified recipient first.
export AWS_ACCOUNT_ID=YOUR_12_DIGIT_ACCOUNT_ID
aws budgets create-budget --account-id "$AWS_ACCOUNT_ID" \
  --budget file://deploy/aws_budget.json \
  --notifications-with-subscribers file://deploy/aws_budget_notifications.json
aws budgets describe-budget --account-id "$AWS_ACCOUNT_ID" \
  --budget-name capstone-week7-monthly
```

Expected: tagged monthly cost budget $250 with 80% actual and 100% forecast alerts.
In the AWS console, verify recipient subscription/delivery using an account-approved
notification test. Creating a budget does not prove receipt. Capture the budget,
filters, thresholds and a redacted received notification. Do not spend money merely
to trigger an alert. AWS does not include an external model vendor's bill or staffing.

## Spend rejection demonstration

```bash
SPEND_CEILING_USD=0 CACHE_ENABLED=false python -m uvicorn api.main:app --port 8001
# In a second terminal:
curl -i http://127.0.0.1:8001/triage -H 'Content-Type: application/json' \
  -d '{"message":"synthetic demo"}'
curl -fsS http://127.0.0.1:8001/metrics
```

Expected HTTP 503, spend_rejections=1, provider_calls=0. Save spend-guard.png.
Restart the default service afterward; restarts reset this demonstration's guard.

Outstanding production evidence: dated pricing quote, representative token usage,
clinical validation, traffic/capacity study, privacy/retention review, durable shared
budget test, real provider failure drill and any self-host GPU capacity results.
These are explicit future gates, not missing screenshots of work claimed complete.
