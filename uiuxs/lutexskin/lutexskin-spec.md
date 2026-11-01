# LUTEXskin — Flexible LUT, Texture, Zone and Skinning Standard

**Status:** Normative reusable UI/UX and theme-system specification  
**Version:** 1.0  
**Scope:** Cross-project software skinning, semantic colour systems, LUT palette generation/editing, gradients, procedural textures, part/state theming and theme interchange  
**Reference pins:** RetroBar-Extreme master at 65b36c0fba6ef8d8e44294b3ea332b03e32f638c; XenoField main at e6bdf5e741a69976be81066329cecda4cd6e20f6  
**Normative language:** **MUST**, **SHOULD**, and **MAY** indicate requirements, recommendations and optional capabilities.

LUTEXskin defines a portable theme model in which **colour, material, texture and component styling are reusable assets rather than one-off project code**.

The central model is:

~~~text
semantic colour roles + LUT banks + material recipes
                    ↓
          zone / part / state rules
                    ↓
            resolved visual properties
                    ↓
        platform-specific renderer / UI
~~~

The standard is inspired principally by:

- **RetroBar-Extreme** for deterministic LUT-coloured procedural textures, gradients, texture presets, live palette references, safe external greyscale tiles, part/property theming and property-atomic fallback;
- **XenoField** for dense 256-entry LUT banks, seeded palette generation/variation, spatial editing, selection/clipboard tools, A/B colour painting, gradients, transforms and bounded undo/redo.

LUTEXskin extends those approaches with a more general target hierarchy and a more approachable primary palette/material editor.

## Contents

1. **Goals and boundaries** — Defines what LUTEXskin standardizes and what it intentionally leaves to applications.
2. **Theme architecture** — Separates semantic roles, LUT banks, materials, targets, rules and renderer output.
3. **Zone / part / state / property model** — Generalizes RetroBar-style part theming across different applications.
4. **Colour system and semantic roles** — Defines named UI colour roles and contrast-safe fallbacks.
5. **LUT banks and palette generation** — Defines dense palettes, anchors, interpolation, generation and variation.
6. **LUT editor UX** — Defines a friendly primary composer plus an advanced XenoField-style spatial editor.
7. **Brushes, gradients and materials** — Defines solid, gradient, texture and composed material recipes.
8. **Procedural texture system** — Defines deterministic generators, controls, presets and extensibility.
9. **Texture LUT application and tone pipeline** — Defines greyscale-to-colour mapping, alpha, contrast and post-processing.
10. **Zones, continuity groups and coordinate spaces** — Extends part styling so textures and gradients can flow coherently across surfaces.
11. **Theme editor UX** — Defines selection, preview, inheritance, copy/paste, reset and high-frequency workflows.
12. **Theme document and interchange contract** — Defines portable declarative data, assets, versioning and fallback.
13. **Safety, accessibility and platform adaptation** — Bounds assets and preserves usability under constrained modes.
14. **Performance and caching** — Keeps live theming responsive and deterministic.
15. **Acceptance criteria** — Defines conformance tests for palette, texture, targeting, fallback and editing behaviour.
16. **Reference-derived design notes** — Records the reusable lessons taken from RetroBar-Extreme and XenoField.

# 1. Goals and boundaries

LUTEXskin SHOULD let projects share a consistent conceptual theme system without forcing them to share one GUI toolkit or renderer.

A conforming project should be able to reuse the same ideas and, where practical, the same theme assets across:

- desktop GUI applications;
- web applications;
- terminal/TUI applications with reduced capability;
- editors and dashboards;
- games/tools;
- visualization and creative applications.

The standard covers:

- semantic colour roles;
- dense one-dimensional LUT palettes;
- colour generation and editing;
- gradients;
- deterministic procedural textures;
- optional bounded local texture assets;
- materials/brushes;
- zones, parts and interaction states;
- inheritance/fallback;
- theme editing and live preview;
- declarative interchange.

It does **not** require:

