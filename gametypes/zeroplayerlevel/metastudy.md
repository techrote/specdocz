---
title: "Zero-Player Level Design: Research Synthesis and Agentic Engineering Reference"
subtitle: "Auto-Mario, Don't Do Anything, Don't Move, Press Nothing, Press Forward, and physics-authored spectacle"
document_type: "structured narrative metastudy / implementation reference"
version: "1.0"
research_cutoff: "2026-10-30"
status: "research synthesis; proposed engineering practices are not implemented or experimentally validated here"
primary_terms:
  - zero-player level design
  - auto-play level
  - Automatic Mario / Auto-Mario
  - Don't Do Anything (DDA)
  - Don't Move
  - Press Nothing (PN)
related_terms:
  - Press Forward (PF)
  - Keep Right
  - physics choreography
  - Rube Goldberg machine
  - music level
  - kinetic narrative
intended_audience: ["game-engine developers", "level-editor designers", "agentic coding assistants", "QA engineers", "researchers"]
---

# Zero-Player Level Design — Metastudy and Agentic Development Reference

**Research date:** 30 October 2026  
**Document class:** Structured narrative literature synthesis, NOT a statistical meta-analysis.  
**Central design principle:** The stage, its objects, and its simulated physics *perform* the run; the viewer does not steer an actor. The apparent simplicity of observation hides extensive labor in staging, timing, and simulation qualification.  
**Reading convention:** `[Sxx]` references the URL-indexed source register in §12. **[E]** denotes empirical/documented evidence; **[I]** an explicit synthesis/inference; **[R]** a proposed engineering recommendation. No recommendation is presented as a proven finding.

## Contents

1. **Definition and boundary** — Establish the exact input contract and exclude superficially similar features.
2. **Method, sources, and evidence quality** — Record how this synthesis was assembled and what the evidence does not prove.
3. **Terminology and historical development** — Map the relevant community labels and their chronology.
4. **Comparative game case studies** — Connect each editor ecosystem to its distinct form of automatic play.
5. **Cross-source findings** — Extract the recurrent design, audience, and tooling principles.
6. **Mechanics and creative pattern library** — Describe composable, physics-led devices for editors and authors.
7. **Implementation architecture for agentic teams** — Translate research into clear interfaces, invariants, and authoring tools.
8. **Determinism, portability, and QA** — Specify evidence needed before declaring an authored run repeatable.
9. **Generation and optimization research** — Apply procedural-generation literature without overclaiming.
10. **Reference demonstration suite** — Provide small qualifying levels and concrete acceptance gates.
11. **Agent task contract and decision record** — Define a safe, evidence-producing development workflow.
12. **Annotated source register and research gaps** — Preserve source provenance, relative strength, and unanswered questions.

---

## 1. Definition and boundary

### 1.1 Canonical definition

A **zero-player level** is a designed simulation environment in which, after an explicit start, the intended spectacle and/or completion progresses with **no gameplay control inputs from the viewer**. Progress is produced by ordinary game mechanisms—gravity, springs, collision, forces, moving surfaces, fluid flow, triggers, and interacting game objects—rather than by a human steering the character through the sequence. Robert Yang describes this broad family as *zero-player level design* [S01, S02]; developer Metanet specifically calls its `N` variant *Don't Do Anything* [S04].

A zero-player experience may be fully deterministic, seeded-and-variable, or deliberately stochastic. **The historical genre includes all three; reliable replay is a separate quality property, not a definitional prerequisite.** For a publishable, reproducible engine demonstration, determinism or well-characterized bounded variability is recommended [R].

### 1.2 Input contract: distinguish the categories

| Label | Exact viewer action during the run | Canonical examples | In scope? |
|---|---|---|---|
| **Zero input / PN / DDA / Don't Move** | No actor steering, jump, action, or sustained button | `N` DDAs, `Happy Wheels` Don't Move, Mario Auto, TrackMania PN | **Core** |
| **Constant input / PF / Keep Right** | One continuous, invariant input; no corrections | TrackMania Press Forward, Mario Keep Runs | **Adjacent; model separately** |
| **Triggered automatic** | One discrete initiation (e.g., press start, release a ball), then no inputs | Rube Goldberg / one-shot physics levels | **Core after trigger; disclose it** |
| **Self-running kinetic sandbox** | No controllable avatar; physics objects become subjects | Line Rider ride, automatic contraptions, sand-and-rigid-body display | **Core for demonstration mode** |
| **Auto-scroll** | Camera moves automatically, but avatar still requires control | A typical auto-scrolling Mario level | **Not sufficient** [S19] |
| **Tool-assisted playback / prerecorded trajectory** | Input script or animation is played back rather than environment causing motion | TAS, cutscene, fake zero-player demo | **Different technique** |
| **Idle/incremental game / zero-player game broadly** | Systems advance without input, often via resource progression | Idle economies, unattended games | **Broader category; not equivalent** |

**Hard distinction:** A simulation can advance *without an avatar* and still be a valid physics-led zero-player exhibit; conversely, simply removing the controller from a normal playable map does **not** make the map self-advancing. Similarly, PF is not literally zero-input; it is a closely related low-agency sibling [S01, S05].

### 1.3 Fundamental invariants for an implementation [R]

- `actor_control_input = neutral` for the whole demonstration (after any disclosed start event).
- Environment state progresses through the same authoritative simulation used for normal play.
- If an avatar exists, its motion follows collisions, forces, and game rules; no hidden per-frame positional puppeteering should masquerade as physics.
- Camera controls, pause, restart, single-step, time scaling, editor painting, and **spawning physics objects** remain available when enabled by the host application. These are **observation/authoring controls**, not avatar-control inputs.
- Intervention can legitimately alter or break an authored route; provide an explicit pristine restart and mark the run as modified.

---

## 2. Method, sources, and evidence quality

