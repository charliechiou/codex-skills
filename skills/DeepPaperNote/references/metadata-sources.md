# Metadata Sources

Use the strongest available source first, but backfill aggressively.

## Preferred Order

1. user-provided exact source
2. PDF front page metadata and `pdfinfo`
3. DOI resolution and publisher metadata
4. Semantic Scholar
5. OpenAlex
6. arXiv metadata

## Required Fields to Attempt

- title
- authors
- affiliations
- year
- venue
- DOI
- source URL

## Optional Fields

- abstract
- code URL
- project URL
- citation counts
- arXiv ID

## Rules

- Treat explicit evidence from the local PDF as stronger than title-only internet metadata.
- Use external metadata only to fill missing venue, DOI, or year fields when the PDF itself is incomplete.
- Do not invent missing metadata.
- If a Chinese title is assistant-generated, mark it as a translation.
- Distinguish:
  - `not found`
  - `not provided by source`
  - `ambiguous`