- one rendering API;
- one file format encoding;
- identical pixel output across platforms;
- remote theme download;
- executable theme scripts;
- unrestricted layout mutation.

## 1.1 Visual skin versus functional layout

A theme MAY influence bounded presentation metrics such as:

- border thickness;
- radius;
- shadow strength;
- texture scale;
- font family from an approved set;
- compact/comfortable density tokens.

A theme MUST NOT silently change:

- command semantics;
- control order in a way that changes workflow;
- hit targets below project accessibility bounds;
- safety-critical visibility;
- data or application state.

Functional layout remains an application responsibility unless a project explicitly adopts a separate layout-skin contract.

# 2. Theme architecture

A theme SHOULD be decomposed into reusable layers:

~~~text
Theme
 ├─ metadata
 ├─ semanticRoles
 ├─ palettes
 │   ├─ swatch palettes
 │   └─ LUT banks
 ├─ materials
 │   ├─ solids
 │   ├─ gradients
 │   ├─ procedural textures
 │   └─ bounded local texture assets
 ├─ rules
 │   └─ target selectors → visual properties/material refs
 ├─ optional metrics
 └─ accessibility / capability variants
~~~

The same material or LUT SHOULD be referenceable from many targets rather than copied into every part.

Themes SHOULD distinguish **source definitions** from **resolved renderer output**.

# 3. Zone / part / state / property model

LUTEXskin generalizes RetroBar-Extreme's part/property mapping into:

~~~text
zone → part → state → property
~~~

### Zone

A large logical visual area or UI domain.

Examples:

- chrome;
- navigation;
- workspace;
- content;
- inspector;
- status;
- overlay;
- dialog;
- canvas;
- timeline.

### Part

A recurring visible component or sub-region.

Examples:

- panel;
- toolbar;
- button;
- tab;
- input;
- menu;
- list-row;
- card;
- titlebar;
- divider;
- scrollbar;
- selection;
- tooltip.

Applications MAY define namespaced parts such as:

~~~text
timeline.note
timeline.grid
inspector.plot
terminal.cursor
simulation.cell
~~~

### State

Interaction or semantic state.

Core states SHOULD include where applicable:

- default;
- hover;
- active/pressed;
- selected;
- focused;
- disabled;
- attention/flashing;
- warning;
- error;
- success.

### Property

A styleable visual property.

Core properties SHOULD include where applicable:

- background;
- foreground;
- border;
- accent;
- icon;
- highlight;
- shadow;
- texture/material;
- focus indicator.

## 3.1 Target registry

Each application SHOULD publish a target registry describing:

- stable zone IDs;
- stable part IDs;
- supported states;
- supported properties;
- optional semantic tags;
- renderer limitations.

A theme MUST NOT need to know internal widget class names.

## 3.2 Selector precedence

Recommended precedence from most specific to least specific:

~~~text
instance/tag override
zone + part + state
part + state
zone + part
part
zone
semantic-role default
application base theme
~~~

The exact syntax is implementation-specific, but resolution MUST be deterministic.

## 3.3 Property-atomic fallback

A malformed, unsupported or missing property MUST fall back for that property without invalidating unrelated valid theme properties.

For example, a broken custom texture on one panel background must not erase:

- that panel's foreground;
- other parts;
- the rest of the theme.

This follows the robust property-level fallback demonstrated by RetroBar-Extreme.

# 4. Colour system and semantic roles

Themes SHOULD define a semantic role layer independently of concrete component targets.

Recommended core roles include:

~~~text
surface.base
surface.raised
surface.sunken
surface.overlay

text.primary
text.secondary
text.disabled
text.inverse

accent.primary
accent.secondary

state.hover
state.active
state.selected
state.focus
state.attention

status.info
status.success
status.warning
status.error

border.normal
border.strong
shadow.normal
~~~

Applications MAY extend this vocabulary.

## 4.1 Semantic roles should not encode every component

Use roles for concepts that recur throughout the application.

Use target rules for component-specific styling.

