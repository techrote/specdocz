# Development workflow references

**Status:** Non-normative, engine-independent implementation references  
**Updated:** 2026-11-04  
**Source:** Robin-Yann Storm, [*Gyms, Zoos, and Museums: Your documentation should be in-game*](https://www.youtube.com/watch?v=5PJRCz0t7yY); [author's written version](https://rystorm.com/blog/gyms-zoos-museums-your-documentation-should-be-in-game).

This folder describes ways to put useful documentation **inside the working game or editor**, near the objects and behaviour it explains. The three patterns are complementary, not interchangeable. These documents synthesise the source talk and offer explicitly marked implementation guidance; they do **not** establish universal requirements for games or for other repositories.

## Choose the right pattern

| Pattern | Primary question | The user actually does | Typical content |
| --- | --- | --- | --- |
| [Gym](gyms.md) | *What can the character or mechanic do?* | Plays, moves, interacts, measures, repeats | Movement distances, slopes, jumps, cover, abilities, enemy behaviours |
| [Zoo](zoos.md) | *What assets exist, what are they like, and which should I use?* | Browses and compares many specimens at once | Meshes, props, materials, VFX, animations, audio, NPCs |
| [Museum](museums.md) | *How does this technology or system work?* | Observes and operates explanatory demonstrations | Cloth, physics, lighting, scripting, tools, modding and engine systems |

**Selection rule:** Choose by the primary question, not by the room name. A collection of static materials is a Zoo even if called a “test map”; a working physics demonstration with explanatory annotations is a Museum. A firing range that lets users test weapons and movement is a Gym. One environment may deliberately contain more than one pattern.

## Shared principles

- **Work in context.** A live scene can answer spatial and behavioural questions faster than searching detached documents. The scene should stay connected to the actual game data or system under discussion.
- **Make navigation cheap.** Provide a discoverable entry point, categories, signage, fast travel or equivalent selection controls, and a way back to the starting point.
- **Pair visual and textual information.** Colour is useful but not sufficient; show names, units, expected results, accessible text, and links to source/API documentation where needed.
- **Show provenance.** Distinguish observed runtime behaviour, desired design, current limitations and known failures. A useful demonstration is not automatically a normative specification or proof of correctness.
- **Maintain by use.** Integrate scenes into content and test workflows; prefer generation from authoritative assets, reusable fixtures and automated smoke checks where feasible.
- **Keep project authority explicit.** A consuming project must review, tailor, pin the `specdocz` commit and write its own applicable contracts and tests. These references are **advisory**.

## Shared implementation extensions

The following are **proposed engineering practices**, not requirements attributed to Storm's talk:

1. Give each exhibit or test a stable identifier, purpose, owner, source asset/system reference and last-verified build or revision.
2. Provide a cold-start path: documented scene name, launch procedure, reset action and minimal dependencies.
3. Separate a clear **expected/observed** display from a pass/fail assertion; human-readable showcases do not replace regression suites.
4. Capture screenshots, logs and issue links with scene coordinates or specimen IDs to keep bug reports actionable.
5. Include accessibility and performance considerations: non-colour labels, readable scale, controllable motion/audio and bounded scene load.
6. When a scene changes, update linked design/API documents if they are themselves the authoritative contract.

## Boundaries and source fidelity

Storm's talk argues for spatial, contextual in-engine documentation, while still retaining written documentation where it is appropriate (especially technical API references). It gives examples from Unreal, Valve games, Overwatch, Skin Deep, and tooling for Godot and Unity. This folder is an **original summary and engineering interpretation**, not a transcript or an implementation already qualified in a target engine.

- [Source video](https://www.youtube.com/watch?v=5PJRCz0t7yY)
- [Author's written presentation](https://rystorm.com/blog/gyms-zoos-museums-your-documentation-should-be-in-game)
- [GodotFest talk listing](https://godotfest.com/talks/gyms-zoos-and-museums-your-documentation-should-be-in-game/)
- [Repository overview](../README.md)

Use [Gym](gyms.md), [Zoo](zoos.md), or [Museum](museums.md) individually when briefing an implementation agent; do not infer requirements for the other two without a project need.
