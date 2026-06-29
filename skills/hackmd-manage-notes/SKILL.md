---
name: hackmd-manage-notes
description: Manage HackMD notes and folders with Microsoft Edge through Playwright. Use when Codex needs to read, create, update, move, organize, or verify notes in HackMD while preserving Markdown and writing style; create or verify Book Mode; manage custom share links; resolve editor conflicts; or verify server persistence.
---

# HackMD Note Manager

Use Microsoft Edge through Playwright for all HackMD operations. Treat the
server-saved Markdown as the source of truth and preserve unrelated content.

## Required browser workflow

1. Read and use the `playwright` skill for all browser operations.
2. Open HackMD with headed Microsoft Edge and a persistent profile:
   `--browser msedge --headed --persistent`.
3. Prefer the user's existing Edge profile when an authenticated workspace is
   required. If HackMD is logged out, leave the browser at the login page and ask
   the user to sign in manually. Never request, read, or enter their password.
4. Take a fresh snapshot before using element references and after navigation,
   dialogs, folder changes, editor mode changes, or reloads.
5. Use browser navigation, workspace search, and folder views to locate notes.
   Do not use `hackmd-cli`.
6. Keep the Edge window open unless the user asks to close it.

## Locate the target

- For this user's note-update tasks, only operate on notes inside the `Codex`
  folder. If the resolved note is outside `Codex`, stop and ask the user before
  making any change.
- In Edge, navigate through the workspace and requested folder rather than
  relying on a title-only global search when duplicate note names are possible.
- Confirm both the folder and exact note title before editing.
- For an existing note, inspect the relevant surrounding sections and the full
  document outline. Match its language, heading depth, prose density, code-block
  style, dates, and attribution conventions.
- If the requested target remains ambiguous after inspecting the workspace, ask
  the user before changing anything.

## Create a note

1. Open the destination folder in Edge before creating the note.
2. Set the exact requested title and permissions.
3. Confirm the note is listed in the intended folder. If it is elsewhere, move
   it with normal workspace controls in Edge.
4. Write Markdown that follows any nearby project notes when the user requests a
   matching style.
5. Follow the safe editing and verification procedures below.

## Write for the intended reader

- Treat the user's stated audience and technical background as a hard
  requirement. If they do not specify an audience for technical documentation,
  default to a beginner who is new to the domain.
- Explain each important code block and the role of its significant declarations,
  fields, control flow, constants, and function calls. Connect each code fragment
  to the larger execution or data flow.
- Define domain terms before relying on them, explain why the implementation is
  needed, and distinguish current behavior from limitations or future work.
- Focus beginner-oriented explanations on the document's actual technical
  domain. Do not reteach basic programming-language syntax unless the user asks
  for it or the syntax is essential to understanding the design.
- Include concrete input/output or command examples and a safe way to verify the
  result. Do not merely list changed files or paste code without explaining it.
- Match the existing note's style without copying its assumed knowledge level
  when the requested reader needs more foundational explanation.

## Update a note safely

Before changing content:

1. Read the current Markdown from CodeMirror.
2. Record its length and identify a unique insertion or replacement marker.
3. Confirm the marker count is exactly one. Do not replace content using a
   non-unique heading or phrase.
4. Preserve the original source in memory until server verification succeeds.

Choose the narrowest edit:

- Append a new change-log section at the document end when documenting new work.
- For this user's documentation sync or progress updates, default to appending a
  dated change-log entry instead of rewriting the main body unless the user
  explicitly asks for a section rewrite.
- Change-log entries should describe technical behavior, interfaces, data flow,
  constraints, or design intent. Do not use them to record routine README
  syncing, pushes, tool installation, or the agent's work log.
- Replace only the requested section when revising existing documentation.
- Do not rewrite the entire note merely to add a section.

Do not use `playwright-cli type`; per-character typing can trigger CodeMirror
indentation and auto-completion and corrupt the document. Focus the hidden
CodeMirror textarea with `eval`, then update the CodeMirror document atomically.
Derive the new value from the current value and the verified unique boundary.
Use `setValue` only when creating an empty note or when the complete preserved
source is included; otherwise prefer a bounded `replaceRange`.

After the edit, verify in the editor before waiting for sync:

- expected title or heading exists;
- insertion marker appears once;
- required identifiers, dates, links, or commit hashes exist;
- document length is plausible;
- the tail is complete and code fences are balanced;
- unrelated leading content remains unchanged.

## Handle synchronization conflicts

If HackMD reports an offline version or merge conflict:

1. Open **Merge and sync** and compare the offline and current versions.
2. Identify which side contains the complete intended edit and whether the other
   side has unrelated newer work.
3. Apply the offline changes only when they are the verified complete edit and
   do not discard unrelated server changes.
4. Discard the offline changes when the server version is authoritative, then
   reapply the bounded edit to the latest source.
5. If both sides contain independent changes or the correct resolution is not
   clear, stop and ask the user.
6. Finish the merge dialog and confirm the offline/conflict banner disappears.

Never select a conflict-resolution action merely to dismiss the dialog.

## Verify server persistence

1. Wait for HackMD's save state to settle and reload the page so the editor
   reads the server version again.
2. Re-read the server Markdown from the page and repeat the structural checks.
3. Confirm there is no offline-edit or conflict banner.
4. Report completion only after the post-reload source contains the intended
   content exactly once.

## Safety boundaries

- Do not delete notes or folders unless the user explicitly asks.
- Do not change sharing, publishing, permissions, ownership, or team membership
  unless explicitly requested.
- Do not expose note contents, authentication state, or private URLs beyond what
  is necessary for the task.
- Do not resolve ambiguous concurrent edits without user confirmation.