Bad:

~~~text
taskbar_button_hover_blue
timeline_button_hover_blue
dialog_button_hover_blue
~~~

Better:

~~~text
state.hover
button hover rule → state.hover material
~~~

## 4.2 Contrast and readability

The resolver SHOULD validate or derive readable foregrounds against resolved backgrounds.

Themes MAY provide explicit pairs, but the application MUST retain a safe fallback for:

- focus indicators;
- error/warning text;
- selected text;
- disabled text;
- critical confirmation UI.

# 5. LUT banks and palette generation

A LUT bank is a dense ordered colour sequence used by gradients, procedural textures, visualization, theme materials or application-specific rendering.

LUTEXskin SHOULD support arbitrary declared LUT lengths, with **256 entries as the recommended interoperable default**.

A LUT entry MAY contain RGBA where the renderer supports alpha.

## 5.1 Source versus sampled representation

A LUT SHOULD be able to retain both:

~~~text
editable source:
    anchor stops
    interpolation mode
    generation parameters
    seed
    locks

sampled result:
    N explicit RGBA entries
~~~

This avoids forcing users to hand-edit 256 values when the palette is conceptually a small set of meaningful anchors.

## 5.2 Anchor model

Recommended anchor:

~~~text
LutAnchor {
    position: 0..1
    colour: RGBA
    locked?: boolean
    label?: string
}
~~~

Anchors SHOULD support:

- add;
- remove;
- drag/reorder;
- exact numeric position;
- exact hex/RGBA edit;
- lock against generators/variation.

## 5.3 Interpolation

Implementations SHOULD offer at least:

- sRGB;
- linear RGB.

Implementations MAY additionally offer perceptual interpolation such as OKLab/OKLCH where supported.

The interpolation mode MUST be stored with the LUT source.

Cyclic LUTs MUST define endpoint wrapping explicitly rather than accidentally repeating the first entry.

## 5.4 Generator modes

A capable LUT generator SHOULD support several strategies:

- anchors → smooth linear palette;
- anchors → cyclic palette;
- monochrome / tinted monochrome;
- complementary;
- analogous;
- triadic/tetradic;
- warm/cool biased;
- luminance-ramp;
- seeded free generation;
- variation of current LUT.

Generated results MUST be bounded and reproducible when a seed is stored.

## 5.5 Seeded variation

Variation SHOULD support:

- amount from 0 to 100%;
- deterministic seed;
- locked anchors/regions;
- optional preserve-luminance or preserve-hue bias;
- preview before commit.

At zero variation the LUT MUST be unchanged.

XenoField's seeded generation and linear-light blend toward a generated cyclic palette is a useful reference, but the standard does not mandate its exact algorithm.

## 5.6 LUT libraries

A theme MAY contain multiple named LUT banks.

Recommended operations:

- duplicate;
- rename;
- reorder;
- favourite/pin;
- import/export;
- compare;
- derive variant;
- reference another palette or semantic role set.

# 6. LUT editor UX

The LUT editor MUST provide both a **friendly primary surface** and an **advanced dense editor**.

## 6.1 Primary surface: Palette Composer

The default interaction SHOULD be a composer built around:

- large continuous preview strip;
- draggable anchor stops;
- selected-anchor colour editor;
- interpolation selector;
- cyclic toggle;
- generator family;
- seed;
- variation amount;
- regenerate/variant controls;
- luminance/chroma/hue shaping;
- lock controls;
- live preview on representative themed surfaces.

The primary UI should answer:

> What colours define this theme/material, and how does the result flow?

It SHOULD NOT initially present a wall of 256 hex cells.

## 6.2 Palette Composer editing

Recommended high-frequency interactions:

- click strip to add anchor;
- drag anchor to move;
- double-click anchor for exact edit;
- right-click/context action to remove;
- Shift or multi-select for grouped anchor edits;
- lock anchor;
- distribute evenly;
- reverse;
- rotate cyclic LUT;
- resample to canonical size;
- generate variants without losing the current LUT.