### 2.1 Review question

How have player-designer communities constructed zero-input, physics-driven levels, what functions do these levels serve, and what engineering principles can modern browser/native simulation engines and AI coding agents extract?

### 2.2 Search and screening procedure

A targeted, non-exhaustive web literature search was conducted on **30 October 2026** using terms including `zero player level design`, `Automatic Mario`, `don't move level Happy Wheels`, `N DDA`, `TrackMania press nothing`, `press forward track`, `Geometry Dash Auto`, `Line Rider track physics music`, `autoplay level genetic algorithm`, and `deterministic physics engine replay`. Sources were screened for (a) direct relevance to player-authored levels, (b) specificity about *how the run is propelled*, (c) identifiable author/developer or institution, and (d) utility for implementations or QA.

**Evidence classes:**

- **A — direct / primary:** statements from game creators, engine maintainers, artists documenting their own work, and first-party manuals [S04, S10, S13, S16–S19].
- **B — research:** peer-reviewed scholarship, scholarly books and graduate thesis work [S01, S03, S14, S15]. These have different methods and are not interchangeable.
- **C — contemporary reporting / practitioner analysis:** journalism and editor observations [S05, S06, S07, S08, S11].
- **D — community documentation:** wikis and community recollections, useful for terminology and examples but not authoritative for broad quantitative or cross-platform guarantees [S09, S12].

A source can have primary provenance yet still offer *interpretation* rather than controlled experimental proof. In particular, the Happy Wheels platform-divergence report is a community observation [S09], not a controlled cross-device study.

### 2.3 Scope and methodological limitations

This is a **structured narrative metastudy**, not a PRISMA systematic review and not a statistical meta-analysis. There is no meaningful common effect size across these mixed qualitative, historical, and engineering sources. No original gameplay experiments, interviews, independent level replays, device matrix, or reproducibility trials were performed for this document. The quantitative figures from [S07], [S14], and [S15] belong to their respective study designs; **do not pool them** or extrapolate them into an industry-wide success rate.

Some historical community material is archived or wiki-maintained; live page accessibility can change. The source list preserves direct canonical URLs, identifiers, and source-specific limitations where known. The research does **not** assert that a link's original interactive level remains playable today.

---

## 3. Terminology and historical development

| Era | Ecosystem / event | Community terminology | Significance | Evidence |
|---|---|---|---|---|
| **2004 onward** | `N` by Metanet Software, with built-in editor | **DDA — Don't Do Anything** | Community used launch pads, moving hazards and collision chains to transport a ninja without control; Metanet later explicitly credited this invention. | [S04]; historical recollection [S20] |
| **2006 onward** | `Line Rider`, browser drawing/sled simulation | Tracks, rides, animations | The drawn world becomes a physics performance; the rider's path can support spectacle, music synchronization and long-form artworks. | [S10, S13] |
| **2007–2008** | `Super Mario World` custom levels and online remix culture | **Automatic Mario / 自動マリオ** | Levels are built to complete with little/no control; sound-producing collisions can be composed into musical performances. | [S02, S21] |
| **2008–2010s** | `TrackMania Nations Forever` and descendants | **PF — Press Forward; PN — Press Nothing** | Elaborate stunt/rube-goldberg tracks use a constant input or, more rarely, no input with boost pads. | [S01, S05] |
| **2010 onward** | Browser `Happy Wheels` editor | **Don't Move** | Springs, fans, hazards, and propulsion gadgets carry the character; community records sensitivity to device/platform differences. | [S08, S09] |
| **2013 onward** | `Geometry Dash` user levels | **Auto** | Auto becomes a recognizable difficulty and searchable level category; visual, musical, and trigger showcases. | [S11, S12] |
| **2015 onward** | `Super Mario Maker` | **Auto-Mario, Automatic, Keep Right** | No-input sequences became a highly visible authored genre; `Super Mario Maker 2` later formalized `Auto-Mario` as a tag. | [S01–S03, S06, S07] |
| **2019–2024** | Academic studies | **zero-player level design**, **AutoPlay** | Explicit scholarly treatment of choreography, creative labor, and procedural generation. | [S01, S03, S14, S15] |

**Historical caution:** This is a chronology of **documented examples**, not a claim of first invention; the communities often arrived at related techniques independently.

---

## 4. Comparative game case studies

### 4.1 `N` / `N++`: Don't Do Anything [S04]

**Observed:** Metanet's own retrospective confirms that the user-level editor yielded DDA maps in which the ninja reaches the exit automatically via Rube Goldberg-like contraptions. Common elements include launch surfaces, momentum, reactive enemies, narrowly avoided traps and timed passages. Community recollections describe hold-left and hold-right variants as well [S20].

**Transferable lesson [I/R]:** Expose simple physics primitives and a fast editor→test loop. Designers can discover sophisticated routing **without** an editor-provided cutscene graph. Support near-miss tuning, path inspection, and neutral-input trace capture.

### 4.2 `Happy Wheels`: Don't Move [S08, S09]

**Observed:** The community documents levels moving the character via spring platforms, fans, swinging objects and other hazards with no controls. Its editor supports triggers and collision filters. The same community warns that finely tuned Don't Move levels may fail on different computers [S08, S09].

**Transferable lesson [I/R]:** Publish a run's engine version and tested platform; never mistake one successful author-machine replay for portability. Editor gadgets should expose impulses, collision masks, and timers clearly. Provide safer, less knife-edge variants where a demo must reliably reach an ending.

### 4.3 `Super Mario Maker`: Automatic Mario [S01–S03, S06, S07]

