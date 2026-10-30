# MZPaint Unified Glyph/Cell Editing UI/UX Specification

**Status:** Reference UI/UX contract  
**Version:** 1.0  
**Scope:** Character-grid, glyph-grid, ANSI/ASCII, tile/cell, symbolic-map, scientific-grid, annotation and expressive cell-art editors  
**Normative language:** **MUST**, **SHOULD**, and **MAY** indicate requirements, recommendations and optional capabilities.

MZPaint treats precision/semantic and expressive/painterly authoring as two deliberately different specializations of a common cell-grid editor.

> **The Precision discipline prioritizes semantic glyph identity, deterministic geometry, global categorical styling, coordinate awareness and text/grid fidelity. The Expressive discipline prioritizes per-cell appearance, material-like brushes, broad visual shape language, colour mixing and raster-oriented interchange. A project must choose the appropriate balance rather than blindly combining every feature.**

## Contents

1. **Unified philosophy and reference feature inventory** — Defines both disciplines and all major reference capabilities.
2. **Document and cell meaning** — Compares semantic style ownership with per-cell expressive style.
3. **Mark-making and brush behaviour** — Compares deterministic footprints with painterly/stochastic brushes.
4. **Colour, glyph and palette systems** — Explains categorical legends versus local colour freedom.
5. **Geometry, shapes, selection and transforms** — Defines common editing foundations and precision/expressive tradeoffs.
6. **View, coordinates and presentation** — Covers grids, rulers, zoom, square cells, status and UI modes.
7. **Text, files and interchange** — Defines fidelity levels for JSON, text, HTML, raster and image conversion.
8. **Hybrid crossover model** — Recommends layered combinations without semantic corruption.
9. **Use-case appropriateness** — Recommends Precision-, Expressive- or Hybrid-dominant approaches by project class.
10. **Acceptance criteria** — Makes semantic fidelity, expressive fidelity and crossover behaviour testable.

# 1. Unified philosophy and reference feature inventory

## 1.1 Precision / scientific pole

A precision/scientific cell editor SHOULD emphasize:

- an exact rows × columns cell lattice;
- cursor coordinates, document dimensions and selection dimensions in the status surface;
- gridlines enabled by default;
- horizontal and vertical rulers;
- zoom from 25% to 800%;
- optional square-cell presentation;
- Shift-constrained 1:1 shapes and lines;
- deterministic pencil/eraser footprints;
- brush sizes from 1–60;
- circle, square, 3:1, 5:1, 1:3 and 1:5 brush footprints;
- primary and secondary glyph slots, mapped to left/right mouse;
- a glyph palette whose colours are resolved globally from glyph identity;
- a Glyph Colour Manager with Glyph / Colour / Hex / Uses / Represents / Actions;
- searchable/sortable glyph metadata by palette order, glyph, colour, usage or semantic label;
- global glyph replacement across palette and canvas;
- palette import/export;
- reusable colourways such as Pastel, Neon, Ocean, Forest, Monochrome and High contrast;
- a single field background;
- pencil, flood fill, text, eraser, glyph picker, magnifier and selection tools;
- rectangular and free-form selection;
- transparent selection;
- crop, clear/delete, move, cut/copy/paste and select all;
- resize by cells or percentage, aspect preservation and horizontal/vertical skew;
- rotate 90°/180°/270° and flip horizontal/vertical;
- line, rectangle, ellipse, triangle, right triangle, diamond, four arrows and explicit slash/backslash shapes;
- shape stroke modes Glyph / Lines / None;
- fill using primary or secondary glyph;
- line/box-drawing glyph generation for structured outlines;
- undo/redo history;
- text placement with font, scale, bold, italic, underline and transparent/opaque background;
- project JSON;
- direct plain-text import/export;
- coloured-HTML import/export;
- print;
- Ribbon and Win98-style Classic presentation modes operating on the same document state;
- local browser preferences and no required network service.

Most importantly, the Precision discipline's rendered foreground colour is **derived from glyph identity via the palette** rather than treated as arbitrary per-cell colour. The palette can attach a human-readable **Represents** label and usage count to a glyph. This is the central scientific/semantic design decision.

### Precision philosophy

A mark should be:

