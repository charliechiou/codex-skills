# HackMD CLI Reference

Use the official `@hackmd/hackmd-cli` to reduce browser automation and return
structured output. Source:
[`hackmdio/hackmd-cli`](https://github.com/hackmdio/hackmd-cli), MIT License,
Copyright 2022 HackMD.

## Setup

```bash
npm install -g @hackmd/hackmd-cli
export HMD_CLI_CONFIG_DIR=/tmp/hackmd-cli-config
export HMD_API_ACCESS_TOKEN=YOUR_TOKEN
hackmd-cli whoami
```

Prefer `HMD_API_ACCESS_TOKEN` over interactive `hackmd-cli login`. In constrained
shells, `login` may fail because it depends on an interactive prompt, and some
environments do not allow writing `~/.hackmd/config.json`. When a config
directory is needed, set `HMD_CLI_CONFIG_DIR` to a writable path such as
`/tmp/hackmd-cli-config`.

The user must create and manage their own API token. Never expose or commit the
token, shell history containing the token, or any generated config file.

## Known environment issues

- Interactive `hackmd-cli login` can fail in shells where `read -s` is not
  supported.
- `hackmd-cli whoami` and other commands can fail if they try to create
  `~/.hackmd` under a read-only home directory.
- `HMD_API_ACCESS_TOKEN` plus a writable `HMD_CLI_CONFIG_DIR` avoids both
  failure modes and should be the default workflow.

## Authentication check

Use a writable config directory even when authenticating entirely by
environment variable:

```bash
export HMD_CLI_CONFIG_DIR=/tmp/hackmd-cli-config
export HMD_API_ACCESS_TOKEN=YOUR_TOKEN
hackmd-cli whoami
```

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
