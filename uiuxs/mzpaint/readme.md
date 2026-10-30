# mzpaint

Reusable specifications for **glyph/cell-grid creation and editing** across a spectrum from precision/semantic authoring to expressive/painterly authoring.

The reference philosophy is unified from two related programs:

- **GlyphPoint** is the main reference for precision, scientific, categorical and reproducible work.
- **GlyphPaint** is the main reference for expressive, artistic and painterly work.

They share a cell-grid substrate, selection/transform/history model, rulers/status/zoom workflow, text tooling, local file handling and Paint-like interaction language, but deliberately differ in **what a cell means** and **how appearance is owned**.

The reusable specs therefore do not prescribe one winner. A project should choose a Point-dominant, Paint-dominant or layered-hybrid profile according to its actual purpose.

## Documents

| Document | Purpose |
|---|---|
| [mzpaint-uiux-spec-glyphpoint-glyphpaint.md](mzpaint-uiux-spec-glyphpoint-glyphpaint.md) | Unified normative UI/UX spec with direct GlyphPoint/GlyphPaint comparison and provenance |
| [mzpaint-uiux-spec.md](mzpaint-uiux-spec.md) | Standalone unified UI/UX spec using Precision and Expressive disciplines |
| [mzpaint-implementation-spec-glyphpoint-glyphpaint.md](mzpaint-implementation-spec-glyphpoint-glyphpaint.md) | Direct implementation contract with reference examples |
| [mzpaint-implementation-spec.md](mzpaint-implementation-spec.md) | Standalone implementation contract |
| [mzpaint-spec-tailoring.md](mzpaint-spec-tailoring.md) | Procedure for choosing and integrating the appropriate balance for an active project |

## Core distinction

**Precision / semantic discipline**

A glyph or category is authoritative. Appearance is resolved from shared semantic mappings where possible. Global recolouring, categorical meaning, deterministic marks, coordinates, rulers, selection dimensions, exact grid transforms and reversible data interchange matter more than local painterly variation.

**Expressive / painterly discipline**

The cell's local appearance is authoritative. Per-cell foreground/background/style, material-like brushes, local blending, broad shape vocabularies, raster import/export and visual spontaneity matter more than globally uniform semantic encoding.

**Layered hybrid**

Keep semantic identity and expressive appearance separable. This is the preferred combination when a project needs both scientific meaning and rich annotation/visual treatment.

## Recommended use

For a new project:

1. use the standalone UI/UX spec as the baseline;
2. classify the project and each editable layer as Precision-dominant, Expressive-dominant, or Hybrid;
3. review the implementation spec as a pattern library;
4. use the tailoring guide to write a self-contained project-specific contract;
5. consult the reference-backed variants for concrete behaviours and tradeoffs.
