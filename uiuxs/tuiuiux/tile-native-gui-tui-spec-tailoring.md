# Tile-Native GUI/TUI Specification Tailoring Guide

**Status:** Reusable project-tailoring procedure  
**Version:** 1.0  
**Purpose:** Instruct the agent responsible for an active project how to derive a project-specific GUI/TUI specification from the reusable `specdocz` standards without cargo-culting unrelated architecture.  
**Normative language:** **MUST**, **SHOULD**, and **MAY** describe requirements, recommendations, and optional behaviour for the tailoring process.

The goal is to separate **product requirements** from **reference architecture**:

> **Use the standalone UI/UX specification as the normative design baseline, treat the direct implementation specification as a pattern library, consult MDBM-referenced material only as evidence/examples, then integrate the applicable material into a self-contained project-specific specification.**

The project-specific document is not a wrapper around `specdocz`. It MUST express the resulting design and implementation decisions directly in the active project's own language.

## Contents

1. **Authority and precedence** — Defines which documents are normative, advisory, or project-specific.
2. **Tailoring workflow** — Specifies the required review and synthesis process.
3. **Adopt / Adapt / Reject / Extend decisions** — Provides the applicability classification.
4. **Required project-specific output** — Defines what the generated specification must contain.
5. **Conflict, deviation, and evidence rules** — Prevents silent weakening or inappropriate inheritance.
6. **Lifecycle and baseline updates** — Defines how projects handle later `specdocz` changes.
7. **Worked example** — Shows how the method applies to a VM/agent orchestrator.
8. **Reusable agent instruction** — Provides a compact prompt for project agents.

# 1. Authority and precedence

Use the source documents in the following roles.

1. **Standalone UI/UX specification = normative baseline.**  
   The project SHOULD satisfy its interaction, layout, theming, accessibility, input-parity, responsiveness, and acceptance principles unless a project-specific requirement justifies a documented deviation.

2. **Direct implementation specification = implementation pattern library.**  
   Review it systematically, but do **not** treat every architecture or data structure as mandatory. Import only patterns that genuinely fit the project's domain, existing architecture, platforms, performance constraints, and maintenance model.

3. **MDBM-referenced variants = evidence and concrete precedent.**  
   Use them to understand proven behaviours, edge cases, or implementation examples. Do not inherit MDBM-specific behaviour merely because MDBM implements it.

4. **Project-specific specification = authoritative project contract.**  
   After tailoring, the resulting project document governs that project's GUI/TUI behaviour and adopted implementation architecture, subject to higher-priority safety, functional, compatibility, and repository requirements.

Recommended precedence inside an active project:

```text
project safety / functional / compatibility requirements
    ↓
project-specific GUI/TUI specification
    ↓
standalone specdocz UI/UX baseline
    ↓
adopted/adapted direct-implementation patterns
    ↓
MDBM examples and other non-normative references
```

The agent MUST record the exact `specdocz` source revision used for tailoring — preferably a commit SHA plus file paths — so later changes to the shared standards do not silently alter an existing project's contract.

# 2. Tailoring workflow

The agent responsible for the active project SHOULD perform the following sequence.

## 2.1 Audit the project first

Before importing patterns, inspect the active project's authoritative material:

- current architecture and runtime model;
- existing UI/TUI code and interaction behaviour;
- project requirements and user workflows;
- supported platforms, terminals, window systems, and input devices;
- performance and latency constraints;
- accessibility requirements;
- persistence/session/recovery model;
- existing tests and qualification evidence;
- current issues, planned features, and known limitations where relevant.

Do not begin by assuming that the generic implementation architecture is suitable.

## 2.2 Read the standalone baseline

Review the standalone UI/UX specification as the product-design baseline.

For every substantial normative requirement, determine whether it is:

- directly applicable;
- applicable only after domain-specific adaptation;
- genuinely inapplicable;
- insufficient for the project's needs.

A baseline requirement MUST NOT be silently omitted merely because the existing application does not currently implement it.

## 2.3 Review the direct implementation spec

Treat the direct implementation specification as a catalogue of candidate patterns, including where relevant:

- semantic command registry;
- mouse/keyboard command parity;
- persistent tile/view state;
- split-tree or constraint-based layout;
- geometry-derived hit maps;
- pointer capture and transactional drags;
- overlay/modal stack;
- semantic theme roles;
- adaptive ANSI/ASCII compositor;
- configuration/session separation;
- generation-tagged background work;
- logical damage tracking;
- conformance tests.

For each relevant pattern, explicitly classify it using the decision model in Section 3.

## 2.4 Consult referenced examples only when useful

Use MDBM-referenced variants when a concrete implementation, edge case, or failure mode would improve the decision.

Examples are evidence, not authority.

The agent SHOULD avoid copying:

- application-specific tile names;
- editor-specific text-selection behaviour where no text editing exists;
- source/preview synchronisation where the project has no such concept;
- MDBM-specific layout defaults;
- implementation constraints arising only from MDBM's runtime stack.

