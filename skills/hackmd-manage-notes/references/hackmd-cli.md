# HackMD CLI Reference

Use the official `@hackmd/hackmd-cli` to reduce browser automation and return
structured output. Source:
[`hackmdio/hackmd-cli`](https://github.com/hackmdio/hackmd-cli), MIT License,
Copyright 2022 HackMD.

## Setup

```bash
npm install -g @hackmd/hackmd-cli
hackmd-cli login
hackmd-cli whoami
```

The user must create and enter their own API token. Alternatively, the CLI reads
`HMD_API_ACCESS_TOKEN`. Never expose or commit either the token or
`~/.hackmd/config.json`.

## Personal notes

```bash
hackmd-cli notes --output=json --columns=id,title
hackmd-cli notes --noteId=<id> --output=json
hackmd-cli notes create --parentFolderId=<folder-id> --title='Title' \
  --readPermission=owner --writePermission=owner
hackmd-cli notes update --noteId=<id> --content='# Updated'
hackmd-cli notes update --noteId=<id> --parentFolderId=<folder-id>
hackmd-cli export --noteId=<id>
```

Pipe long Markdown through stdin instead of embedding it in an argument:

```bash
hackmd-cli notes create --title='Title' < /tmp/note.md
hackmd-cli notes update --noteId=<id> < /tmp/note.md
```

Do not delete a note unless the user explicitly requests deletion.

## Personal folders

```bash
hackmd-cli folders --output=json --columns=id,name
hackmd-cli folders --folderId=<id> --output=json
hackmd-cli folders create --name='Docs'
hackmd-cli folders create --name='Child' --parentFolderId=<folder-id>
hackmd-cli folders update --folderId=<id> --name='Updated Docs'
hackmd-cli folders order
```

Do not delete or reorder folders unless explicitly requested.

## Team workspace

```bash
hackmd-cli teams --output=json
hackmd-cli team-notes --teamPath=<team-path> --output=json
hackmd-cli team-notes create --teamPath=<team-path> \
  --parentFolderId=<folder-id>
hackmd-cli team-notes update --teamPath=<team-path> --noteId=<id>
hackmd-cli team-folders --teamPath=<team-path> --output=json
```

## Permissions

Supported values:

| Flag | Values |
| --- | --- |
| `--readPermission` | `owner`, `signed_in`, `guest` |
| `--writePermission` | `owner`, `signed_in`, `guest` |
| `--commentPermission` | `disabled`, `forbidden`, `owners`, `signed_in_users`, `everyone` |

Map UI wording carefully:

- `owner`: only the owner.
- `signed_in`: signed-in HackMD users.
- `guest`: anyone with access to the link.

Do not infer permission changes from a content-edit request.

## Efficient output

Use these options to minimize context:

```bash
--output=json
--columns=id,title
--filter=title='Title'
--sort=title
--no-truncate
```

## Verification

After every create or update:

```bash
hackmd-cli export --noteId=<id>
```

Verify exact title or heading counts, required identifiers, plausible length,
balanced code fences, complete tail content, and preservation of unrelated
Markdown. Use Edge afterward only when Book Mode, custom URLs, conflicts, or
visual rendering must be checked.