## 6.3 Advanced surface: Spatial LUT Editor

An advanced view SHOULD retain XenoField-level direct control.

For a 256-entry LUT, use a 16 × 16 grid.

Required power features:

- rectangular drag selection;
- additive selection;
- subtract selection;
- toggle selection;
- Select All / None / Invert / Row / Column;
- bounded undo/redo;
- A/B colours;
- picker;
- brush;
- fill;
- horizontal/vertical/diagonal/radial gradients;
- flip horizontal;
- flip vertical;
- rotate 180°;
- copy/cut/paste;
- sparse selection-aware clipboard;
- native hex-matrix paste;
- direct single-entry edit.

Brush shapes SHOULD include:

- pixel;
- round;
- square;
- diamond;
- irregular.

The advanced editor MAY use different dimensions when the LUT size is not 256, but MUST show the logical ordering clearly.

## 6.4 Shared history

Primary and advanced LUT surfaces MUST operate on one authoritative LUT history.

Switching surfaces MUST NOT discard edits or create divergent copies.

# 7. Brushes, gradients and materials

A visual property SHOULD resolve to a **material** rather than only a raw colour.

Core material kinds:

~~~text
solid
gradient
texture
composite
reference
~~~

## 7.1 Solid

A solid material contains a semantic role or explicit RGBA value.

## 7.2 Gradient

A gradient SHOULD support:

- 2 or more stops;
- arbitrary stop offsets;
- angle/direction;
- linear minimum;
- optional radial/conic modes where supported;
- semantic-role or LUT references as stop sources;
- alpha.

Gradients SHOULD remain editable as stops rather than being flattened immediately.

## 7.3 Texture

A texture material consists conceptually of:

~~~text
greyscale field generator / tile
        ↓
tone shaping
        ↓
LUT colour mapping
        ↓
opacity / blend
        ↓
coordinate transform
~~~

## 7.4 Composite material

A composite MAY layer a bounded number of materials.

Recommended operations:

- over;
- multiply;
- screen;
- overlay;
- mask.

Implementations SHOULD cap composition depth.

A simple project MAY omit composite materials while still conforming to the core solid/gradient/texture model.

# 8. Procedural texture system

Procedural textures SHOULD be deterministic for a fixed recipe.

The standard recommends the RetroBar-Extreme pattern vocabulary as a useful baseline:

- brushed;
- carbon;
- noise;
- scanlines;
- checker;
- diamond;
- clouds;
- cells;
- marble;
- weave;
- bricks;
- dots;
- waves.

Projects MAY provide additional generators.

## 8.1 Generator metadata

Each generator SHOULD declare which parameters it uses.

Recommended common parameters:

~~~text
seed
frequency
octaves
strength
scale
angle
contrast
brightness
saturation
whiteLevel
resample
sharpen
sharpenRadius
phase/offset (optional)
warp (optional)
~~~

A UI SHOULD hide or disable parameters unused by the selected generator.

## 8.2 Deterministic periodic textures

Tiled generators SHOULD be periodic at tile boundaries by construction.

A procedural tile MUST NOT regenerate randomly on every paint/frame.

Random-looking generators MUST use a stored seed.

## 8.3 Texture presets

A preset stores generator/tone parameters independently from colour when useful.

This enables:

- apply “Fine brushed steel” while retaining current LUT;
- apply “Wild marble” to another colour scheme;
- share texture geometry separately from palette identity.

A preset MAY optionally include a LUT/material if explicitly saved as a full material preset.

## 8.4 Live generation

Edits SHOULD update a bounded preview immediately.

Expensive regeneration SHOULD be coalesced/debounced, but the UI should still feel continuous.

# 9. Texture LUT application and tone pipeline

Recommended pipeline:

~~~text
source greyscale / coverage
    → generator or local tile
    → optional resample
    → optional sharpen
    → contrast around midpoint
    → white-level remap
    → LUT sample
    → saturation adjustment
    → brightness adjustment
    → source alpha/coverage multiplication
    → material opacity/blend
