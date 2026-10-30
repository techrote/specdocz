# Tile-Native GUI/TUI UI/UX Specification — MDBM-Derived

**Status:** Reference UI/UX contract  
**Version:** 1.0  
**Scope:** Desktop GUI applications, terminal TUIs, and applications sharing a common GUI/TUI interaction core  
**Design basis:** MDBM interaction, layout, compositor, configuration, theme, and acceptance conventions  
**Normative language:** **MUST**, **SHOULD**, and **MAY** are requirements, recommendations, and optional capabilities respectively.

The central design principle is:

> **The interface is a configurable workspace of persistent tiles, backed by one semantic command system, with complete pointer/keyboard command parity and a cell-aware presentation layer capable of adapting rich ANSI/ASCII artwork to the available space and terminal capabilities.**

“Mouse can do anything the keyboard can do” means every **application command or state transition** available from a key binding MUST also have a practical pointer-accessible route. Arbitrary character composition is text input rather than an application command and is outside this parity rule.

## Contents

1. **Core design model** — Shared semantic architecture and interaction principles.
2. **Command and input parity** — Complete mouse/keyboard command equivalence.
3. **Tile workspace and responsive layout** — Configurable, resizable, persistent panel behaviour.
4. **Pointer and direct-manipulation UX** — Mouse interaction, dragging, menus, selection, and overlays.
5. **Theme, colour, and semantic styling** — Safe data-driven themes and colour-depth adaptation.
6. **Adaptive ANSI/ASCII graphics** — Scaling cell art, frames, patterns, fallbacks, and animation.
7. **Accessibility and constrained environments** — Narrow-mode, reduced-motion, high-contrast, and capability fallbacks.
8. **Configuration and persistence** — Durable configuration versus dynamic workspace state.
9. **Rendering and implementation architecture** — Shared GUI/TUI rendering model and performance requirements.
10. **Acceptance criteria** — Measurable parity, responsiveness, rendering, and native-platform gates.

# 1. Core design model

The application MUST separate **what an action means** from **how the user invokes it**.

Preferred event flow:

    input event → normalized interaction → hit/focus resolution → CommandID
    → state mutation → layout → render/composite → presentation

Keyboard shortcuts, mouse gestures, menu items, toolbar controls, command-palette entries, context menus, and accessibility actions MUST converge on the same semantic CommandID rather than maintaining parallel behaviour.

The UI SHOULD have:

- a single command registry;
- persistent tile identities independent of current placement;
- deterministic layout geometry;
- hit regions generated from final rendered geometry;
- an explicit overlay/modal stack;
- a semantic colour/style layer rather than hard-coded component colours;
- capability-aware rendering for GUI, truecolour terminal, ANSI-256, ANSI-16, monochrome, Unicode, and ASCII-only environments.

The application MUST preserve user work and spatial context across presentation changes. Hiding, moving, resizing, stacking, maximizing, or temporarily collapsing a tile MUST NOT silently discard its cursor, scroll position, selection, navigation history, or relevant local state.

Presentation code MUST NOT own application semantics.

# 2. Command and input parity

## 2.1 Command registry

Every meaningful application action MUST have a stable command identifier, for example:

- file.open
- tile.hide
- tile.restore_all
- tile.focus_next
- layout.resize_left
- theme.select
- search.next

A command MAY have multiple keyboard bindings and multiple pointer routes.

Every registered command SHOULD expose:

| Field | Purpose |
|---|---|
| id | Stable semantic identifier |
| label | Human-readable action |
| category | File, Edit, View, Tile, Navigate, Theme, etc. |
| enabled(state) | Current availability |
| keyboard_routes | Zero or more shortcuts |
| pointer_routes | Menu/button/context/direct-manipulation routes |
| destructive | Whether confirmation/special styling is required |
| discoverable | Whether exposed in command search |
| help | Concise description |

## 2.2 Pointer parity rule

A release MUST NOT contain a keyboard-accessible application command for which no practical pointer route exists.

Pointer routes do **not** require a permanent button for every command. Valid routes include:

- ribbon/menu entry;
- searchable command palette operated by mouse;
- toolbar or title-bar control;
- context menu;
- clickable object;
- drag operation;
- scroll/wheel interaction;
- workspace/tile manager.

