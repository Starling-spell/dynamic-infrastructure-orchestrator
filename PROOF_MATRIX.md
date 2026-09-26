# Proof matrix

| Invariant | Direct test | Live evidence |
|---|---|---|
| Supported ordered batch atomically advances model | test_safe_batch_advances_once | APPLIED; see LIVE_PROOFS.md |
| Reversed shutdown order blocked | test_dependency_cannot_be_disabled_first | Not claimed |
| Documented maintenance restriction enforced | test_documented_restriction_rejects | REJECTED; see LIVE_PROOFS.md |
| Changed hash fails closed | test_changed_document_fails_closed | Not claimed |
| UNKNOWN cannot apply | test_unknown_cannot_apply | Not claimed |
| Deadline expires safely | test_expiry_preserves_model | Not claimed |
| Competing old parent cannot overwrite | test_competing_plan_is_stale | STALE; see LIVE_PROOFS.md |
| Owner and network isolation | test_owner_and_network_binding | Not claimed |
| Exact comparison rejects a decision mismatch | test_consensus_comparison_rejects_decision_difference | Pure predicate only |
| CLI-safe compact plan canonicalizes and applies | test_compact_cli_entrypoint | APPLIED; see LIVE_PROOFS.md |

GenVM lint/SDK validation passed. All 11 direct tests passed. Compact malformed
schema rejection is also covered by `test_compact_schema_rejects`.

Direct mode does not execute validator comparison. A unit predicate test is not a
live disagreement proof. Live receipts and stored state are documented separately.
