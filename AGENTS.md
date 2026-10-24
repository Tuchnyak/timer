# AGENTS.md

Pomodoro timer with Plans (pre-designed queues of sessions) and Flow mode. Desktop app for Linux.

- Requirements and decisions: [docs/spec.md](docs/spec.md)
- Stage order and backlog: [docs/roadmap.md](docs/roadmap.md)

## Stack

Python 3.12 · Tkinter + ttkbootstrap · SQLite (`sqlite3`) · uv · pytest · PyInstaller (last stage).

## Commands

```
uv sync            # set up .venv from uv.lock
uv run timer       # run the app
uv run pytest      # run tests
uv add <pkg>       # add a dependency (--dev for tooling)
```

## Layout

- `src/timer/` — application package; entry point `timer.app:main`.
- `tests/` — pytest tests, mirroring `src/` (e.g. `tests/timer/test_logic.py`).
- `docs/` — project documentation, in English.

## Rules

- Implement only what `docs/spec.md` describes, stage by stage per the roadmap. No extra features, options or abstractions; propose them instead.
- Keep timer logic out of UI code and cover it with tests.
- Use ttk widgets; classic `tk` widgets only where ttk has none (e.g. `Canvas`).
- Every UI string goes through the `t(key)` localization helper.
- All data lives in the one SQLite database described in the spec.
- Code, comments and docs in English.
- When the owner says they are learning something, explain and give commands for them to run; do not make the changes yourself.