Likewise, pointer-only semantic commands SHOULD have keyboard equivalents.

Automated parity validation SHOULD compare the command registry against all declared input surfaces and fail when commands become unintentionally keyboard-only or mouse-only.

## 2.3 Discoverability

The application SHOULD provide both a conventional menu/ribbon for spatial discoverability and a searchable command palette for exhaustive discovery.

Critical recovery commands — such as restore workspace, dismiss overlay, open command palette, or guarded exit — SHOULD always remain reachable even if user key bindings are extensively customised.

MDBM examples: Ctrl+P supplies the emergency command route, Ctrl+T restores tiles, Tab/Shift+Tab cycles visible tiles, and Alt+1…Alt+4 directly reveal/focus its four persistent tile identities. These are examples of routes into commands, not requirements for those exact bindings.

# 3. Tile workspace and responsive layout

## 3.1 Tile model

A **tile** is a persistent functional view with its own local state.

Tiles MUST be independently capable of being:

- focused;
- shown or hidden;
- resized;
- repositioned or swapped;
- restored;
- optionally stacked/tabbed;
- optionally maximized into the workspace.

Applications SHOULD support named workspace presets.

Tile identity MUST remain separate from current geometry. Moving a tile therefore changes its placement, not its identity or state.

MDBM's concrete reference layout demonstrates the model with Filesystem, Contents, Edit, and View. Filesystem/Contents share the left region while View/Edit occupy the right stack; the tile memories survive switching, hiding, swapping, and compact-mode collapse.

## 3.2 Split geometry

The layout SHOULD be represented by a split tree or equivalent deterministic constraint model.

Every split MUST have orientation, current ratio or size, minimum dimensions for each child, clamping rules, a structural divider, and a persisted user preference.

Dragging a divider MUST:

1. capture the pointer;
2. continue tracking if the pointer leaves the divider;
3. preview only valid/clamped geometry;
4. commit once on release;
5. roll back on Escape;
6. roll back safely on lost application/terminal focus.

The divider itself MUST remain visually distinct from decorative theme bands.

In TUIs, a structural divider will normally occupy exactly one terminal cell. In GUIs, its visual thickness MAY be narrow while using a slightly enlarged invisible pointer hit-slop region.

MDBM's reference defaults are 30/70 for the major column split and 50/50 for the right stack, with one-cell structural divider targets.

## 3.3 Responsive priority

Available space MUST be allocated in this order:

**essential application controls → minimum usable tile content → user-requested spacing → decorative theme geometry**

Decoration therefore yields before useful content.

When the workspace becomes too small for a meaningful multi-tile layout, the application MUST switch to a **compact focused-tile mode** rather than compressing several panels into unusable rectangles.

Hidden or temporarily compacted tiles remain logically alive and restorable.

A completely hidden workspace MUST retain an obvious restore route.

# 4. Pointer and direct-manipulation UX

Mouse support is a first-class interaction system, not a compatibility layer.

## 4.1 Hit testing

Pointer hit rectangles MUST be generated from the **final solved layout**, not duplicated from assumed geometry.

Clickable controls SHOULD expose their full visible area as a hit target. Whole logical rows SHOULD normally be clickable in trees, lists, tables, menus, and navigation panes.

A click inside an unfocused actionable tile SHOULD both focus that tile and perform the intended click action. Requiring a first click merely to focus and a second identical click to act is prohibited unless preventing accidental activation is itself a deliberate safety requirement.

MDBM explicitly follows this “focus and act” rule for editor clicks.

## 4.2 Standard direct manipulation

Where applicable:

- single click positions/focuses/selects;
- drag selects or manipulates;
- double-click performs semantic secondary selection/action;
- triple-click MAY select a complete logical row/line;
- wheel scrolling is local to the tile under the pointer;
- horizontal wheel/Shift-wheel SHOULD be supported where useful;
- right-click opens a context menu.

A right-click inside an existing selection SHOULD preserve that selection. A right-click outside it MAY first move the caret/selection to the pointed object.

Direct manipulation MUST update visible feedback immediately.

