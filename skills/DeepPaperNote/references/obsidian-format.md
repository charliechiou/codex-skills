# Markdown Output Format

## Heading Rules

- Use `#` for the note title only.
- Use `##` for major sections.
- Use `###` only when a section genuinely needs internal structure.
- Do not flatten everything into bullet points.
- For method, system, benchmark, or clinical empirical papers, prefer meaningful `###` subheadings in technical sections instead of one long undifferentiated block.
- For method, framework, or system papers, default to `### 機制流程` inside `方法主線` and write it as a numbered 3 to 4 step flow.

## File Naming

Default file name:
- sanitized English title with underscores
- default local-workspace note layout is flat by top-level artifact type:
  - `raw/<paper_slug>.md`
  - `raw/<paper_slug>.plan.json`
  - `img/<paper_slug>/...`
- keep note files directly under `raw/`; do not create an extra paper-local note folder unless the user explicitly asks for that layout
- store extracted or materialized figure images under `img/<paper_slug>/`
- when deciding analytical domain tags or section emphasis, domain routing may still use the editable taxonomy in `references/domain_rules.yaml`, but domain choice should not force a nested output directory in the default workflow
- if the target output directory cannot be created, stop and report the write failure rather than omitting it

If the user already has a repository output convention, preserve it.

## Markdown Style

- Prefer short paragraphs over long bullet lists.
- Use bullets for metadata and sharply list-shaped content.
- Keep code or metric identifiers in backticks.
- When English proper nouns (model names, dataset names, method names, metric names, venue abbreviations) or standalone key numeric values appear inline within Chinese prose, wrap them in backticks for visual separation — e.g. `GPT-4`、`SQuAD`、`BLEU`、`87.3%`.
- Preserve stable internal links where useful.
- Use normal LaTeX delimiters for math:
  - inline math: `$...$`
  - display math:
    `$$`
    `...`
    `$$`
- Do not wrap formulas in backticks or fenced code blocks unless you are literally showing source code.

## Core Info Block

`## 核心資訊` is a fixed metadata zone.

Formatting and scope rules:
- Core info field schema: use only the following fields, in this order, and no free prose:
  `標題`, `標題翻譯`, `作者`, `機構`, `發表時間`, `發表管道`, `DOI`, `arXiv`, `論文連結`, `程式碼 / 專案`, `資料 / 資源`, `論文型別`
- keep each entry in `- 欄位名: 值` form
- omit fields that are unavailable or not applicable; do not add placeholder rows just to fill the schema
- do not add interpretation, commentary, judgment, or takeaway lines inside `核心資訊`
- do not use the last metadata bullet as a place to append extra analysis
- move explanatory content to `一句話總結`、`深度分析`、`我的筆記` or another true analysis section

## YAML Frontmatter

Every note must start with a YAML properties block **above** the `#` title heading.

Required fields:
- `tags`: use `papers/<domain>` hierarchy, e.g. `papers/NLP`, `papers/CV`, `papers/multimodal`
- `aliases`: English short name or common abbreviation for wikilink resolution
- `date`: ISO publication date; use `YYYY` if only the year is known
- `doi`: DOI string without the `https://doi.org/` prefix; omit the field entirely if unavailable

Example:

```yaml
---
tags:
  - papers/NLP
aliases:
  - "Paper Short Name"
date: 2024-05-01
doi: 10.18653/v1/2024.acl-long.1
---
```

Rules:
- Do not invent placeholder values for missing fields; omit them instead.
- The `tags` field must always be present with at least one `papers/<domain>` tag.
- `aliases` should be the paper's short name or acronym (e.g. "GPT-4", "LoRA"), not a paraphrase.

## Figure Placeholder Style

Use this callout format only for placeholders that remain unresolved in the final note:

```md
> [!figure] Fig. 3 資料分佈與品質評估
> 建議位置：資料與任務定義
> 放置原因：這張圖同時展示樣本構成、對話長度統計和專家品質檢查結果，是理解 `PsyInterview` 資料邊界最重要的圖之一。
> 當前狀態：保留佔位；當前提取結果只拿到區域性子圖，無法穩定還原成可獨立解釋的完整原圖。
```

Formatting rules:
- keep the original paper numbering, for example `Fig. 3` or `Table 2`
- keep a short human-readable label on the first line
- always include `建議位置`
- always include `放置原因`
- always include `當前狀態`

`當前狀態` should be explicit, for example:
- `保留佔位；未找到高置信度整圖。`
- `保留佔位；當前只匹配到疑似區域性子圖，不足以穩定替換。`

The structured `[FIGURE_PLACEHOLDER] ... [/FIGURE_PLACEHOLDER]` block is legacy/internal only.
Do not use it in the final user-facing note unless you are debugging the pipeline.

If a real image has been selected and materialized into the local image directory, do not keep the `[!figure]` callout for that same figure.
Use a Markdown image embed with a stable relative path.
The embed must be followed immediately by exactly one italic caption line:

```md
![Fig. 2 資料產生流程圖](../img/paper_slug/page_003_img_01.png)
*論文原圖編號：Fig. 2。資料產生流程圖。這裡插入是因為它最能幫助理解方法主線。*
```

## Default Section Order

1. `核心資訊`
2. `原文摘要翻譯`
3. `創新點`
4. `一句話總結`
5. `研究問題`
6. `資料與任務定義`
7. `方法主線`
8. `關鍵結果`
9. `深度分析`
10. `侷限`
11. `我的筆記`
12. `引用`

When abstract metadata exists, `原文摘要翻譯` should be a single Chinese translation block for the original abstract rather than a bilingual subsection pair.

This order is the stable backbone, not a full outline.
When the paper is complex, add `###` subsections such as:
- `### 資料來源`
- `### 任務定義`
- `### 機制流程`
- `### 為什麼結果成立`
- `### 哪些地方容易被誤讀`

## 引用 Section Format

Entries in `## 引用` should be plain-text citations unless the user explicitly maintains a local note-linking convention.
If the synthesis bundle includes `references.candidates`, use confirmed candidate `wikilink` values when present. When `wikilink` is empty, treat `display_text` as the plain-text fallback.
Follow this priority order for each reference:

1. **Plain-text citation first**: record a stable citation entry even when no local note-link exists.
   - Match by note basename (the `<paper_slug>` part of the folder name).
   - Match by the `aliases` field in the note's YAML frontmatter.
2. **If a match is found**: write a wikilink that separates the target from the display text:
   ```
   - [[paper_slug_or_alias|Human Readable Title]]
   ```
3. **If no match is found**: do not invent a wikilink target. Write the reference as plain text instead:
   ```
   - Vaswani et al. (2017). Attention Is All You Need.
   ```
   Use the candidate `display_text` as the plain fallback when available.

Rules:
- Do not depend on vault-specific wikilink targets in the default local-PDF workflow. Prefer plain-text citations or confirmed local links that still make sense after the note is moved inside an ordinary workspace.
- To derive a likely slug from a title: lowercase the title and replace spaces and special characters with underscores — but only use the result as the target if you have confirmed the file exists.
- List only papers cited or directly relevant to this note.
- Do not add extra DOIs or author metadata when using wikilink format; the display text is enough.