~~~

The exact colour math MUST be documented.

## 9.1 LUT sampling

At minimum, sample piecewise linearly between neighbouring LUT entries.

Implementations SHOULD define whether interpolation occurs in:

- sRGB;
- linear RGB;
- another declared colour space.

Do not mix colour spaces silently.

## 9.2 Alpha

LUT alpha and source coverage MUST be conceptually separate.

Recommended:

~~~text
resultAlpha = lutAlpha × sourceCoverage × materialOpacity
~~~

Fully transparent output SHOULD zero hidden RGB where serialization/caching benefits from canonical output.

## 9.3 Tone controls

Texture tone controls SHOULD be non-destructive recipe values.

Recommended semantics:

- Contrast 1 = identity;
- Contrast 0 = midpoint;
- Brightness 0 = identity;
- Saturation 1 = identity;
- White level 1 = identity.

# 10. Zones, continuity groups and coordinate spaces

A major LUTEXskin extension over simple part theming is the ability to coordinate material mapping across several targets.

## 10.1 Coordinate spaces

A gradient/texture SHOULD declare a coordinate space:

- **local** — each target starts its own material coordinates;
- **part** — instances of the same part share a mapping basis where possible;
- **zone** — material is continuous across a zone;
- **window/workspace** — material flows across related zones;
- **screen/global** — optional, platform-dependent.

Local SHOULD be the safe default.

## 10.2 Continuity groups

Themes MAY define a continuity group:

~~~text
continuityGroup: "main-chrome"
~~~

Targets in the same group can share:

- texture origin;
- gradient origin;
- scale;
- angle;
- phase.

This enables a texture or gradient to cross a toolbar, status strip and adjacent chrome without obvious seams.

## 10.3 Orientation adaptation

Targets MAY expose orientation metadata.

A material rule MAY specify:

- preserve absolute orientation;
- follow part orientation;
- rotate with vertical layout;
- use explicit orientation variant.

Do not hard-code platform-specific 90-degree rotations into the theme data model.

## 10.4 Mapping modes

Texture/image mapping SHOULD support a bounded set such as:

- tile;
- stretch;
- contain;
- cover;
- native-density.

Procedural textures SHOULD normally use tile or native-density.

# 11. Theme editor UX

The theme editor SHOULD be organized around **what the user is styling**, not around the serialization format.

Recommended primary layout:

~~~text
target browser / live application preview
        │
        ├─ Zone
        ├─ Part
        └─ State

property cards
        ├─ Background
        ├─ Foreground
        ├─ Border
        ├─ Accent
        └─ Shadow / extras

selected property material editor
        ├─ Solid
        ├─ Gradient
        └─ Texture
~~~

## 11.1 Live preview

Every valid edit SHOULD update:

- a local material swatch;
- a representative component preview;
- the live application/theme preview when safe.

Invalid text/numeric input MUST NOT commit.

## 11.2 Inheritance visibility

The editor MUST distinguish:

- explicit override;
- inherited theme value;
- semantic-role reference;
- application fallback;
- invalid/missing asset fallback.

Useful actions:

- Reset property;
- Reset part/state;
- Reset zone;
- Reset theme overrides;
- Copy material;
- Paste material;
- Link to palette/LUT;
- Detach reference into local copy.

## 11.3 Zone/part browser

The target browser SHOULD support:

- search;
- filter by zone;
- state preview;
- only-overridden filter;
- inheritance/fallback badges;
- live “pick target from preview” where toolkit integration permits.

## 11.4 Material editor

For a texture, the high-frequency header SHOULD contain:

- pattern;
- preset;
- LUT/palette selector;
- scale;
- angle;
- strength/contrast where relevant.

Less-common generator/tone/resample settings SHOULD be progressively disclosed.

This improves on a flat parameter wall while retaining RetroBar-Extreme's full capabilities.

# 12. Theme document and interchange contract