**Observed:** Designers time trampolines, enemies, moving objects, lifts, and obstacles so Mario crosses a map untouched. A 2015 *Ars Technica* survey of the then-top 50 Most Starred courses counted **19/50** as finishable without button presses *or by simply holding right*; 11 of the top 13 fell in this combined class. This is a **snapshot of a popularity leaderboard, not a random sample of all levels** [S07]. Kotaku described the viewer who moves as potentially *breaking* the very sequence they are supposed to watch [S06]. Johnson's scholarly analysis emphasizes the high level-construction labor behind apparently effort-free consumption [S03].

**Transferable lesson [I/R]:** Design for perceptual staging as well as completion. The best experience is not merely a valid path: it reveals machinery, creates rhythm and suspense, shows apparent danger, and delivers a legible ending. Label the intended non-interaction explicitly in the UI.

### 4.4 `TrackMania`: PF versus PN [S01, S05]

**Observed:** PF tracks ask users to hold acceleration without steering; PN tracks use boosters so even acceleration can be omitted. Author Randy O'Connor connects their existence to near-instant testing and repeatable physics. Yang argues they shift skill from driving to architectural choreography. The player can wreck a perfect PF by making a normal driving decision [S01, S05].

**Transferable lesson [I/R]:** Keep **zero-input** and **fixed-input** as separate manifestable run contracts. Test both the intended control stream and at least one controlled deviation; do not classify a PF as PN merely because both are effortless.

### 4.5 `Line Rider`: the stage as kinetic artwork [S10, S13]

**Observed:** The creator's work began as a browser sandbox in which users draw a sled track and watch the physics unfold [S10]. In a documented long-form art project, an artist reported a **51-minute** Line Rider performance synchronized to an album, with **272 hours** of work over 18 months [S13]. These are an individual artist's self-reported figures, not population statistics.

**Transferable lesson [I/R]:** The zero-player format need not end in a finish flag. Time, pacing, motion and composition can be the entire product. Allow a level to specify a cinematic endpoint, loop, fade or indefinite ambient exhibition; expose viewing/scrubbing and capture controls.

### 4.6 `Geometry Dash`: Auto as a first-class discovery category [S11, S12]

**Observed:** Community documentation defines an Auto level as one normally completed with no input; game discovery recognizes an Auto difficulty class. The genre includes visual, mechanical and musical presentations, rather than only athletic traversal. [S11, S12]

**Transferable lesson [I/R]:** Add explicit **Auto / No Input** tags, filterable listings and metadata indicating whether a level is a narrative ride, kinetic installation, puzzle-machine or music visualizer. A plain “easy” difficulty label does not describe this experience.

---

## 5. Cross-source findings

| Finding | Evidence | Qualification | Development implication |
|---|---|---|---|
| **F1. The designer performs; the viewer witnesses.** | Yang, Johnson, Metanet [S01–S04] | Strong qualitative convergence, not controlled audience psychology. | Evaluate *authoring quality* and staging, not player skill. |
| **F2. Physics primitives are a compositional language.** | `N`, Mario, TrackMania, Line Rider [S01, S04–S06, S10] | Different engines have very different mechanics. | Prefer reusable primitives over bespoke scripted movement. |
| **F3. Timing and near misses generate spectacle.** | Yang, Kotaku, Happy Wheels [S01, S06, S08] | Mostly descriptive/editorial. | Trace moments of danger, reveal payoff, maintain screen legibility. |
| **F4. Low-friction test iterations are foundational.** | First-person editor analysis [S05]; Mario editor manual [S19] | Plausible practical observation. | One-action test/reset/step/replay; persistent trajectory overlays. |
| **F5. No-input is not necessarily hands-off software.** | PF/PN distinction [S01, S05] and art tool cases [S10, S13] | Conceptual separation. | Retain pause, speed, camera, paint and spawn commands. |
| **F6. Portability/reproducibility is fragile.** | Happy Wheels community [S09]; engine maintainers [S16–S18] | Engine- and build-specific; no universal guarantee. | Explicit deterministic contract, pinned builds, QA matrix. |
| **F7. Discovery taxonomies matter.** | Mario Maker taxonomy and Geometry Dash [S01, S11, S12] | Community classifications evolve. | Expose `mode: auto`, distinct from `difficulty: easy`. |
| **F8. Generation needs expressive fitness functions.** | Sabraw 2024 [S14], Abdullah et al. 2019 [S15] | Research on custom/related engines, not production validation. | Reward motion, completion, timing and clarity; penalize trivial slides. |
| **F9. Musical and narrative works are legitimate primary outputs.** | Yang, Line Rider artist, Johnson [S01, S03, S13] | Artistic examples, not universal preferences. | Support timeline cues and audience-facing story beats as optional layers. |

### 5.1 Important tensions

- **Determinism vs. emergence:** Exact repeatability makes authoring easier; natural variability can make a machine feel alive. Choose deliberately per level, record seeds and test probability of completion if stochastic.
- **Spectacle vs. visual comprehension:** More collisions and hazards can create wonder or unintelligible clutter. Authoring UI should preview cinematic framing.
- **User intervention vs. intended choreography:** Painting or spawning a rigid body can invalidate the reference run. Allow intervention, but label it an **edited / exploratory branch** rather than continuing to assert certification.
- **Physical correctness vs. spectacle:** A game physics engine can produce visually implausible but mechanically genuine chains. Do not disguise teleports, cutscenes, or scripted repositioning as physical interaction.
- **Pure zero-input vs. low-input:** PF/Keep Right is adjacent, but its continuous-control requirement changes the formal test harness and user instructions.

---

## 6. Mechanics and creative pattern library

The patterns below are **cross-case design abstractions [I/R]**, not a claim that every cited game supports every element.

