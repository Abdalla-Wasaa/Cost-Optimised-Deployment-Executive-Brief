# Pull requests and focused commits

Repository: https://github.com/Abdalla-Wasaa/Cost-Optimised-Deployment-Executive-Brief

| PR | Branch | Scope | Status at packet preparation |
|---|---|---|---|
| [1](https://github.com/Abdalla-Wasaa/Cost-Optimised-Deployment-Executive-Brief/pull/1) | chore/capstone-foundation | API, stub, initial tests and CI | Merged after both CI checks passed |
| [2](https://github.com/Abdalla-Wasaa/Cost-Optimised-Deployment-Executive-Brief/pull/2) | feat/cost-model-budget-controls | Cost, deployment, guard | Merged after both CI checks passed |
| [3](https://github.com/Abdalla-Wasaa/Cost-Optimised-Deployment-Executive-Brief/pull/3) | feat/exact-match-cache | Cache, gate, independent A/B evidence | Merged after both CI checks passed |
| 4 | feat/batch-queue | Bounded batch worker and A/B/C evidence | Publication in progress |
| 5 | docs/capstone-decision-packet | Memo, executive brief, evidence, reproduction | This packet, publication pending |

Focused implementation commits (merge commits additionally integrate updated main):
- `60e5ebc` feat(api): establish tested deterministic capstone foundation
- `b06673d` feat(finops): add reproducible costs deployment and spend reservations
- `d5eee2b` feat(cache): add bounded exact cache and measured regression fixture
- `8988c75` feat(batch): add bounded queue and staged performance evidence

The remote started empty. An empty main initialization commit established the PR
base. Initial restricted-network auth failed; after network-enabled auth succeeded,
prepared local branches were integrated with updated main and published sequentially.
No force-push, history rewrite or classwork changes. Generic local author identity
is documented in IMPLEMENTATION_PLAN.md. Each actual GitHub PR has the required
review template. The bodies below are preserved as reviewable descriptions.

At repository root, reproduce the review record:

```bash
gh pr list --repo Abdalla-Wasaa/Cost-Optimised-Deployment-Executive-Brief --state all
gh run list --repo Abdalla-Wasaa/Cost-Optimised-Deployment-Executive-Brief --workflow capstone-ci.yml
git log --oneline --all --graph
```

## PR 1 description

### Summary
Establish a free reproducible API foundation.

### Why
Complete a focused part of the Week 7 economics capstone with reproducible evidence.

### Changes
FastAPI contract, deterministic stub, validated inputs, configuration, initial README and GitHub Actions.

### Capstone deliverables addressed
Deployment foundation and quality scaffolding.

### Evidence / measurements
4 tests passed locally; no model credentials or live deployment.

### Testing
Local pytest and relevant regression checks passed before publication.

### Risks / trade-offs
No clinical validation. Synthetic keyword decisions only.

### Screenshots/manual evidence required
Cloud account budget alert delivery and any live-provider experiment remain manual.

### Checklist
- [x] tests pass locally
- [x] no secrets committed
- [x] documentation updated
- [x] measurements are reproducible where applicable
- [x] measured vs estimated results clearly labelled

## PR 2 description

### Summary
Make operating cost and spending assumptions reproducible.

### Why
Complete a focused part of the Week 7 economics capstone with reproducible evidence.

### Changes
Configurable input/output rates, infrastructure and people costs, 10x traffic, sensitivity, spend reservations, Docker and AWS budget examples.

### Capstone deliverables addressed
Cost model (20) and deployment/budget controls (20).

### Evidence / measurements
7 tests passed locally; baseline modelled $147.55/month at 100k requests. Compose configuration validated.

### Testing
Local pytest and relevant regression checks passed before publication.

### Risks / trade-offs
Rates are illustrative; cloud templates are unapplied; spend guard is per-process.

### Screenshots/manual evidence required
Cloud account budget alert delivery and any live-provider experiment remain manual.

### Checklist
- [x] tests pass locally
- [x] no secrets committed
- [x] documentation updated
- [x] measurements are reproducible where applicable
- [x] measured vs estimated results clearly labelled

## PR 3 description

### Summary
Reduce repeated processing while preserving the fixed demo contract.

### Why
Complete a focused part of the Week 7 economics capstone with reproducible evidence.

### Changes
Conservative exact keys, TTL and capacity bounds, metrics, hit-rate exit gate, fixtures and A/B measurement.

### Capstone deliverables addressed
Optimisation levers (25), cache portion.

### Evidence / measurements
11 tests passed; 60/100 cache hits; 100/100 contract checks in both modes. Raw A/B artifact committed.

### Testing
Local pytest and relevant regression checks passed before publication.

### Risks / trade-offs
Fixture hit rate is not a production forecast; no clinical equivalence claim.

### Screenshots/manual evidence required
Cloud account budget alert delivery and any live-provider experiment remain manual.

### Checklist
- [x] tests pass locally
- [x] no secrets committed
- [x] documentation updated
- [x] measurements are reproducible where applicable
- [x] measured vs estimated results clearly labelled

## PR 4 description

### Summary
Consolidate queued requests into bounded provider batches.

### Why
Complete a focused part of the Week 7 economics capstone with reproducible evidence.

### Changes
Batch size/window limits, overload rejection, deadlines, shutdown, failure recovery, per-item reservations and staged A/B/C evidence.

### Capstone deliverables addressed
Optimisation levers (25), batch and measurement portion.

### Evidence / measurements
16 tests passed; B to C transport calls 40 to 4, items unchanged at 40; all 100 fixture responses correct.

### Testing
Local pytest and relevant regression checks passed before publication.

### Risks / trade-offs
No token discount claimed. Stub overhead and short samples do not establish live-model performance.

### Screenshots/manual evidence required
Cloud account budget alert delivery and any live-provider experiment remain manual.

### Checklist
- [x] tests pass locally
- [x] no secrets committed
- [x] documentation updated
- [x] measurements are reproducible where applicable
- [x] measured vs estimated results clearly labelled

## PR 5 description

### Summary
Make capstone evidence and the decision understandable to a marker and business reader.

### Why
Complete a focused part of the Week 7 economics capstone with reproducible evidence.

### Changes
Decision memo, break-even, executive brief, rubric map, evidence checklist and complete reproduction commands.

### Capstone deliverables addressed
API/self-host memo (15), executive brief (20), integrated evidence.

### Evidence / measurements
Final verification is recorded in evidence/VERIFICATION.md.

### Testing
Local pytest and relevant regression checks passed before publication.

### Risks / trade-offs
No cloud deployment or clinical validation; all costs are modelled or estimated.

### Screenshots/manual evidence required
Cloud account budget alert delivery and any live-provider experiment remain manual.

### Checklist
- [x] tests pass locally
- [x] no secrets committed
- [x] documentation updated
- [x] measurements are reproducible where applicable
- [x] measured vs estimated results clearly labelled