- reproducible;
- positionally unambiguous;
- categorically interpretable;
- globally restylable without changing meaning;
- exportable to simple text where possible;
- inspectable by coordinates and counts;
- constrained deliberately when geometry matters.

The visual presentation serves the model.

## 1.2 Expressive / artistic pole

An expressive/artistic cell editor SHOULD emphasize a familiar direct-painting workflow over an HTML/ANSI-style character-grid document.

Its current design emphasizes:

- each cell storing glyph, foreground colour, background colour, monospaced font and bold/italic/underline state;
- primary and secondary colours mapped to left/right mouse;
- pencil, fill, text, eraser, colour picker and magnifier;
- brush sizes 1–5;
- Brush, Calligraphy 1, Calligraphy 2, Airbrush, Oil, Crayon, Marker, Natural Pencil and Watercolor brush types;
- stochastic glyph distributions for airbrush/oil/crayon/natural pencil;
- calligraphic directional footprints;
- Marker behaviour that paints background colour while retaining glyph identity;
- Watercolor colour mixing into existing foreground/background state;
- rectangular and free-form/lasso selection;
- move, cut/copy/paste, transparent selection, select all and delete;
- crop;
- resize by cells or percentage with aspect preservation;
- horizontal and vertical skew;
- rotate 90°/180°/270°;
- flip horizontal/vertical;
- colour inversion;
- line and curve;
- rectangle and rounded rectangle;
- ellipse;
- polygon;
- triangle/right triangle;
- diamond, pentagon and hexagon;
- arrows;
- 4-, 5- and 6-point stars;
- rectangular/rounded/oval callouts;
- heart and lightning;
- solid, none or rough-glyph outlines;
- no fill, Color 1, Color 2 or glyph fill;
- editable standard-style colour palette and custom colour picker;
- text with font, scale, bold/italic/underline and transparent/opaque background;
- zoom 25–800%;
- gridlines, rulers, status bar and full screen;
- cursor coordinates and selection dimensions;
- project JSON;
- coloured-HTML import;
- raster image import converted to coloured glyph cells;
- selectable-text HTML export;
- plain text export;
- PNG, JPEG, BMP and GIF export;
- print and browser-safe wallpaper export;
- Ribbon and Win98-style Classic UI modes;
- local/self-contained operation with no server/framework/external assets required.

### Expressive philosophy

A mark should be:

- immediately manipulable;
- locally styleable;
- visually rich;
- brush-like rather than merely categorical;
- easy to layer, blend, distort and transform;
- interoperable with raster imagery;
- comfortable for familiar painting workflows.

The model serves the visual result.

## 1.3 Shared substrate

Both disciplines share important foundations:

- discrete cell coordinates;
- monospaced glyph-based canvas;
- local browser operation;
- dirty-state document lifecycle;
- undo/redo snapshots;
- primary pointer drawing;
- selection and clipboard;
- crop/resize/skew/rotate/flip;
- text placement;
- shapes;
- rulers/status/zoom;
- transparent selections;
- Ribbon/Classic presentation alternatives;
- JSON project persistence;
- plain text and HTML interchange;
- keyboard shortcuts for common document operations.

These commonalities SHOULD form the reusable base. The divergent semantics SHOULD remain explicit policy choices.

# 2. Document and cell meaning

The most important decision is **who owns appearance**.

## 2.1 Semantic ownership

In the Precision discipline, a cell's authoritative category is primarily its glyph. Visual colour is resolved from the shared glyph palette plus field background.

Conceptually:

```text
cell glyph
    -> palette entry
        -> semantic label ("Represents")
        -> shared colour
        -> rendered appearance
```

Advantages:

- recolour one category globally;
- category cannot accidentally drift into many colours;
- plain text retains most semantic content;
- glyph usage can be counted reliably;
- colour can remain redundant with glyph identity rather than becoming the only carrier of meaning;
- category labels/legends can be maintained centrally;
- deterministic comparisons and diffs are simpler.

Costs:

- local colour nuance is intentionally constrained;
- one glyph cannot easily carry many unrelated local colours without breaking the model;
- imported coloured artwork is normalized toward semantic glyph ownership;
- painterly shading is limited unless added as a separate layer.

This model is appropriate when a glyph represents a material, state, class, measurement band, topology feature, annotation type, simulation cell, terrain type, logical role or other repeatable category.