| Pattern ID | Primitive arrangement | Observable effect | Editor controls and verification |
|---|---|---|---|
| `ZP-P01` Gravity cascade | Release a ball/boulder/sand mass onto a lever or switch | Starts a chain naturally | Spawn height, mass/density, release time, collision/contact logs |
| `ZP-P02` Bounce corridor | Springs, launch pads, rebound surfaces | Recurring flight and near-miss traversal | Normal, elasticity, impulse range, contact position/velocity trace |
| `ZP-P03` Moving conveyor | Moving surfaces, belt-like forces, gravity | Carries an inert subject through stages | Speed, force limits, timing and phase |
| `ZP-P04` Pendulum relay | Hinged body strikes next body | Rube Goldberg chain with rhythm | Joint limits, damping, mass, tick-of-impact |
| `ZP-P05` Funnel-and-gate | Slopes/chutes, timed gate, collision filters | Captures and releases objects into next device | Clearance, trigger window, actuator timing |
| `ZP-P06` Fluid messenger | Water/lava/sand/smoke transport force, buoyancy or pressure analogues | Material flow drives the sequence | Material policy, coupling limits, conservation and visual clarity |
| `ZP-P07` Near-miss aperture | Moving hazard plus narrow safe passage | Apparent peril, safe deterministic outcome | Minimum clearance, earliest collision time, robust margin |
| `ZP-P08` Triggered scenic reveal | Object enters sensor, toggles lights/particles/camera emphasis | Narration without words | Event-time cue, separation of visual vs physics state |
| `ZP-P09` Rhythm instrument | Contacts or sensors trigger original/cleared audio, lighting or particle beats | Physics creates a time-based score | Beat timeline, trigger IDs, latency measurements |
| `ZP-P10` Endless kinetic loop | Closed sequence that replenishes motion safely | Ambient gallery/installation loop | Energy source disclosure, leak detection, cycle length, restart mode |
| `ZP-P11` Fixed-input variant | Neutral inputs replaced with constant accelerate/right | PF/Keep style cousin | Precise held-input contract, release/deviation negative test |

**Composition syntax (conceptual):** `trigger -> transfer -> transformation -> reveal -> next trigger -> finale`. The arrows represent observed causal events in the simulated world, not hard-coded actor position changes. A useful editor displays both the **causal graph** and the **spatial trajectory** without conflating them.

### 6.1 Narrative/sightseeing patterns

A practical silent narrative has: **establish** the world (quiet opening) → **animate** a machine or organism (first autonomous event) → **travel** through meaningful spaces → **escalate** physical complexity or apparent danger → **reveal** a surprise or change → **resolve** to a finale or loop. The character may act as camera proxy, a moving token, an observer, or be omitted entirely. This is a recommended pattern, not a documented universal structure.

### 6.2 Authoring ergonomics

For zero-player design, a strong editor exposes quick reset, tick advance, real-time / slowed / accelerated previews, adjustable ghost trails, impact markers, object wake/sleep indicators, timeline bookmarks, collision-debug geometry, and comparison of two runs. The `Super Mario Maker` manual confirms immediate create/test switching as an official part of its workflow [S19]; the more specialized trace tools are **proposals** [R].

---

## 7. Implementation architecture for agentic teams

### 7.1 Functional separation [R]

```
Level file / authored contraption manifest
       | scene objects, materials, initial states, versioned parameters
       v
RunController ---------------------------┐
  - start/reset/stop                     |
  - fixed-tick progression               |
  - pause/step/time-scale                 |
  - input policy (neutral vs fixed)      |
       v                               v
Authoritative world simulation --> event/sensor log
  - cellular / material simulation       |       |
  - rigid body physics                   |       v
  - ordered boundary exchange            |    Timeline / metrics
  - deterministic command queue          |
       |                                  |
       v                                  |
Immutable snapshots ----------------> Renderer / camera / UI
       ^                                  |
       |                                  v
Editor tools (paint, spawn, inspect) --> interaction branch marker
```

**Boundary rule:** There must be one authoritative owner for each simulation state component. Do not alter live physics body positions merely to synchronize a cinematic trajectory. For heterogeneous engines, let each solver advance at the agreed tick boundary; synchronize material–body coupling through explicit deterministic commands, not unordered callbacks.

### 7.2 Suggested level schema (illustrative, not an existing project API)

```yaml
schema: zp-level/v1
id: relay-cascade-001
mode: zero_input                  # zero_input | fixed_input | kinetic_sandbox
viewer_contract:
  actor_controls: disabled        # must remain neutral throughout the run
  camera_controls: allowed
  pause_step_speed: allowed
  editor_painting: allowed
  rigid_body_spawning: allowed
  interaction_marks_run_modified: true
run:
  start: on_explicit_play
  fixed_step_seconds: 0.0166666666667 # example; engine must choose/pin actual tick
  seed: 1717
  max_ticks: 3600
  completion: event:finale_trigger
  exit_behavior: pause            # pause | loop | end_screen | continue_ambient
  physics_authority: engine
  scripted_actor_trajectory: forbidden
provenance:
  source_commit: "<fill at qualification>"
  engine_build: "<fill at qualification>"
  simulation_rules_hash: "<fill at qualification>"
  world_file_hash: "<fill at qualification>"
  solver_configs: {}
  runtime_assets_hashes: {}
qualification:
  target_platforms: []
  golden_run_id: null
  expected_keyframes: []
  policy: reproducible_or_bounded_stochastic
```

**Caution:** `0.016666...` is a schema example, not a mandated engine frequency. Tick rates, substeps, contact ordering, material defaults, and solver admission/refusal must be grounded in the **actual target repository** before implementation.

### 7.3 Runtime semantics

