# Tile-Native GUI/TUI Direct Implementation Specification

**Status:** Implementation contract  
**Version:** 1.0  
**Audience:** Engineers implementing a GUI, TUI, or shared GUI/TUI workspace framework  
**Normative language:** **MUST**, **SHOULD**, and **MAY** are requirements, recommendations, and optional capabilities.

This document turns the companion UI/UX specification into concrete state, interfaces, algorithms, invariants, and acceptance checks.

## Contents

1. **Required subsystem boundaries** — Minimum architecture and ownership.
2. **Command model** — One semantic command layer for every input surface.
3. **Application and tile state** — Concrete persistent state model.
4. **Layout solver** — Split-tree geometry, compact mode, and resize transactions.
5. **Hit testing and pointer routing** — Geometry-derived pointer behaviour.
6. **Overlay and modal stack** — Z-order, dismissal, and no-click-through.
7. **Cell/scene compositor** — Shared GUI/TUI presentation representation.
8. **Theme engine** — Data-only schema, semantic styling, adaptive ANSI/ASCII art.
9. **Input normalization** — Keyboard, mouse, focus, wheel, and paste events.
10. **Persistence and recovery** — Config/session boundaries and validation.
11. **Performance and concurrency** — Damage, budgets, generations, and latency.
12. **Conformance tests** — Automated and native qualification gates.

# 1. Required subsystem boundaries

Implement at least these logical modules:

- **CommandRegistry** — declares semantic commands and all routes.
- **Controller/Reducer** — sole owner of mutable application state.
- **TileRegistry** — declares persistent tile identities and capabilities.
- **LayoutSolver** — produces final rectangles from viewport + layout state.
- **HitMapBuilder** — builds z-ordered hit regions from solved geometry.
- **InputRouter** — normalizes platform events and resolves hits/capture/focus.
- **OverlayManager** — owns modal/overlay stack and input capture.
- **ThemeCompiler** — validates data-only themes into immutable runtime objects.
- **Compositor** — produces semantic scene/cells and protection metadata.
- **PlatformRenderer** — TUI terminal backend or GUI drawing/widget backend.
- **Persistence** — validates configuration and dynamic session state.
- **JobCoordinator** — generation-tags background results.

Required flow:

    platform event
      → normalize
      → capture/hit/focus resolution
      → command lookup
      → reducer/state mutation
      → layout solve
      → hit map + composition
      → logical damage
      → platform presentation

**Invariant:** platform input code MUST NOT directly mutate domain state outside the controller/reducer.

# 2. Command model

Use one stable command ID per semantic action.

Suggested type:

~~~text
CommandSpec {
    id: string
    label: string
    category: string
    help: string

    enabled(state) -> bool
    execute(state, context) -> State

    keyboard_routes: KeySequence[]
    pointer_routes: PointerRoute[]

    discoverable: bool
    destructive: bool
    reserved: bool
}
~~~

Examples:

~~~text
tile.hide
tile.restore_all
tile.focus_next
tile.swap
layout.resize
theme.choose
file.open
search.next
app.quit_guarded
~~~

### Parity invariant

For every enabled application command:

~~~text
has_keyboard_route(command) implies has_pointer_route(command)
~~~

Where pointer route includes menu, context menu, toolbar/title control, clickable object, direct manipulation, or mouse-operable command palette.

The reverse SHOULD also hold for meaningful semantic actions.

### Startup parity audit

~~~text
for command in registry:
    if command.is_application_semantic:
        assert command.keyboard_routes or command.pointer_routes

    if command.keyboard_routes:
        assert command.pointer_routes

    if command.pointer_only and command.keyboard_equivalent_is_meaningful:
        assert command.keyboard_routes
~~~

Reserved recovery commands SHOULD not be removable by configuration.

# 3. Application and tile state

Recommended immutable state shape:

~~~text
AppState {
    viewport: Viewport
    capabilities: Capabilities
    accessibility: AccessibilityState

    workspace: WorkspaceState
    tiles: Map<TileId, TileState>
    focus: FocusState
    overlays: OverlayStack
    capture: CaptureState?

    theme: ThemeState
    session_generation: int
}
~~~

Tile state:

~~~text
TileState {
    id: TileId
    visible: bool
    placement_hint: Placement
    local_focus: LocalFocus?
    cursor: CursorState?
    selection: SelectionState?
    scroll_x: int
    scroll_y: int
    navigation_memory: object
}
~~~

**Invariant:** hide, show, swap, responsive collapse, and maximize MUST NOT destroy TileState.

A typical workspace might contain Navigator, Outline, Editor, Preview, Inspector, Console, or Timeline tiles. Their identities and local memories remain stable even when current placement changes.

# 4. Layout solver

Use a split tree or equivalent constraint graph.

~~~text
LayoutNode =
    Leaf(tile_id)
  | Split(
        orientation: horizontal | vertical,
        ratio: float,
        first: LayoutNode,
        second: LayoutNode,
        divider_extent: int
    )
  | Stack(active_child, children)
