# Parametermaxing Direct Implementation Specification

**Status:** Implementation contract  
**Version:** 1.0  
**Audience:** Engineers building high-density expert parameter surfaces  
**Normative language:** **MUST**, **SHOULD**, and **MAY** indicate requirements, recommendations, and optional capabilities.

This document translates the Parametermaxing UI/UX contract into concrete data models, transforms, event semantics, layout structures, persistence rules, and tests.

## Contents

1. **Parameter schema and state** — Concrete data types and invariants.
2. **Value validation pipeline** — Engineering bounds, safety caps, window, and effective values.
3. **Control binding** — Slider, numeric entry, inspector, synchronization, and update modes.
4. **Scale transforms and notch engine** — Linear/log mapping, preferred values, quality, and hysteresis.
5. **Dense layout system** — Row grids, spacing tokens, banks, pinned context, and responsive behaviour.
6. **Preset and lock architecture** — Scoped banks, global stacks, and override semantics.
7. **Runtime/effective-value reporting** — Requested versus realized settings and resource feedback.
8. **Persistence/versioning** — Durable state and schema migration.
9. **Performance rules** — Avoiding UI rebuilds, feedback loops, and expensive live work.
10. **Conformance suite** — Property, interaction, layout, and persistence tests.

# 1. Parameter schema and state

Use one declarative schema as the authority for validation, generated controls, help, presets, and serialization.

Recommended types:

~~~text
ParameterSpec {
    id: string
    label: string
    group: string
    help: string
    unit?: string

    defaultValue: number
    defaultWindow: { min, max }

    engineeringMin: number
    engineeringMax: number

    step: number
    scale: linear | log | symlog | discrete
    precision?: number

    updateMode: live | debounced | commit
    preferredRule?: PreferredRule
    qualityFn?: (value, context) -> [0,1]
}
~~~

~~~text
ParameterState {
    value: number
    sliderWindow: { min, max }
    safetyCaps: { min, max }
    functionalExtremums: { min?: number, max?: number }

    alignmentMode: free | indicate | notched | forced

    requestedValue?: number
    effectiveValue?: number
    boundedReason?: string
}
~~~

## 1.1 Invariants

Always enforce:

~~~text
engineeringMin < engineeringMax
engineeringMin <= safetyMin < safetyMax <= engineeringMax
safetyMin <= value <= safetyMax
sliderMin < sliderMax
sliderMin >= safetyMin
sliderMax <= safetyMax
~~~

The current value is allowed to sit outside the slider window.

Changing `sliderWindow` MUST NOT mutate `value`.

Changing safety caps SHOULD fail if the proposed caps exclude `value`.

Functional Extremums are metadata only.

# 2. Value validation pipeline

Separate parse, validity, user-safety, and runtime effectiveness.

Recommended pipeline:

~~~text
raw input
  -> parse finite value
  -> engineering-bound validation
  -> active-safety-cap validation
  -> authoritative requested value
  -> runtime/device/resource bounding if applicable
  -> effective value
~~~

Do not use the visible slider window as a validity check for direct numeric entry.

## 2.1 Range inspector transaction

An advanced inspector should load a coherent snapshot:

~~~text
description/help
slider min/max
active safety min/max
immutable engineering min/max
Functional Extremum min/max
current value
preferred/alignment metadata when applicable
~~~

Commit all mutually dependent limit edits as one validated transaction.

# 3. Control binding

Generate numeric controls from `ParameterSpec`.

Recommended view-model:

~~~text
ParameterControl {
    label
    numberInput
    advancedButton
    rangeInput
    lowLabel?
    highLabel?
    qualityIndicator?
    notchLayer?
}
~~~

## 3.1 Authoritative synchronization

Use one authoritative store value.

Slider path:

~~~text
pointer/input
  -> slider-space value
  -> alignment/notch policy
  -> validation
  -> store.set(parameter, value)
  -> render synchronized value
~~~

Typed path:

~~~text
text edit
  -> parse
  -> validate against safety caps
  -> store.set(parameter, value)
  -> render synchronized value
~~~

When synchronizing:

~~~text
if numberInput currently has editing focus:
    do not overwrite its text
else:
    numberInput.value = formatted authoritative value
~~~

## 3.2 Slider value outside window

If:

~~~text
value < sliderWindow.min
or
value > sliderWindow.max
~~~

the control MUST preserve `value`.

