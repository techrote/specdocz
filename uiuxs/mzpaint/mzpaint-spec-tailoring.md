# MZPaint Specification Tailoring Guide

**Status:** Reusable project-tailoring procedure  
**Version:** 1.0  
**Purpose:** Derive a project-specific glyph/cell editing specification from the unified MZPaint precision/expressive standard.  
**Normative language:** **MUST**, **SHOULD**, and **MAY** describe requirements, recommendations and optional tailoring behaviour.

The governing rule is:

> **Do not decide that a project is “GlyphPoint-like” or “GlyphPaint-like” globally until its actual editable data, workflows and outputs have been audited. Choose the Precision, Expressive or Hybrid philosophy per document/layer/tool where necessary, then integrate the relevant features into a self-contained project specification.**

## Contents

1. **Authority and source pinning** — Establishes baseline, references and project precedence.
2. **Scope audit and philosophy axes** — Determines what kind of work the project actually performs.
3. **Profile selection** — Defines Point-dominant, Paint-dominant and Hybrid profiles.
4. **Adopt / Adapt / Reject / Extend** — Forces explicit decisions on relevant features.
5. **Required tailored output** — Defines the project-specific specification structure.
6. **Crossover safety rules** — Prevents expressive tools from corrupting semantic data and vice versa.
7. **Use-case recommendations** — Provides default guidance for common project classes.
8. **Lifecycle and drift** — Handles later shared-spec changes.
9. **Reusable agent instruction** — Compact prompt for an active project agent.

# 1. Authority and source pinning

Use the MZPaint documents in these roles:

1. **`mzpaint-uiux-spec.md` = normative reusable baseline.**
2. **`mzpaint-implementation-spec.md` = implementation pattern library.**
3. **GlyphPoint/GlyphPaint referenced variants = evidence and concrete examples.**
4. **Project-specific MZPaint-derived specification = authority for the active project**, subject to higher-priority safety, functional, compatibility and repository requirements.

Record the exact `specdocz` revision used.

When reference examples are consulted, also record the reference pins:

- GlyphPoint precision reference: `019578651dfcccabdd3de42f6d427e3d076203b4`
- GlyphPaint expressive reference: `983880c7d7a05bf639a49db73f1fa3cdb165d436`

Recommended precedence:

~~~text
project safety / scientific / functional / compatibility requirements
    ↓
project-specific glyph/cell editing specification
    ↓
standalone MZPaint UI/UX baseline
    ↓
adopted/adapted implementation patterns
    ↓
GlyphPoint/GlyphPaint examples
~~~

# 2. Scope audit and philosophy axes

Before importing UI or tool behaviour, inspect:

- what each cell/glyph represents;
- whether identical glyphs must mean the same thing;
- whether local colour variation is data, decoration or both;
- whether results must be reproducible;
- whether plain text is an important interchange format;
- whether raster imagery is an important source/output;
- whether users paint freely or construct exact maps/diagrams;
- whether coordinates and dimensions are operationally important;
- whether transforms must preserve categories exactly;
- whether stochastic tools are acceptable;
- whether the project has authoritative and annotation layers;
- whether rendering/presentation may be separated from source data;
- existing selection, history, palette, layer, file and export architecture.

Then score the project or each layer on these axes:

| Axis | Precision pole | Expressive pole |
|---|---|---|
| Source authority | semantic class/glyph | local visible cell |
| Colour ownership | global category/legend | per-cell fg/bg |
| Mark making | deterministic | gestural/stochastic |
| Reproducibility | high priority | optional |
| Geometry | exact cell coordinates | visual result |
| Palette | semantic mapping | colour selection/mixing |
| Interchange | native + plain text | native + styled/raster |
| Transform policy | category preserving | appearance preserving |
| Import | explicit classification | direct image conversion |
| Export | data fidelity | visual fidelity |
| Grid/rulers | normally prominent | optional/on demand |

A project may land at different positions for different layers.

# 3. Profile selection

## 3.1 Point-dominant / Precision profile

Choose when:

- glyphs/cells encode categories or system state;
- global recolouring must not alter meaning;
- plain text should preserve useful information;
- coordinates/rulers/grid matter;
- deterministic editing and comparison matter;
- scientific/engineering interpretation matters.

Typical adopted features:

- semantic palette and labels;
- usage counts;
- deterministic brush footprints;
- primary/secondary semantic glyphs;
- category flood fill;
- square-cell view;
- 1:1 shape constraints;
- structured line/box glyphs;
- plain-text import/export;
- precise coordinate/status surfaces.

Expressive brushes should normally be limited to non-authoritative annotation/presentation layers.

## 3.2 Paint-dominant / Expressive profile

