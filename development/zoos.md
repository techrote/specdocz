# Zoos — spatial asset galleries and inspection environments

**Status:** Non-normative development reference; design guidance, not a tested implementation  
**Scope:** Asset discovery, comparative visual review, art direction and content smoke testing  
**Source:** Robin-Yann Storm, [talk](https://www.youtube.com/watch?v=5PJRCz0t7yY) and [written presentation, Chapter 2](https://rystorm.com/blog/gyms-zoos-museums-your-documentation-should-be-in-game).  
**Related:** [Development overview](README.md) · [Gyms](gyms.md) · [Museums](museums.md)

## Definition and purpose

A **Zoo** is an arranged, browsable collection of game assets instantiated in a shared spatial context. Instead of searching opaque filenames or relying on isolated thumbnails, users see a set of assets side by side, with meaningful scale, lighting, variation and usage context. Its primary questions are: *What do we have? Which variant fits? How large does it look? Does anything appear broken?*

Zoos can contain models, props, materials, VFX, animated characters, NPCs, audio emitters, item variants and other inspectable content. They can also contain **vignettes** showing assets used together in an intended composition.

**Boundary:** A Zoo primarily makes **content visible and discoverable**. A [Gym](gyms.md) tests **interactive mechanics**; a [Museum](museums.md) teaches **system behaviour** through runnable demonstrations. A Zoo can have interactive specimens without becoming a comprehensive gameplay test.

## Talk-derived design characteristics

Storm demonstrates the limitations of thumbnail browsers: they hide comparative scale, lighting-dependent appearance, detail and asset discoverability. He uses examples including Valve's `de_nuke` asset Zoo for Counter-Strike: Global Offensive, character/helmet comparisons, VFX displays and an automatic Zoo generator in AssetPlacer for Godot.

Important characteristics taken from the talk:

- **Group by useful context:** per folder, intended use, level, or art direction needs.
- **Compare under meaningful lighting:** include level lighting and time-of-day variations where relevant.
- **Make scale legible:** reference people, measurement textures or other consistent size markers.
- **Show intended composition:** place vignettes next to the raw collection for art-direction guidance.
- **Preserve discoverability:** visual selection should not depend on remembering an internal codename.
- **Exploit generation where possible:** automatically lay out asset families from an authoritative registry.
- **Support diagnostics:** obvious missing assets, shader failures, high shader complexity and overnight image comparisons can expose regressions.

## Suggested scene structure

*Implementation extension — proposed patterns that operationalise the presentation.*

| Area | Contents | Purpose |
| --- | --- | --- |
| Index / category map | Asset families, scene links, filters, specimen counts | Reach an appropriate Zoo without memorising file paths |
| Neutral comparison lane | Aligned specimens, fixed spacing, common scale person/ruler | Compare proportions, silhouette, materials and topology |
| Lighting lane | Same set under reference lighting, dusk/night or runtime conditions | Find lighting- or exposure-specific problems |
| Variant / animation lane | Skins, LODs, character body types, animation cycles | Inspect compatibility and visible differences together |
| Usage vignettes | Small composed scenes approved or reviewed by art direction | Communicate intended combinations and style |
| Diagnostics lane | Missing/shader-error placeholders, debug view modes and labels | Surface pipeline failures instead of silently hiding them |

Use stable specimen IDs, original asset paths and display names; optionally include tags, LOD, bounds, material version and provenance. Generated catalog entries should link back to the real asset, not duplicate or rename it.

## Construction and update pipeline

*Implementation extension.*

1. **Select a manifest:** query an authoritative content registry or explicit reviewed list; distinguish an exhaustive Zoo from a sampled/curated one.
2. **Generate repeatable positions:** sort by stable ID or category, maintain consistent scale and place a reference object in each area. Avoid layouts that reshuffle on every rebuild.
3. **Instantiate safely:** show clear error specimens for unloaded or invalid assets; bound animation, VFX, sound and memory cost.
4. **Attach metadata:** identify asset path, category, owner if known, variant, source revision, material/texture state and links to tickets or guidelines.
5. **Expose context changes:** allow camera preset, relevant lighting/environment settings and inspection modes. Keep settings visible in screenshots.
6. **Include curated vignettes:** capture art direction beyond raw enumeration, with provenance and update ownership.
7. **Regenerate and audit:** compare expected specimen count with instantiated count; detect missing assets, duplicates, unexpected material overrides and unreviewed additions.

### Proposed specimen metadata example

~~~yaml
specimen_id: zoo.props.door.metal.01
source_asset: <canonical-project-asset-path>
collection: environment/doors
variant: <project-variant-id>
scene_revision: <exact-project-revision>
display_modes: [neutral, night, shader_complexity]
status: <loaded-or-explicit-error>
note: <intended-use-or-known-limitation>
~~~

This is an optional integration pattern, **not** an asset manifest standard defined in the talk.

## Visual regression and diagnostics

The presentation suggests overnight screenshots and image comparisons, with escalation when assets unexpectedly change. A useful pipeline can implement:

- **Inventory checks:** assert expected category membership, number of specimens, unique IDs and successful asset loading.
- **Reference captures:** use recorded camera poses, lighting, time, resolution, graphics settings, build and GPU/renderer information.
- **Difference triage:** compare against a version-matched baseline; flag changed regions and keep both images. Treat pixel-change counts as **diagnostic signals**, not automatic proof of a defect.
- **Debug views:** inspect shader complexity, material errors, absent meshes, LOD issues and scale anomalies.
- **Human review:** separate deliberate art changes and renderer/platform noise from genuine content breakage.

Pixel-perfect comparisons across graphics APIs, drivers, temporal rendering and platforms may be unstable. Calibrate tolerances, normalise captures where possible and log environment details. A Zoo screenshot cannot prove an asset's collision, gameplay or authoring correctness.

## Practical adoption scenarios

- **Prop collection:** a layout of wall sections, doors and cables with standard scale and a sample corridor composition.
- **Character customisation:** body-type × clothing/helmet matrix to make clipping and fit problems visible.
- **VFX/audio review:** simultaneous or selectively triggered emitters with labels and controlled playback, to compare appearance and sound without navigating individual preview windows.
- **Generated asset Zoo:** one command builds a scene from a selected folder/group for immediate discovery and QA.

A hybrid **Zoo + Gym** can let users pick up each item and test it instantly, as illustrated by the practice-range discussion in the talk. Keep the visual inventory and behavioural test results distinguishable.

## Failure modes and acceptance checklist

Avoid arbitrary scales, incompatible lighting, missing labels, stale manual layouts, excessive simultaneous VFX/audio, hidden broken assets and misleading unsorted visual diffs. Do not treat every asset as safe to instantiate in a shared scene without resource budgets.

Before adopting the pattern, check that a new team member can enter the Zoo, find an asset without knowing its codename, compare real-world size and variants, inspect expected lighting, identify source files, see broken specimens instead of omissions, and regenerate or refresh the display without losing deliberate art-direction vignettes. Record exact renderer/build for any automated visual regression claim.

Apply **Adopt / Adapt / Reject / Extend** against the consuming project's content pipeline; pin the source `specdocz` commit.

## Sources and attribution

- **Primary concept:** Robin-Yann Storm, [*Gyms, Zoos, and Museums: Your documentation should be in-game* — video](https://www.youtube.com/watch?v=5PJRCz0t7yY).
- **Author's accessible exposition:** [Chapter 2: Zoo](https://rystorm.com/blog/gyms-zoos-museums-your-documentation-should-be-in-game), including Valve, animation, VFX, asset-generation and visual comparison examples.
- **Engineering extensions:** proposed metadata, generation pipeline, triage rules and acceptance checklist are synthesis, **not** claimed verbatim author requirements.
