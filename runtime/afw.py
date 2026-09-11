"""Minimal Agent Flow/Framework prototype for the research runtime.

Conceptual implementation of the research-runtime ontology:
- role layer: Subject -> Role -> Responsibility
- state layer: State -> Transition -> Loop

This is deliberately small: it demonstrates the model without binding the
research-lab template to a specific agent framework.
"""

from dataclasses import dataclass, field
import sys
from typing import Any


@dataclass(frozen=True)
class Role:
    name: str
    responsibility: str


@dataclass(frozen=True)
class Transition:
    source: str
    target: str
    actor: str


@dataclass
class ResearchState:
    state: str = "intent"
    payload: dict[str, Any] = field(default_factory=dict)
    history: list[str] = field(default_factory=lambda: ["intent"])


class AFW:
    """Tiny stateful runtime for role-aware research work."""

    def __init__(self, roles: list[Role], transitions: list[Transition]):
        self.roles = {role.name: role for role in roles}
        self.transitions = transitions
        self.state = ResearchState()

    def available(self) -> list[Transition]:
        return [t for t in self.transitions if t.source == self.state.state]

    def step(self, actor: str, output: dict[str, Any] | None = None) -> ResearchState:
        candidates = [t for t in self.available() if t.actor == actor]
        if not candidates:
            raise ValueError(
                f"invalid transition: state={self.state.state!r}, actor={actor!r}"
            )

        transition = candidates[0]
        if actor not in self.roles:
            raise ValueError(f"unknown role: {actor!r}")

        self.state.state = transition.target
        if output:
            self.state.payload.update(output)
        self.state.history.append(transition.target)
        return self.state

    def run(self, actors: list[tuple[str, dict[str, Any] | None]]) -> ResearchState:
        for actor, output in actors:
            self.step(actor, output)
        return self.state


DEFAULT_ROLES = [
    Role("professor", "question"),
    Role("researcher", "investigate"),
    Role("engineer", "implement"),
    Role("analyst", "evaluate"),
    Role("archivist", "record"),
]


DEFAULT_TRANSITIONS = [
    Transition("intent", "rq", "professor"),
    Transition("rq", "task", "researcher"),
    Transition("task", "investigation", "researcher"),
    Transition("task", "experiment", "engineer"),
    Transition("investigation", "evidence", "analyst"),
    Transition("experiment", "evidence", "analyst"),
    Transition("evidence", "reflection", "analyst"),
    Transition("reflection", "next_rq", "professor"),
    Transition("next_rq", "rq", "professor"),
]


def demo() -> ResearchState:
    """Run one complete experiment branch and return the resulting state."""
    runtime = AFW(DEFAULT_ROLES, DEFAULT_TRANSITIONS)
    return runtime.run(
        [
            ("professor", {"intent": "Can architecture data become research evidence?"}),
            ("researcher", {"rq": "Can a corpus be made comparable?"}),
            ("engineer", {"experiment": "build corpus prototype"}),
            ("analyst", {"evidence": "prototype produced comparable records"}),
            ("analyst", {"reflection": "measurement is reproducible enough for RX"}),
            ("professor", {"next_rq": "Which representation changes the result?"}),
            ("professor", {"rq": "Which representation changes the result?"}),
        ]
    )


def run_from(start_state: str) -> ResearchState:
    """Run a deterministic proof path beginning at a requested state."""
    valid_states = {t.source for t in DEFAULT_TRANSITIONS} | {t.target for t in DEFAULT_TRANSITIONS}
    if start_state not in valid_states:
        raise ValueError(f"invalid start state: {start_state!r}")

    runtime = AFW(DEFAULT_ROLES, DEFAULT_TRANSITIONS)
    runtime.state.state = start_state
    runtime.state.history = [start_state]

    proof_actor = {
        "intent": "professor",
        "rq": "researcher",
        "task": "engineer",
        "investigation": "analyst",
        "experiment": "analyst",
        "evidence": "analyst",
        "reflection": "professor",
        "next_rq": "professor",
    }

    while runtime.state.state not in {"evidence", "rq"}:
        actor = proof_actor[runtime.state.state]
        runtime.step(actor, {"afw": "proof"})

    return runtime.state


if __name__ == "__main__":
    start_state = sys.argv[1] if len(sys.argv) > 1 else "intent"
    result = run_from(start_state)
    print(" -> ".join(result.history))
    print(result.payload)
