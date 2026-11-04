# Gyms — playable mechanics and metrics test spaces

**Status:** Non-normative development reference; design guidance, not a tested implementation  
**Scope:** Gameplay, locomotion, interactions and character/mechanic qualification  
**Source:** Robin-Yann Storm, [talk](https://www.youtube.com/watch?v=5PJRCz0t7yY) and [written presentation, Chapter 1](https://rystorm.com/blog/gyms-zoos-museums-your-documentation-should-be-in-game).  
**Related:** [Development overview](README.md) · [Zoos](zoos.md) · [Museums](museums.md)

## Definition and purpose

A **Gym** is a deliberately constructed, easy-to-enter playable environment in which developers can *try*, *measure* and *understand* a game mechanic. It is a working reference for what a controller or ability does **in the current build**, not merely a chart claiming what it ought to do.

The talk emphasises character controllers, movement and animation. Typical questions are: How far can this character jump? What slope can they ascend? Which ledges can they grab? How does cover work? How does an ability affect a target? A useful Gym makes the answer quickly observable through controlled examples rather than a search through stale prose.

**Boundary:** A Gym foregrounds **interaction and behavioural limits**. A [Zoo](zoos.md) foregrounds **finding and comparing assets**; a [Museum](museums.md) foregrounds **explaining a system through curated demonstrations**. The same scene may combine them, but the interaction contract should remain clear.

## Talk-derived design characteristics

Storm illustrates measurement obstacles and interaction areas, including jump gaps with **easy / difficult-but-possible / beyond-range** indications, metre references, edge climbing, vaults, cover and traversal. The Unreal Game Animation Sample and an Overwatch practice range are discussed as examples. The talk recommends:

- Coverage of major character–environment interactions.
- Readable metric descriptions directly beside the relevant geometry or targets.
- Both text and colour cues for different results or difficulty classes.
- Teleportation or similarly convenient movement between test areas.
- Reusable smoke-test routes; a character getting stuck should be reproducible at a known location.

The exact measurements and categories must come from the consuming game's own mechanics. **The presentation is not a source of universal jump distances, slopes or damage values.**

## Suggested layout and exhibits

*Implementation extension — a practical proposed starting design, not a mandated layout from the talk.*

| Station | Fixture | What it makes observable |
| --- | --- | --- |
| Entry / control desk | Character selection, active build/config, reset and travel map | Which controller and rules are under test |
| Scale and locomotion | Unit grid, distances, timed run and stop lines | Speed, acceleration, collision dimensions and stopping behaviour |
| Jump and traversal | Increasing gaps and heights, marked reachability classes | Reachable limits, mantling, vaults and transitions |
| Surface interactions | Graded slopes, stairs, steps, slippery surfaces, moving platforms | Grounding, friction, slope handling and edge cases |
| Cover and obstruction | Straight/curved cover, crouch spaces, doors, corners | Cover acquisition, clearances, collision and visibility |
| Combat or ability bay | Target types, recoverable consumables and resettable enemies | Attack range, impact, cooldown, resource use and response |
| Regression loop | Short scripted or repeatable traversal through key fixtures | Stalls, input regressions and cross-build change detection |

Keep sections small enough to diagnose. Use visible units and labels (not colour alone); show expected behaviour and current observed limits separately. Include **deliberately unsuccessful** examples, not just ideal cases, with a reason they are not supported.

## Build and operating workflow

*Implementation extension.*

1. **Declare the test subject.** Record character/controller identifier, settings profile, game build and applicable platform. Prefer the real controller and production collision logic over a simplified copy.
2. **Create stable fixtures.** Give each station a durable ID and a self-contained reset path. Parameterise geometry from actual game units; make scene changes reviewable.
3. **Make the observation local.** Put scale, permitted actions, measured outputs and controls at the station. Show effective values when a runtime limit differs from a requested setting.
4. **Minimise setup cost.** A fresh user should be able to launch the Gym, select a test, reset it and return to the hub without hidden console commands.
5. **Exercise expected and edge behaviour.** Include safe/unsafe or reachable/unreachable cases, multiple relevant controller modes, and known regressions.
6. **Record results.** For failures, capture station ID, build/commit, controller configuration, input trace or reproduction steps, expected/observed outcomes and, when helpful, a screenshot/video.
7. **Reconcile after changes.** When physics, animations, abilities or movement tuning change, refresh the relevant station and any project-authoritative written requirements.

### Example fixture record

~~~yaml
id: gym.jump.horizontal.03
purpose: Demonstrate the marginally reachable horizontal jump
controller: <project-controller-id>
units: project_world_units
environment: <scene-and-fixture-revision>
inputs: <recorded-or-repeatable-input-sequence>
expected: <project-approved-behaviour>
observed: <measured-result-and-build-id>
reset: <in-scene-reset-action>
~~~

This is an illustrative metadata shape, **not** a source-defined schema. Avoid hard-coding example distances as if they were proven engine limits.

## Qualification and automation

Storm explicitly proposes running a character through a Gym as a smoke test to detect traversal failures. A responsible implementation can layer these checks:

| Layer | Suggested check | Interpretation |
| --- | --- | --- |
| Human exploration | Play each major interaction; read cues and compare outcomes | Usability and visible behaviour |
| Deterministic fixture test | Reset, apply recorded inputs, inspect collision/position/ability state | Regression evidence at a specified build/config |
| Scripted traversal | Complete bounded route; detect timeouts, stuck states or invalid transitions | Fast build health indication |
| Cross-configuration test | Repeat with supported speeds, controller modes and platforms | Reveals configuration-specific failures |
| Performance observation | Record frame/tick cost and unusual allocations | Diagnostic signal; not proof of all performance targets |

A completed Gym run is **not** proof of universal physics determinism, multiplayer correctness, accessibility or shipping quality. Confirm requirements in the consuming project and qualify on supported platforms.

## Failure modes to avoid

- **Stale stand-in controllers:** a visually convincing Gym running different code from production may mislead.
- **Invisible assumptions:** unnamed units, character scales or settings make measurements untransferable.
- **Colour-only signals:** a red/green gap scheme without readable labels or patterned cues excludes some users.
- **Happy-path-only design:** unreachable cases and boundary transitions are where many bugs emerge.
- **Uncontrolled automation:** variable spawn state or unreset physics can make false regressions.
- **Replacing the design contract:** current observed ability is evidence; it does not silently redefine an approved target.

## Review and adoption checklist

A proposed Gym is useful when a new team member can launch it from a clean checkout, identify the active build/controller, locate and exercise each major interaction, read units and outcomes, reset the examples, reproduce a known failure at a fixture ID, and locate associated authoritative specifications or tickets. Automated pass/fail claims must name their exact test inputs and environments.

Before adopting, use **Adopt / Adapt / Reject / Extend** with project-specific reasoning, and pin the source `specdocz` revision.

## Sources and attribution

- **Primary concept:** Robin-Yann Storm, [*Gyms, Zoos, and Museums: Your documentation should be in-game* — video](https://www.youtube.com/watch?v=5PJRCz0t7yY).
- **Author's accessible exposition:** [Chapter 1: Gym](https://rystorm.com/blog/gyms-zoos-museums-your-documentation-should-be-in-game), with game and workflow examples.
- **Engineering extensions in this document:** station table, fixture metadata, qualification layers and checklist are proposed synthesis, **not** verbatim claims from the author.
