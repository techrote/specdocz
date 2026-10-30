# Research and evidence library

This folder contains **non-normative** syntheses that explain what is documented, how strongly it is supported, what is still uncertain, and what may be worth implementing. These are references for agents and humans; they do not supersede a consuming project's requirements.

## Find a study

The machine-readable entry point is [catalog.yaml](catalog.yaml); a study's `id` is stable across file revisions. Search `topics`, `applicable_to` and `title`, then open only the relevant study and annexes.

| Study | ID | Primary document | Scope |
| --- | --- | --- | --- |
| [Zero-Player Level Design](zero-player-level-design/README.md) | `RESEARCH-ZPL-001` | [metastudy.md](zero-player-level-design/metastudy.md) | Auto-Mario, DDA/PN/PF, physics choreography, deterministic replay and exhibition-style demos |

## Classes and authority

- **Standards** (`../tuiuiux/`, `../mzpaint/`, `../parametermaxing/`): explicitly normative reusable contracts. They are tailored before adoption.
- **Patterns**: possible architectures, techniques and verification recipes. Non-normative unless adopted.
- **Research** (this directory): documented evidence, synthesis, candidate patterns, limitations and research gaps. Always non-normative by default.

Recommended precedence in a project:

```text
project safety / scientific / functional / compatibility rules
  > project-specific authoritative specification
  > applicable reusable normative standard
  > explicitly adopted/adapted implementation pattern
  > research synthesis, examples, community observations
```

## Evidence markings

Prefer primary sources. Clearly distinguish **direct evidence**, **corroboration**, **inference/synthesis**, **proposed engineering guidance**, and **open questions**. Evidence-source type (developer, academic, journalism, community) is **not a confidence score**. Do not claim tests, platform determinism, peer review or independent verification that have not occurred.

## Consuming the library

1. Audit live project state, active ownership, instructions, existing requirements and constraints.
2. Identify the relevant research with `catalog.yaml`; read only scoped chapters/annexes.
3. Record repo+exact commit SHA+document path, study ID/version and (when relevant) source URLs/date.
4. Classify each candidate as **Adopt / Adapt / Reject / Extend**, with rationale and evidence level.
5. Express adopted outcomes directly in the *project repository* as self-contained requirements and acceptance tests.
6. Keep uncertainty and failure evidence visible. Research updates never silently rewrite an earlier project's pinned decisions.

See [CONTRIBUTING.md](CONTRIBUTING.md) for study creation, integrity checks and promotion. Use [the template](_templates/metastudy-template.md) for new syntheses.
