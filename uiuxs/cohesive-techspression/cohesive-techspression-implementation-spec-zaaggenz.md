# Cohesive-Techspression Direct Implementation Specification — Zaaggenz-Referenced

**Status:** Implementation contract  
**Version:** 1.0  
**Audience:** Engineers implementing layered expert interfaces with shared workspaces, intent controls and deep parameter access  
**Reference pin:** techrote/zaaggenz main at 0ea153b714de85bb72e8d1ae55fa1cc6818adf3b  
**Normative language:** **MUST**, **SHOULD**, and **MAY** indicate requirements, recommendations and optional capabilities.

This document translates cohesive-techspression into concrete state models, mapping rules, workspace contracts, synchronization behaviour and tests.

## Contents

1. **Authoritative state architecture** — One project model, many views.
2. **Workspace and surface schema** — Defines task-oriented views and local UI state.
3. **Control-layer model** — Intuitive, Focused, Expert and Inspector surfaces over shared state.
4. **Intent / feel-control schema** — Defines semantic macro controls and target mappings.
5. **Contribution resolution** — Defines base values, mappings, sidechains, locks and effective values.
6. **Task-adjacent grouping model** — Encodes co-use and workflow neighborhoods.
7. **Cross-surface synchronization** — Keeps names, selections, revisions and controls coherent.
8. **Expert parameter integration** — Integrates detailed parametermaxing-style controls safely.
9. **Explainability and reversible operations** — Contribution traces, reset, A/B and bake.
10. **Performance and update scheduling** — Prevents macros and multiple views from causing feedback loops.
11. **Persistence and versioning** — Stores source state separately from workspace-local state.
12. **Conformance suite** — Tests workspace cohesion, macro semantics and expert-detail consistency.

# 1. Authoritative state architecture

Use one authoritative project state.

Recommended separation:

~~~text
ApplicationState {
    project: ProjectState
    directParameters: Map<ParameterId, Value>
    intentControls: Map<IntentId, Value>
    parameterPins: Set<ParameterId>
    effectiveParameters: Map<ParameterId, Value>   // derived/cacheable
    context: ContextState

    workspaceSession: WorkspaceSession
    history: History
    revision: RevisionId
}
~~~

Authoritative user/project data MUST NOT be duplicated per workspace.

Derived/effective values MAY be cached, but MUST be reproducible from authoritative state plus declared context.

## 1.1 State classes

Distinguish:

- **base/direct state** — exact user-authored parameter values;
- **intent state** — broad macro positions;
- **context state** — selected source/layer/mode/device/etc.;
- **effective state** — resolved values used by the runtime;
- **view state** — workspace-local zoom, scroll, panel visibility;
- **derived state** — measurements, analysis, diagnostics or previews.

Derived and view state MUST NOT silently become project authority.

# 2. Workspace and surface schema

Recommended schema:

~~~text
WorkspaceSpec {
    id: WorkspaceId
    label: string
    purpose: string
    mutationPolicy: READ_WRITE | PROPOSAL_ONLY | READ_ONLY | SPECIALIZED
    surfaces: SurfaceSpec[]
    defaultSurface?: SurfaceId
    preserveContextKeys: string[]
}
~~~

~~~text
SurfaceSpec {
    id: SurfaceId
    role: PRIMARY | EDITOR | INSPECTOR | OUTPUT | TRANSPORT | DISCLOSURE
    groups: ControlGroupId[]
    sharedSelection?: SelectionChannelId
    sharedTransport?: TransportChannelId
}
~~~

A workspace switch SHOULD only change:

- representation;
- control availability;
- local layout state;
- task-specific derived state.

It MUST NOT clone or reset authoritative parameters.

## 2.1 Revision binding

Derived workspaces SHOULD bind to explicit source revisions when stale application would be harmful.

Recommended:

~~~text
DerivedViewState {
    sourceRevision: RevisionId
    currentRevision: RevisionId
    stale: bool
}
~~~

Mutation from a derived view MUST reject or explicitly rebase when stale.

# 3. Control-layer model

Represent progressive disclosure explicitly.

~~~text
ControlLayer =
    INTUITIVE
  | FOCUSED
  | EXPERT
  | INSPECTOR
~~~

The same ParameterId may appear in several layers through different controls.

Examples:

~~~text
INTUITIVE:
    "Punch" semantic macro

FOCUSED:
    Transient / Envelope / Drive group

EXPERT:
    exact attack_ms, transient_amount, drive_db ...

