# MZPaint Direct Implementation Specification — GlyphPoint + GlyphPaint Referenced

**Status:** Implementation contract  
**Version:** 1.0  
**Audience:** Engineers implementing glyph/cell-grid editors, scientific cell tools, ANSI/ASCII art tools, maps, or hybrid semantic/artistic editors  
**Reference pins:** `techrote/GlyphPoint@019578651dfcccabdd3de42f6d427e3d076203b4` and `techrote/GlyphPaint@983880c7d7a05bf639a49db73f1fa3cdb165d436`  
**Normative language:** **MUST**, **SHOULD**, and **MAY** indicate requirements, recommendations and optional capabilities.

This contract implements one engine with explicit precision/expressive policy modes rather than two unrelated editors.

## Contents

1. **Unified document model** — Semantic, expressive and hybrid layer policies.
2. **Style resolution and rendering** — Who owns colour/style and how cells compose.
3. **Tool capability model** — Semantic mutation, appearance mutation and geometry mutation.
4. **Precision tool engine** — Deterministic footprints, category fill and constrained geometry.
5. **Expressive tool engine** — Material-like brushes, stochastic marks and local colour blending.
6. **Palette and legend architecture** — Semantic legends and artistic colour roles.
7. **Selection, transforms and history** — Full-payload preservation and transform safety.
8. **View and coordinate system** — Zoom, rulers, cell aspect, grid and hit mapping.
9. **Import/export fidelity** — Native, text, HTML and raster preservation contracts.
10. **Testing and qualification** — Precision, expressive and hybrid gates.

# 1. Unified document model

Recommended model:

~~~text
Document {
    cols: int
    rows: int
    layers: Layer[]
    activeLayerId: LayerId
    semanticPalette: Map<SemanticId, SemanticEntry>
    artisticPalette: ArtisticPalette
    selection: Selection?
    history: History
}

Layer {
    id: LayerId
    name: string
    policy: SEMANTIC | EXPRESSIVE | HYBRID
    visible: bool
    locked: bool
    cells: Cell[]
}

Cell {
    glyph: string
    semanticId?: SemanticId
    appearance?: CellAppearance
    textStyle?: TextStyle
}

SemanticEntry {
    id: SemanticId
    glyph: string
    label: string
    colour: Colour
    metadata?: object
}

CellAppearance {
    fg?: Colour
    bg?: Colour
    opacity?: number
    blendMode?: string
}
~~~

GlyphPoint maps naturally to **SEMANTIC**: glyph identity is primary, shared palette colour resolves presentation, and the palette carries a human-readable `represents` label.

GlyphPaint maps naturally to **EXPRESSIVE**: each cell stores foreground/background colour plus text styling, so identical glyphs can look different locally.

A hybrid implementation MUST store policy explicitly. Do not infer semantics from whichever optional fields happen to be populated.

# 2. Style resolution and rendering

Use one resolution path per policy.

~~~text
resolveCell(cell, layer, document):

    SEMANTIC:
        semantic = lookup(cell.semanticId or semanticFromGlyph(cell.glyph))
        glyph = semantic.glyph or cell.glyph
        fg = semantic.colour
        bg = document.semanticFieldBackground
        textStyle = cell.textStyle

    EXPRESSIVE:
        glyph = cell.glyph
        fg = cell.appearance.fg
        bg = cell.appearance.bg
        textStyle = cell.textStyle

    HYBRID:
        base = semantic style
        visual = appearance override
        output = compose(base, visual)
~~~

Recommended hybrid precedence:

~~~text
semantic identity determines meaning
appearance override determines presentation
~~~

An appearance-only operation MUST NOT mutate `semanticId`.

A semantic recolour SHOULD update the palette entry and invalidate dependent cells rather than rewriting every cell. That follows GlyphPoint's global glyph-colour behavior.

An expressive repaint writes local `fg/bg` state, following GlyphPaint.

# 3. Tool capability model

Each tool SHOULD declare its authority.

~~~text
ToolSpec {
    id: string
    allowedPolicies: Set<LayerPolicy>
    mutatesSemantic: bool
    mutatesAppearance: bool
    mutatesGeometry: bool
    deterministic: bool
}
~~~

Examples:

~~~text
semanticPencil:
    semantic=true appearance=false deterministic=true

watercolor:
    semantic=false appearance=true deterministic=true by committed result

airbrush:
    semantic=false appearance=true deterministic=false unless seeded

categoryFlood:
    semantic=true appearance=false

