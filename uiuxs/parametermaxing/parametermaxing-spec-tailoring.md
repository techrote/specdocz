# Parametermaxing Specification Tailoring Guide

**Status:** Reusable project-tailoring procedure  
**Version:** 1.0  
**Purpose:** Derive a project-specific expert parameter-control specification from the reusable Parametermaxing standards.  
**Normative language:** **MUST**, **SHOULD**, and **MAY** describe requirements, recommendations, and optional behaviour for the tailoring process.

The default strategy is:

> **Use the standalone Parametermaxing UI/UX specification as the product baseline, review the direct implementation specification as a pattern library, classify each parameter family by its real semantics, and integrate only the relevant range, slider, notch, layout, preset, and persistence mechanisms into a self-contained project-specific specification.**

## Contents

1. **Authority and precedence** — Defines the shared baseline versus project authority.
2. **Parameter audit** — Classifies the project's parameters before choosing controls.
3. **Adopt / Adapt / Reject / Extend** — Applies implementation patterns deliberately.
4. **Required project-specific output** — Defines what the tailored document must contain.
5. **Notch and density tailoring rules** — Prevents misuse of preferred values or compact layout.
6. **Lifecycle and drift** — Pins the shared source and handles later updates.
7. **Reusable agent instruction** — Provides a compact project-agent prompt.

# 1. Authority and precedence

Use the documents as follows.

1. **Standalone Parametermaxing UI/UX spec = normative baseline.**
2. **Standalone direct implementation spec = pattern library.**
3. **XenoField-referenced variants = evidence/examples.**
4. **Project-specific parameter specification = final project authority**, subject to higher-priority safety, functional, compatibility, and repository requirements.

Recommended precedence:

```text
project safety / functional / compatibility requirements
    ↓
project-specific parameter specification
    ↓
standalone Parametermaxing UI/UX baseline
    ↓
adopted/adapted direct implementation patterns
    ↓
XenoField examples and other references
```

Record the exact `specdocz` revision used.

# 2. Parameter audit

Before designing controls, inventory the project's parameter families.

Each numeric parameter SHOULD be classified by relevant traits.

## 2.1 Semantic type

Choose one or more:

| Type | Typical control consequences |
|---|---|
| **Continuous artistic** | Smooth slider; usually no notches |
| **Physical/measurement** | Units and precision matter; may need log/symlog |
| **Integer/count** | Discrete stepping; direct entry important |
| **Compute-aligned** | Preferred-value indication/notches may be valuable |
| **Enumerated numeric** | Discrete preferred set or selector |
| **Wide-dynamic-range** | Log/symlog mapping likely |
| **Signed around zero** | Symlog/centered presentation may help |
| **Safety-sensitive** | Engineering bounds and active safety caps important |
| **Expensive/rebuild** | Debounced or commit update mode |
| **Runtime-bounded** | Requested/effective reporting required |
| **Context-dependent** | Preferred values/valid range may depend on backend/device/document |

Do not choose a notched slider merely because a parameter is numeric.

## 2.2 Required metadata

For each significant parameter or family, define:

- label and unit;
- default;
- engineering bounds;
- default slider window;
- safety-cap policy;
- step/precision;
- linear/log/symlog/discrete mapping;
- update mode;
- preferred-value rule if any;
- quality interpretation if any;
- cost/resource consequence;
- preset ownership;
- persistence requirements;
- help/description source.

## 2.3 Existing implementation is evidence, not automatic authority

If the current app uses a simple min/max slider but the domain requires direct entry outside that working range, record the missing capability instead of redefining the requirement to match the implementation.

# 3. Adopt / Adapt / Reject / Extend

For each substantial pattern, classify:

| Decision | Meaning |
|---|---|
| **Adopt** | Fits directly; integrate it |
| **Adapt** | Principle fits but concrete shape changes |
| **Reject** | Inappropriate; record why when material |
| **Extend** | Baseline is insufficient; add project-specific behaviour |

Likely patterns to classify include:

- slider + typed entry pair;
- working slider window;
- active safety caps;
- immutable engineering bounds;
- Functional Extremums;
- advanced parameter inspector;
- linear/log/symlog mapping;
- Free/Indicate/Notched/Forced preferred-value modes;
- quality score;
- fine adjustment;
- semantic control banks;
- pinned preview/metrics;
- panel presets;
- global preset stacks;
- submenu/panel locks;
- requested/effective reporting;
- UI/preset persistence.

Do not confuse **unimplemented** with **Reject**.

# 4. Required project-specific output

The resulting specification SHOULD be self-contained and include:

## 4.1 Basis and source pins