INSPECTOR:
    base value, macro contribution, effective value, runtime bound
~~~

Each control MUST resolve back to stable domain IDs.

## 3.1 Deep-link context

A reveal action SHOULD carry context:

~~~text
RevealRequest {
    targetParameterIds[]
    sourceObjectId?
    workspaceHint?
    focusGroup?
}
~~~

This lets “Show affected parameters” open the correct Expert group instead of a generic parameter list.

# 4. Intent / feel-control schema

Recommended model:

~~~text
IntentControlSpec {
    id: IntentId
    label: string
    description: string

    domain: BIPOLAR | UNIPOLAR | ENUMERATED
    minimum: number
    maximum: number
    neutral: number
    default: number

    mappings: IntentMapping[]
    semanticContract: IntentSemanticContract
}
~~~

~~~text
IntentSemanticContract {
    promisedDirection: string
    targetFamilies: string[]
    exclusions: string[]
    contextNotes: string[]
    safetyNotes: string[]
}
~~~

~~~text
IntentMapping {
    target: ParameterId
    mode:
        ADD_NORMALIZED
      | MULTIPLY
      | RATIO
      | BLEND_TO_TARGET
      | OFFSET_IN_DOMAIN
      | CUSTOM_BOUNDED

    weight: number
    curve: CurveSpec
    condition?: ConditionSpec
    sidechain?: SidechainSpec
    priority?: number
    stage?: string
}
~~~

Mappings MUST be declarative or otherwise inspectable.

A feel control MUST NOT invoke arbitrary unrelated project mutation.

## 4.1 Neutral identity

For each mapping:

~~~text
contribution(intent.neutral, context) == identity
~~~

unless the semantic contract explicitly declares a non-neutral baseline profile.

Test this property.

# 5. Contribution resolution

Recommended resolution pipeline:

~~~text
base direct parameters
    ↓
evaluate active intent mappings against current context
    ↓
remove contributions for pinned/excluded targets
    ↓
combine same-target contributions
    ↓
apply declared sidechain/compensation stages
    ↓
apply engineering/safety/domain constraints
    ↓
compute effective parameters
    ↓
runtime may further report requested vs effective limits
~~~

Do not implement feel controls by destructively rewriting the base parameter store on every slider movement.

## 5.1 Contribution record

For inspectability, generate:

~~~text
ParameterContribution {
    parameterId
    intentId
    baseValue
    contribution
    intermediateValue
    effectiveValue
    mappingMode
    mappingStage
    contextBranch
}
~~~

The Inspector layer can then explain the result without reverse-engineering UI history.

## 5.2 Composition rules

Prefer order-independent contribution systems.

For example, multiple normalized additive macros can combine before one parameter-domain transform:

~~~text
delta = sum(weight_i * curve_i(intent_i))
effectiveNormalized = clamp(baseNormalized + delta)
effective = fromNormalized(effectiveNormalized)
~~~

If a domain requires ordered stages, encode the order explicitly.

Do not rely on event-listener invocation order.

## 5.3 Sidechain graph

Sidechains form dependencies between mappings or parameter families.

Represent them as a directed graph.

The graph MUST be:

- bounded;
- deterministic;
- acyclic, unless a separately specified convergent solver exists;
- inspectable.

Reject accidental cycles during configuration/registration.

## 5.4 Context branches

A mapping MAY use context such as:

~~~text
source family
selected layer
mode
preset/profile
device capability
current parameter region
headroom/resource state
~~~

Conditions SHOULD be discrete or otherwise deterministic.

Changing context MUST recompute contributions from the same authoritative intent values.

# 6. Task-adjacent grouping model

A group schema SHOULD encode user purpose, not module path.

~~~text
ControlGroupSpec {
    id
    label
    purpose
    controls[]
    likelyNextGroups[]
    relatedOutputs[]
    revealTargets[]
}
~~~

A project MAY record co-use metadata:

~~~text
ControlRelationship {
    a
    b
    kind: CO_ADJUST | CAUSAL | COMPARE | NEXT_STEP | SHARED_OUTPUT
    strength: 0..1
}
~~~

This metadata can guide layout, but SHOULD NOT automatically reorganize the UI without deliberate product review.

## 6.1 Workflow routes

Represent important workflows explicitly:

~~~text
Workflow {
    id
    steps: [
        select source,
        shape intent,
        audition,
        inspect,
        compare,
        commit/export
    ]
}
~~~

The UI can then keep adjacent steps spatially or navigationally close.

# 7. Cross-surface synchronization