1. **Start:** Deserialize or construct a complete pinned initial state; reset simulation time, active timers, controller state, queued commands, and camera to their defined initial conditions.
2. **Tick:** Apply sorted authorized commands; advance material solver and rigid-body solver in an explicitly documented order; record contacts/triggers; commit a snapshot for rendering.
3. **No actor input:** Enforce input policy at the ingestion boundary, not merely by hiding buttons. If a mouse click would normally move an avatar, suppress that action while still allowing painting or object spawning through distinct editor tools.
4. **Pause / step:** Paused simulation advances zero ticks even while rendering/UI continues; single-step advances exactly one simulation tick, then freezes the world again. Timer and spawn semantics must depend on simulation ticks, not wall-clock frame rates.
5. **Time scaling:** Fast-forward means executing more fixed simulation steps (or a deliberately qualified alternative); it must not silently alter gravity, contact resolution, solver timestep or scripted deadline semantics.
6. **Intervention:** Separate `reference` (pristine), `modified` (user intervention), and `authoring-preview` runs. Export/record both scene hash and event log.
7. **Complete/loop:** On reaching a finale, present the stated behavior, not an unexplained hard reset. For infinite/ambient art, expose a stable loop or deliberate endless-mode identifier.

### 7.4 Source-agnostic interfaces (pseudo-contracts)

```text
LoadLevel(manifest, source_provenance) -> initial_world
ResetRun() -> run_id
ApplyObserverCommand(Paint|SpawnRigidBody|Camera|Pause|Step|Speed)
TickFixed() -> {sim_tick, snapshot_ref, events, state_digest}
InspectRun() -> {start_state, actor_input_trace, timeline, divergences, outcome}
ExportEvidence() -> {manifest, hashes, engine_id, seed, logs, checks}
```

A real project should adapt these names to its existing scheduler, thread ownership, material rules, and renderer; do not create a parallel physics loop or a new physics authority just to support the demonstration.

### 7.5 Application to a mixed cellular/rigid-body web demonstration

A falling-sand plus rigid-body engine can provide **two legitimate modes** without confusing them:

- **`zero_input_actor`** — an actor token, if available, is propelled by world forces without gameplay commands.
- **`kinetic_sandbox`** — **no actor is required**: sand flows, fluids displace bodies, pendulums transfer impulse, and the camera reveals a sequence. The observer still paints materials, pauses/steps, changes speed, and spawns rigid bodies.

Before implementing, inspect the live repository and preserve its pre-existing physics authority, existing material semantics, protected tests/fixtures, threading ownership, graphics architecture, and performance budgets. The scheme above is not evidence that any named repository already supports every primitive. Confirm actual body/material interaction contracts and web build provenance before making claims.

---

## 8. Determinism, portability, and QA

### 8.1 Three levels of guarantee

| Guarantee | Meaning | Evidence demanded |
|---|---|---|
| **Same-run local repeatability** | Same build, initial state and tick sequence yield matching state/event outcomes on one environment. | Multiple complete same-machine replays with state digests and event logs. |
| **Cross-runtime equivalent spectacle** | Different devices/browsers preserve core events and finish successfully even if exact floating point traces differ. | Platform matrix; bounded event-time and trajectory deviations; outcome comparisons. |
| **Bitwise deterministic cross-platform** | Entire defined simulation state hashes equal across environments after the same tick count. | Exact equal hashes plus documented engine/compiler/build/configuration guarantee; no untracked state. |

**Documented caveats:** The Rapier **JavaScript/WASM** determinism guide claims cross-platform determinism for the same version under *identical initial conditions, object insertion/removal order and parameters*, while warning that application computations (including transcendental functions) can violate the premise [S16]. Its native/C and Godot integration paths have distinct requirements [S17, S18]. Godot-Rapier explicitly distinguishes deterministic physics-server state from other Godot scene-tree state [S18]. Box2D's engine author advises regression-testing determinism in CI because compiler/platform changes can break assumptions [S17]. **None of these statements establishes determinism for an arbitrary combined cellular+rigid simulation.**

### 8.2 Why visually plausible simulations diverge

Risks include: variable timesteps; unseeded randomness; unordered object creation; differing contact processing order; worker scheduling; floating point/compiler/SIMD variation; time-based callbacks; async resource loads; interest-window updates; sleeping/waking; inconsistent paint/rigid-body command timing; stale material-body occupancy; mismatched assets; and browser/native build differences. This is an engineering risk list, not proof that any particular engine exhibits all failures.

### 8.3 QA plan [R]

**Unit:** impulse geometry, restitution, trigger gating, initial-state reset, start-condition neutrality, seed replay, effect of single-step, speed setting independence.  
**Integration:** material ↔ rigid-body coupling, repeated contacts, sleeping, camera follow, editor painting/spawning during paused/running state, immediate reset after intervention.  
**System:** native and browser runs with exact build provenance, varied render frame rates / tab focus and visibility, varied core counts if applicable, time controls, WebGL/WASM startup, and cleanup/shutdown during active jobs.  
**Human review:** can a spectator understand the action without controlling it? Are timing, framing, near misses, and finale satisfying? Are interventions clearly marked? Automated coverage cannot replace this assessment.

For a candidate level, propose **at least 30 local replays per supported runtime** as a *project policy starting point* (not a literature-backed industry standard); require all to reach the authored ending for a deterministic reference. For intentionally stochastic art, specify the acceptable outcome distribution, sample size and confidence method **before** testing; avoid presenting a one-off seed as universal reliability.

### 8.4 Evidence manifest to retain

```text
run_id
level_id, scene_hash, initial_state_hash, seed
source_repository, source_commit, build_id, build_config
physics_lib_version, ruleset_version, solver_options
platform, OS, CPU architecture, browser/runtime, hardware acceleration
fixed_dt, substeps, tick_count, input_contract
commands (with tick), ordered object creation/deletion log
checkpoints (sim_tick -> state_digest), contact/trigger timeline
outcome (complete | fail | timeout | loop | stalled)
rendered recording (optional; supplement, NOT replacement for state evidence)
all test invocations, negative cases, known failures, artifact paths and retention
```

The manifest must be generated from *actual execution*. Placeholder hashes, imagined CI status, or a visual-only video do not prove source-matched qualification.

---

## 9. Generation and optimization research

### 9.1 Automatic Mario via genetic algorithms [S14]