Theme data MUST be declarative and MUST NOT contain executable code.

Recommended top-level structure:

~~~json
{
  "schema": "lutexskin/1.0",
  "name": "Example",
  "semanticRoles": {},
  "palettes": {},
  "materials": {},
  "rules": [],
  "metrics": {},
  "variants": {},
  "assets": {}
}
~~~

## 12.1 Material references

Rules SHOULD reference named materials where reuse is intended.

Inline material definitions MAY be allowed for one-off overrides.

## 12.2 Example rule

~~~json
{
  "selector": {
    "zone": "chrome",
    "part": "button",
    "state": "hover"
  },
  "properties": {
    "background": {"material": "blue-brushed"},
    "foreground": {"role": "text.primary"}
  }
}
~~~

## 12.3 Example procedural texture material

~~~json
{
  "type": "texture",
  "generator": "brushed",
  "lut": {"palette": "steel-256"},
  "seed": 7,
  "frequency": 8,
  "strength": 0.7,
  "scale": 1.25,
  "angle": 155,
  "contrast": 1.4,
  "brightness": -0.05,
  "saturation": 0.9,
  "whiteLevel": 1,
  "mapping": "tile",
  "coordinateSpace": "zone"
}
~~~

## 12.4 Versioning

Themes MUST declare a schema version.

Unknown future fields SHOULD be ignored only where the schema explicitly allows extension.

Invalid known fields SHOULD fall back atomically with a diagnostic.

## 12.5 Portability

A theme MAY contain platform variants, but SHOULD preserve common semantic roles/material names across them.

Renderer-specific data SHOULD be namespaced.

# 13. Safety, accessibility and platform adaptation

## 13.1 Local assets

External theme assets SHOULD be local/package-scoped by default.

Do not allow arbitrary remote URLs in the core standard.

For user-supplied texture files, implementations SHOULD bound:

- filename/path form;
- file size;
- dimensions;
- decoded memory;
- image count.

RetroBar-Extreme's plain-filename-only, no traversal/reparse, bounded PNG approach is a useful model.

## 13.2 Greyscale recolourable assets

For LUT-coloured user textures, prefer greyscale + alpha source tiles.

Reject or explicitly classify coloured source assets rather than silently treating RGB as luminance.

## 13.3 Accessibility variants

Themes SHOULD support capability/accessibility variants including:

- high contrast;
- reduced transparency;
- reduced motion;
- monochrome / low-colour;
- colour-vision-safe alternatives where the project requires them.

The application MUST retain a visible focus indicator and critical status semantics.

## 13.4 Reduced rendering capability

When textures or advanced gradients are unsupported, fall back in order to:

1. simplified material using the same LUT/semantic role;
2. solid semantic role;
3. safe application base theme.

# 14. Performance and caching

Theme resolution SHOULD avoid regeneration during ordinary paint callbacks.

Recommended cache key inputs for texture output:

- generator name/version;
- generator parameters;
- seed;
- source asset content hash;
- resolved LUT content;
- tone parameters;
- resampling/sharpen parameters.

Scale/transform values MAY remain brush/runtime transformations when they do not require resampling.

Caches MUST be bounded.

Palette/LUT edits MUST invalidate any material whose resolved colour output depends on that palette.

A file asset replacement SHOULD invalidate by content identity rather than timestamp alone where practical.

# 15. Acceptance criteria

A conforming implementation SHOULD test the following.

### Theme resolution

- selector precedence is deterministic;
- one invalid property does not invalidate the theme;
- missing rules fall back correctly;
- state overrides resolve correctly;
- namespace extensions cannot overwrite core IDs accidentally.

### Semantic roles

- foreground/background fallback remains readable;
- critical focus/error/warning states survive malformed themes;
- high-contrast variant remains navigable.

### LUT generation

- exact declared sample count;
- deterministic generation from stored seed;
- zero variation is identity;
- locked anchors survive generation/variation;
- cyclic and non-cyclic interpolation differ as declared;
- import/export round-trips.

