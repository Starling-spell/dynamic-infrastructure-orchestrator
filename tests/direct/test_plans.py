import hashlib
import json
from pathlib import Path

SPEC = Path("examples/specification.txt").read_text()
RUNBOOK = Path("examples/runbook.txt").read_text()
GOOD = [{"component": "machine", "from": "ACTIVE", "to": "STANDBY"},
        {"component": "cooling", "from": "ACTIVE", "to": "MAINTENANCE"}]
DEADLINE = 1767229200


def sha(text):
    return hashlib.sha256(text.encode()).hexdigest()


def setup(direct_vm, direct_deploy, direct_alice, runbook_hash=None):
    direct_vm.sender = direct_alice
    direct_vm.warp("2026-01-01T00:00:00Z")
    contract = direct_deploy("contracts/DynamicInfrastructureOrchestrator.py")
    contract.create_network("demo", "https://a.example/spec", sha(SPEC),
                            "https://a.example/runbook", runbook_hash or sha(RUNBOOK))
    contract.register_component("demo", "cooling", "ACTIVE")
    contract.register_component("demo", "machine", "ACTIVE", "cooling")
    contract.seal_network("demo")
    direct_vm.mock_web(r".*a\.example/spec", {"status": 200, "body": SPEC})
    direct_vm.mock_web(r".*a\.example/runbook", {"status": 200, "body": RUNBOOK})
    return contract


def vote(direct_vm, allowed="PASS", sequence="PASS", recovery="PASS"):
    direct_vm.mock_llm(r".*Evaluate a PLANNED infrastructure model transition.*", json.dumps({
        "maintenance_allowed": allowed, "sequencing_safe": sequence, "recovery_defined": recovery}))


def propose(contract, name="good", steps=GOOD):
    contract.propose_transition("demo", name, 0, json.dumps(steps), DEADLINE)


def test_safe_batch_advances_once(direct_vm, direct_deploy, direct_alice):
    c = setup(direct_vm, direct_deploy, direct_alice)
    propose(c)
    vote(direct_vm)
    before = c.get_snapshot("demo", 0)
    c.apply_transition("demo", "good")
    n = c.get_network("demo")
    assert n["version"] == 1 and n["components"]["machine"]["state"] == "STANDBY"
    assert n["components"]["cooling"]["state"] == "MAINTENANCE"
    assert c.get_plan("demo", "good")["state"] == "APPLIED"
    assert before == c.get_snapshot("demo", 0)
    with direct_vm.expect_revert("terminal plan"):
        c.apply_transition("demo", "good")


def test_dependency_cannot_be_disabled_first(direct_vm, direct_deploy, direct_alice):
    c = setup(direct_vm, direct_deploy, direct_alice)
    with direct_vm.expect_revert("active dependency would be interrupted"):
        propose(c, steps=list(reversed(GOOD)))
    assert c.get_network("demo")["version"] == 0


def test_documented_restriction_rejects(direct_vm, direct_deploy, direct_alice):
    c = setup(direct_vm, direct_deploy, direct_alice)
    propose(c, steps=[{"component": "machine", "from": "ACTIVE", "to": "MAINTENANCE"}])
    vote(direct_vm, allowed="FAIL", sequence="FAIL")
    c.apply_transition("demo", "good")
    assert c.get_plan("demo", "good")["state"] == "REJECTED"
    assert c.get_network("demo")["version"] == 0


def test_changed_document_fails_closed(direct_vm, direct_deploy, direct_alice):
    c = setup(direct_vm, direct_deploy, direct_alice, "f" * 64)
    propose(c)
    vote(direct_vm)
    c.apply_transition("demo", "good")
    assert c.get_plan("demo", "good")["state"] == "INCONCLUSIVE"
    assert json.loads(c.get_record("demo", "good"))["packet"]["report"]["matches"] == [True, False]
    assert c.get_network("demo")["version"] == 0


def test_unknown_cannot_apply(direct_vm, direct_deploy, direct_alice):
    c = setup(direct_vm, direct_deploy, direct_alice)
    propose(c)
    vote(direct_vm, recovery="UNKNOWN")
    c.apply_transition("demo", "good")
    assert c.get_plan("demo", "good")["state"] == "INCONCLUSIVE"
    assert c.get_network("demo")["version"] == 0


def test_expiry_preserves_model(direct_vm, direct_deploy, direct_alice):
    c = setup(direct_vm, direct_deploy, direct_alice)
    propose(c)
    direct_vm.warp("2026-01-01T02:00:00Z")
    # gltest 0.29.2 refreshes sender but not message_raw.datetime after warp.
    from genlayer import gl
    gl.message_raw["datetime"] = "2026-01-01T02:00:00Z"
    c.apply_transition("demo", "good")
    assert c.get_plan("demo", "good")["state"] == "EXPIRED"
    assert c.get_network("demo")["version"] == 0


def test_competing_plan_is_stale(direct_vm, direct_deploy, direct_alice):
    c = setup(direct_vm, direct_deploy, direct_alice)
    propose(c, "first")
    propose(c, "second")
    vote(direct_vm)
    c.apply_transition("demo", "first")
    c.apply_transition("demo", "second")
    assert c.get_plan("demo", "second")["state"] == "STALE"
    assert c.get_network("demo")["version"] == 1


def test_owner_and_network_binding(direct_vm, direct_deploy, direct_alice, direct_bob):
    c = setup(direct_vm, direct_deploy, direct_alice)
    propose(c)
    c.create_network("other", "https://a.example/spec", sha(SPEC),
                     "https://a.example/runbook", sha(RUNBOOK))
    with direct_vm.expect_revert("not proposed in this network"):
        c.apply_transition("other", "good")
    direct_vm.sender = direct_bob
    with direct_vm.expect_revert("network owner required"):
        c.apply_transition("demo", "good")


def test_consensus_comparison_rejects_decision_difference():
    # Pure predicate test only: direct mode does not exercise live validators.
    source = Path("contracts/DynamicInfrastructureOrchestrator.py").read_text()
    start = source.index("def same_report(")
    end = source.index("\n\n@allow_storage", start)
    scope = {}
    exec(source[start:end], scope)
    assert scope["same_report"]({"vector": ["PASS"] * 3}, {"vector": ["PASS"] * 3})
    assert not scope["same_report"]({"vector": ["PASS"] * 3}, {"vector": ["FAIL", "PASS", "PASS"]})