Shawn Douglas Sabraw's November 2024 MSc thesis, *Generating Automatic Mario Levels With a Genetic Algorithm*, evolves layouts for an **experimental 2D platformer** to move the character automatically. It uses goals/tie-breakers including farthest-right movement, total movement and level sparsity. Its experiments varied search-space constraints and density. The thesis reports improved search in constrained sparse layouts, while also observing that a superficially high movement score can come from a boring slide across a solid surface and that indiscriminate sparsity penalization can hurt some outcomes. These results are **thesis-specific**, not a drop-in optimal recipe for Mario Maker or mixed-media sand engines.

**Practical inference:** Evaluate not only “reaches finish” but also *quality of movement*: useful height changes, variety of forces, visible cause/effect, scenic coverage, clear transitions, low dead time, and a legible payoff. Optimize **progress plus spectacle**, without hiding failure behind a score.

### 9.2 Rube Goldberg modules [S15]

Abdullah, Paliyawan, Thawonmas, Harada and Bachtiar (IEEE CoG 2019) construct *Angry Birds*-like domino-effect levels from segments, with procedural variation. They report a favorable expressivity/runtime comparison to their selected baselines and emphasize interaction among several segments. **One projectile initiation is not the same as pure zero input before startup**; it is structurally useful as an analogy to automatic chains.

**Practical inference:** Author small tested contraption **modules** with explicit entry conditions (position, velocity, body shape, material state) and exit envelopes. Compose modules only after validating their hand-off tolerances. This is more tractable than optimizing an entire giant scene blind.

### 9.3 Proposed objective vector (not empirically validated)

For candidate `c` in simulator `sim`, collect the following observable measures before choosing weights:

```text
validity:        reached finale without gameplay input; zero unhandled fatal errors
completion_rate: successful qualifying replays / attempted qualifying replays
path_progress:   distance to authored milestones, not only horizontal displacement
motion_variety:  diversity of contact/flight/roll/float/cascade segments
causal_clarity:  proportion of significant events whose initiating objects stay visible
scene_coverage:  important authored locations entered and visible
pacing:          intentional alternation of action and rest; no accidental stalls
robustness:      sensitivity to allowed perturbations and target runtime differences
cost:            CPU simulation, render frame time, memory, object count
complexity:      number of active primitives; penalty only when irrelevant
```

Use a **hard feasibility gate** (`validity`, input policy, physics provenance) followed by a Pareto comparison of non-commensurable artistic/technical goals. Do not collapse all dimensions into one magic metric. A simple scripted camera move may improve scene coverage while undermining a claim of physics-authored motion if it teleports an actor; evaluate those separately.

### 9.4 Incremental authoring / search loop

1. Start with one stable physical transfer (e.g., rolling body strikes a platform).
2. Record its output-state envelope over qualifying runs.
3. Attach a second primitive conditioned on the observed output.
4. Search local placement, mass, restitution or gate-window parameters in constrained ranges.
5. Re-run all prior checkpoints after each accepted change (a new gadget can disturb earlier physics).
6. Prefer a robust plateau over a visually spectacular single-pixel / single-tick knife-edge, unless unreliability is explicitly part of the artwork.
7. Freeze seed, ruleset, engine version and exemplar replay before publishing.

**Never assume** a learned level generator understands the engine's physics. Fitness should call the authoritative simulation or a separately validated behavioral surrogate; otherwise generated visual plausibility is not proof of reachability.

---

## 10. Reference demonstration suite

These are **proposed fixtures**, not demonstrations claimed to exist or to have passed.

| Fixture | What is shown | Minimum qualifying claim |
|---|---|---|
| `ZP-FX-01-neutral-spring` | Actor/token falls onto spring, rebounds to goal | Neutral input from start to finish; same state after reset/replay |
| `ZP-FX-02-pendulum-relay` | Three or more bodies transfer energy via contacts | Events arrive in declared causal sequence; no scripted teleport |
| `ZP-FX-03-liquid-carrier` | Material flow displaces/transports floating body or gate | Material↔body contract measured; no unaccounted coupling jumps |
| `ZP-FX-04-scenic-ride` | Camera witnesses multiple themed beats with beginning/end | Route coverage, timing, framing and finale tested by humans |
| `ZP-FX-05-ambient-loop` | Continuous autonomous kinetic scene without actor | Loop remains stable over predetermined duration; resource ceilings respected |
| `ZP-FX-06-intervention` | Viewer paints/spawns a body and alters the sequence | Reference run explicitly marked modified; full reset restores baseline |
| `ZP-FX-07-time-controls` | Pause, step, slow motion and fast-forward | No physics advance while paused; step advances exact tick; world outcomes qualified |
| `ZP-FX-08-platform-matrix` | Exact scene run in browser and native environments | Build provenance and outcome comparison available; divergence reported, not suppressed |
| `ZP-FX-09-fixed-input-negative` | PF variant holding forward/right | Fails/changes when input released; correctly classified as PF rather than PN |
| `ZP-FX-10-inactive-region` | Autonomy and boundary transfers across interest regions | Off-camera rules deliberate; no unexplained freeze at buffer boundary |

### 10.1 Acceptance rubric [R]

**Required for a “qualified zero-input demonstration”:**

- [ ] Correctly classified as `zero_input` or `kinetic_sandbox`, never PF by omission.
- [ ] Specified baseline completes or exhibits the declared autonomous behavior with actor-control trace **all neutral**.
- [ ] Authoritative world progression and physics coupling are unchanged from the supported engine, except approved explicit changes.
- [ ] Reset restores the source-matched state; expected interaction commands remain available.
- [ ] Renderer/camera do not silently change the simulation outcome.
- [ ] Reference replay evidence lists seed, engine build, source commit, material policy and exact input log.
- [ ] Repetition and platform matrix demonstrate the *stated*, not assumed, reliability class.
- [ ] No core regressions in protected functional/performance fixtures.
- [ ] At least one human evaluation confirms visual legibility and narrative/kinetic purpose.

