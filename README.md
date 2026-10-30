# specdocz

**Reusable software-design standards, implementation patterns, and research references for project teams and development agents.**

`specdocz` is organised **by subject**; document authority is explicit rather than inferred from its folder. Normative specifications establish reusable requirements, implementation libraries offer candidate patterns, and research records evidence and uncertainty. Consuming projects should develop their own self-contained contracts and pin the source revision used.

## Browse the repository

| Subject | Location | What you'll find |
| --- | --- | --- |
| **User interfaces** | [uiuxs/](uiuxs/) | GUI/TUI design, cell-grid editing, and expert parameter-control specifications |
| **Game types** | [gametypes/](gametypes/) | Game-play modes, mechanics, and related design research |
| **Research registry** | [research/](research/) | Study catalog, authoring template, evidence quality and promotion rules |

### UI/UX specification families

| Family | Purpose | Read first |
| --- | --- | --- |
| [cohesive-techspression](uiuxs/cohesive-techspression/) | Layered workspaces, task-adjacent expert controls and broad semantic intent/feel macros | [UI/UX baseline](uiuxs/cohesive-techspression/cohesive-techspression-uiux-spec.md) · [tailoring](uiuxs/cohesive-techspression/cohesive-techspression-spec-tailoring.md) |
| [mzpaint](uiuxs/mzpaint/) | Precision/scientific and expressive/artistic glyph and cell-grid editing | [UI/UX baseline](uiuxs/mzpaint/mzpaint-uiux-spec.md) · [tailoring](uiuxs/mzpaint/mzpaint-spec-tailoring.md) |
| [parametermaxing](uiuxs/parametermaxing/) | Dense expert controls, numerical ranges, presets, safety bounds and inspectability | [UI/UX baseline](uiuxs/parametermaxing/parametermaxing-uiux-spec.md) · [tailoring](uiuxs/parametermaxing/parametermaxing-spec-tailoring.md) |
| [tuiuiux](uiuxs/tuiuiux/) | Tile-native GUI and terminal UI requirements and implementation patterns | [UI/UX baseline](uiuxs/tuiuiux/tile-native-gui-tui-uiux-spec.md) · [tailoring](uiuxs/tuiuiux/tile-native-gui-tui-spec-tailoring.md) |

Each family distinguishes standalone normative baselines, advisory implementation approaches, reference-backed variants and project-tailoring procedures. The original source project's architecture is **not** automatically mandatory elsewhere.

### Game types and research

| Collection | Focus | Primary documents |
| --- | --- | --- |
| [zeroplayerlevel](gametypes/zeroplayerlevel/) | Self-running levels, Auto-Mario, DDA/PN/PF terminology, physics choreography, replay and determinism | [Metastudy](gametypes/zeroplayerlevel/metastudy.md) · [patterns](gametypes/zeroplayerlevel/patterns.md) · [sources](gametypes/zeroplayerlevel/sources.md) |

The zero-player metastudy is a **non-normative narrative evidence synthesis**, not a tested engine implementation or a universal design requirement. Find registered research by topic using [research/catalog.yaml](research/catalog.yaml).

## For development agents

1. **Audit the active repository.** Read its own requirements, architecture, constraints, tests, CI and active task ownership.
2. **Select relevant references.** Start with a subject README, then the normative baseline or research chapters that match the job; do not load unrelated documents.
3. **Pin provenance.** Record the exact `specdocz` **commit SHA**, complete file paths, study IDs/versions and source identifiers. Treat later upstream changes as explicit deltas.
4. **Tailor deliberately.** Classify applicable techniques as **Adopt / Adapt / Reject / Extend** with reasoning, edge cases, limitations and deviations.
5. **Write a self-contained project contract.** Put adopted requirements and acceptance tests in the consuming project's own repository; do not make it dependent on a live `specdocz/main`.
6. **Qualify the actual implementation.** Source-matched tests, platform checks and human/scientific gates must be satisfied where applicable; passing documentation checks is not evidence of runtime correctness.

## Authority and evidence

```text
project safety / functional / scientific / compatibility requirements
    ↓
project-specific authoritative specification and acceptance tests
    ↓
applicable reusable normative UI/UX or engineering baseline
    ↓
explicitly adopted/adapted implementation patterns
    ↓
non-normative research, historical precedents, examples and hypotheses
```

**Location does not confer authority.** Check each document's status and normative language. Research claims and engineering proposals remain distinct from requirements until reviewed and intentionally promoted. See [research/CONTRIBUTING.md](research/CONTRIBUTING.md).

## Layout, validation and path changes

```text
specdocz/
  uiuxs/
    cohesive-techspression/
    mzpaint/
    parametermaxing/
    tuiuiux/
  gametypes/
    zeroplayerlevel/
  research/
    catalog.yaml        # study IDs and repository-root-relative paths
    _templates/
    CONTRIBUTING.md
  scripts/
    validate_research.py
```

Run `python scripts/validate_research.py` (Python standard library only). GitHub Actions performs structural checks for catalog entries, local links and zero-player source/pattern index consistency; it cannot independently verify scholarly claims or simulation determinism.

**Moved paths (30 October 2026):** `mzpaint/`, `parametermaxing/` and `tuiuiux/` are now under `uiuxs/`. `research/zero-player-level-design/` is now `gametypes/zeroplayerlevel/`. Update external references accordingly: GitHub may not redirect old document URLs. Previously pinned commit URLs remain historical references.
