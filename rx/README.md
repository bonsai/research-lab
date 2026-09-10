# RX — Research Experience

RX is the subject-side experience layer of the research system.

It records how a research subject experiences observations, decisions, actions,
outcomes, evaluation, learning, and changes to the next research question.

## Architecture

```text
RP → RQ → RW → TF → AW → Outcome/Evidence → Evaluation
                                      ↓
                                     RX
                                      ↓
                              Research State Update
                                      ↓
                                  Next RQ ↺
```

RX does not execute research. AW executes Work. RX records how the subject's
research state changes through that work.

## Canonical event

An RX event is a state transition:

```text
prior_state
  → trigger
  → experience
  → interpretation
  → state_update
  → next_question?
```

See `ontology/rx.yaml` and `schemas/rx-event.schema.json`.

## Example

```json
{
  "id": "RX-001",
  "subject": "researcher-001",
  "timestamp": "2026-09-10T12:00:00+09:00",
  "trigger": "EXP-001 produced a counterexample",
  "prior_state": {"confidence": 0.7},
  "experience": "The five-layer ontology did not cleanly classify the system.",
  "interpretation": "The ontology may work better as an epistemic coordinate system than as an implementation taxonomy.",
  "state_update": {"confidence": 0.45, "strategy": "test boundary cases first"},
  "uncertainty": 0.35,
  "confidence": 0.45,
  "strategy_change": "prioritize falsification experiments",
  "next_question": "Does the ontology add value when no learned cognition is present?"
}
```

## Evidence boundary

An RX event is not automatically evidence. Evidence requires provenance and
research evaluation. Experience can generate a question, change a strategy,
or motivate an experiment without becoming empirical evidence by itself.

## Human and agent subjects

The same event model can represent a human researcher, research agent, or team.
The subject changes; the experience ontology does not.