## 2.2 Explicit-cell appearance ownership

In the Expressive discipline, each cell can own:

```text
glyph
foreground colour
background colour
font
bold
italic
underline
```

Advantages:

- local shading and colour variation;
- heterogeneous appearance for identical glyphs;
- faithful styled-HTML/raster-like work;
- brush mixing and material simulation;
- richer image conversion and export.

Costs:

- identical glyphs can cease to mean visually identical things;
- global semantic recolouring requires explicit classes/layers rather than simple glyph mapping;
- plain-text export loses substantial appearance information;
- scientific meaning may become ambiguous if encoded only by colour;
- diffs and reproducibility can be noisier.

This model is appropriate when the visual result itself is primary.

## 2.3 Recommendation

Projects MUST explicitly choose one of:

- **Semantic-authoritative** — category/glyph identity owns appearance.
- **Appearance-authoritative** — each cell owns visual style.
- **Layered hybrid** — semantic identity is stored separately from an expressive appearance/annotation layer.
- **Mode-separated hybrid** — distinct document/layer types use different policies.

Do not create an accidental hybrid where some tools mutate semantic meaning and others merely repaint it without the user knowing which happened.

# 3. Mark-making and brush behaviour

## 3.1 Deterministic precision brushes

Precision-style brushes SHOULD favor exact footprints:

- single-cell pencil;
- square/circle footprints;
- aspect-ratio footprints;
- explicit integer size;
- deterministic line interpolation;
- repeatable result for the same path and settings.

Large size ranges are useful for mask editing, categorical regions and coarse scientific fields.

Flood fill in a semantic document SHOULD normally match semantic identity (for example glyph/class) rather than arbitrary local visual colour.

## 3.2 Expressive brushes

Expressive-style brushes MAY use:

- stochastic density;
- alternate glyph distributions;
- local colour mixing;
- directional calligraphy;
- glyph-preserving background treatment;
- texture-like marks.

the Expressive discipline examples:

