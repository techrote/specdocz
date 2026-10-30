# Cohesive-Techspression UI/UX Specification — Zaaggenz-Derived

**Status:** Reference UI/UX contract  
**Version:** 1.0  
**Scope:** Expert creative, technical and scientific applications with many parameters, modes, views or related workflows  
**Reference pin:** techrote/zaaggenz main at 0ea153b714de85bb72e8d1ae55fa1cc6818adf3b  
**Normative language:** **MUST**, **SHOULD**, and **MAY** indicate requirements, recommendations and optional capabilities.

Cohesive-techspression means:

> **Preserve deep technical capability while organizing the application around coherent user intentions, adjacent workflows and layered views, so the system can be shaped intuitively without hiding or fragmenting its underlying controls.**

It complements parametermaxing. Parametermaxing answers **“how should an expert parameter be exposed?”** Cohesive-techspression answers **“which controls belong together, which view should expose them, and how can broad human intent map coherently onto many parameters?”**

## Contents

1. **Core philosophy** — Defines cohesion, layered control and technical expressiveness.
2. **Workspace model** — Defines alternate task views over shared authoritative state.
3. **Task-adjacent grouping** — Groups functions by co-use, causality and sequence rather than code ownership.
4. **Progressive control layers** — Defines Intuitive, Focused, Expert and Inspector levels without duplicate state.
5. **Intent / theme / feel controls** — Defines broad subjective controls that drive multiple technical parameters.
6. **Mapping and sidechain UX** — Defines context-sensitive relationships, locks and interaction expectations.
7. **Cross-surface cohesion** — Keeps naming, state, selection, transport, feedback and semantics consistent.
8. **Relationship to detailed parameters** — Preserves exact parametermaxing-style access beneath macros.
9. **Feedback, trust and explainability** — Makes broad controls reversible, inspectable and honest.
10. **Layout, presentation and responsive behaviour** — Defines coherent spatial organization and progressive disclosure.
11. **Applicability and use cases** — Explains when semantic macro controls help and when they do not.
12. **Acceptance criteria** — Makes workspace, grouping and broad-control behaviour testable.

# 1. Core philosophy

A technically powerful interface SHOULD not require the user to think in the same decomposition as the implementation.

The product model should expose at least three related layers of meaning:

~~~text
user intent / desired feel
        ↓
task-oriented control groups and workflows
        ↓
technical parameters and algorithms
        ↓
effective runtime state / output
~~~

All layers must remain coherent.

The interface SHOULD optimize:

- **intuitiveness** — common tasks are understandable without memorizing internal architecture;
- **cohesion** — related controls behave and appear as parts of the same system;
- **adjacency** — controls commonly used together or in close succession are near one another;
- **continuity** — switching views does not reset context or create disconnected copies of state;
- **depth** — exact technical controls remain available;
- **expressiveness** — broad intent can shape many lower-level details together;
- **inspectability** — users can discover what a high-level control actually affected;
- **recoverability** — broad edits can be reset, compared, undone or excluded from selected parameters.

“Simple” MUST NOT mean deleting expert capability. Prefer **layering and progressive disclosure** over removing controls.

# 2. Workspace model

A **workspace** is an alternate task-oriented representation of the same authoritative project/system state.

Workspaces MAY focus on:

- composition or creation;
- source/material setup;
- detailed synthesis or parameter editing;
- arrangement/timeline;
- analysis/inspection;
- comparison/A-B;
- research/evidence;
- export/delivery;
- diagnostics/performance.

Workspaces MUST NOT create independent copies of authoritative state merely because they show different views.

## 2.1 Shared-state requirement

If the same parameter, object or project property appears in multiple workspaces:

- it MUST have one authoritative identity;
- changes in one surface MUST become visible in the others;
- units, naming and meaning MUST remain consistent;
- stale or derived views MUST be identifiable;
- switching workspaces MUST preserve the project state.

Workspace-local UI state — scroll position, zoom, selected tab, panel visibility — MAY remain local.

