# Museums — functional system demonstrations with in-context explanations

**Status:** Non-normative development reference; design guidance, not a tested implementation  
**Scope:** Engine/technology demonstrations, onboarding, tooling, modding and system-debugging workflows  
**Source:** Robin-Yann Storm, [talk](https://www.youtube.com/watch?v=5PJRCz0t7yY) and [written presentation, Chapter 3](https://rystorm.com/blog/gyms-zoos-museums-your-documentation-should-be-in-game).  
**Related:** [Development overview](README.md) · [Gyms](gyms.md) · [Zoos](zoos.md)

## Definition and purpose

A **Museum** is a navigable collection of **working, explained examples** of a game or engine system. Each exhibit demonstrates how a capability behaves, includes enough context to interpret the result, and points to deeper technical documentation when needed. The central question is: *How does this system work, and how should I use or avoid using it?*

Museums are especially appropriate for rendering/shaders, physics, cloth, reusable prefabs, scripting and content-creation conventions. They can serve internal contributors or external modders. Unlike a static wiki gallery, an exhibit is generally functional: users can play it, change a controlled input, see the consequence and understand it.

**Boundary:** A [Gym](gyms.md) is a hands-on **mechanic limit and interaction** space; a [Zoo](zoos.md) is an **asset comparison** space; a Museum primarily **communicates a system's intended operation and constraints**. A single scene can incorporate all three, but a Museum exhibit requires explanatory context.

## Talk-derived design characteristics

Storm discusses Unreal's cloth sample, Chaos Destruction demonstrations and the public Mod Museum in *Skin Deep*. These show how an in-engine scene can make complex behaviours understandable without requiring a user to read a long document before seeing anything.

A Museum, as summarised by the speaker, should:

- Functionally demonstrate the system in real time.
- Include concise explanatory text next to the relevant phenomenon.
- Link to deeper technical documentation or API details.

The talk also illustrates a **hub** that routes visitors to focused demonstration levels, explicit examples of *what not to build*, dimensional guidance, and scripting examples whose live results correspond to the shown sequence. Markers, commentary nodes, and readable constraints put explanation alongside the actual system.

## Suggested exhibit anatomy

*Implementation extension — an engineering proposal, not a source-defined schema.*

Each exhibit can be treated as a small, runnable lesson with:

| Element | Purpose |
| --- | --- |
| Identity and scope | Stable exhibit ID, system/version, maintainer and intended audience |
| Question / expected result | Short statement of the behaviour being demonstrated |
| Live specimen | Real physics, renderer, script, tool or prefab behaviour, not a prerecorded substitute |
| Controlled interaction | Reset, play/pause, safe parameter preset or one clear trigger |
| In-context explanation | Units, configuration, constraints, expected/observed differences and accessibility cues |
| Positive and negative cases | Supported usage and deliberately invalid or discouraged usage with rationale |
| Deep link | API reference, technical specification, source location, issue or approved workflow |
| Diagnostic capture | Build/config, screenshot/log/trace and link for reproducible defects |

For a complex system, prefer multiple small exhibits over a single ambiguous spectacle. If a negative example is hazardous or expensive, show a safe simulation or controlled refusal rather than triggering an uncontrolled failure.

## Illustrative museum wings

*Examples are based on source categories; exact exhibit layouts below are proposed.*

| Wing | Possible exhibit | What the visitor learns |
| --- | --- | --- |
| Cloth / animation | Anchored cloth, wind variation and collision cases | How constraints and simulation settings change deformation |
| Destruction / physics | Supported fracture and contact sequences with reset | Which rigid-body behaviours and coupling rules are expected |
| Rendering and materials | Lighting, shader mode, shadows and diagnostic views | Capabilities, trade-offs and visual failure modes |
| Scripting / event flow | A small sequence showing state/steps and matching live output | Execution order, waits, triggers and side effects |
| Prefabs / placement rules | Valid and invalid placement/configuration examples | Integration constraints, scale and forbidden patterns |
| Modding / UGC | Authoring and runtime samples reached from one hub | Safe extension points and observable usage contracts |

In the talk, the *Skin Deep* Mod Museum demonstrates developer guidance on dimensions and interactions, including prohibited constructions; this is an example of **demonstrating constraints**, not a universal set of game-design limits.

## Design and maintenance workflow

*Implementation extension.*

1. **Choose the audience and questions.** Prioritise high-friction system concepts and repeated onboarding questions.
2. **Map the visitor path.** Provide one discoverable entrance or index, category navigation, fast travel, and clear return controls; no special editor command should be needed merely to find a demo.
3. **Bind the real system.** Prefer production code, live engine effects and version-matched assets over hand-animated stand-ins.
4. **Present one interpretable variable at a time.** Show units and currently selected options; label expected behaviour separately from observations and known bugs.
5. **Attach depth without burying the demonstration.** Keep labels short; link to authoritative APIs, constraints, detailed specs and issue records.
6. **Document boundaries.** Include supported patterns, contraindications and reasons, including counterexamples where safe.
7. **Offer replay and reset.** Re-running a scripted/physical exhibit should not require reloading the entire project unless that is intentional.
8. **Track drift.** When a system changes, review affected exhibits, expected outcomes and linked documentation in the same change process.

### Proposed exhibit manifest fragment

~~~yaml
exhibit_id: museum.physics.contact.01
question: <specific-physics-question>
source_system: <canonical-module-or-component>
tested_revision: <exact-project-commit>
configuration: <named-preset>
interaction: <trigger-and-reset>
expected: <approved-observable-result>
documentation: <project-api-or-design-link>
limitations: <known-platform-or-mode-constraints>
~~~

This is illustrative metadata; it is not an official format from the talk.

## Verification and evidence limits

A Museum gives users a **functional explanation**, which is valuable but should not be confused with a full test suite or an approval gate. Consider three complementary checks:

- **Exhibit health:** loads from a clean environment; navigation, labels, controls, links and reset all work.
- **Behavioural evidence:** the scenario produces the described outcome on an identified engine/build/configuration; record negative cases and failure conditions.
- **Document consistency:** linked API and design contracts are current, and any divergence between observed and intended behaviour is visible.

For physics, rendering and timing-sensitive examples, capture relevant seed, fixed/variable timestep, platform, GPU/driver and runtime mode. A green scripted demo in one environment does not establish portability or scientific reproducibility. Add dedicated tests where correctness matters.

## Failure modes and acceptance checklist

Avoid a static screenshot hall marketed as a functional Museum; unlabeled spectacle; too many unrelated behaviours in one exhibit; documentation links that silently rot; missing reset; showing accidental engine behaviour as if it were an approved standard; or hiding constraints that the user most needs to understand.

A useful Museum lets a newcomer open the hub, choose a system without knowing internal filenames, operate a working example, see what should happen and why, explore at least one important boundary/anti-pattern, reach deeper documentation, and reproduce a reported failure with its exhibit ID and build/config.

Apply **Adopt / Adapt / Reject / Extend** to project needs and pin the referenced `specdocz` commit. If a team wants to elevate a Museum's demonstrated behaviour into a normative requirement, write that requirement and its acceptance test in the consuming project.

## Sources and attribution

- **Primary concept:** Robin-Yann Storm, [*Gyms, Zoos, and Museums: Your documentation should be in-game* — video](https://www.youtube.com/watch?v=5PJRCz0t7yY).
- **Author's accessible exposition:** [Chapter 3: Museum](https://rystorm.com/blog/gyms-zoos-museums-your-documentation-should-be-in-game), including Unreal demos and the *Skin Deep* Mod Museum.
- **Engineering extensions:** exhibit metadata, organisation, qualification distinctions and checklist are proposed synthesis, **not** asserted requirements by the speaker.