- Airbrush randomly emits `.`, `:`, `*`;
- Oil draws from `@#%&`;
- Crayon draws from `xX#`;
- Natural Pencil draws from `.,/\`;
- Marker changes background while preserving existing glyph;
- Watercolor blends existing fg/bg toward the active colour.

These tools are appropriate when texture and gesture matter more than exact repeatability.

## 3.3 Crossover

Scientific/precision projects MAY use expressive brushes for:

- annotation layers;
- confidence overlays;
- presentation-only emphasis;
- non-authoritative masks;
- illustrative exports.

They SHOULD NOT silently alter authoritative semantic/data layers.

Artistic projects MAY use deterministic brushes for:

- pixel-perfect edges;
- tiling masks;
- hard-surface glyph art;
- repeatable pattern construction;
- constrained palettes.

If stochastic brushes are used where replay/reproducibility matters, the implementation SHOULD retain exact resulting deltas or a deterministic seed.

# 4. Colour, glyph and palette systems

## 4.1 Semantic palette

A precision palette SHOULD support:

- glyph/category identifier;
- colour;
- human-readable semantic label;
- usage count;
- search/filter;
- sort by usage/category/label/colour;
- global recolour;
- global category replacement;
- import/export;
- recoverable colourways.

Colourways MAY restyle a semantic document without changing category identity.

This separation is especially useful for accessibility themes, print themes and alternate scientific colour maps.

## 4.2 Expressive palette

An expressive palette SHOULD support:

- primary and secondary colours;
- left/right pointer roles;
- quick swatches;
- custom colour picking;
- per-cell foreground/background ownership;
- local mixing/blending.

A primary/secondary colour workflow is familiar for painting and shape fills.

## 4.3 Crossovers and tradeoffs

A semantic palette can improve artistic workflows when the artist wants:

- limited-palette discipline;
- instant global recolouring;
- material-role palettes;
- consistent character roles.

Per-cell colour can improve precision workflows when used for:

- temporary highlights;
- annotations;
- uncertainty/heat overlays;
- selection feedback.

When per-cell colour carries independent scientific meaning, that meaning MUST have explicit metadata/legend rather than relying on appearance alone.

# 5. Geometry, shapes, selection and transforms

## 5.1 Shared core

Both disciplines benefit from:

- rectangular and free-form selection;
- move/cut/copy/paste;
- transparent selection;
- crop;
- resize;
- rotate/flip;
- text;
- line/shape preview before commit;
- undo/redo around committed operations.

Selections SHOULD preserve the full cell payload relevant to the document model.

## 5.2 Precision geometry

Precision-oriented shape tools SHOULD favor:

- exact cell endpoints;
- coordinate-visible cursor;
- deterministic rasterization;
- 1:1 / constrained geometry modifier;
- box-drawing/structural line glyphs where useful;
- square-cell display option for geometric interpretation;
- explicit stroke width and fill category.

the Precision discipline's smaller shape vocabulary is suitable for diagrams, masks and structured maps because it emphasizes geometric primitives over decorative variety.

## 5.3 Expressive geometry

Expressive tools MAY provide a broader symbol vocabulary:

- curves;
- rounded rectangles;
- polygons;
- multiple regular polygons;
- stars;
- callouts;
- hearts/lightning and other illustrative primitives;
- colour fills and rough glyph outlines.

This improves speed for visual composition but can clutter precision-oriented interfaces if exposed without relevance.

## 5.4 Transform tradeoffs

Rotate/flip of a discrete grid is usually semantically safe when it is exact.

Resize and skew require more care.

For scientific/semantic documents:

- default to nearest-cell/category-preserving transforms;
- disclose when resampling duplicates/drops categories;
- avoid pretending a skewed/resampled categorical map is measurement-preserving;
- preserve an undoable source state.

For expressive documents:

- visual resampling/skew is acceptable when the result is the intended art;
- appearance preservation may matter more than categorical identity.

# 6. View, coordinates and presentation

Both styles SHOULD retain optional:

- cursor coordinate readout;
- selection dimensions;
- document cell dimensions;
- zoom control;
- rulers;
- gridlines;
- status feedback;
- full-screen editing.

### Precision defaults

Prefer:

- grid visible;
- rulers visible;
- coordinates/status visible;
- square-cell option prominent;
- exact zoom steps and 1:1 reset;
- constrained-shape affordances.

### Expressive defaults

Prefer:

- uncluttered canvas;
- grid optional/off by default where it distracts;
- rulers/status available on demand;
- visual preview prioritized.

## 6.1 Presentation mode is not document semantics

Both the Precision discipline and the Expressive discipline support Ribbon and Win98-style Classic interfaces over the same document state.

Therefore UI chrome style SHOULD be treated independently from the precision/expressive document model.

A project can have a compact modern UI while remaining precision-first, or a classic Expressive-like UI while using semantic categories.

# 7. Text, files and interchange

Different formats preserve different information.

| Format | Precision semantics | Expressive appearance | Recommended role |
|---|---|---|---|
| Project JSON/native | Full | Full | Authoritative editable source |
| Plain text | Strong glyph/category fidelity | Loses colour/style | Interchange, diff, code/data workflows |
| Styled/selectable HTML | Glyph + visible style | Strong | Portable visual/text sharing |
| PNG/JPEG/BMP/GIF | Visual only | Strong | Publication/display, not editable authority |
| Raster image import | No inherent semantics | Strong starting point | Expressive conversion or explicit classification workflow |

## 7.1 Precision-first interchange

Plain text SHOULD be first-class when glyph identity carries meaning.

Styled HTML export MAY resolve semantic palette colours at export time.

Raster export MAY be provided, but MUST NOT be presented as a reversible scientific source format.

## 7.2 Expressive-first interchange

Image import and raster export are appropriate.

Raster-to-glyph conversion MUST be described as a visual approximation, not recovery of original semantic categories.

## 7.3 Hybrid import

When importing styled HTML into a semantic project, choose explicitly:

- discard external colours and map by glyph;
- preserve imported colours as a non-authoritative appearance layer;
- convert styles into named semantic categories through a user mapping step.

Never silently reinterpret arbitrary colours as scientific meaning.

# 8. Hybrid crossover model

The preferred hybrid architecture is layered:

```text
semantic/source layer
    glyph/category/role
    label/legend metadata
    deterministic geometry

appearance layer
    fg/bg override
    emphasis
    annotation
    texture
    painterly effects

