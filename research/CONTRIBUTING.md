# Research contribution and promotion guide

## Creating a research study

Copy [_templates/metastudy-template.md](_templates/metastudy-template.md) into a semantic subfolder. Add an entry to [catalog.yaml](catalog.yaml), a brief subfolder README, and a bibliography with stable source IDs. Place full original reference material in links/citations, not as copied copyrighted articles.

Choose a stable `RESEARCH-<DOMAIN>-NNN` ID. The *catalog* is the registry of identity and paths; an older imported document's original front matter may be preserved. Use the template's metadata for new studies.

## Evidence and review discipline

Every substantial finding should be marked as one of:

| Finding label | Meaning |
| --- | --- |
| `E` | Directly documented evidence, with source reference |
| `C` | Corroborated by independent sources, with citations |
| `I` | Explicit inference or synthesis; not direct measurement |
| `R` | Proposed engineering recommendation; not validated implementation |
| `U` | Unresolved/contradictory or unverified |

Keep separate: source **provenance** (primary creator, peer-reviewed research, journalism, community), source **quality**, claim **confidence**, and project **applicability**. Record search date and terms, selection method and exclusions, publication dates where known, links, study limits, counterexamples, and research gaps. Never relabel a narrative review as a systematic review/meta-analysis without a reproducible protocol and methods.

A study may be `draft`, `synthesis`, `reviewed`, or `superseded`. `reviewed` requires a documented substantive review; green CI alone does not establish factual accuracy. Do not erase older source-matched evidence when updating conclusions.

## Supporting documents and update rules

A study's `metastudy.md` is canonical. Adjacent `sources.md` and `patterns.md` are *indexes/extracts*, not independent authority. When copied source annotations change, regenerate the source index and ensure source identifiers remain stable. Avoid duplicating an entire study into overlapping variants. Preserve historical negative results.

## Promotion into a specification

1. Identify a specific `E/C/I/R/U` research claim, exact sources, and its limitations.
2. Audit target product constraints, performance, security, platforms and tests.
3. Classify as `Adopt / Adapt / Reject / Extend` and justify the disposition.
4. Draft explicit, testable normative text in a specification family or in the consuming repository; do not change the research document into a standard.
5. Review interaction with existing standards and evidence. Record acceptance criteria and provenance to the study ID, version/path and source commit.
6. Publish the new contract independently. Research remains a cited evidence record, not a source of silent requirements.

## Agent and maintainer checks

Before publication, run `python scripts/validate_research.py` from repository root (standard library only). Check relative links, canonical source IDs, bibliography URLs, catalog paths and front matter. Human review must also assess source claims, rights, misclassifications and factual uncertainty. A passing validator is **structural**, not scholarly or operational qualification.