Use stable IDs for:

- parameters;
- source objects;
- timeline/events/items;
- outputs;
- revisions;
- presets/profiles;
- selection channels.

A control renders from authoritative state, not a private mutable copy.

## 7.1 Shared selection

Where several surfaces inspect the same object:

~~~text
SelectionChannel {
    selectedIds[]
    primaryId?
}
~~~

Switching workspace SHOULD preserve this channel when meaningful.

## 7.2 Shared transport/output

Playback, current output slot or preview target SHOULD have one state owner when multiple views expose it.

Avoid two transports appearing to control different hidden copies of the same output.

## 7.3 Naming registry

Use one semantic registry for labels/units/help where possible.

Different workspaces MAY use shorter contextual labels, but their underlying meaning must remain traceable to the same domain identity.

# 8. Expert parameter integration

Detailed parameters SHOULD use an explicit schema such as:

~~~text
ParameterSpec {
    id
    label
    unit
    type
    default
    bounds
    scale
    help
    group
}
~~~

Parametermaxing-style controls MAY add:

- direct numeric input;
- slider window;
- safety caps;
- engineering bounds;
- fine adjustment;
- notches/preferred values;
- requested/effective display.

## 8.1 Base versus effective editing

Recommended Expert presentation:

~~~text
Parameter: Drive
Base          12.0 dB
Intent delta  +2.1 dB  [Harshness +1.4] [Punch +0.7]
Effective     14.1 dB
~~~

Editing the normal numeric control changes **Base** by default.

Provide a separate explicit mechanism if the product supports post-intent overrides.

## 8.2 Pinning

Pin state SHOULD be addressable by ParameterId and optionally IntentId.

Possible policies:

~~~text
pin all intent effects on parameter
pin only one intent -> parameter edge
pin one group/family
~~~

The UI must show active pins.

# 9. Explainability and reversible operations

## 9.1 Contribution inspection

Expose at least one of:

- contribution badges beside detailed controls;
- “Affected by” list;
- macro-to-target graph;
- before/base/effective table;
- highlighted target groups.

For complex products, provide a dedicated Inspector surface.

## 9.2 Reset semantics

Distinct operations:

~~~text
Reset intent control:
    set one IntentId to neutral

Reset all intents:
    neutralize all intent controls

Reset parameter:
    restore direct/base value according to parameter policy

Unpin:
    restore macro eligibility, not old values

Bake intents:
    write current effective values into base
    neutralize selected intents
    clear only selected contributions
~~~

Baking SHOULD be transactional and undoable.

## 9.3 A/B

A/B comparison SHOULD capture:

- base/project revision;
- intent-control state;
- effective resolved state or deterministic recipe;
- relevant context.

Do not compare only visible slider positions if context can alter mapping.

# 10. Performance and update scheduling

Intent controls can fan out to many parameters.

Requirements:

- recompute only affected dependency subgraphs where practical;
- batch UI notifications after one resolution pass;
- avoid N controls each triggering full downstream recomputation independently;
- debounce expensive output/render work separately from lightweight state updates;
- keep dragging responsive;
- prevent workspace listeners from feeding resolved values back into base state.

Recommended:

~~~text
intent change
    -> mark affected mapping graph dirty
    -> resolve once
    -> publish effective-state revision
    -> update visible controls
    -> schedule/coalesce expensive preview
~~~

# 11. Persistence and versioning

Persist separately:

~~~text
project/base state
intent control values
pin/exclusion state
preset/profile state
workspace-local preferences
mapping schema/version identity
~~~

Do not serialize effective values as independent authority unless required for audit/reproducibility.

For reproducibility, store enough mapping/version identity to reconstruct effective state.

A mapping-schema change MAY alter output even when macro positions are unchanged; therefore migrations must be explicit.

# 12. Conformance suite

### State identity

- one ParameterId has one base value across workspaces;
- switching workspace does not mutate project state;
- same selection/revision is preserved where specified;
- stale derived state cannot silently apply.

### Control layers

- Intuitive and Expert controls resolve to the same model;
- reveal links focus correct affected parameters;
- Expert base edits recompute effective values without rewriting intent state;
- Inspector traces match actual resolution.

### Intent controls

For every IntentControlSpec:

- neutral produces identity;
- min/max remain within all target constraints;
- fixed input/context yields deterministic output;
- target set matches declared mappings;
- pins suppress only intended contributions;
- reset affects only the intended intent;
- context changes select the documented branch;
- mappings have no accidental side effects.