composited view/export
```

This avoids the most dangerous crossover failure: visually editing a scientific category map while unintentionally destroying its source meaning.

## 8.1 Useful crossovers

**Borrow from the Precision discipline into expressive tools**

- semantic palette roles;
- usage counts;
- global category recolour;
- glyph labels/“Represents” metadata;
- large deterministic brush footprints;
- square-cell mode;
- coordinate/ruler visibility;
- plain-text fidelity.

**Borrow from the Expressive discipline into precision tools**

- richer annotation brushes;
- local colour overlays;
- broader shape vocabulary;
- image import for tracing/reference;
- raster export;
- artistic presentation layer.

## 8.2 Conflicting choices

Where the philosophies conflict, the project specification MUST state which policy wins.

Examples:

| Question | Precision answer | Expressive answer |
|---|---|---|
| Same glyph, different local colours? | Usually no | Yes |
| Flood-fill equivalence | Semantic class/glyph | Full visible cell signature or visual policy |
| Brush randomness | Avoid/default deterministic | Useful and expected |
| Grid default | Usually visible | Often hidden |
| Colour role | Redundant/category style | Primary visual information |
| Raster import | Reference/classification only | Direct content source |
| Resize/skew | Preserve categories; warn on resampling | Visual result can dominate |
| Palette recolour | Global semantic operation | Optional stylistic operation |
| Output authority | Native/text data | Native/styled/raster art |

# 9. Use-case appropriateness

## 9.1 Precision-dominant / precision-first

Recommended for:

- scientific cell maps;
- cellular automata/material maps;
- simulation/debug masks;
- engineering or topology diagrams;
- categorical annotation;
- terminal/UI layout masks;
- level collision/material maps;
- symbol-coded planning tools;
- datasets where glyph identity must survive plain-text export;
- reproducible technical diagrams.

Use expressive features only in separate annotation/presentation layers unless explicitly safe.

## 9.2 Expressive-dominant / expressive-first

Recommended for:

- ANSI/ASCII art where appearance is the primary objective;
- glyph illustration;
- concept art;
- posters/banners;
- sprite-like character art;
- decorative terminal graphics;
- image-to-glyph reinterpretation;
- textured colour fields;
- artistic level decoration;
- visual mockups.

Semantic palette metadata remains optional but can be useful for global recolouring and role consistency.

## 9.3 Layered hybrid

Recommended for:

- game editors with collision/material semantics plus decorative glyph art;
- scientific visualization with hand-authored annotations;
- map editors with semantic terrain classes plus presentation overlays;
- dashboards/diagrams where symbols have meaning but colours/styles need local emphasis;
- educational visualizations;
- procedural-art tools with authoritative masks and expressive rendering;
- UI/layout authoring where cells have structural roles plus visual themes.

## 9.4 Mixed-mode documents

A project MAY allow some layers to be precision-authoritative and others expressive-authoritative.

The mode MUST be visible and persisted. Tool availability SHOULD reflect the active layer's policy.

# 10. Acceptance criteria

### Semantic fidelity

For precision/semantic layers verify:

- recolouring a palette category does not change glyph/category identity;
- “Represents”/legend metadata survives native save/load;
- usage counts match actual category occurrences;
- plain-text export preserves glyph/category grid;
- deterministic tools reproduce the same result for the same input;
- square-cell/ruler/grid presentation does not mutate document data;
- global glyph replacement updates intended cells consistently.

### Expressive fidelity

For expressive layers verify:

- per-cell foreground/background/font/style survive native save/load;
- brush types produce their declared visual behaviour;
- primary/secondary colours route correctly by pointer button;
- styled HTML preserves visible cell styling;
- raster exports correspond to the composed view;
- image import is locally converted without claiming semantic recovery.

### Shared editing

Verify:

- selection payload survives move/copy/paste;
- transparent selection behaves consistently;
- crop/resize/rotate/flip are undoable;
- coordinate and selection dimensions remain correct after zoom;
- text insertion preserves declared attributes;
- Ribbon/Classic UI mode changes presentation only.

### Hybrid safety

Verify:

- expressive annotation cannot silently mutate protected semantic layers;
- semantic recolour does not erase explicit appearance overlays unless that is the documented operation;
- import policy is explicit;
- export warns when the destination loses semantics or appearance;
- active layer/mode and tool policy are visible;
- undo restores both semantic and appearance state affected by an operation.