MDBM's editor uses drag selection, double-click word selection, triple-click line selection, and selection-preserving right-click behaviour.

## 4.3 Capture and transactionality

Drag operations are transactions.

The system MUST maintain explicit capture state for divider resizing, selection drags, tile movement/reordering where implemented, and sliders or continuous controls.

Escape SHOULD cancel an active drag and restore its pre-drag state.

Loss of window/terminal focus MUST not leave the application believing a mouse button remains held.

## 4.4 Menus and overlays

Overlays MUST have deterministic z-order and input capture.

An outside click that dismisses the top overlay MUST be **consumed**. It MUST NOT dismiss the overlay and simultaneously activate whatever happened to lie beneath it.

Escape closes one logical overlay level at a time.

Menus MUST remain inside the visible viewport. Submenus SHOULD open inward when insufficient space exists on their preferred side.

Mouse hover and keyboard menu selection MUST be tracked independently. Hovering another row MUST NOT silently rewrite keyboard-selection state unless the user actually changes selection.

These behaviours directly follow MDBM's overlay and menu contracts.

## 4.5 Pointer visibility of keyboard operations

Commands normally thought of as keyboard operations — such as tile swapping, maximize, restore, focus transfer, theme switching, search navigation, workspace presets, or layout reset — MUST remain reachable through pointer-operated menus or controls.

This is the principal requirement behind **“anything the keyboard can do.”**

# 5. Theme, colour, and semantic styling

## 5.1 Themes are data

Themes MUST be declarative presentation data.

Themes MUST NOT contain executable code, shell commands, command bindings, filesystem operations, document-content queries, arbitrary terminal escape sequences, clipboard access, or process access.

A malformed theme MUST fail closed without partially mutating the live interface.

The application MUST always provide an embedded safe/recovery theme.

This matches MDBM's strict data-only theme boundary.

## 5.2 Semantic roles

Colours SHOULD be assigned through semantic roles rather than component-specific literals.

Minimum recommended roles include:

background, text, muted, border, title, accent, heading, code, link, selection, diagnostic, status, warning, error, success.

State modifiers SHOULD include:

focused, hover, pressed, selected, disabled, dirty, busy, caution, destructive.

User-critical states such as caret, selection, focus outline, confirmation, and destructive controls MUST retain sufficient contrast even when a theme supplies poor values.

## 5.3 Colour capability

The presentation layer MUST support deterministic degradation through:

**truecolour → ANSI-256 → ANSI-16 → monochrome**

Colour quantisation SHOULD be deterministic so screenshots, golden tests, and repeated sessions remain reproducible.

Themes SHOULD provide explicit monochrome and high-contrast behaviour rather than relying exclusively on automatic approximation.

## 5.4 Transactional theme selection

Theme changes SHOULD be previewable.

Recommended behaviour:

- hover/click or arrow selection previews;
- explicit confirmation commits;
- Escape restores the previous committed theme;
- uncommitted previews MUST NOT leak into persistent session state.

MDBM's theme selector is explicitly transactional in this way.

User palette overrides SHOULD be separate from the source theme so themes remain upgradeable and recoverable.

# 6. Adaptive ANSI/ASCII graphics

Rich terminal artwork MUST be treated as **structured cell graphics**, not preformatted strings containing uncontrolled escape codes.

## 6.1 Cell representation

A composed cell SHOULD contain:

- grapheme/glyph;
- foreground colour;
- background colour;
- text attributes;
- wide-character continuation state;
- protection/ownership metadata.

Wide glyphs MUST be clipped atomically and MUST NOT be divided across panel boundaries.

Decorative rendering MUST NOT overwrite host-protected controls, caret, selection, menus, confirmations, or essential content.

## 6.2 Adaptive composition

ANSI/ASCII decoration SHOULD adapt semantically rather than merely stretching character arrays.

Supported adaptation techniques SHOULD include:

**Frame fitting / nine-slice** — corners retain identity while horizontal and vertical edge sections repeat or sample across the destination.

**Tiled motifs** — small reusable motifs repeat across expanding space.

**Procedural patterns** — hatching, grids, scanlines, dithering, noise, rails, connectors, particles, bands, or other deterministic patterns regenerate for available dimensions.