## 2.2 Workspace boundaries should be meaningful

Create a separate workspace when the task has a substantially different:

- mental model;
- information density;
- safety/mutation contract;
- interaction mode;
- provenance requirement;
- visual representation.

Do not create workspaces merely to mirror source-code modules.

## 2.3 Default path and optional depth

The ordinary creation path SHOULD open into the workspace needed for the primary product task.

Specialist analysis, research or diagnostics SHOULD remain reachable but SHOULD NOT become prerequisites for ordinary creation unless the domain truly requires them.

# 3. Task-adjacent grouping

Controls SHOULD be grouped by **how users actually accomplish work**, not only by where the underlying parameter is implemented.

A control group is strong when its members are:

- commonly adjusted together;
- causally related;
- compared against each other;
- used in immediate sequence;
- needed to understand the same output property;
- part of one reversible decision.

Examples of useful grouping logic include:

~~~text
source choice -> shaping -> audition -> compare -> commit

select object -> edit timing/value -> duplicate/mute/delete

choose intent -> adjust amount -> hear/see result -> inspect underlying changes

render region -> name output -> A/B -> export
~~~

## 3.1 Cohesive neighborhoods

A panel or surface SHOULD form a **control neighborhood** around one user goal.

The neighborhood may include controls owned by several internal subsystems if the user normally needs them together.

Conversely, parameters implemented in one backend module MAY belong in different UI neighborhoods if they serve different workflows.

## 3.2 Sequence-sensitive layout

When a workflow has a strong sequence, arrange controls to make the next likely action obvious.

Use:

- left-to-right or top-to-bottom progression;
- nearby preview/result surfaces;
- inline status;
- persistent source/selection context;
- explicit “open in expert” or “inspect effect” links.

Avoid making the user repeatedly traverse distant panels for a routine multi-step action.

# 4. Progressive control layers

Cohesive-techspression SHOULD support multiple **control layers** over the same underlying state.

Recommended layers:

| Layer | Purpose |
| --- | --- |
| **Intuitive** | Broad intent, feel, theme and outcome-oriented controls |
| **Focused** | Task-specific groups of closely related technical controls |
| **Expert** | Full detailed parameter access, exact values, ranges and edge cases |
| **Inspector** | Derived measurements, provenance, diagnostics, requested/effective state and explanation |

These are conceptual layers. A project MAY use different names or combine layers.

## 4.1 No duplicate authorities

An Intuitive control MUST NOT have an unrelated private copy of the parameters later shown in Expert mode.

Focused and Expert views must reveal the same authoritative model.

## 4.2 Promotion and reveal

Users SHOULD be able to move from broad intent toward technical detail without losing context.

Useful routes include:

- **Show affected parameters**
- **Open in Expert**
- **Inspect contribution**
- **Pin this parameter**
- **Reset this macro**
- **Compare before / after**

The system SHOULD preserve the selected object, source, region or output while moving between layers.

# 5. Intent / theme / feel controls

A **feel control** is a broad, human-readable control that intentionally affects multiple lower-level parameters.

Examples of generic labels include:

- Punch
- Harmonisation
- Harshness
- Depth
- Width
- Density
- Warmth
- Clarity
- Motion
- Cohesion
- Aggression
- Softness

These names are domain-dependent. A project MUST use labels that produce a coherent, repeatable perceptual or functional direction in that product.

## 5.1 Feel controls are semantic macros, not blind multipliers

A feel control MAY drive targets through:

- proportional scaling;
- weighted additive offsets;
- nonlinear curves;
- ratios;
- target blending;
- conditional mappings;
- context-specific mappings;
- cross-parameter compensation;
- sidechains;
- exclusions/locks.

Example:

~~~text
Punch ↑
    transient emphasis ↑
    attack time ↓
    body/tail smearing ↓
    selected drive component ↑ slightly
    limiter/headroom compensation may react contextually
~~~

The exact relationships are domain-specific. The important principle is that **one named direction coordinates several technically different changes that users experience as one coherent result**.