~~~

Each leaf declares minimum usable width/height. Each split ratio is clamped after minimums are known.

### Solve order

1. Reserve non-negotiable host controls.
2. Compute minimum usable tile geometry.
3. Allocate user-requested margins/artspace.
4. Allocate theme decoration.
5. If multi-tile minimums fail, enter compact focused-tile mode.
6. Produce final rectangles.
7. Build hit regions from those rectangles.

Decoration MUST shrink before usable content.

### Divider transaction

~~~text
on_pointer_down(divider):
    capture = ResizeCapture(
        split_id,
        original_ratio,
        pointer_origin,
        preview_ratio = original_ratio
    )

on_pointer_move(capture):
    capture.preview_ratio = clamp(pointer_to_ratio(), legal_range)
    render_preview(capture.preview_ratio)

on_pointer_up(capture):
    commit_ratio(capture.preview_ratio)
    capture = null

on_escape_or_focus_loss(capture):
    restore_ratio(capture.original_ratio)
    capture = null
~~~

TUI: divider target SHOULD be the structural cell itself.  
GUI: target MAY use extra invisible hit slop without changing visual thickness.

# 5. Hit testing and pointer routing

Hit regions MUST be rebuilt from the final layout/composition, with z-order.

~~~text
HitRegion {
    rect: Rect
    z: int
    role: HitRole
    target_id: string
    command_id: CommandId?
    cursor_hint: CursorHint?
    metadata: object
}
~~~

Recommended roles:

~~~text
tile
tile_control
divider
menu_item
context_target
text
link
selection
scroll_area
overlay
~~~

Resolution:

~~~text
hit = highest_z_region_containing(pointer)

if capture exists:
    route_to_capture()
else if overlay exists:
    route_within_overlay_or_dismiss()
else:
    focus_target_if_needed()
    dispatch_hit_action_same_event()
~~~

### Focus-and-act invariant

Clicking an actionable unfocused tile MUST focus it and perform the clicked action in the same gesture.

### Selection conventions

Where text semantics exist:

- drag: exclusive-end selection;
- double-click: word;
- triple-click: source/logical line;
- right-click inside selection: preserve selection;
- right-click outside selection: move caret/selection first, then open context;
- wheel: scroll tile under pointer without moving keyboard selection.

# 6. Overlay and modal stack

Represent overlays explicitly:

~~~text
Overlay {
    id
    kind
    rect
    modal: bool
    dismiss_on_outside_click: bool
    keyboard_selection
    hover_selection
}
~~~

Rules:

1. Top overlay receives input first.
2. Outside-click dismissal consumes the click.
3. Escape closes exactly one overlay level.
4. Submenus clamp to viewport and open inward when needed.
5. Hover selection and keyboard selection are independent.
6. Opening/closing an overlay MUST NOT synthesize a click into underlying content.

Transactional choosers SHOULD snapshot pre-open state:

~~~text
open chooser → snapshot committed_value
highlight/click → preview candidate
confirm → commit candidate
Escape → restore snapshot
~~~

Uncommitted previews MUST never enter persisted session state.

# 7. Cell/scene compositor

Use a semantic intermediate representation even when the GUI renderer is not cell-based.

TUI cell:

~~~text
Cell {
    grapheme: string
    fg: Colour
    bg: Colour
    attrs: Attributes
    continuation: bool
    protection: ProtectionClass
}
~~~

GUI scene items MAY be vector/native equivalents, but should retain semantic role, state, rectangle, and protection metadata.

Recommended protection classes:

~~~text
decorative
content
interactive
critical
overlay
~~~

Compositing order:

    background
    → decorative underlay
    → adaptive frame/pattern layers
    → content
    → protected interactive surfaces
    → overlays

Decorative painters MUST NOT overwrite protected interactive/critical cells.

Wide terminal glyphs MUST be emitted/clipped atomically.

# 8. Theme engine

Themes are validated, immutable data. Never execute theme content.

Recommended top-level structure:

~~~toml
schema = "tile-theme/1.0"
id = "example"
name = "Example"
fps = 20

[palette]
background = "#101014"
text = "#d8d8df"
accent = "#64d8ff"
warning = "#ffcf66"
error = "#ff667a"

[styles.focused]
fg = "accent"

[geometry]
outer = [2, 2, 2, 2]
border = 1
divider = 1

[[layers]]
id = "outer-frame"
slot = "outer"
art = "@art.frame"
fit = "frame"

[[variants]]
min_width = 120
show_layers = ["wide-masthead"]

[fallbacks.ascii]
glyph = "#"

[fallbacks.monochrome]
palette = "mono"

[fallbacks.reduced_motion]
hide_layers = ["particles"]
~~~

### Required theme properties

- semantic palette roles, not arbitrary control-specific escape strings;
- deterministic inheritance/override;
- closed schema validation;
- bounded decoded art;
- bounded layer count;
- bounded animation tracks;
- safe fallback theme;
- responsive variants;
- ASCII fallback;
- monochrome fallback;
- reduced-motion fallback.