**Discrete responsive artwork** — themes MAY provide compact, normal, and expansive versions of complex mastheads or illustrations.

**Cropping/simplification** — nonessential ornament disappears progressively when space becomes constrained.

Decorative scaling MUST NOT expand beyond layout-approved decorative masks.

MDBM's theme grammar directly demonstrates frame fitting, patterns, motifs, masks, responsive variants, and protected host surfaces.

## 6.3 Responsive theme variants

Themes SHOULD support conditions including minimum/maximum width, minimum/maximum height where useful, colour depth, Unicode availability, ASCII-only mode, reduced motion, and high contrast.

A theme MUST provide practical narrow, ASCII, monochrome, and reduced-motion fallbacks if it relies materially on those capabilities.

At narrow sizes, decorative complexity SHOULD be reduced before structural UI is removed.

## 6.4 Layer model

A useful presentation stack is:

    background → decorative underlay → frame/pattern layers → content
    → protected interaction surfaces → overlays

Decorative layers MAY support replace, underlay, glyph-only, foreground-only, background-only, masks, transparency, and deterministic dithering.

Theme layers MUST be clipped and budgeted.

## 6.5 Animation

ANSI animation MUST remain bounded.

Spatial/shape animation MAY run at a configurable cadence up to approximately **30 FPS** where performance allows.

Potentially flash-like changes — particularly whole-style, major palette, or visibility transitions — SHOULD be restricted to approximately **2 transitions per second or less**.

Reduced-motion MUST disable nonessential animation. Motion-off MUST produce a stable deterministic frame.

Animation MUST never alter functional hit geometry unexpectedly.

MDBM uses the same distinction between bounded spatial/shape animation and stricter limits on style/palette/visibility transitions.

# 7. Accessibility and constrained environments

Accessibility settings override theme aesthetics.

The system MUST support, where applicable:

- high-contrast mode;
- reduced motion;
- motion off;
- ASCII-only rendering;
- monochrome rendering;
- keyboard-only operation;
- pointer-only command operation;
- visible focus state.

Text and important status information MUST NOT depend solely on colour.

Decorative glyph substitution MUST preserve meaning. Unsupported Unicode decoration MAY fall back to ASCII, but user content MUST remain intact.

GUI zoom or terminal resizing MUST trigger a complete geometry re-solve rather than assuming previous hit regions remain valid.

Extremely small viewports SHOULD enter compact/focused mode with an explicit indication that additional tiles remain available.

# 8. Configuration and persistence

Static preferences and dynamic session state MUST be distinct.

## 8.1 Configuration

Configuration SHOULD define defaults such as:

- initial tile visibility/order;
- split ratios;
- minimum dimensions;
- spacing/artspace limits;
- input profile;
- theme and theme search paths;
- colour capability override;
- Unicode/ASCII policy;
- mouse enablement;
- accessibility settings;
- animation level;
- performance limits.

Invalid individual values SHOULD fall back independently rather than invalidating unrelated valid settings.

Unknown or conflicting bindings SHOULD be diagnosed.

Hand-maintained configuration SHOULD NOT be silently rewritten merely because the interactive layout changed.

MDBM follows this separation: its manually maintained configuration remains read-only during normal operation while dynamic layout/session choices are persisted separately.

## 8.2 Session state

Session state SHOULD retain dynamic choices such as active workspace, tile visibility, tile placement, split ratios, active tile, per-tile scroll/navigation memory, committed theme, and optional workspace preset.

Session restoration MUST be bounded, validated, and recoverable.

A safe-start option SHOULD permit launching with default layout, safe theme, and session restoration disabled.

# 9. Rendering and implementation architecture

GUI and TUI front ends SHOULD share the same semantic state and layout model wherever practical.

Recommended architecture:

    state model → geometry solver → semantic scene/cell model → platform renderer

For a TUI, the final scene becomes terminal cells and ANSI/style operations.

For a GUI, the same scene MAY be rendered with native widgets, a retained-mode scene, or a cell-emulation canvas, provided semantic geometry and command behaviour remain equivalent.