### LUT primary editor

- anchor add/remove/move;
- exact colour edit;
- reverse/rotate/distribute;
- generator preview/commit;
- variation preview/commit;
- undo/redo shared with advanced mode.

### LUT advanced editor

For a 256-entry implementation verify:

- 16×16 construction;
- rectangle/add/subtract/toggle selection;
- row/column/all/none/invert;
- A/B pick and paint;
- brush shapes and sizes;
- fill;
- four gradient modes;
- flips and 180° rotation;
- sparse clipboard;
- offset paste;
- 2D hex-matrix paste;
- bounded undo/redo.

### Procedural textures

- fixed recipe yields deterministic tile;
- built-in generators tile cleanly where declared;
- unused parameters do not alter a generator;
- scale/angle/contrast/tone changes are independent;
- palette-linked textures refresh immediately;
- preset application can preserve current LUT where declared.

### Zones and continuity

- local mapping repeats independently;
- zone mapping remains continuous across participating targets;
- orientation rules are deterministic;
- continuity groups do not leak into unrelated zones.

### Assets and fallback

- oversized/malformed/missing asset falls back only for affected properties;
- traversal/remote asset attempts are rejected;
- content changes invalidate cache;
- theme remains usable without optional assets.

### Editor UX

- live preview reflects current valid state;
- invalid numeric/text edit is never committed;
- inherited versus explicit values are visible;
- Reset property/part/zone restores the correct fallback layer;
- copy/paste does not lose material source metadata.

# 16. Reference-derived design notes

## RetroBar-Extreme

Reference: master at 65b36c0fba6ef8d8e44294b3ea332b03e32f638c.

Relevant reusable practices include:

- stable human-facing part/property names mapped onto renderer/theme resource keys;
- theme-family capability differences hidden behind the part map;
- solid, gradient and texture brushes sharing one property slot;
- deterministic 64×64 procedural patterns;
- built-in brushed, carbon, noise, scanlines, checker, diamond, clouds, cells, marble, weave, bricks, dots and waves generators;
- generator-specific Seed / Frequency / Octaves / Strength usage;
- texture scale, angle, contrast, brightness, saturation, white level, resampling and sharpening;
- texture presets whose parameters can be applied while preserving colour;
- explicit LUT colours or a live reference to the style palette;
- texture palette slots;
- property-atomic fallback;
- bounded caches;
- safe bounded greyscale PNG tiles;
- content-hash asset invalidation;
- extensive DPI/tile-repeat/editor qualification;
- JSON styles in which omitted parts keep the underlying theme appearance.

LUTEXskin generalizes RetroBar's taskbar-specific parts into zone/part/state/property selectors and adds continuity groups plus a more approachable material editor.

## XenoField

Reference: main at e6bdf5e741a69976be81066329cecda4cd6e20f6.

Relevant reusable practices include:

- ten named 256-entry LUT banks;
- generated cyclic palettes from anchor colours;
- seeded palette variation;
- strict LUT validation;
- 16×16 spatial editor;
- rectangular/additive/toggle/subtractive selection;
- shape-preserving sparse clipboard;
- A/B paint colours;
- picker and brush tools;
- pixel/round/square/diamond/irregular brushes;
- fill and horizontal/vertical/diagonal/radial gradients;
- flips and 180° transform;
- direct cell editing;
- bounded 64-step undo/redo;
- text import/export compatibility;
- renderer-facing LUT representation remaining stable while the editing UI evolves.

LUTEXskin keeps that advanced editing power but makes a stop-based Palette Composer the normal first interaction.

## Relationship to other specdocz families

LUTEXskin can be combined with:

- **parametermaxing** for detailed numeric material/generator controls;
- **cohesive-techspression** for task-oriented theme workspaces and broad “feel” shaping;
- **tuiuiux** for tile/panel interaction contracts.

A consuming project should tailor the relevant pieces into one project-specific theme contract rather than treating every optional LUTEXskin capability as mandatory.
