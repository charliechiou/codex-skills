@AGENTS.md

## Claude Code Integration

The root `SKILL.md` is both the canonical workflow definition and the Claude Code skill entrypoint.
There is no separate Claude Code wrapper — `SKILL.md` is loaded directly when the skill is invoked.

- Do not fork or restate the DeepPaperNote workflow in any Claude-only file.
- All workflow logic stays in the root `SKILL.md`.

### Skill Invocation

End users running Claude Code invoke the skill with natural language or the
`/deeppapernote` slash command. Recognized trigger examples:
- `給這篇論文產生深度筆記`
- `寫一篇高品質論文精讀筆記`
- `把這篇文章整理成 obsidian 筆記`
- `/deeppapernote <paper title, DOI, arXiv ID, or local PDF path>`