### Adaptive art algorithms

Implement at least:

1. **Nine-slice/frame fitting** — preserve corners; stretch/repeat edges.
2. **Tiled motif** — repeat a bounded motif within a slot.
3. **Procedural pattern** — regenerate from destination dimensions.
4. **Responsive variant** — switch/simplify art by viewport/capability.
5. **Clipped crop** — trim nonessential decoration without invading content.

### Colour pipeline

~~~text
semantic colour
  → accessibility override
  → target colour-depth quantization
  → renderer colour representation
~~~

Support:

    truecolour → ANSI-256 → ANSI-16 → monochrome

Quantization MUST be deterministic.

### Animation

Two rate classes are recommended:

- spatial/shape animation: bounded by theme/app cadence, max about 30 FPS;
- flash-like style/palette/visibility changes: max about 2 transitions/second.

Reduced motion disables nonessential tracks. Motion off freezes to a deterministic base frame.

# 9. Input normalization

Normalize platform-specific input before command routing.

~~~text
InputEvent =
    Key(sequence)
  | TextInput(text)
  | PointerDown(button, x, y, modifiers)
  | PointerUp(button, x, y, modifiers)
  | PointerMove(x, y, modifiers)
  | Wheel(dx, dy, x, y, modifiers)
  | FocusGained
  | FocusLost
  | Resize(width, height)
  | Paste(text, bracketed_or_native)
~~~

Keyboard and pointer events that represent commands become CommandIDs. TextInput remains text input.

On FocusLost:

- cancel or roll back pointer captures;
- clear held-button/key transient state;
- retain persistent focus identity only if platform semantics allow;
- never leave a drag active.

# 10. Persistence and recovery

Separate durable configuration from session state.

### Configuration

User-maintained configuration contains defaults and policy:

~~~text
layout defaults
minimum dimensions
input bindings
theme search paths
colour-depth override
unicode/ascii policy
mouse capability override
accessibility
motion level
render budgets
~~~

Configuration SHOULD remain read-only during normal interaction.

### Session state

Machine-written session state contains dynamic values:

~~~text
active workspace
tile visibility/order
split ratios
focused tile
per-tile memories
committed theme
workspace preset
~~~

Validate every restored field individually.

Provide a safe launch path:

~~~text
default layout
+ embedded safe theme
+ no session restore
~~~

# 11. Performance and concurrency

Maintain logical damage between composed frames.

~~~text
damage = diff(previous_scene, current_scene)
~~~

An unchanged frame SHOULD have zero logical damage.

A local caret/control change SHOULD NOT force unconditional full-screen clear/repaint.

Background tasks MUST use generation/version tags:

~~~text
request(gen=N, immutable_input)

on_result(result, gen):
    if gen != current_generation:
        discard(result)
    else:
        publish(result)
~~~

Prefer a bounded replaceable pending request over an unbounded queue for preview/layout-like work.

Set explicit budgets for:

- maximum decoded art cells;
- maximum layers;
- maximum animation tracks;
- maximum paint operations per frame;
- maximum FPS;
- maximum overlay/menu depth;
- maximum background pending work.

Measure **composition latency** and **input-to-frame latency** separately.

# 12. Conformance tests

Minimum automated suite:

### Command parity

~~~text
for command in command_registry:
    assert route_metadata_is_valid(command)
    if command.keyboard_routes:
        assert command.pointer_routes
~~~

### Geometry

Test combinations of viewport sizes, visible/hidden tiles, split extremes, minimum dimensions, compact-mode threshold, and resize while captured.

Use at least four representative small/normal/large/very-large viewport fixtures for golden geometry and rendering tests.

### Pointer

Verify:

- click-to-focus-and-act;
- full-row hits;
- wheel locality;
- double/triple-click semantics;
- right-click selection preservation;
- divider capture outside original target;
- Escape rollback;
- focus-loss rollback;
- overlay click-through prevention.

### Theme

Verify:

- invalid theme is atomic failure;
- deterministic quantization;
- ASCII fallback;
- monochrome fallback;
- narrow fallback;
- reduced-motion fallback;
- frame corner identity after resize;
- divider visual continuity;
- protected cells cannot be overwritten;
- motion-off deterministic frame.

### Damage/performance

Verify:

- identical frame → zero logical damage;
- local edit → bounded damage;
- no unbounded background queue;
- p50/p95/p99 composition distributions;
- separate native input-to-frame measurements.

### Native acceptance

For TUI targets, run real PTY integration tests where practical and manually qualify supported terminal emulators. For GUI targets, run native event-loop integration tests and manually qualify supported window systems.

Native checks include mouse press/release, focus loss during drag, resize during drag, wheel and horizontal wheel, high-DPI/zoom where applicable, Unicode/CJK/wide glyph boundaries, colour capability, crash/exit restoration, reduced motion, and high contrast.