Choose when:

- visual appearance is the principal output;
- local colour/style variation is essential;
- brush texture and gesture matter;
- images are common inputs/outputs;
- a broad shape vocabulary improves creation speed.

Typical adopted features:

- per-cell fg/bg;
- primary/secondary colours;
- painterly brush families;
- local colour blending;
- broad decorative shape vocabulary;
- raster image conversion;
- PNG/JPEG/BMP/GIF-style outputs;
- colour inversion and visual transforms.

Semantic labels/palettes remain useful when global recolouring or role consistency is desired, but need not govern every cell.

## 3.3 Layered Hybrid profile

Choose when the project contains both authoritative meaning and visual treatment.

Recommended architecture:

~~~text
authoritative semantic layer(s)
    + optional expressive annotation/presentation layer(s)
    -> composed view/export
~~~

Examples:

- simulation material grid + visual annotation;
- game collision/material map + decorative art;
- scientific data map + hand-drawn explanatory overlays;
- semantic UI/layout map + theme/presentation layer.

This is preferable to allowing arbitrary painterly operations to rewrite the same cell fields that carry source meaning.

## 3.4 Mode-separated Hybrid profile

Some projects may use whole documents/modes with different policies.

Examples:

- data-edit mode uses semantic cells;
- presentation-edit mode uses expressive cells;
- export compositor merges them.

Mode/layer policy MUST be visible and persisted.

# 4. Adopt / Adapt / Reject / Extend

For every relevant MZPaint feature classify:

| Decision | Meaning |
|---|---|
| **Adopt** | Fits directly |
| **Adapt** | Useful principle but project-specific form required |
| **Reject** | Not appropriate for this project |
| **Extend** | Baseline is insufficient; add project-specific behaviour |

Review at minimum:

### Document/style model

- semantic palette;
- per-cell foreground/background;
- text attributes;
- field background;
- hybrid appearance overrides;
- semantic labels/legend;
- usage counts.

### Tools

- deterministic pencil;
- large square/circle/ratio brushes;
- flood fill;
- eraser;
- glyph/category picker;
- colour picker;
- magnifier;
- calligraphy;
- airbrush;
- oil/crayon/natural pencil;
- marker;
- watercolor;
- text;
- precision shapes;
- expressive/decorative shapes.

### Selection/transforms

- rectangular/free selection;
- transparent selection;
- cut/copy/paste;
- crop;
- resize;
- skew;
- rotate/flip;
- invert colour;
- 1:1 constraint;
- category-preserving resampling.

### View

- grid;
- rulers;
- status;
- coordinates;
- selection dimensions;
- square cells;
- zoom range;
- full screen;
- alternative Ribbon/Classic presentation.

### Files/interchange

- native project format;
- plain text;
- styled HTML;
- raster import;
- raster export;
- palette import/export;
- print.

Do not classify an unimplemented requirement as **Reject** merely because current code lacks it.

# 5. Required tailored output

The project-specific specification SHOULD include:

## 5.1 Basis

- exact MZPaint baseline revision;
- direct implementation spec revision;
- reference variants actually consulted;
- project architecture/requirements used.

## 5.2 Philosophy profile

State whether the project is:

- Precision-dominant;
- Expressive-dominant;
- Layered Hybrid;
- Mode-separated Hybrid;

and justify the choice.

If different layers use different policies, provide a table:

| Layer/document | Authority | Style policy | Allowed tools | Export role |
|---|---|---|---|---|

## 5.3 Cell/document authority

Define exactly:

- what a cell means;
- where semantic identity lives;
- where appearance lives;
- whether same glyph can have multiple colours;
- how blank/background is represented;
- what transformations are allowed.

## 5.4 Palette and colour contract

Define:

- semantic palette/legend if used;
- artistic primary/secondary colours if used;
- colourway/theme behaviour;
- usage counts/labels;
- override precedence in hybrid mode.

## 5.5 Tool policy matrix

For each tool family record:

| Tool | Semantic mutation | Appearance mutation | Deterministic | Allowed layers |
|---|---:|---:|---:|---|

This is especially important for expressive brushes in scientific projects.

## 5.6 Geometry and transform policy

Define:

- cell coordinate model;
- square/font/custom aspect;
- rulers/grid/status;
- shape constraints;
- resize/skew resampling policy;
- whether transforms may alter category counts.

## 5.7 Selection/history contract

Define full-payload copy/paste, transparency semantics, undo/redo granularity and stochastic brush redo policy.

## 5.8 Interchange fidelity matrix

For every supported format record whether it preserves:

- glyphs;
- semantics;
- semantic labels;
- local colour/style;
- layers;
- editability.

Lossy formats MUST be identified as such.

