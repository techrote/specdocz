# cohesive-techspression

Reusable specifications for **cohesive, layered expert interfaces that preserve deep technical control while presenting task-oriented, intuitive ways to shape a system as a whole**.

Cohesive-techspression is derived from Zaaggenz and is closely related to parametermaxing, but solves a different problem:

- **parametermaxing** optimizes access to individual parameters, ranges, precision, safety and expert inspection;
- **cohesive-techspression** optimizes how many parameters, tools and representations are organized into a coherent user experience.

Its core ideas are:

- multiple workspace/layer views over one authoritative state;
- grouping controls by user intent, causal relationship and likely sequence of use rather than implementation module;
- progressive disclosure from intuitive controls to focused parameter groups to full expert detail;
- shared context, naming, feedback and state across surfaces;
- broad **intent / theme / feel controls** that drive several lower-level parameters through proportional, curved, conditional, sidechained or context-dependent mappings;
- exact lower-level access remaining available underneath those broad controls.

## Documents

| Document | Purpose |
| --- | --- |
| [cohesive-techspression-uiux-spec-zaaggenz.md](cohesive-techspression-uiux-spec-zaaggenz.md) | Normative UI/UX specification with Zaaggenz provenance and concrete workspace examples |
| [cohesive-techspression-uiux-spec.md](cohesive-techspression-uiux-spec.md) | Standalone normative UI/UX specification |
| [cohesive-techspression-implementation-spec-zaaggenz.md](cohesive-techspression-implementation-spec-zaaggenz.md) | Direct implementation contract with Zaaggenz-oriented examples |
| [cohesive-techspression-implementation-spec.md](cohesive-techspression-implementation-spec.md) | Standalone direct implementation contract |
| [cohesive-techspression-spec-tailoring.md](cohesive-techspression-spec-tailoring.md) | Procedure for creating a project-specific workspace/control-layer specification |

## Relationship to other specdocz families

Cohesive-techspression SHOULD often be combined with:

- **parametermaxing** for detailed numerical parameter controls;
- **tuiuiux** for tile/workspace interaction and mouse/keyboard parity;
- domain-specific families such as **mzpaint** where the editable content model has additional semantics.

Use the tailoring guide rather than copying the reference application's exact workspace names or control mappings.
