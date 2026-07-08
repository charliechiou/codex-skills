<div align="center">

# DeepPaperNote

**Turn a local paper PDF into a deep-reading Markdown note with grounded figures.**

[English](./README.md) | [繁體中文](./README.zh-CN.md)

[![Homepage](https://img.shields.io/badge/homepage-online-2563eb)](https://917dhj.github.io/DeepPaperNote/)
[![Status](https://img.shields.io/badge/status-stable-16a34a)](https://github.com/917Dhj/DeepPaperNote)
[![Release](https://img.shields.io/github/v/release/917Dhj/DeepPaperNote?display_name=tag&color=0f766e)](https://github.com/917Dhj/DeepPaperNote/releases/tag/v2.0.0)
[![License](https://img.shields.io/badge/license-MIT-c9a227)](./LICENSE)
[![Agents](https://img.shields.io/badge/agents-Claude%20Code%20%2B%20Codex-7c3aed)](./SKILL.md)
[![Output](https://img.shields.io/badge/output-workspace%20markdown-16a34a)](./SKILL.md)
[![Figures](https://img.shields.io/badge/figures-captioned%20images-f59e0b)](./references/figure-placement.md)
[![Writing](https://img.shields.io/badge/writing-evidence--first-7c3aed)](./references/model-synthesis.md)

</div>

[![DeepPaperNote Hero](./assets/hero-academic.svg)](https://917dhj.github.io/DeepPaperNote/)

DeepPaperNote is a skill for **deep paper reading from a local PDF**. It is designed for the workflow where you give the agent a concrete PDF path and want a durable Markdown note plus extracted figures in your current workspace.

It is not a generic paper-summary bot. The target is a note that preserves:

- the paper's actual research problem
- method structure and technical mechanism
- key figures with captions and correct identity
- important experiments, limitations, and boundary conditions
- the paper's place relative to prior work

## What It Produces

For one input PDF, DeepPaperNote writes three kinds of artifacts into the current workspace:

- `raw/<note>.md`
- `raw/<note>.plan.json`
- `img/<note>/...`

Default expectations:

- the note is Markdown and written in Traditional Chinese with Taiwan wording
- figure images live under `img/<note>/`
- figure links inside the note point to those local image files
- figures should include captions when available
- placeholders are only acceptable after real extraction or recropping attempts fail

## Default Input Model

The **normal path** is:

- you provide a local PDF path
- the PDF is treated as the canonical source of truth
- metadata is derived from the PDF first
- external metadata is only supplementary when the PDF is incomplete

Compatibility inputs such as title, DOI, arXiv ID, or URL may still be supported in some environments, but they are not the primary workflow this skill is now optimized for.

## Quick Start

### 1) Install the skill

```bash
npx skills add 917Dhj/DeepPaperNote
```

Or install for a specific agent:

```bash
npx skills add 917Dhj/DeepPaperNote -a codex
npx skills add 917Dhj/DeepPaperNote -a claude-code
```

### 2) Install the PDF runtime dependency

```bash
python3 -m pip install PyMuPDF
```

### 3) Use it with a local PDF

Typical prompts:

- `Use DeepPaperNote on /absolute/path/to/paper.pdf`
- `Read /absolute/path/to/paper.pdf and generate a deep-reading note`
- `幫我用 DeepPaperNote 整理這個 PDF：/absolute/path/to/paper.pdf`

## Output Contract

A successful run should generally satisfy the following contract:

- one note per paper under `raw/`
- one note-local image directory under `img/`
- stable relative image links from note to figure files
- evidence-backed section writing rather than abstract paraphrase
- explicit handling of missing evidence, ambiguous claims, and extraction failures

If a figure is inserted as a real image, it should be the correct figure, not just a visually convenient crop from the same page.

## Note Shape

The generated note is expected to cover at least these areas:

- core metadata
- research problem
- what existing research already does
- important reference papers related to the current paper
- method / mechanism
- experiments and key results
- limitations
- takeaways
- references cited by the paper when they are important to understanding the work

The `研究問題` section should not only restate the target paper's goal. It should also explain the existing line of research and record important reference papers that define the baseline, predecessor, or contrast position for the current work.

## Figure Policy

DeepPaperNote is image-first, but not image-naive.

- prefer real extracted or recropped images over placeholders
- keep captions with figures whenever possible
- verify figure identity against the surrounding text and caption
- if the extracted object is wrong, contaminated, truncated, or mismatched, retry with direct page recropping before giving up
- only keep placeholders when a real usable figure still cannot be recovered

## Configuration

Minimal configuration is enough for the default workflow.

- `PyMuPDF` is required for the normal PDF extraction path
- the current workspace is the default output target
- no Obsidian vault, Zotero library, DOI lookup, or paper database is required for the normal path

## Schema Stability

Canonical field names now follow the neutral local-workspace model. Prefer these names in new integrations:

- `note_target` instead of `vault_target`
- `note_relative_path` instead of `vault_relative_path`
- `note_match` instead of `vault_match`
- `notes_root_relative_image_path` and `notes_root_wikilink_embed` instead of Obsidian-specific image fields
- `notes_root` or `--notes-root` instead of assuming an Obsidian vault

Deprecated compatibility fields still exist for older consumers, but they should be treated as aliases only:

- `vault_target`
- `vault_relative_path`
- `vault_relative_image_path`
- `obsidian_embed`
- `configured_root_relative_image_path`
- `root_relative_wikilink_embed`
- `--vault` and `DEEPPAPERNOTE_OBSIDIAN_VAULT`

## When To Use This Skill

Use DeepPaperNote when:

- you already have the paper PDF locally
- you want a note that is stronger than a polished summary
- you care about method details, figure grounding, and experiment interpretation
- you want workspace-local Markdown artifacts that can be reviewed or versioned directly

## Current Positioning

DeepPaperNote is now optimized around a **local PDF -> workspace Markdown** workflow. If you maintain extra personal systems such as Obsidian, Zotero, or a paper database, those can be treated as optional downstream integrations rather than core assumptions.
