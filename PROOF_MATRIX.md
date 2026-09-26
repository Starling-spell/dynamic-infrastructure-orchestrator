# Proof matrix

| Invariant | Direct test | Live evidence |
|---|---|---|
| Supported ordered batch atomically advances model | test_safe_batch_advances_once | Pending |
| Reversed shutdown order blocked | test_dependency_cannot_be_disabled_first | Pending |
| Documented maintenance restriction enforced | test_documented_restriction_rejects | Pending |
| Changed hash fails closed | test_changed_document_fails_closed | Pending |
| UNKNOWN cannot apply | test_unknown_cannot_apply | Not claimed |
| Deadline expires safely | test_expiry_preserves_model | Not claimed |
| Competing old parent cannot overwrite | test_competing_plan_is_stale | Pending |
| Owner and network isolation | test_owner_and_network_binding | Not claimed |
| Exact comparison rejects a decision mismatch | test_consensus_comparison_rejects_decision_difference | Pure predicate only |
| CLI-safe compact plan canonicalizes and applies | test_compact_cli_entrypoint | Pending |

Direct mode does not execute validator comparison. A unit predicate test is not a
live disagreement proof. Live receipts and stored state are documented separately.