visualFlood:
    semantic=false appearance=true

rotateSelection:
    geometry=true
~~~

The UI SHOULD disable, adapt, or clearly relabel tools that are inappropriate for the active layer. A scientific layer must not silently run a painterly tool that destroys semantic identity.

# 4. Precision tool engine

## 4.1 Deterministic footprints

Support integer-cell footprints such as:

~~~text
single
square(size)
circle(size)
rect(ratioX, ratioY, size)
~~~

GlyphPoint directly demonstrates circle, square, 3:1, 5:1, 1:3 and 1:5 footprints with brush size 1–60.

The same path/settings MUST yield the same cell set.

## 4.2 Category painting

~~~text
for each footprint cell:
    assign active semantic category/glyph
    preserve or clear visual overrides according to explicit layer policy
~~~

Left/right pointer buttons MAY map to primary/secondary semantic glyphs, as GlyphPoint does.

## 4.3 Semantic flood fill

Flood equivalence SHOULD compare category identity:

~~~text
target = semanticSignature(startCell)

while queue:
    if semanticSignature(cell) == target:
        assign active category
~~~

GlyphPoint's current fill compares glyph identity.

Do not compare visible colour if colour is only presentation metadata.

## 4.4 Structured geometry

Precision shapes SHOULD support deterministic integer rasterization.

GlyphPoint supplies a useful precedent:

- Glyph stroke;
- box-drawing/Lines stroke;
- no stroke;
- primary/secondary glyph fill;
- direction-aware line glyphs;
- connectivity-aware box glyphs;
- Shift-constrained 1:1 geometry.

Constraints MUST operate in cell coordinates rather than screen pixels.

# 5. Expressive tool engine

## 5.1 Primary/secondary colour routing

Recommended pointer convention:

~~~text
left pointer  -> Color 1 foreground / Color 2 background
right pointer -> Color 2 foreground / Color 1 background
~~~

This matches GlyphPaint.

## 5.2 Brush families

GlyphPaint provides concrete expressive precedents:

| Brush | Reference behaviour |
|---|---|
| Brush | active glyph over local footprint |
| Calligraphy 1 | diagonal `dx == dy` footprint |
| Calligraphy 2 | diagonal `dx == -dy` footprint |
| Airbrush | sparse random marks from `.:*` |
| Oil | random marks from `@#%&` |
| Crayon | random marks from `xX#` |
| Natural Pencil | random marks from `.,/\\` |
| Marker | retain glyph/foreground, paint background |
| Watercolor | blend existing fg/bg toward active colour |

These literal glyph sets are examples, not mandatory standard values.

## 5.3 Stochastic replay

If reproducibility matters:

- store exact changed-cell deltas; or
- use a recorded deterministic seed plus stable brush algorithm version.

Undo MUST restore the exact pre-stroke state even for stochastic brushes.

## 5.4 Visual flood fill

GlyphPaint's fill equivalence uses glyph + foreground + background.

A generic expressive fill SHOULD define an explicit visible signature such as:

~~~text
(glyph, fg, bg, optional text attributes)
~~~

Do not reuse semantic-fill equality accidentally.

# 6. Palette and legend architecture

## 6.1 Semantic palette

Recommended:

~~~text
SemanticEntry {
    id
    glyph
    colour
    label
    usageCount (derived)
}
~~~

A manager SHOULD support:

- search by glyph/label/colour;
- sort by order/glyph/colour/usage/label;
- direct colour + hex editing;
- global category/glyph replacement;
- add/remove/reset;
- import/export;
- colourway application;
- transactional revert.

GlyphPoint's manager exposes **Glyph / Colour / Hex / Uses / Represents / Actions** and supports palette order, glyph, colour, usage and Represents sorting.

Replacing a semantic glyph SHOULD migrate all intended cells atomically.

## 6.2 Artistic palette

Recommended:

~~~text
ArtisticPalette {
    primary: Colour
    secondary: Colour
    swatches: Colour[]
    recent?: Colour[]
}
~~~

Provide colour picker input and predictable left/right semantics.

## 6.3 Crossover

A hybrid project may use:

- semantic colourways for authoritative classes;
- artistic colours for annotation/appearance layers.

The UI MUST show which palette affects which layer.

# 7. Selection, transforms and history

## 7.1 Selection

Support:

~~~text
RectSelection { x, y, width, height }
FreeSelection { bounds, mask }
~~~

Internal copy/cut/paste MUST preserve the full native cell payload, not only glyph text.