Recommended presentation:

- thumb clamps visually to nearest endpoint;
- explicit underflow/overflow marker appears;
- number input continues to show authoritative value;
- slider movement re-enters the visible window only when the user acts.

Never silently set the authoritative value to the visual endpoint.

## 3.3 Update modes

Declare update cost per parameter:

- **live** — apply every slider input event;
- **debounced** — keep visual value live but coalesce expensive downstream work;
- **commit** — preview locally if possible, apply expensive state on release/Enter.

Do not infer update mode from control type.

# 4. Scale transforms and notch engine

Every slider needs invertible mapping functions:

~~~text
toUnit(value) -> u in [0,1]
fromUnit(u) -> value
~~~

### Linear

~~~text
u = (v - min) / (max - min)
~~~

### Log

For strictly positive domain:

~~~text
u = (log(v) - log(min)) / (log(max) - log(min))
~~~

### Symlog

Use a documented monotonic signed transform with a linear region around zero.

Notches MUST use the exact same mapping as the thumb.

## 4.1 Preferred-value rules

Represent preference independently from validity.

~~~text
PreferredRule {
    values(context, window) -> number[]
    quality(value, context) -> number in [0,1]
    priority?(value, context) -> number
}
~~~

Useful rules include:

~~~text
powersOfTwo
multipleOf(N)
divisorsOf(dimension)
backendRecommended
benchmarkedSet
semanticMilestones
~~~

Do not attach preferred-value rules to continuous artistic parameters without a domain reason.

## 4.2 Four alignment modes

~~~text
FREE:
    render no attraction
    optional preference metadata may be hidden

INDICATE:
    render notches/quality
    output raw value

NOTCHED:
    render notches/quality
    magnetically capture near preferred display positions
    preserve intentional escape via hysteresis

FORCED:
    interactive output belongs to preferred rule/set
    direct entry must explicitly obey/refuse/normalize under the same policy
~~~

## 4.3 Pixel-space notch algorithm

Let `rawX` be pointer position relative to the track.

For each preferred value `p`:

~~~text
xp = trackWidth * toUnit(p)
distance = abs(rawX - xp)
~~~

Use a default capture radius of approximately **2–3 CSS px**.

Candidate selection SHOULD use:

1. smallest display-space distance;
2. then rule priority/quality if tied.

Maintain a latched notch:

~~~text
if latchedNotch exists:
    if distance_to_latched <= releaseRadius:
        return latchedNotch.value
    else:
        latchedNotch = none

if nearest.distance <= captureRadius:
    latchedNotch = nearest
    return nearest.value

return rawMappedValue
~~~

Requirement:

~~~text
releaseRadius > captureRadius
~~~

The exact release radius is a UI tuning parameter, but MUST create perceptible hysteresis without making the notch sticky.

If two notch attraction zones substantially overlap, suppress/merge one zone or choose a stable priority so pointer jitter cannot toggle between them.

## 4.4 Quality presentation

Maintain independent state:

~~~text
validity = valid | invalid
quality  = 0..1
bounded  = false | true
~~~

Never encode all three with one color.

A low quality score can be rendered as degraded/inefficient while remaining valid.

# 5. Dense layout system

Use layout tokens rather than per-component ad hoc margins.

Recommended token roles:

~~~text
space.micro
space.control
space.group
space.panel
control.heightCompact
control.heightNormal
numeric.width
advancedButton.width
~~~

Tune exact values for font, platform, and target-size requirements.

## 5.1 Parameter row grid

Recommended desktop grid:

~~~text
row:
    columns = [minmax(label), numericWidth, advancedWidth]

track:
    columns = [endpointWidth, 1fr, endpointWidth]
    spans row width
~~~

Compact variant:

~~~text
row:
    columns = [1fr, compactNumericWidth, compactAdvancedWidth]

track:
    endpoints hidden
~~~

Use tabular numerals.

## 5.2 Semantic bank transform

When a control group becomes too tall:

~~~text
rows -> classify by semantic concern -> subtab/subpage banks
~~~

Do not chunk solely by row count.

## 5.3 Pinned context

Structure panels as:

~~~text
fixed/pinned context
    preview / performance / active source

scrolling parameter body
    presets
    controls
    advanced groups
~~~

## 5.4 Responsive policy

Prefer this collapse order:

~~~text
remove/reflow decorative whitespace
-> reduce secondary columns
-> move/collapse sidepanels
-> hide secondary windows with restore route
-> preserve primary control usability
~~~

Do not respond to narrow width by shrinking every control below its practical interaction size.

# 6. Preset and lock architecture

Represent preset ownership explicitly.

~~~text
PanelPreset {
    panelId
    name
    values: subset of parameters owned by panel
}
~~~

~~~text
GlobalStack {
    name
    panelPresetByPanel: Map<PanelId, PresetName>
}
~~~

Panel loads MUST only mutate owned parameter keys.

## 6.1 Custom capture

When a global stack is saved while a panel is Custom:

1. capture that panel's current values as a named panel preset;
2. store the resulting panel preset name in the global stack.

## 6.2 Lock states

Per-submenu:

~~~text
OFF
LOCK
~~~

Optional panel-global override:

~~~text
NONE     -> honor submenu locks
LOCK     -> block global load for all submenus
UNLOCK   -> temporarily force global load through
~~~

Global override MUST NOT mutate stored submenu lock states.

Explicit panel-preset loads and direct edits MAY intentionally bypass global-load locks if the product documents this distinction.

# 7. Runtime/effective-value reporting

For runtime-bounded parameters, store/report:

~~~text
requested
effective
bounded: boolean
reason
cost metrics
~~~

Examples:

- requested render scale versus actual dimensions;
- requested sample count versus device-limited count;
- requested cache size versus memory-budget result.

The parameter surface SHOULD place effective/cost feedback close enough to the relevant controls that users can tune intelligently.

# 8. Persistence/versioning

Persist user-editable state separately from immutable schema.

Suggested snapshot:

~~~text
version
values
sliderWindows
safetyCaps
functionalExtremums
alignmentModes
uiPreferences
panelPresetBanks
panelSelections
globalStacks
globalStackSelection
locks
panelLayout
~~~

Do not persist engineering bounds as user authority.

Migration MUST:

- validate every field;
- clamp/refuse only according to documented migration rules;
- preserve meaningful user presets where possible;
- never reinterpret old slider windows as safety caps.

# 9. Performance rules

Parameter surfaces often generate high-frequency events.

Requirements:

- slider movement MUST NOT rebuild unrelated preset menus;
- state synchronization SHOULD update only affected controls;
- expensive downstream effects SHOULD use declared debounce/coalescing;
- an active text field MUST not be rewritten by background sync;
- live performance graphs SHOULD have an independent paint cadence;
- DOM/layout reads and writes during drag SHOULD be bounded;
- preset-bank refresh occurs when banks change, not when parameter values merely move.

# 10. Conformance suite

Automate the following.

### Schema/property tests

For every parameter:

~~~text
engineeringMin < engineeringMax
defaultWindow within engineering bounds
defaultValue within default safety caps
step > 0
scale transform monotonic
fromUnit(toUnit(v)) approximately v
~~~

### Safety/range tests

- cap beyond engineering bounds -> reject;
- cap excluding current value -> reject;
- slider window outside caps -> reject;
- slider window edit -> current value unchanged;
- direct value outside window but inside cap -> accept;
- Functional Extremum -> stored but no clamp side effect.

### Notch tests

Across multiple track widths and device pixel ratios:

- 2–3 CSS px capture;
- release hysteresis > capture;
- Free never changes raw result;
- Indicate never changes raw result;
- Notched captures and releases deterministically;
- Forced always yields an allowed/preferred value;
- log slider notch geometry uses log/display transform;
- overlapping notch zones choose deterministically;
- quality score stays within `[0,1]`;
- low quality does not become invalid automatically.

### Interaction tests

- slider live/debounce/commit policies;
- direct entry Enter commit;
- Escape revert;
- focused input survives background sync;
- invalid entry reports without corrupting state;
- fine adjustment modifies sensitivity predictably.

### Layout tests

At narrow/normal/wide sizes:

- aligned numeric fields;
- no clipping;
- sufficient hit targets;
- pinned context remains visible;
- large groups become semantic banks;
- dead padding collapses before core controls.

### Preset/lock tests

- panel preset only touches owned keys;
- global stack resolves panel presets;
- submenu lock blocks global load only;
- panel lock/unlock override does not mutate submenu locks;
- custom panel capture preserves a savable global stack.

### Effective-value tests

A runtime-bound request must expose the effective value and bounded reason rather than silently claiming the request succeeded exactly.
