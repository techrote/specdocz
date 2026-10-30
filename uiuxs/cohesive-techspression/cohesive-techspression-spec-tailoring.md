# Cohesive-Techspression Specification Tailoring Guide

**Status:** Reusable project-tailoring procedure  
**Version:** 1.0  
**Purpose:** Derive a project-specific workspace, control-layer and intent-control specification from the cohesive-techspression baseline.  
**Normative language:** **MUST**, **SHOULD**, and **MAY** describe requirements, recommendations and optional tailoring behaviour.

The governing rule is:

> **Start from the project's real workflows and state model. Use cohesive-techspression to reorganize deep capability around user intent and adjacent tasks; use feel controls only where one broad semantic direction can be mapped coherently and inspectably onto several technical parameters.**

## Contents

1. **Authority and source pinning** — Establishes precedence and reproducibility.
2. **Project audit** — Maps workflows, surfaces, parameters and state ownership.
3. **Workspace tailoring** — Decides which views should be separate and which should remain adjacent.
4. **Control-layer tailoring** — Defines Intuitive, Focused, Expert and Inspector depth.
5. **Feel-control design** — Defines semantic contracts and mapping suitability.
6. **Adopt / Adapt / Reject / Extend** — Applies reusable patterns deliberately.
7. **Required project-specific output** — Defines the tailored document structure.
8. **Interaction with parametermaxing and other families** — Combines specifications without duplicate authority.
9. **Lifecycle and drift** — Handles later shared-spec or mapping changes.
10. **Reusable agent instruction** — Compact prompt for an active project agent.

# 1. Authority and source pinning

Use the documents in these roles:

1. **cohesive-techspression-uiux-spec.md** = normative reusable baseline.
2. **cohesive-techspression-implementation-spec.md** = implementation pattern library.
3. Zaaggenz-backed variants = examples and precedent.
4. The consuming project's tailored specification = project authority, subject to higher-priority safety, functional, scientific, compatibility and repository requirements.

Record the exact specdocz commit SHA used.

Recommended precedence:

~~~text
project safety / scientific / functional / compatibility requirements
    ↓
project-specific UI/UX and control-layer specification
    ↓
cohesive-techspression baseline
    ↓
explicitly adopted implementation patterns
    ↓
Zaaggenz/reference examples
~~~

# 2. Project audit

Before creating workspaces or feel controls, inspect:

- primary user goals;
- common task sequences;
- functions/parameters typically used together;
- current UI surfaces and navigation;
- authoritative project/state ownership;
- derived/analysis state;
- selection, playback/preview and revision models;
- parameter schema and ranges;
- presets/locks;
- safety/scientific constraints;
- current tests and supported platforms.

Produce a workflow map before a panel map.

## 2.1 Co-use questions

For each important control ask:

- What usually happens immediately before this?
- What usually happens after?
- Which other controls does the user compare while adjusting it?
- Which output/result must remain visible?
- Is the control describing user intent or implementation detail?
- Is it safe to coordinate with related controls?
- Does another workspace expose the same state?

# 3. Workspace tailoring

Create a separate workspace only when it has a genuinely distinct task model or mutation contract.

For each candidate workspace record:

| Field | Question |
| --- | --- |
| Purpose | What job is this view optimized for? |
| Authority | Does it edit project state, propose changes, or inspect only? |
| Shared context | Which source/selection/revision follows the user here? |
| Primary surface | What must dominate the layout? |
| Adjacent controls | Which editor/transport/output belongs next to it? |
| Return path | How does the user return without losing context? |

Avoid creating separate workspaces for features that are normally used in immediate succession and benefit from spatial adjacency.

# 4. Control-layer tailoring

For each domain decide what belongs in:

### Intuitive

Outcome/feel controls, presets and essential high-level choices.

### Focused

Controls commonly tuned together for one task.

### Expert

Exact parameter access, ranges, units, edge cases, locks and detailed configuration.

### Inspector

Measurements, contributions, diagnostics, provenance, requested/effective state.

A project MAY omit layers it does not need.

Every representation MUST point to the same underlying state identities.

# 5. Feel-control design

A broad feel control is appropriate only when:

- users genuinely think in that direction;
- several lower-level changes are usually coordinated;
- the direction remains meaningfully coherent across relevant contexts;
- the mapping can be bounded and deterministic;
- underlying effects can be inspected;
- the control does not hide a safety-critical independent decision.

## 5.1 Semantic contract template

For every feel control define:

~~~text
Label:
User-facing intent:
Domain / neutral:
Target parameter families:
Expected directional tendencies:
Context branches:
Sidechains / compensations:
Excluded/protected parameters:
Safety constraints:
Interaction with other feel controls:
Reset behavior:
Bake behavior:
How to inspect affected parameters:
~~~

## 5.2 Mapping classes

Classify each mapping as one of:

- proportional;
- additive;
- multiplicative;
- nonlinear/curved;
- target blend;
- context switch;
- sidechain compensation;
- conditional exclusion;
- custom bounded algorithm.

Avoid undocumented arbitrary callback behaviour.

## 5.3 Labels

Subjective labels such as Punch, Warmth or Depth are acceptable when the product establishes a stable practical meaning.

Do not use fashionable textural words that do not correspond to a repeatable output direction.

# 6. Adopt / Adapt / Reject / Extend

For each relevant pattern classify:

| Decision | Meaning |
| --- | --- |
| **Adopt** | Fits directly |
| **Adapt** | Useful but must change for the domain |
| **Reject** | Inappropriate or misleading |
| **Extend** | Baseline is insufficient |

Review at minimum:

- workspace/state sharing;
- task-adjacent grouping;
- progressive control layers;
- shared selection/context;
- feel controls;
- mapping contribution model;
- sidechains;
- pinning/exclusions;
- affected-parameter reveal;
- base/effective display;
- A/B/reset/bake;
- parametermaxing integration;
- responsive/pinned layout.

Do not classify an unimplemented requirement as Reject merely because current code lacks it.

# 7. Required project-specific output

The tailored specification SHOULD contain:

## 7.1 Basis and pins

Record exact reusable spec paths/revisions and project authority sources.

## 7.2 Workflow map

List the primary workflows and likely action sequences.

## 7.3 Workspace map

For each workspace define:

- purpose;
- mutation contract;
- primary/secondary surfaces;
- shared context;
- responsive behavior;
- cross-workspace links.

## 7.4 Control-layer map

For each major task/domain define which controls appear at Intuitive / Focused / Expert / Inspector depth.

## 7.5 Control neighborhoods

Document groups of functions/parameters that users tune together or in close succession.

## 7.6 Feel-control registry

For every semantic macro include its semantic contract plus mapping families.

## 7.7 Parameter interaction policy

Define:

- base versus effective value;
- pinning;
- macro conflict/composition;
- direct edits while macros are active;
- context changes;
- safety limits;
- reset/bake semantics.

## 7.8 Explainability

Specify how users discover:

- what a macro affects;
- why a detailed value changed;
- current contributions;
- exclusions;
- stale/derived state.

## 7.9 Acceptance criteria

Test real workflows, workspace switching, mapping determinism, state identity and responsive layouts.

## 7.10 Implementation status boundary

Distinguish required, implemented, planned, known-deviation and qualified behavior.

# 8. Interaction with parametermaxing and other families

Use **parametermaxing** for the detailed Expert-control mechanics.

Use **cohesive-techspression** for:

- workspace structure;
- task adjacency;
- progressive disclosure;
- semantic macro/feel controls;
- cross-surface state cohesion.

Use **tuiuiux** where tile/workspace pointer/keyboard behavior is relevant.

Do not create competing specifications for the same state concept. Tailor them into one project contract.

# 9. Lifecycle and drift

Pin the project specification to an exact specdocz revision.

When the reusable baseline changes:

1. compare revisions;
2. review relevant deltas;
3. classify changes Adopt / Adapt / Reject / Extend;
4. update the project contract deliberately;
5. rerun affected UX/mapping tests.

Mapping changes are especially important: changing coefficients, curves, conditions or sidechains can change output even when saved macro values do not change.

Store/version mapping semantics where reproducibility matters.

# 10. Reusable agent instruction

> **Create or update this project's cohesive layered UI/UX specification using specdocz/uiuxs/cohesive-techspression/cohesive-techspression-uiux-spec.md as the normative baseline. First audit the project's authoritative state model, user workflows, existing surfaces, parameters, presets/locks, derived analysis, selection/transport/revision behavior, platforms and tests. Pin the exact specdocz revision. Map common task sequences and identify functions/parameters frequently adjusted together or in immediate succession. Design workspaces around distinct user tasks and mutation contracts rather than backend modules; preserve one authoritative state across them. Define progressive Intuitive, Focused, Expert and Inspector control layers as appropriate, using parametermaxing for detailed Expert controls. For each proposed intent/theme/feel control, write a semantic contract covering its label, neutral point, target families, directional behavior, context branches, sidechains, exclusions, safety limits, interactions, reset/bake behavior and inspectability. Use broad macros only where the direction is coherent and repeatable; never use them to hide safety-critical independent decisions. Review the direct implementation spec as a pattern library and classify relevant patterns Adopt, Adapt, Reject or Extend. Consult the Zaaggenz-backed variants for examples such as Compose/Research workspace separation, task-adjacent timeline/inspector grouping, and Intuitive controls including Punch, Harmonisation, Harshness, Depth and Width. Produce a self-contained project-specific specification with workflow, workspace, control-layer, control-neighborhood, feel-control and acceptance matrices, and distinguish required behavior from current implementation/qualification status.**