The application SHOULD have one authoritative renderer per surface. Competing rendering systems must not independently manipulate the same terminal/window state.

The final rendered geometry MUST be the source of truth for hit testing.

Unchanged frames SHOULD produce zero logical damage.

Local changes such as moving a caret or toggling a control SHOULD NOT cause an unconditional full-screen redraw or terminal clear.

Rendering budgets SHOULD constrain decoded artwork size, layer count, generated cells, animation tracks, and repaint work per frame.

Background computation MUST publish results using generation/version identifiers so stale work cannot replace newer UI state.

MDBM's implementation provides a concrete example: normalized input and command state feed a geometry solver and host-owned cell compositor; the terminal backend then performs physical screen diffing.

# 10. Acceptance criteria

A release conforming to this specification SHOULD satisfy all of the following.

### Input parity

- Every keyboard command has at least one pointer route.
- Every meaningful pointer-only command has a keyboard route where technically meaningful.
- Clicking an unfocused actionable panel focuses and acts in one gesture.
- Divider capture, commit, Escape rollback, and focus-loss rollback work.
- Context menus preserve valid selections.
- Overlay dismissal cannot click through.
- Mouse wheel behaviour is tile-local.
- Menus remain inside the viewport.

### Tile/layout behaviour

- Tile state survives hide/show, swap, resize, maximize, and responsive collapse.
- Split ratios clamp correctly.
- Decorations shrink before usable content.
- Small viewports enter focused compact mode rather than unusable multi-panel mode.
- All-hidden or corrupted layouts retain an obvious recovery route.
- Workspace layout can be restored to defaults.

### Theme and ANSI behaviour

Test at minimum across representative geometries such as:

**40×12, 80×24, 120×40, 200×60**

and across:

**truecolour, ANSI-256, ANSI-16, monochrome, Unicode, ASCII, high contrast, reduced motion**

Adaptive frames MUST preserve corner identity and divider continuity when resized.

No theme may cover protected controls or change application semantics.

Invalid themes must leave the previous valid theme intact.

### Responsiveness

Measure composition time separately from actual **input-to-frame latency**.

Interactive performance targets SHOULD be expressed as percentile limits rather than best-case samples.

Unchanged frames MUST not generate unnecessary logical damage.

Resize, theme preview, animation, and rapid pointer movement MUST not create unbounded work queues.

### Native qualification

Automated tests SHOULD include command-registry parity checks, deterministic geometry tests, golden composed-cell tests, pointer hit-map tests, overlay/capture tests, theme fallback tests, resize stress tests, and GUI integration tests and/or real PTY terminal tests.

Manual qualification SHOULD include the actual supported GUI platforms and terminal emulators, particularly mouse press/release reports, divider dragging, focus loss during drag, double/triple click, wheel behaviour, terminal/window resizing, Unicode/CJK/wide-character boundaries, colour-depth fallbacks, reduced-motion behaviour, and crash/exit restoration.

Passing logical renderer tests alone MUST NOT be represented as proof of correct behaviour in native terminals or native GUI environments.

## Reference basis

This specification derives its core interaction and rendering principles from MDBM, inspected against **techrote/mdbm main at commit a826b4f6d3803b8ec88542cc0a9c4bd9138607ed**:

- https://github.com/techrote/mdbm/blob/main/README.md
- https://github.com/techrote/mdbm/blob/main/docs/MDBM_PRODUCT_SPEC.md
- https://github.com/techrote/mdbm/blob/main/docs/MDBM_TECHNICAL_DESIGN.md
- https://github.com/techrote/mdbm/blob/main/docs/CONFIG_FILE_SPEC.md
- https://github.com/techrote/mdbm/blob/main/docs/THEME_FILE_SPEC.md
- https://github.com/techrote/mdbm/blob/main/docs/TEST_AND_ACCEPTANCE_PLAN.md
- https://github.com/techrote/mdbm/blob/main/docs/IMPLEMENTATION_REPORT.md

The intended result is not an MDBM clone. It is a reusable UI contract preserving the strongest MDBM conventions: **semantic command parity, persistent tile workspaces, geometry-derived pointer interaction, transactional UX, data-only theming, capability-aware colour, and adaptive cell-native artwork.**
