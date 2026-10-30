Instruction for the agent responsible for the active project to use the standalone as a base, and pull then integrate relevant/helpful implementation details from direct, in order to create a tailored project specific spec document.

This separates **product requirements** from **reference architecture** and forces the active project agent to make an explicit applicability judgment.


1. **Standalone UI/UX spec = normative baseline.** The project should satisfy its interaction, layout, theming, accessibility, and mouse/keyboard-parity principles unless the project records a reason to diverge.
2. **Direct implementation spec = implementation pattern library.** The agent reviews it and imports only structures that genuinely fit the project: command registry, tile-state persistence, split-tree layout, hit maps, overlay stack, generation-tagged jobs, compositor, etc.
3. **MDBM-referenced material = evidence/examples.** Consult it when a concrete implementation or edge case is useful, but do not inherit MDBM-specific behaviour merely because MDBM does it.
4. **Project-specific UI/UX spec = final authority for that project.** The agent synthesizes the above with the project's actual domain, workflows, data model, platform constraints, and users.

That gives you a useful flow:

```text
Standalone UI/UX standard
        │
        ├── project requirements / constraints
        │
        ├── relevant patterns from Direct Implementation spec
        │
        └── optional concrete precedents from MDBM
        │
        ▼
Project-specific UI/UX + implementation specification
```

The important part is that the agent should **integrate**, not merely reference. The resulting project document should say things such as:

> This project adopts persistent tile identity and geometry-derived hit maps, modifies the generic split model to support dockable agent dashboards, does not use editor-oriented selection semantics, and adds topology canvases, terminal-session tiles, job queues, and resource-monitoring surfaces.

That is much stronger than saying “follow these two documents.”

### I would make the agent perform an applicability pass

For every substantial implementation pattern, classify it as:

| Decision | Meaning |
|---|---|
| **Adopt** | Fits directly; incorporate into project spec |
| **Adapt** | Useful principle, but change it for the domain |
| **Reject** | Inappropriate for this project; document briefly why |
| **Extend** | Baseline is insufficient; add project-specific behaviour |

This prevents cargo-culting the direct spec.

For a VM/agent orchestrator, for example:

| Pattern | Likely decision |
|---|---|
| Semantic `CommandRegistry` | Adopt |
| Mouse/keyboard parity | Adopt |
| Persistent tile state | Adopt |
| Geometry-derived hit testing | Adopt |
| Split-tree workspace | Adapt — add docking/tabbing |
| Text editor selection rules | Reject unless terminal/editor tiles need them |
| Adaptive ANSI theme engine | Adopt/Adapt |
| Generation-tagged async work | Adopt |
| Source/preview synchronization | Reject |
| Agent topology canvas | Extend |
| Job queue visualization | Extend |
| VM lifecycle controls | Extend |
| Live log/terminal panes | Extend |

I would also make the generated project-specific document record its provenance near the top:

```text
Basis:
- specdocz standalone GUI/TUI UI/UX specification — normative baseline
- specdocz direct implementation specification — selectively incorporated
- project requirements and existing architecture — authoritative where more specific

Precedence:
project-specific safety/functional requirements
→ this project UI/UX specification
→ standalone UI/UX baseline
→ direct implementation guidance
```

That gives future agents a clear answer when two documents disagree.

A good reusable instruction for project agents would be:

> **Use the `specdocz` standalone GUI/TUI UI/UX specification as the baseline design contract. Review the companion direct implementation specification as a pattern library, not as mandatory architecture. For each relevant implementation pattern, decide whether to adopt, adapt, reject, or extend it based on this project's domain, existing architecture, platform constraints, workflows, and performance requirements. Where useful, inspect the MDBM-referenced variants for concrete examples and edge cases. Integrate the resulting decisions into a self-contained project-specific UI/UX and implementation specification stored in this repository. The project-specific specification becomes authoritative for this project and must not require readers to consult MDBM or `specdocz` to understand required behaviour. Record material deviations from the baseline and the rationale for them.**
