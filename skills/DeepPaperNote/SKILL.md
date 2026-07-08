---
name: deeppapernote
description: Generate a high-quality deep-reading note for a single paper from a local PDF and write Markdown plus extracted images into the current workspace. Use when the user gives a local PDF path and wants a polished Markdown note with strong structure, evidence-based analysis, grounded figures, and reproducible local outputs.
---

# DeepPaperNote

Use this skill when the user wants one outcome:
- read one paper carefully
- generate a high-quality Markdown note
- save the note into the current workspace as Markdown plus image assets

Traditional Chinese trigger examples:
- `給這篇論文產生深度筆記`
- `寫一篇高品質論文精讀筆記`
- `把這篇文章整理成 md 筆記`
- `讀這篇論文並產生 md 筆記`

This skill is intentionally narrow:
- it handles one paper at a time
- it does not update daily reading lists
- it does not treat a shallow abstract rewrite as a successful output
- it does not split the public entrypoint into separate setup, troubleshooting, or start commands

## Core Standard

The finished note must be more than a summary. It should reconstruct the paper's argument:
- what problem it solves
- how the task is defined
- what data or materials it uses
- how the method or analysis actually works
- what results matter most
- what the paper does not prove
- why the paper is worth keeping

Default writer persona:
- a top-tier researcher or algorithm engineer
- writing a replication-oriented lab note
- not writing a popular-science explanation
- assuming the reader can follow Python, PyTorch, training loops, and evaluation logic

The note must adapt to the paper type. Use the same base structure, but shift emphasis for AI methods, benchmarks, clinical studies, and humanities or social-science papers.

## Workflow

Follow this order:
1. accept a local PDF path as the canonical source
2. extract canonical raw source text: `*_raw_sections.jsonl`, `*_source_manifest.json`, and optional derived `*_full_text.md`
3. extract structural indexes and PDF assets
4. plan figure placement
5. build the full figure/table decision table
6. build the manifest synthesis bundle
7. have the model read the bundle plus raw sections and plan the note
8. run grounding lint on the note plan before drafting from it
9. have the model write the note
10. inspect every inserted figure/table/algorithm candidate visually
11. if a kept placeholder has a known source page, retry with direct PDF recropping before finalizing the placeholder
12. lint the final note — if the lint output contains `passes_style_gate: false`, apply the Style Gate Enforcement rule before advancing to step 13, 14, or 15
13. perform `final_quality_review` after lint passes
14. perform `final_readability_review` after the quality review passes
15. write the Markdown note plus image assets into the local workspace

This is the required workflow for a normal single-paper note request, not a loose suggestion.
Unless this skill explicitly marks a stage as optional, required stages must not be silently skipped, reordered into a shortcut, or treated as complete just because a partial artifact already exists.

Global no-short-circuit rule:
- do not stop after only the early stages and present the workflow as finished
- do not treat slowness, inconvenience, or temporary uncertainty as permission to bypass a required stage
- do not replace the declared workflow with an improvised shortcut
- if a required stage fails, only do one of three things:
  - retry that stage
  - enter a fallback that is explicitly allowed by this skill
  - stop and report which stage is blocked and which downstream required stages remain incomplete
- do not describe the whole task as complete while required downstream stages are still pending

Completion-language rule:
- say `筆記已完成` only when the required workflow is actually complete
- say `已產生草稿` when drafting is done but lint, final readability review, or save is still pending
- say `已透過校驗` only when lint has actually been run and passed
- say `筆記已完成` only when the final local write step has actually succeeded and linked images exist
- do not treat `lint 已透過` as equivalent to `整篇筆記已經潤色完成`
- if final readability review is still pending, explicitly say the draft passed script lint but has not finished final language review
- if the workflow stopped early, name the current stage and the still-missing required stages instead of using completion language
- lint is a floor, not the writing objective

## Core Execution Contract

`SKILL.md` plus the generated `synthesis_bundle.json` must be enough to complete a normal note-generation run.
Files under `references/` are optional stage-specific deep dives, not a default reading checklist.

