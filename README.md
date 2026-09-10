# research-lab

Reusable research laboratory templates and protocols.

This repository contains the **template layer** extracted from `bonsai/research-worldmodel` so that future research projects can start from a common structure without inheriting World Model-specific content.

## Template structure

```text
research-lab/
├── README.md
├── research-plan.md
├── protocol.md
├── questions/
│   └── RQ-000.md
├── theses/
│   └── current.md
├── experiments/
│   └── EXP-000/
│       ├── README.md
│       ├── matrix.yaml
│       └── counterexamples.md
├── evidence/
│   └── initial-observations.md
└── ontology/
    └── lab.yaml
```

## Principle

`Research Plan → RQ → Thesis/Antithesis → Gap → RW → TF → AW → Evidence → Evaluation → Revision → Next RQ`

Templates separate research process from domain content.

- **Research Plan** — what should be investigated
- **RQ** — what is not yet known
- **RW** — how it will be investigated
- **TF** — who/which roles perform the work
- **AW** — how Work is executed
- **Evidence** — what was actually observed and can support evaluation
- **Thesis Revision** — how knowledge changes

Domain-specific research belongs in the project repository that uses these templates.
