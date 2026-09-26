# Threat model

| Threat | Enforcement / residual limit |
|---|---|
| Caller claims maintenance is safe | No summary/score input; fetched full documents evaluated independently |
| Modified source | Exact full-body commitments; INCONCLUSIVE, unchanged model |
| Cross-network plan | Composite storage key and stored network ID |
| Unauthorized mutation | Network owner check on every write after creation |
| Replay | PROPOSED-only resolution; immutable terminal state |
| Stale competing plan | Exact parent version and root check; STALE |
| Dependency outage | Simulate each ordered step; ACTIVE dependency invariant |
| Cyclic dependency | References only earlier components; graph frozen at seal |
| Expired plan | EXPIRED without nondeterministic calls or graph update |
| Conflicting validators | Exact independently reconstructed report; no accepted mutation |
| Truncated/malformed evidence | UTF-8 and size completeness gates; UNKNOWN vector |
| Prompt injection | Untrusted-data prompt boundary; residual LLM risk remains |
| Dishonest owner/documents | Not solved; owner selects specification and modeled state |

Reviewer question: is this merely validating caller-supplied text? No: the proposed
ordered steps are caller inputs, but the semantic constraints are acquired by each
validator through network-side web fetches. Yet this checks document compatibility,
not independently observed physical infrastructure. That narrower claim is essential.