Record the exact standalone UI/UX and implementation spec revisions and any referenced examples consulted.

## 4.2 Parameter taxonomy

Document the real project parameter families and their control profiles.

A useful matrix:

| Family | Scale | Window/caps | Preferred rule | Update mode | Preset scope |
|---|---|---|---|---|---|

## 4.3 Range policy

Define:

- engineering bounds;
- safety-cap editability;
- slider-window editability;
- out-of-window direct entry;
- Functional Extremum/reference policy;
- resets.

## 4.4 Slider interaction profile

Define per family:

- mapping;
- step/fine mode;
- alignment mode;
- preferred rule;
- capture/hysteresis if notched;
- keyboard behaviour;
- commit/update behaviour.

## 4.5 Layout/density profile

Define:

- row structure;
- numeric widths;
- spacing tokens;
- compact variants;
- grouping/subtabs;
- pinned context;
- narrow/wide responsive arrangements.

The objective is **efficient scanning and adjustment**, not the smallest possible pixel count.

## 4.6 Preset/lock ownership

Specify which subsystems own which parameters and how broad preset loads interact with locks/custom state.

## 4.7 Runtime/effective feedback

Specify when the system may bound or alter a request and exactly how the UI reports the effective value/cost.

## 4.8 Acceptance criteria

Turn the chosen behaviour into project-specific tests at real panel widths, device-pixel ratios, backends, and input methods.

Writing the requirement is not evidence that the implementation passes it.

# 5. Notch and density tailoring rules

## 5.1 Preferred values require evidence

Use preferred values for real computational or semantic advantages such as powers of two, vector/workgroup alignment, exact divisors, backend recommendations, or benchmarked sweet spots.

Do not invent “optimal” notches for subjective continuous values.

If preference changes with backend/device/context, make the rule context-aware.

## 5.2 Display-space geometry is mandatory for notches

If a project adopts Notched mode:

- compute attraction in rendered/CSS pixel space;
- use the same linear/log/symlog transform as the slider;
- start from roughly 2–3 CSS px capture as a tuning baseline;
- use a larger release threshold for hysteresis;
- test multiple track widths and device-pixel ratios.

## 5.3 Quality is separate from validity

If quality scoring is adopted, specify:

- score range and meaning;
- visual treatment;
- how it differs from warning/error;
- whether quality affects any automatic behavior.

Do not make poor quality invalid unless the domain actually requires it.

## 5.4 Density must preserve operability

Compactness may remove:

- redundant prose;
- excessive outer padding;
- repeated endpoint labels in quick controls;
- unused whitespace.

Compactness must not remove:

- authoritative value visibility;
- control identification;
- reliable hit targets;
- advanced-range access where required;
- focus/keyboard operability;
- important requested/effective distinction.

# 6. Lifecycle and drift

A project-specific parameter spec is pinned to a known `specdocz` revision.

When the shared Parametermaxing specs change:

1. compare the old and new shared revisions;
2. review the delta;
3. classify relevant changes as Adopt / Adapt / Reject / Extend;
4. update the project specification deliberately;
5. record the new source pin.

Do not silently reinterpret old projects against current `specdocz/main`.

Revisit the tailored spec when there is a major change to:

- parameter schema;
- rendering/compute backend;
- device constraints;
- preset architecture;
- panel framework;
- accessibility/input model;
- resource budgeting;
- principal expert workflows.

# 7. Reusable agent instruction

> **Create or update this project's expert parameter-control specification using `specdocz/uiuxs/parametermaxing/parametermaxing-uiux-spec.md` as the normative baseline. First audit the project's existing parameter schema, UI, workflows, platforms, performance/resource constraints, presets, persistence, tests, and safety limits. Pin the exact `specdocz` revision used. Classify each important parameter family as continuous artistic, physical/measurement, integer/count, compute-aligned, enumerated numeric, wide-dynamic-range, signed/zero-centered, safety-sensitive, expensive/rebuild, runtime-bounded, and/or context-dependent. Review `parametermaxing-implementation-spec.md` as a pattern library rather than mandatory architecture. For relevant patterns decide Adopt, Adapt, Reject, or Extend. Apply preferred-value/notched behaviour only where the domain provides real preferred values; when adopted, compute attraction in display/CSS pixel space using the same scale transform as the slider, include hysteresis, and keep quality distinct from validity. Integrate the resulting decisions into a self-contained project-specific specification covering range hierarchy, numeric/slider interaction, layout density, information hierarchy, presets/locks, requested/effective values, persistence, and project-specific acceptance tests. Consult the XenoField-referenced variants only for useful examples and edge cases. Distinguish required behaviour from current implementation and qualification status.**