Non-negotiable rules:
- evidence-first: draft from the synthesis bundle, `source_manifest`, raw sections, coverage metadata, explicit `note_plan`, and inspected paper evidence; never finish from title/abstract/headings alone
- raw-source authority: for ordinary PDFs, `*_raw_sections.jsonl` and `*_source_manifest.json` are the canonical reading material; old top-N evidence buckets, truncated `section_texts`, and `candidate_chunks` are not model-facing writing inputs
- fail-closed: if a usable PDF or sufficient evidence cannot be obtained after supported acquisition paths, stop and ask for better source material rather than producing a finished degraded note
- model-first: scripts structure evidence, but the model must decide emphasis, contribution, mechanism, limitations, and final Traditional Chinese prose using Taiwan terminology
- output locale: the final note must be written in 繁體中文 with natural 臺灣用語; avoid simplified Chinese characters, Mainland-preferred wording, or mixed locale phrasing unless the source proper noun requires it
- explicit planning: before drafting, save a compact JSON `note_plan` such as `<note>.plan.json` or `*_note_plan.json`; pass it to `scripts/lint_note.py --plan-file ...`
- grounding gate: after the JSON `note_plan` exists, run `scripts/lint_grounding.py --note-plan ... --source-manifest ... --bundle-json ... --figure-decisions ...`; each substantive section must cite valid `section_id` values or valid page ranges
- required structure: include the canonical required sections, with `原文摘要翻譯` before `一句話總結` and a dedicated `創新點` section immediately after `原文摘要翻譯`
- abstract translation: when abstract metadata exists, `原文摘要翻譯` is a faithful Traditional Chinese translation of the original abstract in Taiwan wording, not a bilingual block and not the model's own summary
- mechanism depth: method, framework, and system papers should include `### 機制流程` under `方法主線`, normally as a 3 to 4 step numbered flow with input, operation, and output destination
- placeholder-first figures: plan major figure/table placeholders first; replace one only when identity match and visual usability are both strong; otherwise keep the placeholder
- final quality gates: lint is a floor; after lint passes, first run `final_quality_review` for analytical depth, then run `final_readability_review` for language polish, and rerun lint if either review edits the note
- local-workspace save: by default, write the final note to `raw/<note>.md`, write the note plan to `raw/<note>.plan.json`, and write extracted images to `img/<note>/`
- schema naming: prefer neutral field names such as `note_target`, `note_relative_path`, `note_match`, and `notes_root_*`; older `vault_*` or `obsidian_*` fields are compatibility aliases rather than the canonical contract

Reference usage policy:
- do not load every reference file by default
- consult `references/workflow.md` only for detailed data contracts or pipeline debugging
- consult `references/evidence-first.md`, `references/deep-analysis.md`, or `references/final-writing.md` only when the paper is complex or the draft is too shallow
- consult `references/figure-placement.md` only for ambiguous figure/table placement or image replacement decisions
- consult `references/obsidian-format.md` only for Markdown output, frontmatter, or reference-link formatting details
- consult `references/note-quality.md` or `references/paper-types.md` only for final review or domain adaptation
- consult `references/metadata-sources.md` only when metadata is incomplete, and `references/architecture.md` only for repository maintenance decisions

## Tool and Source Priority

Prefer the strongest available source in this order:
1. local PDF path given by the user
2. PDF front page metadata, `pdfinfo`, and body text
3. optional DOI or publisher metadata backfill when the local PDF is missing basic fields

Local-PDF-only rule:
- treat the local PDF path given by the user as the canonical source
- do not require Zotero, DOI resolution, arXiv lookup, or network PDF acquisition in the normal path
- do not let weaker title-only internet metadata override explicit evidence from the local PDF
- if DOI or venue metadata is missing, infer from the PDF front matter first and use external metadata only as a non-authoritative supplement

## Output Rules

- The default output is a Markdown note plus image assets written into the current workspace.
- The default flat output layout is:
  - `raw/<note>.md`
  - `raw/<note>.plan.json`
  - `img/<note>/...`