## 2.5 Synthesize, do not concatenate

The final project document MUST integrate the chosen behaviour and architecture into the project's own terminology.

Bad:

> Follow the standalone spec and direct implementation spec.

Good:

> The Agent Grid, VM Inspector, Job Queue, Logs, and Terminal views have persistent identities independent of docking geometry. Moving, hiding, stacking, or maximizing a view preserves its filter, scroll, selection, and active-object state. The workspace uses a dock/split tree with tab groups rather than a fixed editor-style split.

The resulting project-specific specification MUST be understandable without requiring the reader to open MDBM or `specdocz`.

# 3. Adopt / Adapt / Reject / Extend decisions

For each substantial implementation pattern — and for any baseline requirement that does not transfer directly — classify the decision as follows:

| Decision | Meaning | Required treatment |
|---|---|---|
| **Adopt** | Fits the project directly | Integrate it into the project spec in project terminology |
| **Adapt** | Principle fits, concrete form does not | Define the modified project-specific form and rationale |
| **Reject** | Inappropriate or conflicting | Record the rejection and concise reason when material |
| **Extend** | Baseline is insufficient | Add project-specific behaviour, invariants, and acceptance criteria |

This classification prevents cargo-culting while still requiring deliberate treatment of useful patterns.

A decision log MAY be retained in the project specification itself or in a companion design/ADR document. Material **Adapt**, **Reject**, and **Extend** decisions SHOULD remain reviewable.

## 3.1 Do not confuse absence with rejection

If the project simply has not implemented a baseline requirement yet, classify it as **required / planned / unimplemented**, not **Reject**.

**Reject** means the requirement or pattern is intentionally unsuitable for the project.

## 3.2 Do not confuse implementation choice with UX requirement

A product requirement such as:

> panels must retain local state when rearranged

does not inherently mandate a particular internal split-tree class.

The project specification SHOULD preserve the behavioural requirement while allowing the architecture to evolve unless a specific implementation invariant is genuinely required.

# 4. Required project-specific output

The tailoring process SHOULD produce one self-contained project-specific GUI/TUI specification, or a clearly linked UI/UX specification plus implementation companion.

At minimum, the output MUST contain:

## 4.1 Basis and source pin

Record:

- standalone UI/UX specification path and exact revision;
- direct implementation specification path and exact revision;
- any MDBM-referenced material actually consulted;
- project documents/architecture used as authoritative input.

Example:

```text
Basis:
- specdocz/uiuxs/tuiuiux/tile-native-gui-tui-uiux-spec.md @ <commit>
  — normative baseline
- specdocz/uiuxs/tuiuiux/tile-native-gui-tui-implementation-spec.md @ <commit>
  — selectively incorporated pattern library
- project architecture and safety requirements
  — authoritative where more specific
```

## 4.2 Project-specific precedence

State how conflicts are resolved inside the project.

## 4.3 Domain model and primary workflows

Identify the actual things the UI manipulates and the highest-value user flows.

Examples:

- documents and navigation;
- VMs, agents, jobs, and terminals;
- simulations and inspectors;
- media assets and timelines;
- devices, alerts, and telemetry.

This prevents a generic tile system from becoming the product model by accident.

## 4.4 View/tile/workspace model

Define:

- persistent view identities;
- placement/docking/stacking rules;
- local state that survives rearrangement;
- compact/narrow behaviour;
- restore/recovery routes;
- workspace presets if relevant.

## 4.5 Input and command model

Define:

- keyboard/pointer parity;
- command discovery;
- focus behaviour;
- context menus;
- drag/capture semantics;
- project-specific gestures;
- touch/gamepad/other device behaviour where relevant.

## 4.6 Theme and presentation model

Define:

- semantic colour roles;
- user theme/palette control;
- ANSI/ASCII adaptation where applicable;
- responsive decoration;
- colour-depth and Unicode fallbacks;
- reduced motion/high contrast;
- protected critical controls.

## 4.7 Project-specific extensions

Explicitly define capabilities absent from the generic baseline, such as:

- topology canvases;
- node graphs;
- detachable windows;
- dashboards/cards;
- timeline views;
- terminal sessions;
- drag/drop task routing;
- live telemetry;
- multi-selection/action batches;
- alert/incident surfaces.

## 4.8 Implementation profile

For each important direct-spec pattern, record **Adopt / Adapt / Reject / Extend** and integrate the chosen design.

The final document need not reproduce every rejected pattern, but material decisions SHOULD be traceable.

## 4.9 Acceptance criteria

Translate the design into project-specific tests and qualification gates.

Do not rely only on generic conformance wording. Include the project's real platforms, interaction paths, responsive states, performance expectations, failure/recovery cases, and accessibility modes.

## 4.10 Implementation status boundary

The specification MUST distinguish:

- **required behaviour**;
- **implemented behaviour**;
- **planned but unimplemented behaviour**;
- **known deviations/limitations**;
- **qualification status**.

Writing a requirement into the tailored specification MUST NOT be represented as evidence that the current code already satisfies it.

