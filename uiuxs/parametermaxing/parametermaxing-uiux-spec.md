# Parametermaxing UI/UX Specification

**Status:** Reference UI/UX contract  
**Version:** 1.0  
**Scope:** Expert parameter surfaces for creative tools, technical applications, simulators, renderers, dashboards, editors, and other highly configurable systems  
**Normative language:** **MUST**, **SHOULD**, and **MAY** indicate requirements, recommendations, and optional capabilities.

Parametermaxing means:

> **Maximize useful control, inspectability, parameter reach, and experimentation speed per unit UI area without sacrificing precision, safety, comprehension, or recoverability.**

It does **not** mean exposing every possible variable at once.

## Contents

1. **Core parameter model** — Separates value, slider window, safety caps, engineering bounds, and reference extrema.
2. **Primary control contract** — Defines synchronized slider, numeric entry, information, and update behaviour.
3. **Notches and preferred values** — Defines Free / Indicate / Notched / Forced alignment and display-space hysteresis.
4. **Dense presentation and layout** — Defines compact rows, spacing, grouping, pinning, and responsive arrangements.
5. **Information hierarchy and discoverability** — Keeps expert detail available without permanently consuming space.
6. **Presets, locks, and experimentation** — Preserves tuned subsystems while enabling rapid exploration.
7. **Effective values, cost, and quality** — Distinguishes requested, valid, preferred, and runtime-limited states.
8. **Persistence and recovery** — Defines what parameter metadata and UI state should survive sessions.
9. **Accessibility and interaction quality** — Preserves precision and meaning across input/accessibility modes.
10. **Acceptance criteria** — Makes range, notch, density, preset, and interaction behaviour testable.

# 1. Core parameter model

Every numeric parameter SHOULD be treated as more than a single min/value/max triple.

A mature parameter surface distinguishes at least:

1. **Current value** — authoritative requested value.
2. **Slider window** — the working range exposed by the visible slider.
3. **Active safety caps** — user-adjustable limits beyond which normal direct entry is refused.
4. **Engineering bounds** — immutable absolute limits imposed by implementation, numerical validity, resource safety, or product policy.
5. **Functional extremums** — optional reference-only observations about where useful or interesting behaviour has been found.
6. **Default value/window** — recoverable baseline.
7. **Preferred values/rules** — optional computationally or semantically advantageous values.
8. **Effective runtime value** — optional value actually used after device/resource/runtime bounding.

These concepts MUST NOT be collapsed merely to simplify the UI.

## 1.1 Range precedence

The intended relationship is:

```text
engineering bounds
    contain active safety caps
        contain valid direct-entry values

slider window is a user working viewport inside the valid domain
and need not redefine the current value
```

Changing the slider window MUST NOT silently rewrite the current parameter value.

Active safety caps MUST NOT exceed engineering bounds.

Reducing active safety caps SHOULD be refused if the proposed caps would exclude the current value unless the product explicitly runs a separate, visible value-migration transaction.

Functional Extremums MUST remain reference metadata unless a project explicitly promotes them into another policy.

# 2. Primary control contract

For ordinary numeric expert parameters, the default control SHOULD provide:

- a concise label;
- direct typed numeric entry;
- a slider;
- an advanced information/range control;
- contextual description/help;
- visible units where meaningful.

A useful full row is:

```text
LABEL                  [ numeric ] [advanced]
[min] [----------- slider --------] [max]
```

## 2.1 Slider and numeric entry are complementary

The slider is for **fast embodied exploration**.

Numeric entry is for **precision, reproducibility, and reaching values outside the current slider window**.

Direct numeric entry MAY extend beyond the visible slider window up to the active safety caps.

The slider MUST remain synchronized with the authoritative value, but MUST NOT silently clamp or rewrite an out-of-window authoritative value merely because the slider cannot represent it. The UI SHOULD signal under/overflow when the value lies outside the visible slider window.

## 2.2 Edit semantics

Recommended behaviour:

- slider drag updates live when the operation is cheap enough;
- typed value commits on Enter/change;
- Escape abandons an uncommitted text edit and restores the authoritative value;
- invalid entry remains visibly invalid or reverts with a clear error;
- background synchronization MUST NOT overwrite the field while the user is actively editing it.

Expensive parameters MAY use debounced or commit-on-release application, but this must be visible and consistent.

## 2.3 Fine control

Parameters with large ranges or high sensitivity SHOULD provide a fine-adjustment route such as a modifier, secondary drag, or precision mode.

The fine mode MUST change sensitivity rather than secretly changing the parameter's semantic units.

# 3. Notches and preferred values

