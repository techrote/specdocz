# parametermaxing

Reusable specifications for **high-density expert parameter interfaces**.

Parametermaxing means maximizing useful controllability, inspectability, experimentation speed, and parameter reach per unit UI area **without sacrificing precision, safety, comprehension, or recoverability**.

The design family is derived from XenoField's long-running UI tuning work: synchronized slider + numeric entry, editable working ranges, safety/engineering bounds, functional extremums, dense control banks, modular presets and locks, pinned context, and carefully tuned preferred-value/notched slider behavior.

## Documents

| Document | Purpose |
|---|---|
| [parametermaxing-uiux-spec-xenofield.md](parametermaxing-uiux-spec-xenofield.md) | Normative UI/UX specification with XenoField provenance and examples |
| [parametermaxing-uiux-spec.md](parametermaxing-uiux-spec.md) | Standalone normative UI/UX specification |
| [parametermaxing-implementation-spec-xenofield.md](parametermaxing-implementation-spec-xenofield.md) | Direct implementation contract with XenoField examples |
| [parametermaxing-implementation-spec.md](parametermaxing-implementation-spec.md) | Standalone direct implementation contract |
| [parametermaxing-spec-tailoring.md](parametermaxing-spec-tailoring.md) | Procedure for deriving a project-specific parameter-control specification |

## Recommended use

For a new project:

1. use the **standalone UI/UX spec** as the normative baseline;
2. review the **standalone implementation spec** as a pattern library;
3. consult the **XenoField-referenced variants** for concrete precedents and edge cases;
4. use the **tailoring guide** to create a self-contained project-specific parameter specification.

The project-specific specification should define which parameters are continuous, discrete, compute-aligned, wide-dynamic-range, expensive, safety-sensitive, or context-dependent rather than applying one slider model indiscriminately.