## 5.9 Acceptance criteria

Write tests for the project's actual profile rather than claiming conformance merely because generic MZPaint features exist.

## 5.10 Implementation status boundary

Distinguish:

- required;
- implemented;
- planned;
- known deviation;
- qualified/tested.

# 6. Crossover safety rules

## 6.1 Expressive does not silently overwrite meaning

If a cell/layer has authoritative semantics, painterly operations SHOULD:

- write to a separate appearance/annotation layer; or
- require an explicit destructive/semantic mode.

A colour-only brush must not silently reclassify a data cell.

## 6.2 Semantic recolour does not silently erase art

In hybrid mode, global semantic recolouring SHOULD update base/category presentation while preserving independent appearance overrides unless the user chose a flatten/restyle operation.

## 6.3 Flood fill must use the correct equivalence

Precision fill usually compares semantic class/glyph.

Expressive fill may compare glyph + foreground + background/style.

Hybrid tools must declare which equivalence they use.

## 6.4 Raster import is not semantic recovery

Image-to-glyph conversion is an expressive visual conversion by default.

If the project needs categories from an image, specify a classification/mapping workflow.

## 6.5 Resize/skew can be scientifically destructive

For category maps, resampling can duplicate/drop classes and alter counts.

Warn, preview, retain undo, and use a declared categorical policy.

## 6.6 Randomness and reproducibility

If stochastic brushes are allowed in a reproducible workflow, record exact result deltas or deterministic seeds.

# 7. Use-case recommendations

| Project/use case | Recommended profile | Rationale |
|---|---|---|
| Cellular simulation/material editor | Precision | glyph/category identity and exact coordinates dominate |
| Collision/terrain/material mask editor | Precision or Hybrid | semantic source with optional decorative overlay |
| Scientific annotation grid | Hybrid | authoritative classes plus expressive notes/highlights |
| Engineering/topology diagram | Precision | deterministic geometry and semantic legend |
| ASCII/ANSI artwork | Expressive or Hybrid | depends whether glyphs are visual marks or semantic roles |
| Terminal UI/layout designer | Precision/Hybrid | structural cells plus theme/presentation layer |
| Game map editor | Hybrid | gameplay semantics plus visual decoration |
| Glyph poster/banner/art tool | Expressive | local colour/brush freedom dominates |
| Image-to-glyph converter/editor | Expressive | raster appearance is the source |
| Educational diagram | Hybrid | semantic content plus illustrative emphasis |
| Procedural-art mask authoring | Hybrid | exact masks feeding expressive render |
| Debug/diagnostic overlay editor | Precision | repeatable categories and coordinates |

These are defaults, not substitutes for project audit.

# 8. Lifecycle and drift

Pin the project-specific spec to an exact `specdocz` revision.

When MZPaint changes:

1. compare shared-spec revisions;
2. review only the relevant delta;
3. classify new/changed patterns as Adopt / Adapt / Reject / Extend;
4. update the project specification deliberately;
5. record the new pin.

Revisit the project profile when:

- cell semantics change;
- a layer system is added/removed;
- raster import/export becomes important;
- scientific reproducibility requirements change;
- new painterly tools are introduced;
- transform/resampling behaviour changes;
- palettes/legends become authoritative.

# 9. Reusable agent instruction

> **Create or update this project's glyph/cell editing specification using `specdocz/mzpaint/mzpaint-uiux-spec.md` as the normative baseline. First audit what each editable cell/layer represents, whether appearance or semantic identity is authoritative, reproducibility requirements, coordinate/grid needs, palettes/legends, brush workflows, transforms, file interchange, existing UI, tests and current architecture. Pin the exact `specdocz` revision. Classify the project and, where necessary, each layer as Precision-dominant, Expressive-dominant, Layered Hybrid or Mode-separated Hybrid. Review `mzpaint-implementation-spec.md` as a pattern library rather than mandatory architecture and classify relevant patterns as Adopt, Adapt, Reject or Extend. Use GlyphPoint-referenced material as the main precision/scientific precedent and GlyphPaint-referenced material as the main expressive/artistic precedent. Preserve all relevant philosophies/features of both where they add value, but explicitly document crossover tradeoffs: semantic palette vs per-cell colour, deterministic vs stochastic brushes, category vs visual flood-fill equivalence, exact vs appearance-driven transforms, plain-text vs raster interchange, and authoritative vs presentation layers. In hybrid projects, keep semantic/source meaning separately recoverable from expressive appearance by default. Produce a self-contained project-specific specification with tool-policy, palette, selection/history, transform, view, interchange-fidelity and acceptance matrices, and distinguish required behaviour from current implementation/qualification status.**