Notches are appropriate only when the domain contains **genuinely preferred values**.

Examples include:

- powers of two;
- SIMD/workgroup multiples;
- divisors of a relevant dimension;
- backend-dependent efficient sizes;
- benchmark-derived sweet spots;
- exact semantic milestones.

Do **not** add notches to arbitrary artistic coefficients, positions, colours, probabilities, opacity, strengths, or other continuously meaningful values without evidence that particular values deserve preference.

## 3.1 Alignment modes

A preferred-value slider SHOULD support four modes where the domain benefits:

| Mode | Behaviour |
|---|---|
| **Free** | No notch influence. The parameter behaves continuously/discretely according to its base step. |
| **Indicate** | Preferred values and quality are shown, but pointer motion is not altered. |
| **Notched** | Preferred values exert a small magnetic capture near their display positions; the user can deliberately pull away. |
| **Forced** | Interactive adjustment is constrained to the preferred set/rule. Arbitrary direct entry must be explicitly refused or normalized; never silently disagree with the displayed mode. |

## 3.2 Display-space attraction

Notch capture MUST be calculated in **rendered slider/display space**, not naïvely in raw value space.

The recommended attraction region is approximately **2–3 CSS pixels** around the displayed notch.

This is essential for wide-range or logarithmic controls: equal numeric distance does not imply equal visual distance.

For a transform `T(value) -> normalized_position`:

```text
notch_px = track_left + T(preferred_value) * track_width
raw_px   = track_left + T(raw_value)       * track_width
distance = abs(raw_px - notch_px)
```

Use the same transform for drawing, hit attraction, keyboard position mapping, and quality visualization.

## 3.3 Hysteresis

Notched mode MUST use hysteresis.

Once a notch has captured the slider:

- small pointer jitter must not repeatedly release/reacquire it;
- the release threshold MUST be larger than the capture threshold;
- the user must still be able to pull away deliberately;
- the thumb must never oscillate between nearby notches.

If preferred values are visually too close for stable independent capture, merge, prioritize, or suppress competing attraction regions.

## 3.4 Quality is not validity

A parameter MAY expose a continuous **quality/alignment score** in `[0, 1]`.

Quality MUST be semantically separate from validation:

- a low-quality value may be completely valid;
- an invalid value is an error;
- an inefficient but valid value should use a distinct degraded/quality visual state rather than error styling.

# 4. Dense presentation and layout

Parametermaxing optimizes **information density**, not visual emptiness.

The UI SHOULD reduce dead space before reducing legibility, target size, or semantic grouping.

## 4.1 Spacing hierarchy

Use a small, consistent spacing scale rather than unrelated margins.

Typical roles are:

- **micro gap:** tightly coupled items such as label/value/button;
- **control gap:** adjacent controls in a row;
- **group gap:** separation between semantic banks;
- **panel padding:** outer breathing room around scrollable content.

Exact pixels are product-specific, but the hierarchy MUST remain visually consistent.

## 4.2 Stable alignment

Numeric fields SHOULD have consistent widths within a panel.

Use tabular numerals for numeric entry/readouts.

Labels SHOULD align predictably and truncate gracefully rather than pushing numeric controls horizontally from row to row.

The slider should receive the majority of flexible width.

## 4.3 Compact and full rows

A full parameter row MAY show endpoint labels and the complete slider track.

A compact/quick-control variant MAY omit repeated endpoint labels when:

- the numeric value is visible;
- the range is discoverable through the advanced control;
- the omission materially improves density.

## 4.4 Semantic banks

Long unstructured vertical lists SHOULD be split into semantic banks/subtabs once scanning becomes materially inefficient.

The threshold is product-specific; grouping should reflect how users reason about the parameters, not arbitrary equal-sized chunks.

## 4.5 Pinned context

Context that users need while tuning SHOULD remain visible while detailed controls scroll.

Candidates include:

- live preview;
- profiler/performance meter;
- active mode/source;
- critical warning;
- current preset identity.

## 4.6 Responsive arrangement

When horizontal space becomes constrained:

- reduce column count;
- move sidepanels inward;
- collapse secondary windows before crushing controls;
- keep primary parameter rows usable;
- preserve access to hidden/restorable panels.

# 5. Information hierarchy and discoverability

Expert interfaces need deep information, but not all information must permanently occupy the canvas.

The default surface SHOULD prioritize:

1. parameter name;
2. current value;
3. fast adjustment;
4. essential state/quality;
5. optional detailed explanation.

Long descriptions SHOULD move into tooltips, help surfaces, or the advanced parameter inspector when this materially reduces clutter.