**Optional for a “featured gallery piece”:** meaningful pacing, distinct scene beats, creative use of physical materials, original/cleared audio cues, interesting close calls, meaningful title/tag/description, coherent finale, high-contrast accessible visuals, and easy loop/restart.

---

## 11. Agent task contract and decision record

### 11.1 Agent kickoff protocol

When an agent is asked to implement this design in a real project:

1. **Audit current source first:** repository HEAD, instructions, architecture, active PRs, engine/solver ownership, existing editor, tests, demo constraints and open issues. This study does not override live repo authority.
2. **Select exact experience class:** pure zero-input actor, kinetic sandbox, one-shot triggered, or PF. Explicitly distinguish “no actor controls” from “no editor controls.”
3. **Declare evidence contract:** platform/build matrix, material rules and solver version, fixed timestep, seeded starting state, command logging, completion criteria.
4. **Prototype a minimal source-matched reference:** one gadget, one transfer, repeatable outcome. Avoid constructing a long spectacle before physics and replay are qualified.
5. **Build authoring instrumentation:** trajectory overlay, contact times, state hashes, rewind/reset or reproducible restart, explanatory status when intervention invalidates golden run.
6. **Expand through modules:** merge only after objective replay gates and meaningful visual review; record negative tests and known failures.
7. **Review independent of success screenshots:** inspect actual source, inputs, runtime artifacts, exception paths, performance metrics, and cleanup behavior.
8. **Publish precise claims:** `locally replayable`, `cross-runtime visually equivalent`, or `bitwise deterministic` only when supported by matching artifacts. Never claim the untested stronger tier.
9. **Handoff:** supply machine-readable manifest, actual run commands, tests and outputs, limitation list, and prioritized next work.

### 11.2 Decisions to resolve with the owner (not silently assume)

| Decision | Safe default | Alternatives / consequences |
|---|---|---|
| Actor required? | **No** for physics art/demo; optional for a narrative ride | Mandatory avatar narrows editor/sandbox design |
| Gameplay inputs during exhibit? | Disabled | Fixed-input PF documented as different mode |
| Painting/time/spawning? | Retained in editor/observer layer | Read-only gallery can be separate distribution mode |
| Determinism target? | Reproducible local golden run + cross-platform outcome matrix | Strict cross-platform hashes require demonstrated complete-stack guarantee |
| Artificial choreography? | Disallow direct actor teleport/position scripts in “physics-native” mode | Cinematic/animated variant may permit it if honestly labeled |
| Stochastic outcomes? | Explicit seed and success criterion | Probabilistic art needs statistical testing and descriptions |
| Spectacle optimization? | Human-artistic review plus trace metrics | Fully automated generation demands calibration and robust failure reporting |
| Runtime asset distribution? | Source-matched manifest and hashes | Portable ZIP/web bundle must independently satisfy licensing, build and LFS requirements |

### 11.3 Definition of done for a development PR

A PR is **not done** because the scene looks correct once. It must identify the exact source and runtime, show a neutral actor-input trace (or absence of an actor), demonstrate physical causality, survive repeated reset/launch, verify time controls and editor interventions, preserve the original engine authority and protected fixtures, and state any unmet cross-platform or human-viewing gates explicitly. Release readiness is a separate decision.

---

## 12. Annotated source register and research gaps

The cited items are arranged by their function. The value `A/B/C/D` denotes source type (see §2), **not** an automatic truth score. All URLs were located or inspected in the 30 October 2026 research session; no claim is made that every external media embed can still be played.

### Central studies and historical analysis

- **[S01] A/B — Robert Yang (2019).** *Dancing About Architecture: On Zero Player Level Design*. In *Video Game Art Reader*, vol. 3, pp. 37–46, Amherst College Press. Open-access scholarly chapter, peer-reviewed book. **Most directly relevant treatment** of PF/PN, Auto-Mario and architecture-as-performance. https://www.jstor.org/stable/10.3998/mpub.12471295.7
- **[S02] B — Robert Yang, revised online essay.** *Zero player level design*, *The Level Design Book*. Accessible expanded treatment with historical examples, Auto-Mario tag, music levels, and Line Rider-adjacent framing. Later revision; do not assume text identical to 2019 print chapter. https://book.leveldesignbook.com/culture/zero-player
- **[S03] B — Mark R. Johnson (2019).** *Playful Work and Laborious Play in Super Mario Maker*. *Digital Culture & Society* 5(2), 103–120. DOI in publisher text: `10.14361/dcs-2019-0207`; repository metadata also gives `10.25969/mediarep/21861`. Relevant on maker labor and Auto-Mario vs high-input Kaizo design. https://d-nb.info/1322611386/34
- **[S14] B — Shawn Douglas Sabraw (2024).** *Generating Automatic Mario Levels With a Genetic Algorithm*, MSc thesis, Memorial University of Newfoundland, November 2024. Direct generation experiment. Focus on movement-based fitness, sparsity/search-space constraints and their limits; **not** a production or cross-engine guarantee. https://www.cs.mun.ca/~dchurchill/publications/pdf/theses/ShawnSabraw_Thesis_MSc.pdf
- **[S15] B — Febri Abdullah, Pujana Paliyawan, Ruck Thawonmas, Tomohiro Harada, Fitra A. Bachtiar (2019).** *An Angry Birds Level Generator with Rube Goldberg Machine Mechanisms*. IEEE Conference on Games. Related single-trigger physics-chain generation, not a zero-input-avatar study. DOI `10.1109/CIG.2019.8847996`. https://ieee-cog.org/2019/papers/paper_205.pdf
- **[S21] B — Michael Austin (2017).** Conference abstract, *The History (and Future) of Automatic Mario Music Videos*, Ludo2017 programme. Context for ROM-hack automation and synchronized sound effects; **conference abstract**, not a full published experimental report. https://www.ludomusicology.org/wp-content/uploads/2017/04/Programme_Draft4.pdf