# 5. Conflict, deviation, and evidence rules

## 5.1 Project requirements may override the baseline

A project-specific safety, functional, compatibility, or domain requirement may override a shared baseline requirement.

When the difference is material, record:

- what differs;
- why;
- whether the difference is permanent or provisional;
- what acceptance evidence is required.

## 5.2 Do not weaken requirements accidentally

Existing implementation limitations are not, by themselves, sufficient reason to weaken the product contract.

Prefer:

> Required, currently unimplemented.

over:

> Not applicable.

unless it is genuinely inapplicable.

## 5.3 Preserve intent when adapting architecture

When replacing a direct-spec mechanism, preserve the reason it existed.

For example:

- replace a split tree with docking → still preserve deterministic geometry and persistent view identity;
- replace cell hit maps with native GUI widgets → still ensure final rendered geometry defines the interactive target;
- replace generation-tagged preview jobs with another concurrency mechanism → still prevent stale asynchronous results from overwriting newer state.

## 5.4 Evidence must match the claim

Do not claim native GUI/TUI support, accessibility, performance, input parity, or responsive correctness solely because the design specifies it.

Qualification evidence SHOULD be source-matched, platform-matched, and testable.

# 6. Lifecycle and baseline updates

A tailored project specification is **pinned**, not silently live-linked, to the shared `specdocz` baseline.

When `specdocz` changes:

1. compare the project's recorded baseline revision with the newer shared revision;
2. review only the relevant delta;
3. classify new/changed material as Adopt / Adapt / Reject / Extend;
4. update the project-specific specification deliberately;
5. record the new source pin and material decisions.

Do **not** automatically reinterpret an existing project against whatever happens to be current in `specdocz/main`.

Likewise, if the project's architecture changes materially, revisit the tailored implementation profile rather than preserving obsolete imported patterns.

The project-specific spec SHOULD be reviewed when there is a major change to:

- UI framework/runtime;
- workspace model;
- supported platforms/input devices;
- theme/rendering system;
- concurrency model;
- accessibility requirements;
- core user workflows.

# 7. Worked example: VM/agent orchestrator

A VM/agent orchestrator might classify the reusable patterns as follows:

| Pattern | Likely decision | Project-specific result |
|---|---|---|
| Semantic `CommandRegistry` | **Adopt** | One command layer for menu, keyboard, toolbar, context, and palette routes |
| Mouse/keyboard parity | **Adopt** | Every lifecycle/action command has both discoverable pointer and keyboard routes where meaningful |
| Persistent tile state | **Adopt** | Agent Grid, VM Inspector, Logs, Queue, and Terminal retain local state across layout changes |
| Geometry-derived hit testing | **Adopt/Adapt** | Native widgets or scene hits derive from final layout rather than duplicated coordinates |
| Split-tree workspace | **Adapt** | Dock/split tree plus tab groups and optional detachable windows |
| Text-editor selection rules | **Reject** | Used only inside terminal/editor views that actually expose text-selection semantics |
| Adaptive ANSI theme engine | **Adapt** | Full TUI support; GUI consumes the same semantic palette but may render natively |
| Generation-tagged async work | **Adopt** | Stale telemetry/query responses cannot replace newer dashboard state |
| Source/preview synchronization | **Reject** | No equivalent domain concept |
| Agent topology canvas | **Extend** | Add graph navigation, zoom/pan, selection, and keyboard-accessible node operations |
| Job queue visualization | **Extend** | Add queue ordering, status transitions, filtering, batch actions, and failure inspection |
| VM lifecycle controls | **Extend** | Define guarded start/stop/reset/snapshot operations and destructive confirmation semantics |
| Live terminal panes | **Extend** | Define focus ownership, paste, scrollback, reconnect, and detach behaviour |

The resulting project specification should describe these behaviours directly. It should not require readers to infer them from this table or from the generic documents.

# 8. Reusable agent instruction

Use the following as a compact instruction for an agent responsible for an active project:

> **Create or update this project's GUI/TUI specification using `specdocz/uiuxs/tuiuiux/tile-native-gui-tui-uiux-spec.md` as the normative design baseline. First audit the project's current architecture, workflows, platforms, UI implementation, constraints, tests, and existing requirements. Pin and record the exact `specdocz` revision used. Review `tile-native-gui-tui-implementation-spec.md` as a pattern library rather than mandatory architecture. For each relevant pattern, decide whether to Adopt, Adapt, Reject, or Extend it according to the project's domain and existing architecture. Consult MDBM-referenced variants only when concrete examples or edge cases are helpful; do not inherit MDBM-specific behaviour by default. Integrate the resulting decisions into a self-contained project-specific UI/UX and implementation specification stored in the project repository. Record material deviations and rationale, define project-specific acceptance criteria, and distinguish required behaviour from current implementation/qualification status. The tailored project specification becomes authoritative for this project, subject to higher-priority project safety, functional, compatibility, and repository requirements. Future `specdocz` changes must be reviewed as explicit deltas rather than silently inherited.**