- Markdown image links should point to `../img/<note>/<filename>` when the note lives in `raw/`.
- Do not create a paper-local output folder unless the user explicitly asks for that layout.
- Real heading levels `#`, `##`, and `###` remain required.
- Every final note must start with a YAML properties block above the `#` title heading. Include at least a `tags` field and useful `aliases`; include `date`, `doi`, or `arxiv_id` when known, and omit unavailable fields rather than inventing placeholders.
- `## 核心資訊` must be a fixed metadata block only. Use only these fields, in this order, as `- 欄位名: 值` bullets: `標題`, `標題翻譯`, `作者`, `機構`, `發表時間`, `發表管道`, `DOI`, `arXiv`, `論文連結`, `程式碼 / 專案`, `資料 / 資源`, `論文型別`. Omit unavailable fields; put any guide sentence, takeaway, or analysis in `一句話總結` or a later section instead.
- The note should include `原文摘要翻譯` near the beginning when abstract metadata is available, before `一句話總結`.
- When abstract metadata is available, `原文摘要翻譯` should directly translate the original paper abstract into Traditional Chinese with Taiwan wording rather than restating it as your own summary.
- The `原文摘要翻譯` section itself should be Traditional-Chinese-only; do not place English abstract sentences or English paragraph excerpts in that section.
- Do not mix later judgments, innovation summaries, or hindsight explanations into `原文摘要翻譯`; keep it as the original abstract translated into Chinese.
- The note should include a dedicated `創新點` section immediately after `原文摘要翻譯` and before `一句話總結`.
- The `創新點` section should not be empty praise. It should enumerate the paper's actual innovations and briefly explain why each one matters.
- High-quality notes should usually contain multiple meaningful `###` subheadings in the technical sections when the paper is non-trivial.
- The note must include figure/table placeholders for all major visuals rather than silently skipping them.
- Every kept figure/table placeholder must appear directly under the most relevant analytical section named by its `建議位置`; do not collect unresolved placeholders in catch-all sections such as `剩餘圖表佔位` or `Remaining figures`.
- Every kept figure/table placeholder must use the standard `> [!figure]` callout format with `建議位置`, `放置原因`, and `當前狀態`; do not use ordinary paragraph markers such as `[圖表佔位 | Fig. 1]`, `圖表佔位：Table 2`, or `Figure Placeholder | Fig. 3`.
- Real images replace placeholders when they clearly match the corresponding paper figure/table and pass the visual-usability gate.
- Before keeping a placeholder in the final note, retry with direct PDF recropping whenever the source page is known and a clean crop may still be recoverable.
- When inserting a real image, render it as a Markdown image embed followed immediately by one italic caption line.
- Do not keep a redundant `> [!figure]` placeholder callout for the same inserted real figure.
- Figure captions in the note must preserve the original paper numbering such as `Fig. 1`, `Figure 1`, `Algorithm 1`, or `Table 2`.
- If a figure/table/algorithm candidate is marked usable and has a real image path, insert the real image. Do not keep a placeholder merely because the item is lower priority, supplemental, already summarized in text, or less central than another inserted figure.
- A kept placeholder is valid only when the image cannot be safely inserted because of a concrete visual defect, missing candidate, unresolved visual review, identity mismatch, contamination, or materialization/copy/write failure.
- When a candidate crop contains another figure body, a wrong caption, title-page material, or paragraph contamination, treat that as a visual defect and retry with a better crop before finalizing a placeholder.
- The final note must pass an image-existence check: every Markdown image link must resolve to a real local file before the task is complete.
- The final note must pass a figure-identity check: inserted image numbering and caption identity must match the figure/table/algorithm they claim to represent.
- The note must pass a style gate: no mixed Chinese-English prose lines except stable proper nouns or citation metadata.
- The note must also pass a locale gate: prefer Taiwan terminology and orthography consistently.
- If PDF or evidence quality is insufficient for a real deep note, fail closed: stop, report the blocked stage, and ask for the better PDF, OCR/source material, or other input needed to continue.

## Scripts

Use these bundled scripts rather than rebuilding the workflow from scratch:
- `scripts/check_environment.py`
- `scripts/create_input_record.py`
- `scripts/run_pipeline.py`
- `scripts/extract_source_text.py`
- `scripts/extract_evidence.py`
- `scripts/extract_pdf_assets.py`
- `scripts/plan_figures.py`
- `scripts/plan_figure_table_decisions.py`
- `scripts/build_synthesis_bundle.py`
- `scripts/lint_grounding.py`
- `scripts/lint_note.py`
- `scripts/materialize_note_figure.py`
- `scripts/write_note_output.py`

Preferred usage pattern:
1. accept the local PDF path as the trusted input
2. use `scripts/create_input_record.py` to materialize a trusted JSON input record when helpful
3. run `scripts/run_pipeline.py` on the local PDF path or input record to produce the bundle
4. read the bundle yourself
5. build a note plan that includes the research landscape and important reference papers
6. write the note in your own words
7. visually inspect every image you plan to insert
8. retry direct PDF recropping for any still-important placeholder with a known source page
9. lint the note and verify every image link before completion
10. write the final Markdown note plus image assets into the local workspace only after lint passes and the final readability review is complete

Python interpreter rule:
- DeepPaperNote requires Python `>=3.10`.
- Before running repository scripts, check the interpreter version instead of assuming the current shell default is compatible.
- If the default `python3` is below `3.10`, automatically look for another available interpreter that satisfies the requirement, such as `python3.12`, `python3.11`, `python3.10`, `/opt/anaconda3/bin/python3`, `/opt/homebrew/bin/python3`, or `/usr/local/bin/python3`.
- Use the first compatible interpreter you find and continue with that interpreter for the repository scripts in the current task.
- If no compatible interpreter is available, stop and clearly tell the user which interpreter was found, which version it reported, and that DeepPaperNote requires Python `>=3.10`.

Troubleshooting rule:
- use `scripts/check_environment.py` only when a concrete dependency or integration question is blocking execution
- explain required dependencies, optional enhancements, and downgrade behavior directly rather than redirecting the skill into a separate troubleshooting workflow
- do not feature environment inspection as a public pseudo-command surface

Current status:
- the single-paper deterministic core pipeline is implemented as an MVP
- `scripts/run_pipeline.py` now defaults to building a model-facing synthesis bundle
- the default local workflow should target `raw/` for notes and `img/` for images
- patch the scripts rather than replacing the workflow ad hoc

## Limits

- If the paper identity is ambiguous, confirm before writing.
- If the local PDF is unavailable or unreadable, stop and report what input is needed; do not produce a degraded, provisional, or abstract-only note as the finished output.
- Placeholder-first figure planning is required; image extraction is optional and must never reduce textual coverage.
