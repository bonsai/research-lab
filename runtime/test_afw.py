"""Verification for the conceptual AFW runtime."""

from afw import AFW, DEFAULT_ROLES, DEFAULT_TRANSITIONS


def test_experiment_branch_reaches_evidence():
    runtime = AFW(DEFAULT_ROLES, DEFAULT_TRANSITIONS)
    runtime.run(
        [
            ("professor", {"intent": "test"}),
            ("researcher", {"rq": "RQ"}),
            ("engineer", {"experiment": "EXP"}),
            ("analyst", {"evidence": "E"}),
        ]
    )
    assert runtime.state.history == ["intent", "rq", "task", "experiment", "evidence"]


def test_investigation_branch_reaches_evidence():
    runtime = AFW(DEFAULT_ROLES, DEFAULT_TRANSITIONS)
    runtime.run(
        [
            ("professor", {"intent": "test"}),
            ("researcher", {"rq": "RQ"}),
            ("researcher", {"task": "investigate"}),
            ("analyst", {"evidence": "E"}),
        ]
    )
    assert runtime.state.state == "evidence"


def test_invalid_actor_is_rejected():
    runtime = AFW(DEFAULT_ROLES, DEFAULT_TRANSITIONS)
    try:
        runtime.step("engineer")
    except ValueError as exc:
        assert "invalid transition" in str(exc)
    else:
        raise AssertionError("invalid actor/state combination was accepted")


def test_research_loop_returns_to_rq():
    runtime = AFW(DEFAULT_ROLES, DEFAULT_TRANSITIONS)
    runtime.run(
        [
            ("professor", {"intent": "test"}),
            ("researcher", {"rq": "RQ"}),
            ("engineer", {"experiment": "EXP"}),
            ("analyst", {"evidence": "E"}),
            ("analyst", {"reflection": "RX"}),
            ("professor", {"next_rq": "RQ2"}),
            ("professor", {"rq": "RQ2"}),
        ]
    )
    assert runtime.state.history[-2:] == ["next_rq", "rq"]