### Practitioner, creator and contemporary reporting

- **[S04] A — Metanet Software (29 May 2019).** *Happy 15th, Metanet Software Inc!* Developers explicitly credit the `N` community's DDA genre. https://www.metanetsoftware.com/2019/happy-15th-metanet-software-inc
- **[S05] C — Randy O'Connor (26 March 2010).** *Acknowledging Trackmania's non-racing mode*, *Game Developer*. Editor iteration and repeatable physics as core to PF design; author interpretation, not measured repeatability. https://www.gamedeveloper.com/design/acknowledging-trackmania-s-non-racing-mode
- **[S06] C — Patricia Hernandez (26 August 2015).** *The Most Ridiculous Mario Maker Levels Basically Play Themselves*, *Kotaku*. Contemporary examples of no-input and constant-input Mario courses. https://kotaku.com/the-most-ridiculous-mario-maker-levels-basically-play-t-1726677683
- **[S07] C — Kyle Orland (2 October 2015).** *Moneyball, but for Mario—the data behind Super Mario Maker popularity*, *Ars Technica*. Historical Most Starred Top 50 analysis, with combined no-input / hold-right category; **selection bias applies**. https://arstechnica.com/gaming/2015/10/how-to-make-a-popular-super-mario-maker-level/
- **[S08] D — Happy Wheels community wiki.** *Frequent Levels* (`Don't Move` entry); descriptive propulsion elements and device variability, not a controlled study. https://happywheels.fandom.com/wiki/Frequent_Levels
- **[S09] D — Happy Wheels community wiki.** *Level Editor* (physics tools, triggers, collision configuration; platform-specific Don't Move caveat). https://happywheels.fandom.com/wiki/Level_Editor
- **[S10] A — International Festival of Computer Arts / MFRU (2020).** *Line Rider* project account, presenting Boštjan Čadež's browser physics/drawing tool as an artistic medium. https://www.mfru.org/projects/line-rider
- **[S11] D — Official Geometry Dash Wiki.** *Glossary* (`auto`: level/section requiring no input). Community-maintained documentation on an official-style wiki. https://geometrydash.wiki.gg/wiki/Glossary
- **[S12] D — Official Geometry Dash Wiki.** *User Levels* (Auto as difficulty/discovery category). Community-maintained; current counts/ratings may change. https://geometrydash.wiki.gg/wiki/User_Levels
- **[S13] A — Bevibel Design / Line Rider artist.** *This Will Destroy You*, original artist statement on 51-minute album-length Line Rider track, time investment and intended artistic contribution. Self-reported production figures. https://bevibeldesign.com/this-will-destroy-you
- **[S19] A — Nintendo.** *Super Mario Maker electronic manual — Create*. Direct documentation of quick editor→play iteration. `Autoscroll` alone does not establish an automatic avatar run; the distinction here is analytic. https://microsite.nintendo-europe.com/super-mario-maker-manual/enGB/page_01.html
- **[S20] D — MetaFilter (5 December 2007), community eyewitness discussion.** A commenter describes specific `N` DDA creations, including missile chase spectacle. Retrospective/community anecdote, not archival proof of first invention. https://www.metafilter.com/67196/the-way-of-the-ninja

### Engineering corroboration

- **[S16] A — Rapier documentation, JavaScript/WASM.** *Determinism*. Cross-platform guarantees and precise identical-initial-condition caveats; documentation version/build applicability must be checked in the target project. https://rapier.rs/docs/user_guides/javascript/determinism/
- **[S17] A — Box2D / Erin Catto (27 August 2024).** *Determinism*. Multiple determinism concepts and CI tests, illustrating why qualification requires actual hashes and target environments. https://box2d.org/posts/2024/08/determinism/
- **[S18] A — Godot Rapier Physics docs.** *Determinism*. Physics server vs Godot scene-state distinction and state restoration constraints; relevant **only if** the target uses this integration. https://godot.rapier.rs/docs/documentation/determinism/

### Research gaps / next studies

1. **Comparative audience study:** Which physical effects increase comprehension, suspense, delight and perceived authorship in non-interactive sequences? Existing sources are largely interpretive.
2. **Portability benchmark:** A cross-OS/browser/CPU/GPU matrix for an identical zero-player scene, including deterministic vs near-equivalent outcomes, with engine/build pins.
3. **Reproducibility of hybrid cellular + rigid-body physics:** Published engine-level determinism does not automatically cover transfer order, material rules, active-region scheduling and rendering-driven behavior.
4. **Editor ergonomics:** Controlled comparison of bare editor, single-step, causal event graph, ghost path and automated local parameter search for creation time and robust completion.
5. **Generative authoring:** Compare all-at-once evolutionary search with staged module composition using real engine simulation, under identical budgets and artistic evaluation.
6. **Accessibility and agency:** Study how users experience an interface that invites observation but preserves optional camera, pause, painting and object interventions.
7. **Preservation:** Identify legally distributable original map files, runtime versions, safe mirrors and captured demonstrations. Historical references alone are insufficient for exact replay.

---

**Research disposition:** The term **zero-player level design** is directly established in scholarly work. `Don't Do Anything`, `Don't Move`, `Press Nothing`, `Auto-Mario`, and `Auto` are genuine related community labels; `Press Forward` / `Keep Right` require constant input and must be distinguished. The strongest implementation lesson is to provide a **physics-native authored sequence, immediate test/reset, reproducible state and provenance, flexible observation controls, and honest cross-runtime qualification**. This document is a reference for building and assessing such systems—not a claim that any specific game engine already implements them.