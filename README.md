# specdocz

Reusable, versioned engineering and UI/UX specifications with supporting research for project-specific tailoring.

## Specification families

| Family | Role |
| --- | --- |
| [tuiuiux](tuiuiux/) | Tile-native GUI/TUI design, implementation patterns, and tailoring |
| [mzpaint](mzpaint/) | Precision/semantic and expressive/painterly cell-grid editing |
| [parametermaxing](parametermaxing/) | High-density expert parameter interfaces and controls |

## Evidence and research

[research/](research/) is a **non-normative reference library**: metastudies (evidence syntheses), technical comparisons, historical precedents, unresolved questions, and candidate patterns. Start with the [catalog](research/catalog.yaml) and the [research index](research/README.md).

**Authority:** project safety, functional and compatibility requirements → project's tailored specification → applicable reusable normative specdocz baseline → explicitly adopted implementation patterns → research evidence and examples. Research is **not automatically a requirement**. Project repositories own their resulting contracts and should pin the exact source commit and document path.

A study is not a statistically pooled meta-analysis merely because its filename uses “metastudy”. The [research contribution guide](research/CONTRIBUTING.md) describes source evidence, promotion, and review requirements.

## Using specdocz in a project

Audit the project first, select applicable normative specifications, assess candidate patterns as **Adopt / Adapt / Reject / Extend**, and integrate decisions into a **self-contained project specification**. Record the exact specdocz commit SHA and file paths used. Do not treat reference project implementations as universal architecture.