## 5.2 Neutral identity

Every feel control SHOULD have a documented neutral state.

At neutral, it SHOULD contribute no hidden change unless the project explicitly defines a baseline profile.

A reset operation MUST restore the neutral contribution without destroying direct parameter edits.

## 5.3 Context dependence

A feel control MAY behave differently depending on:

- active source/material;
- selected layer;
- operating mode;
- current parameter state;
- output/device capability;
- other feel controls;
- safety/headroom state.

Context dependence MUST be deterministic and inspectable.

The same label SHOULD still preserve its broad directional promise across contexts.

## 5.4 Subjective labels require semantic contracts

For each feel control, document:

- intended experiential direction;
- neutral point;
- target parameter families;
- major exclusions;
- expected monotonic tendencies where applicable;
- context-dependent branches;
- safety constraints;
- whether it can be baked/committed.

Do not imply scientific objectivity for inherently subjective labels.

# 6. Mapping and sidechain UX

Broad controls may interact. Their combination MUST be designed rather than left to accidental setter order.

## 6.1 Layered contribution model

Prefer a non-destructive model:

~~~text
base/direct parameter state
        +
feel-control contributions
        +
context/sidechain adjustments
        ↓
validated effective state
~~~

This preserves exact direct edits while allowing broad shaping.

## 6.2 Parameter pinning / exclusions

Users SHOULD be able to protect important detailed parameters from broad controls when appropriate.

A pinned parameter:

- retains its direct/base value;
- ignores specified macro contributions;
- remains visible as excluded;
- can be unpinned without data loss.

## 6.3 Macro interaction

When two feel controls target the same parameter, the system MUST define:

- composition rule;
- normalization/clamping;
- priority if order matters;
- conflict feedback if they strongly oppose;
- sidechain behaviour.

Prefer order-independent composition where practical.

If ordering is necessary, expose the stage or priority in expert/inspector views.

# 7. Cross-surface cohesion

The same system should feel like one product even when it contains radically different views.

Maintain consistency in:

- terminology;
- parameter names;
- units;
- colour/status semantics;
- selection identity;
- transport/playback state;
- source/project identity;
- undo/redo meaning;
- save/export semantics;
- warning/error language;
- shortcuts and common controls.

## 7.1 Shared context anchors

Keep important context visible across surfaces where useful:

- active project/source;
- selected object/region;
- current revision;
- playback/render target;
- comparison slot;
- active preset/profile;
- stale/dirty state.

## 7.2 Cross-surface navigation

A control should link naturally to deeper views.

Examples:

~~~text
Intuitive macro -> Show affected controls
Timeline event -> Open detailed editor
Output -> Inspect analysis
Analysis result -> Return to source object
Performance warning -> Open diagnostics
~~~

Navigation SHOULD preserve context instead of forcing the user to rediscover the relevant object.

# 8. Relationship to detailed parameters

Cohesive-techspression does not replace detailed parameter control.

An Expert layer SHOULD preserve parametermaxing-style capabilities where appropriate:

- direct numeric entry;
- slider working windows;
- engineering/safety bounds;
- detailed help;
- exact units;
- presets and locks;
- requested/effective reporting;
- log/symlog/discrete controls;
- fine adjustment.

Feel controls operate **above** or **alongside** those controls.

## 8.1 Direct edits with active macros

If a user edits a detailed parameter while a feel control is active, the product MUST define whether the direct edit changes:

- the base value beneath the macro;
- the macro's relationship;
- an explicit post-macro override.

The recommended default is **edit the base value** while retaining the macro contribution separately.

Expert views SHOULD be able to show:

~~~text
Base:      0.42
Punch:    +0.11
Depth:    -0.03
Effective: 0.50
~~~

# 9. Feedback, trust and explainability

High-level controls become frustrating when users cannot understand why detailed behaviour changed.

The UI SHOULD provide, proportionate to product complexity:

- affected-control highlighting;
- contribution badges;
- before/after values;
- “why changed” explanations;
- mapping summaries;
- active context branch;
- pinned/excluded targets;
- headroom/safety compensation indicators.

## 9.1 Comparison and reversibility

Broad changes SHOULD support:

- undo/redo;
- reset to neutral;
- A/B or before/after comparison;
- preset snapshots;
- optional “bake macro into base values” as an explicit operation.

Baking MUST be deliberate and SHOULD be undoable.

## 9.2 Honest effect descriptions

A feel control label describes intended direction, not guaranteed perceptual outcome in every case.

If the underlying mapping has little or no effect in the current context, the UI SHOULD indicate that rather than pretending the control is active.

# 10. Layout, presentation and responsive behaviour

Cohesion is spatial as well as semantic.

Use a stable application shell with:

- clear workspace identity;
- consistent headers/navigation;
- task-oriented panels/decks;
- predictable spacing;
- shared control styling;
- nearby status and output feedback.

## 10.1 Primary + secondary surfaces

A productive desktop pattern is:

~~~text
primary working surface
    + adjacent task editor / inspector
    + contextual lower panels or outputs
~~~

When space narrows:

- stack related surfaces;
- move the most immediately editable panel earlier;
- retain context and primary actions;
- avoid exposing the entire expert parameter set merely because responsive layout collapsed.

## 10.2 Pinned operational context

Transport, preview, source identity, performance status or comparison state MAY remain pinned while deeper controls scroll.

Use pinning for **continuous context**, not decoration.

# 11. Applicability and use cases

Cohesive-techspression is especially useful when:

- a system has many technically valid parameters;
- users think in outcomes rather than algorithm names;
- several controls are routinely adjusted together;
- the product has creation plus analysis/diagnostic views;
- expert detail must remain accessible;
- context alters the sensible parameter relationship;
- presets alone are too coarse or static.

Typical domains:

- audio/video/image synthesis;
- simulation and scientific visualization;
- game/editor tooling;
- procedural generation;
- robotics/control tuning;
- data transformation pipelines;
- complex dashboards and orchestrators;
- CAD/material/lighting tools.

## 11.1 When not to use broad feel controls

Avoid semantic macros when:

- a single parameter already maps directly to the user's intent;
- the label would be vague or misleading;
- mappings cannot be made deterministic enough for the domain;
- hidden coupling would violate scientific/engineering expectations;
- safety-critical control requires explicit individual adjustment;
- users need independent parameter manipulation more than coordinated shaping.

In those cases, use task grouping and layered workspaces without feel macros.

# 12. Acceptance criteria

A conforming implementation SHOULD verify the following.

### Workspace/state cohesion

- workspace switches preserve authoritative project state;
- one parameter shown in two surfaces has one identity;
- selected source/object/region survives relevant view transitions;
- stale derived views are marked;
- ordinary creation does not require optional research/analysis setup.

### Task grouping

- common multi-step workflows can be completed without unnecessary panel traversal;
- controls grouped together share a meaningful user goal;
- backend module boundaries do not dictate UI grouping without user-facing reason;
- likely next actions are discoverable near the current task.

### Progressive layers

- Intuitive, Focused and Expert controls resolve to the same underlying model;
- moving deeper preserves context;
- Expert detail can reveal contributions from broad controls;
- no hidden duplicate parameter stores drift apart.

### Feel controls

For every broad control:

- neutral state is defined and testable;
- mappings are deterministic for a fixed context;
- affected target set is bounded and documented;
- context branches are deterministic;
- safety/engineering limits are preserved;
- pinned targets remain unaffected;
- reset removes only that control's contribution;
- undo restores the prior effective state;
- overlapping macros compose according to declared rules.

### Explainability

- the user can determine which broad controls affect a detailed parameter;
- base and effective values can be distinguished where material;
- exclusions/locks are visible;
- zero/limited-effect contexts do not falsely imply strong effect.

### Responsive layout

