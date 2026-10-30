# Research catalog and methodology

This directory provides a **cross-category** catalog, reusable authoring template, and evidence-quality guidance. Studies live inside their subject folders (for example, [gametypes/zeroplayerlevel/](../gametypes/zeroplayerlevel/)), so the repository can grow without a second subject taxonomy hidden under `research/`.

## Discover a study

[**catalog.yaml**](catalog.yaml) is the machine-readable registry. Its `path` and `index` fields are **relative to the repository root**; the stable `id` identifies a study independently of its location.

| Study | ID | Canonical document | Subject |
| --- | --- | --- | --- |
| [Zero-Player Level Design](../gametypes/zeroplayerlevel/README.md) | `RESEARCH-ZPL-001` | [metastudy.md](../gametypes/zeroplayerlevel/metastudy.md) | [gametypes](../gametypes/) |

## Evidence and applicability

- **Research:** evidence, historical comparisons, limitations, hypotheses and candidate patterns. Non-normative by default.
- **Implementation patterns:** suggested techniques and tests; adopt only with an explicit applicability decision.
- **Standards:** reusable normative baselines, such as the [UI/UX specification families](../uiuxs/); tailored project contracts remain authoritative within their own project.

Evidence classifications should distinguish directly sourced claims, independent corroboration, synthesis/inference, recommendations and unresolved questions. A creator's account, a peer-reviewed study, journalistic coverage and a community post have different provenance; none alone constitutes a universal confidence score.

## Consuming research

Audit the target project first; locate relevant studies using the catalog; record the **exact specdocz commit SHA**, study ID/version/path and specific source identifiers. For each technique decide **Adopt / Adapt / Reject / Extend**. Produce project-local normative text, tests and deviation reasoning. Never interpret a future update to `main` as automatically amending a pinned project contract.

See [CONTRIBUTING.md](CONTRIBUTING.md) for evidence, review and research-to-specification promotion. Start new studies from the [template](_templates/metastudy-template.md). Structural validation is not scholarly review or application qualification.
