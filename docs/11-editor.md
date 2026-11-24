# 11. Editor

`pfc2 lsp` is a language server: it speaks the Language Server Protocol over standard input and output, so
any editor that supports the protocol can show PFC2's results while you type.

## What you see

| In the editor | Meaning |
| --- | --- |
| Red underline | an obligation that is not proved, with the formula and, when the solver found one, a counterexample; or a source error with its rule |
| Yellow underline | at level `memory`: arithmetic whose overflow is not proved; the emitted C keeps a runtime trap there |
| Hint on a loop | the invariant PFC2 inferred and proved; or "termination is not claimed" when the loop has no `decreases` |
| Hover on a function name | its contract and how many of its obligations are proved |
| Hover on `while` / `for` | the inferred invariant and whether the loop is proved to terminate |
| Hover on an array access or operator | whether its check was removed by a proof or is kept |
| Outline | functions, laws and globals |

A file that does not contain `#include "pfc.h"` is ignored, so ordinary C sources are left alone.

The server checks a file a moment after you stop typing. It uses the same path as `pfc2 check`, with a fixed
integer layout (32-bit `int`, 64-bit `long`) and, by default, a 3-second solver budget per obligation so that the
editor stays responsive; a result that needs longer shows as not proved with status `timeout`.

## VS Code

The extension lives in `editors/vscode`.

```console
$ cd editors/vscode
$ pnpm install
$ pnpm run compile
$ code --extensionDevelopmentPath="$PWD" ../../examples
```

Open `wrong/off_by_one.c`: the write `a[i] = value` is underlined, and the message ends with `n = 0, value = 0,
i = 0`. Change `i <= n` to `i < n` and the underline goes away.

If `pfc2` is not on your `PATH`, point the extension at the checkout in your settings:

```json
{
  "pfc2.command": ["uv", "run", "pfc2", "lsp"],
  "pfc2.cwd": "/path/to/pfc2"
}
```

| Setting | Default | Meaning |
| --- | --- | --- |
| `pfc2.command` | `["pfc2", "lsp"]` | command that starts the server |
| `pfc2.cwd` | workspace folder | working directory for that command |
| `pfc2.level` | `full` | `memory` turns unproved overflow into a warning |
| `pfc2.timeoutMs` | `3000` | solver budget per obligation |

## Other editors

Run `pfc2 lsp` as a stdio server for C files and pass `{"level": "full", "timeoutMs": 3000}` as initialization
options. For example, in Neovim (a sketch; not part of the tests):

```lua
vim.lsp.start({
  name = "pfc2",
  cmd = { "pfc2", "lsp" },
  root_dir = vim.fn.getcwd(),
  init_options = { level = "full", timeoutMs = 3000 },
})
```

## What has been checked

The analysis behind the server is tested on the examples with positions counted by hand
(`tests/test_lsp_analysis.py`), and one test talks to the real server process over stdio: open a wrong file,
read the diagnostics, hover, list symbols, fix the file, see the errors go (`tests/test_lsp_server.py`). The VS
Code extension compiles; it has not been exercised inside a running VS Code as part of the tests.
