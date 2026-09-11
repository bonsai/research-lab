"""Minimal Agent Flow/Framework prototype for the research runtime.

Conceptual implementation of the research-runtime ontology:
- role layer: Subject -> Role -> Responsibility
- state layer: State -> Transition -> Loop

This is deliberately small: it demonstrates the model without binding the
research-lab template to a specific agent framework.
"""

from dataclasses import dataclass, field
from typing import Any, Callable


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


if __name__ == "__main__":
    result = demo()
    print(" -> ".join(result.history))
    print(result.payload)