Tooltips SHOULD be user-disableable without discarding the underlying help metadata.

The advanced parameter dialog SHOULD double as an information surface rather than being merely a min/max editor.

# 6. Presets, locks, and experimentation

High-dimensional tools need fast experimentation without destroying tuned subsystems.

## 6.1 Modular preset ownership

Preset scope SHOULD match the UI/module scope.

A panel preset MUST NOT silently rewrite unrelated panels.

## 6.2 Global stacks

For modular systems, a global preset SHOULD be a composition of named panel/subsystem presets rather than a flat undifferentiated settings dump when doing so improves ownership and editability.

This allows one subsystem to be replaced without destroying the conceptual structure of the rest.

## 6.3 Locks

Users SHOULD be able to protect tuned regions from broad preset loads.

Useful scopes include:

- individual submenu lock;
- panel-wide global-load lock;
- temporary panel-wide global-load unlock.

A higher-level override SHOULD NOT silently mutate the lower-level lock configuration.

## 6.4 Presets must be materially useful

Built-in presets SHOULD demonstrate meaningfully different parameter-space regions, not cosmetic renamings.

High-value presets that already produce distinctive results SHOULD be preserved during UI rework unless there is a documented reason to replace them.

# 7. Effective values, cost, and quality

Expert parameter UIs SHOULD distinguish among:

- **requested** value;
- **validated/accepted** value;
- **effective runtime** value;
- **quality/preference** score;
- **resource/cost** consequence.

For resource-bounded settings, the UI MUST NOT imply that the requested value was actually realized when the runtime had to reduce it.

Where a parameter changes cost significantly, the UI SHOULD expose its practical consequence near the tuning context.

Quality indicators MUST NOT masquerade as hard safety validation.

# 8. Persistence and recovery

Parameter state persistence SHOULD include, as applicable:

- authoritative values;
- slider windows;
- active safety caps;
- Functional Extremums/reference metadata;
- alignment mode;
- user presets;
- preset selections;
- locks/overrides;
- UI preferences;
- relevant panel arrangement.

Engineering bounds belong to the application/schema and SHOULD NOT be rewritten by ordinary user state.

Versioned persistence MUST validate restored state before applying it.

A reset path SHOULD exist separately for:

- current value;
- working slider window;
- active safety caps;
- presets/UI state.

# 9. Accessibility and interaction quality

Dense does not mean inaccessible.

The interface MUST maintain:

- visible focus;
- sufficient contrast;
- usable hit targets for the declared desktop/mobile context;
- keyboard access to numeric entry and advanced controls;
- non-colour-only status meaning for invalid/warning/quality states where practical;
- predictable tab order;
- text scaling/responsive behaviour that does not make values unreachable.

Notch attraction MUST be based on CSS/display coordinates so device-pixel ratio does not unexpectedly change the physical interaction feel.

Motion or animated quality indicators MUST respect reduced-motion settings.

# 10. Acceptance criteria

A conforming implementation SHOULD verify all of the following.

### Range hierarchy

- engineering bounds cannot be exceeded by active safety caps;
- safety caps cannot silently exclude the current value;
- slider-window edits do not rewrite current value;
- direct numeric entry can reach valid values outside the slider window;
- Functional Extremums do not clamp or validate values;
- reset actions restore the intended layer only.

### Slider/notch behaviour

Test Free, Indicate, Notched, and Forced modes.

Verify:

- preferred markers render at the same transformed positions used for interaction;
- attraction is measured in display/CSS pixels;
- approximately 2–3 px capture feels consistent across track sizes;
- logarithmic/display transforms preserve notch geometry;
- hysteresis prevents chatter;
- the user can intentionally escape a notch;
- nearby notches cannot create unstable oscillation;
- low quality remains valid unless another rule makes it invalid.

### Control synchronization

- slider and numeric entry share one authoritative value;
- active text editing is not overwritten by background sync;
- Enter/change commits;
- Escape restores;
- invalid typed values produce a clear result;
- expensive updates obey their declared live/debounced/commit policy.

### Density/layout

Verify narrow, normal, and wide layouts.

Ensure:

- numeric fields remain aligned;
- controls are not clipped;
- semantic grouping remains obvious;
- dead padding yields before control usability;
- pinned preview/metrics remain visible where specified;
- large banks become navigable without excessive scrolling.

### Presets and locks

- panel preset cannot alter unrelated panel state;
- global stack composes declared subsystem presets;
- locks block only their intended loading path;
- global lock override does not mutate underlying locks;
- current custom values are not silently lost.

### Effective-state honesty

When runtime/device bounds modify a request, the UI clearly distinguishes requested from effective values.