- primary task controls remain usable at narrow sizes;
- secondary surfaces stack/collapse coherently;
- context indicators remain discoverable;
- expert detail does not overwhelm reduced layouts by default.


# Zaaggenz reference notes

Zaaggenz supplies concrete precedents for the principles above.

## Layered workspace precedent

The current runtime opens **Compose** by default and keeps **Research** explicit and optional. Entering Research does not mutate the working Compose project. The same authoritative timeline/project revision survives movement between Compose, Inspector, Listening and Vocal surfaces.

This demonstrates a strong workspace rule:

> Alternate views may have different information density, mutation contracts and representations while remaining attached to one coherent source state.

The Compose timeline groups by workflow rather than backend ownership:

- project/source/render controls;
- phrase timeline;
- adjacent event editor;
- clips and render-region controls;
- named rendered outputs and playback;
- expandable layer/source/limitation disclosure.

The Inspector likewise groups:

- musical controls and Analyse / Freeze / Apply actions;
- linked A/B transport;
- spectral timeline and confidence controls;
- stage/uncertainty;
- requested / estimated / realised values;
- remainder energy;
- interval compatibility;
- expert disclosure.

The Research hub then routes into Inspector, Listening and Vocal according to task intent rather than presenting all research controls on one dashboard.

## Intuitive control-layer precedent

The owner-identified recovered full-instrument **Control Layer Intuitive** uses broad aesthetic/technical directions including **Punch, Harmonisation, Harshness, Depth and Width**.

These controls exemplify semantic feel macros: each label is intended to coordinate several lower-level synthesis or processing parameters through proportional, algorithmic, sidechained and/or context-dependent relationships rather than acting as a one-to-one alias.

The exact coefficients are application-specific and are not generalized here. The reusable lesson is that a user can shape a technically dense system through a smaller set of coherent perceptual intentions while retaining detailed lower-level controls elsewhere.

Zaaggenz's recovered parameter catalogue reinforces why this layering is useful: synthesis, reverse-bass/layer, spectral-sculpt and arrangement domains contain many parameters spanning harmonics, roughness, noise, drive, envelopes, BODY/AUX/SUB balance, event interaction, spectral pockets, compression, crushing, phrase motion and output policy.

## Protected-boundary precedent

Zaaggenz also demonstrates that cohesion does not require collapsing different contracts:

- Compose is the ordinary creative surface.
- Research is derived and isolated.
- Inspector analysis never applies itself implicitly.
- Vocal analysis compiles a proposal that requires explicit application.
- Named outputs retain exact revisions.
- stale derived work is prevented from silently applying to a newer project revision.

Cohesive-techspression therefore favors **shared context with explicit mutation boundaries**, not one universal surface that can modify everything.

## Visual cohesion precedent

The newer Zaaggenz web workspaces use a common dark, restrained panel/deck language, repeated accent/status semantics, consistent control sizing, shared headers and similar responsive stacking. This reinforces visual continuity even when the task model changes substantially.

## Relationship to parametermaxing

Zaaggenz contains both:

- deep technical parameters suitable for parametermaxing-style exact control; and
- task/intuitive surfaces that coordinate those parameters into musical or analytical workflows.

Cohesive-techspression should therefore be understood as an **organizational and semantic layer above detailed parameter exposure**, not a substitute for it.

## Reference material inspected

- README.md
- baseline/V1_2_1_CONTRACT.json
- zaaggenz_contracts/legacy_spec.py
- docs/timeline/README.md
- docs/runtime/ZG041_COMPOSE_RESEARCH.md
- docs/zaaggenz/OVERVIEW.md
- docs/zaaggenz/WORKED_WORKFLOWS.md
- web/timeline/index.html and style.css
- web/inspector/index.html and style.css
- web/listening/index.html
- web/vocal/index.html
- zaaggenz_runtime/server.py

The recovered Control Layer Intuitive labels and feel-control role are retained from the owner's identified Zaaggenz UI behavior; the reusable specification intentionally does not freeze Zaaggenz-specific macro coefficients.