### Mapping graph

- no undeclared cycles;
- same-target composition follows declared rule;
- ordering is explicit when required;
- safety clamps are applied after contributions according to policy;
- contribution traces sum/compose to the effective value.

### Task grouping

- declared workflow steps are reachable through intended adjacent groups;
- common next actions retain context;
- parameter/module ownership does not cause duplicate authority.

### Persistence

- save/reopen restores base values, intent positions and pins;
- view-local state does not overwrite project state;
- mapping schema/version is available for reproducibility;
- migration tests cover changed macro semantics.


# Zaaggenz-oriented implementation examples

These examples illustrate the model. They do **not** freeze Zaaggenz-specific coefficients as reusable requirements.

## Workspace schema example

~~~text
ComposeWorkspace:
    mutationPolicy = READ_WRITE
    surfaces = [
        ProjectAndRender,
        PhraseTimeline,
        EventEditor,
        ClipsAndRegion,
        NamedOutputs,
        ExpertDisclosure
    ]

ResearchWorkspace:
    mutationPolicy = READ_ONLY / SPECIALIZED ROUTES
    surfaces = [
        CurrentSourceBoundary,
        InspectorRoute,
        ListeningRoute,
        VocalRoute,
        WorkspaceDisclosure
    ]
~~~

Zaaggenz's runtime keeps the current Compose TimelineDocument authoritative. Research surfaces bind to its revision rather than creating a competing project.

## Inspector example

The Inspector demonstrates a useful Focused/Inspector split:

~~~text
Musical controls:
    amount
    tuning root
    sonority
    anchor
    analyse / freeze / explicit apply

Linked transport:
    A before
    B after
    compensation
    shared scrub

Analysis surfaces:
    spectral timeline
    confidence mask
    requested / estimated / realised
    uncertainty
    remainder energy
    compatibility map
    expert method disclosure
~~~

This is cohesive because the surfaces all answer one task: **what changed, how confident are we, and should this proposal be applied?**

## Intent-control example

The recovered instrument's owner-identified **Control Layer Intuitive** includes broad controls such as:

- Punch
- Harmonisation
- Harshness
- Depth
- Width

A reusable implementation SHOULD model these as IntentControlSpec objects, not as direct aliases to one hidden parameter.

Illustrative, non-normative mappings might look like:

~~~text
Punch:
    transient family          positive nonlinear contribution
    attack-time family        inverse contribution
    body/tail persistence     mild inverse contribution
    selected drive family     conditional positive contribution
    output/headroom guard     context sidechain

Harmonisation:
    harmony/tuning family     positive contribution
    chord/sonority shaping    positive contribution
    voice/layer interaction   context-dependent contribution
    protected anchor          exclusion or reduced weight

Harshness:
    roughness/noise family    positive contribution
    high-frequency emphasis   positive contribution
    nonlinear-drive family    curved positive contribution
    safety/headroom           compensating sidechain

Depth:
    foreground/body balance   context-specific
    envelope/tail contrast    context-specific
    spectral separation       context-specific

Width:
    spatial/layer spread      positive contribution where available
    opposing/anchor layers    protected or reduced movement
~~~

The reusable point is not those exact routes. It is that the broad label owns a **semantic contract** and the mappings coordinate multiple families while preserving protected invariants.

## Parameter depth example

Zaaggenz's recovered catalogue contains dense families such as:

- synth harmonic structure, jitter, roughness, noise, drive and envelope;
- BODY/AUX/SUB levels, harmonic structure, filtering, interactions and event modulation;
- spectral-sculpt crossover, pocket, compression and crusher controls;
- arrangement timing, rolls, humanization and phrase motion.

This makes Zaaggenz a good example of why one Intuitive surface cannot replace expert controls: it must sit above them.

## Sidechain / ownership precedent

Zaaggenz already protects important ownership relationships:

- persistent SYNTHLINE / BODY / AUX / SUB / SCULPT roles;
- explicit source/project revision identity;
- derived Research state separated from Compose mutation;
- explicit apply instead of implicit analysis-to-project mutation.

An intent-control resolver should respect the same kind of ownership boundaries. A feel macro must not become a back door that silently violates layer ownership.

## Reference material inspected

- baseline/V1_2_1_CONTRACT.json
- zaaggenz_contracts/legacy_spec.py
- docs/runtime/ZG041_COMPOSE_RESEARCH.md
- docs/timeline/README.md
- web/timeline/index.html
- web/inspector/index.html
- zaaggenz_runtime/server.py