Plain-text clipboard integration MAY coexist.

## 7.2 Transparency

Define transparency by policy:

- semantic blank class;
- whitespace glyph;
- explicit alpha;
- project-defined background category.

Do not infer transparency only from colour if colour can carry meaning.

## 7.3 Exact transforms

90°/180°/270° rotations and flips SHOULD preserve:

- semantic ID;
- glyph;
- appearance;
- text attributes.

## 7.4 Resize/skew

Define a transform policy:

~~~text
CATEGORICAL_NEAREST
VISUAL_NEAREST
VISUAL_BLEND
PROJECT_SPECIFIC
~~~

Precision/scientific layers SHOULD default to category-preserving nearest-cell behavior and warn when cells/categories will be duplicated or dropped.

Expressive layers MAY prioritize appearance.

All destructive transforms MUST be undoable.

## 7.5 History

History entries SHOULD include cells, dimensions, selection and any affected palette/layer metadata.

For stochastic brush strokes, record the resulting cells/delta rather than relying on new randomness during redo.

# 8. View and coordinate system

Keep document coordinates independent from display zoom.

~~~text
screenToCell(clientX, clientY):
    local = inverse(displayTransform)
    x = floor(localX / displayedCellWidth)
    y = floor(localY / displayedCellHeight)
~~~

Display state SHOULD include:

~~~text
zoom
showGrid
showRulers
showStatus
cellAspectMode: FONT | SQUARE | CUSTOM
~~~

Both references provide 25–800% zoom plus rulers/status. GlyphPoint also promotes square-cell display.

Rulers must follow zoom but never alter document coordinates.

Status SHOULD include cursor x/y, selection dimensions, document size and operation feedback.

Ribbon/Classic presentation changes MUST NOT change document semantics.

# 9. Import/export fidelity

Describe format capabilities explicitly.

| Format | Glyphs | Semantic IDs/labels | Per-cell style | Layers | Reversible |
|---|---|---|---|---|---|
| Native project | yes | yes | yes | yes | yes |
| Plain text | yes | usually glyph-derived only | no | no | partial |
| Styled HTML | yes | only if explicitly serialized | yes | usually flattened | partial |
| Raster | visualized only | no | composed image | no | no |

## 9.1 Plain text

For semantic documents, plain text MAY remain first-class if glyph identity carries class meaning.

For expressive documents it is explicitly lossy.

GlyphPoint imports/exports plain text directly.

## 9.2 Styled HTML

Styled HTML can preserve visible glyph styling.

GlyphPoint exports resolved palette colour; GlyphPaint preserves per-cell style runs.

If semantic metadata must survive, serialize it separately or through explicit attributes.

## 9.3 Raster image import

GlyphPaint converts raster samples to glyph cells using luminance plus sampled colour.

That is appropriate for expressive content.

A semantic/scientific layer MUST NOT claim that raster-to-glyph conversion recovered categories. Require user mapping, classification, or a reference-only appearance layer.

## 9.4 Raster export

PNG/JPEG/BMP/GIF are publication formats.

They MUST NOT be represented as lossless editable authority for semantic documents.

# 10. Testing and qualification

### Semantic mode

Verify:

- one category resolves consistently across cells;
- palette recolour updates all category references;
- Represents/label metadata survives native save/load;
- usage counts are correct;
- plain text preserves glyph layout;
- deterministic tools produce exact expected cell sets;
- category flood ignores irrelevant appearance;
- square/font cell aspect affects view only.

### Expressive mode

Verify:

- per-cell fg/bg/text style round-trip;
- primary/secondary pointer colour routing;
- each brush family meets its declared behavior;
- stochastic strokes undo/redo exactly;
- HTML preserves expected visible style;
- raster exports match composed output within rendering tolerances.

### Hybrid mode

Verify:

- semantic and appearance mutations are separately permissioned;
- expressive annotation cannot silently change semantic IDs;
- semantic recolour preserves independent appearance overrides unless documented otherwise;
- copy/paste retains both layers of state;
- active policy/layer is visible;
- lossy exports warn about what is lost.

## Reference basis

Precision/scientific reference: `GlyphPoint-v1a-layout-fixed.html` at `techrote/GlyphPoint@019578651dfcccabdd3de42f6d427e3d076203b4`.

Expressive/artistic reference: `GlyphPaint.html` and `README.txt` at `techrote/GlyphPaint@983880c7d7a05bf639a49db73f1fa3cdb165d436`.
