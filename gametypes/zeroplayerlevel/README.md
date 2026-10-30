# Zero-Player Level Design

**ID:** `RESEARCH-ZPL-001` · **Version:** 1.0 · **Researched:** 2026-10-30 · **Status:** narrative research synthesis, **non-normative**.

This study surveys Auto-Mario, *Don't Do Anything* (DDA), *Don't Move*, *Press Nothing* (PN), *Press Forward* (PF), and physics-authored kinetic/sightseeing levels. The distinction is explicit: PF requires a sustained input and is not literally zero-input. This material is research and proposed engineering guidance, not a claim that any engine currently implements the described interfaces or guarantees.

## Documents

| Document | Role |
| --- | --- |
| [metastudy.md](metastudy.md) | **Canonical**, complete 12-section 2026-10-30 source synthesis and engineering reference |
| [sources.md](sources.md) | Extracted annotated bibliography keyed [S01]–[S21]; canonical source annotations remain in metastudy §12 |
| [patterns.md](patterns.md) | Navigational index to the 11 pattern IDs and engineering/test sections of the canonical study |

## For a consuming agent

Read [the input-mode boundary](metastudy.md#1-definition-and-boundary), [patterns](metastudy.md#6-mechanics-and-creative-pattern-library), [implementation architecture](metastudy.md#7-implementation-architecture-for-agentic-teams), [determinism and QA](metastudy.md#8-determinism-portability-and-qa), and [agent task contract](metastudy.md#11-agent-task-contract-and-decision-record) as needed. Record the exact specdocz commit SHA and study path. Make project-specific decisions only after auditing the consuming codebase.

For a painting/physics demonstration, zero-input refers to **actor controls**; editor painting, time control, camera controls and rigid-body spawning can remain active. A viewer intervention invalidates an unchanged “golden run” until reset. Whole-engine determinism must be demonstrated rather than inferred from one solver's guarantees.
