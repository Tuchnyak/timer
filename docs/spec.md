# Timer — Specification

Pomodoro timer for tracking work sessions, run on a dedicated second laptop.
This document records the agreed requirements and decisions. Stage order lives in [roadmap.md](roadmap.md).

## 1. User and goal

The first user is the author. The timer stays open on a second laptop and shows:

- which session is running now, of which type (project), and how much time is left;
- how the planned "budget" of sessions is going: how many are done, skipped, and ahead.

Sessions are grouped into **Plans** that are designed in advance and started in one action, like putting a playlist into a play queue. A plain endless pomodoro (**Flow**) is also available.

## 2. Glossary

| Term | Meaning |
|---|---|
| **Session** | A work interval of one session type. |
| **Break** | A short or long rest interval. Breaks are never placed by hand (see §5). |
| **Stage** | Any timed interval: a session or a break. |
| **Session type** | A user-defined category (project) with a name and a color, e.g. "Work", "Personal". |
| **Plan** | A saved sequence of sessions: rows of "type × count", repeated N times, with optional timer overrides. |
| **Plan run** | One execution of a plan, based on a snapshot of the plan taken at start. |
| **Flow** | Endless mode: session → break → session … until stopped. One session type for the whole flow. |

## 3. Session types

- The user manages the list: create, rename, change color (color picker dialog), archive.
- Names are unique.
- `None` is a system type: always present, cannot be renamed, archived or deleted.
- Types are **archived, never deleted**. An archived type:
  - is hidden from type selection in the plan editor and the flow start;
  - keeps its name and color in history.
- A type **cannot be archived while any plan uses it**. The UI says which plans use it.

## 4. Timer settings

### 4.1 Global settings

| Setting | Default |
|---|---|
| Session length | 25 min |
| Short break length | 5 min |
| Long break length | 15 min |
| Long break interval N (long break after every N sessions) | 4 |
| Transition mode | Wait for confirmation |
| Blink current circle | On |
| Theme | Dark |
| Sound notifications | On (available from the sound stage) |

Durations are whole minutes.

### 4.2 Plan overrides

A plan may override all four timer parameters: session length, short break length, long break length, interval N. Without an override the global values apply. The transition mode is global only.

### 4.3 Transition modes

What happens when a stage ends. Each mode is shown in Settings with a short explanation for the user:

| Mode | User-facing explanation |
|---|---|
| **Auto-start** | "The next stage starts automatically." |
| **Wait for confirmation** | "The timer stops after each stage and waits until you press Next." |
| **Mixed** | "Breaks start automatically. Work sessions wait for you, so time doesn't run while you're away." |

While waiting, the main screen shows what comes next (e.g. "Next: Work · Session 4/6") and a **Next** button (`Enter`).

## 5. Break rules

The same rules apply to Flow and Plans:

- a **short break** follows every session;
- a **long break** replaces the short break after every N-th session (strictly by N, also inside plans — to align long breaks with plan repetitions, override N in the plan);
- in a plan, **no break follows the last session**.

## 6. Flow mode

- Endless cycle of sessions and breaks by the global rules until the user stops it.
- Before start the user picks a session type. Preselected: the type of the previous flow, or `None` if there was none.
- Instead of the circle row the screen shows a session counter.

## 7. Plans

### 7.1 Structure

- A plan has a name, an ordered list of **rows** (session type + number of consecutive sessions), a **repeat count** for the whole list, and optional timer overrides (§4.2).
- Example: rows `Work × 2`, `Personal × 1`, repeat `× 2` → 6 sessions.

### 7.2 Plan editor

```
┌ Edit plan ─────────────────────────────────────────┐
│ Name: [ Work day                               ]   │
│                                                    │
│      Type                 Sessions                 │
│  1   ■ [ Work       ▾ ]   [ 2 ▴▾ ]   [↑] [↓] [✕]  │
│  2   ■ [ Personal   ▾ ]   [ 1 ▴▾ ]   [↑] [↓] [✕]  │
│  [+ Add row]                                       │
│                                                    │
│  Repeat:  [ 2 ▴▾ ] ×                               │
│                                                    │
│  Preview:  ○ ○ ○ ○     ○ ○                         │
│            6 sessions · ~3h 05m                    │
│                                                    │
│  ▸ Timer settings (override global)                │
│                                                    │
│                 [Cancel]  [Save]  [Save & start]   │
└────────────────────────────────────────────────────┘
```

- Each row: color swatch of the type, type selector, session count, move up/down, delete.
- **Preview** updates live: the same circle row as in the running timer (§9), with gaps where long breaks fall.
- **Total duration**: all sessions plus the breaks between them (no break after the last session), using the effective timer settings.
- **Timer settings** is a collapsed section with the four overrides; collapsed means "global settings are used".
- **Save & start** saves the plan and starts a run immediately.

### 7.3 Plans screen

List of saved plans: create, edit, delete (with confirmation), start.

### 7.4 Running a plan

- Only **one plan run** at a time. No queue of plans.
- Starting a run takes a **snapshot** of the plan. Editing the plan during a run is allowed; changes apply from the next run. The current run, resume (§10) and history use the snapshot.
- When the last session ends, the run finishes immediately and shows a summary, e.g. "Plan complete: 5 done, 1 skipped". Then the timer returns to idle.

## 8. Controls

### 8.1 During a stage

| Control | Behavior |
|---|---|
| **Pause / Resume** | No time limit. Paused time is not counted as worked time. |
| **Skip** | Ends the current stage early and moves to the next one. No confirmation. |
| **Stop** | Ends the whole plan run or flow. Asks for confirmation. |

### 8.2 Hotkeys

| Key | Action |
|---|---|
| `Space` | Pause / Resume; Start when idle |
| `Enter` | Next, when waiting for confirmation |
| `F11` | Toggle fullscreen |
| `Esc` | Exit fullscreen; back from a secondary screen |

Skip and Stop have no hotkeys on purpose: an accidental press is too costly.

## 9. Plan progress visualization

A row of circles, one circle per session of the run. Short breaks are not shown.

| State | Look |
|---|---|
| Done | Filled with the type color |
| Skipped | Muted (faded) fill of the type color |
| Current | Theme accent color; blinks (can be turned off in Settings) |
| Future | Outline in the type color |

A long break is shown as a gap two empty circles wide, so sessions are visually grouped between long breaks.

## 10. Resume after interruption

- The run state is saved to the database at every stage transition.
- If the app was closed during a plan run (crash, reboot, closed window), on next start it asks: "Resume plan "X" from session 4 of 6?".
  - **Yes**: the run continues; the interrupted session starts again from the beginning.
  - **No**: the run is ended as stopped.

## 11. Main window

```
┌ Timer ─────────────────────────────────────────┐
│ [Plans] [Types] [History] [Settings]      [⛶]  │
│                                                │
│                 WORK · Session 3/6             │
│                                                │
│                    18:42                       │
│                                                │
│            ●  ●  ◉     ○  ○  ○                 │
│                                                │
│        [⏸ Pause]   [⏭ Skip]   [⏹ Stop]         │
└────────────────────────────────────────────────┘
```

Idle state, instead of the controls:

```
   ( ) Flow   type: [ Work ▾ ]
   (•) Plan:  [ Work day ▾ ]
                 [ ▶ Start ]
```

- The center shows the stage (`WORK`, `SHORT BREAK`, `LONG BREAK`; for sessions — the type name), the session number, a large countdown and the circle row (plan) or session counter (flow).
- Plans, Types, History and Settings open **inside the main window** with a Back button. No secondary windows.
- One layout that **scales with the window**: the countdown and fonts grow with the window size.
- **Fullscreen board** (`[⛶]` / `F11`): only the stage, the countdown and the progress; controls are hidden, hotkeys keep working. `Esc` exits.
- The window remembers its size and position between launches.

## 12. Themes

- Six built-in themes: Light, Dark, Catppuccin Latte, Catppuccin Frappé, Catppuccin Macchiato, Catppuccin Mocha.
- Selected in Settings, applied immediately. The OS theme is not followed.
- The theme provides the accent color (current circle) and neutral colors; session type colors are the user's own.
- A theme editor is in the backlog (see roadmap).

## 13. History

### 13.1 What is recorded

Every stage — sessions **and** breaks — of every plan run and flow:

- kind (session / short break / long break), session type;
- start and end time;
- planned duration, actual duration (pauses excluded);
- status: `completed`, `skipped`, `stopped` (run stopped during the stage), `interrupted` (app closed during the stage; actual duration unknown);
- the run it belongs to: plan run (with the plan name from the snapshot) or flow.

### 13.2 History screen

- Toggle Day / Week (week starts on Monday), previous/next navigation.
- List of **sessions** with type color, type name, start time, actual duration and status.
- Totals of actual time per session type for the selected period.
- Breaks are stored in the database but not shown on this screen.

### 13.3 Own analysis

The database schema is documented so the user can query history directly (`sqlite3`, DBeaver, Python).

## 14. Sound

- A calm, unobtrusive sound on every stage transition.
- One global on/off switch.
- Tkinter has no cross-platform audio; the playback method (library or a system command such as `paplay`) is chosen at that stage.

## 15. Localization

- All UI strings go through one lookup function, e.g. `t("plan.start")`.
- English only for now, stored as one dictionary/file of keys. Adding a language = adding a file with the same keys.
- No OS locale detection, plural rules or `gettext` until a second language exists. The language setting appears only then.

## 16. Data storage

Everything is stored in one SQLite database (`sqlite3` from the standard library):
`$XDG_DATA_HOME/timer/timer.db`, by default `~/.local/share/timer/timer.db`.

It holds settings, session types, plans, the state of the current run and history. The final schema is defined in stage 1 and documented in `docs/`. Indicative entities:

| Entity | Content |
|---|---|
| `setting` | key → value |
| `session_type` | name, color, system flag, archived flag |
| `plan`, `plan_row` | name, repeat count, overrides; rows: position, type, count |
| `run` | plan or flow, plan snapshot, start/end, status |
| `stage` | run, position, kind, type, planned/actual duration, start/end, status |

## 17. Technical constraints

- Linux only. Other OS builds are out of scope for now.
- Python 3.12, Tkinter + ttkbootstrap, ttk widgets only (classic `tk` widgets only where ttk has no equivalent, e.g. `Canvas`).
- uv for dependencies and running; `src/` layout; entry point `timer = "timer.app:main"`.
- Timer logic is kept separate from the UI and covered by pytest tests.
- Packaging (PyInstaller) and CI come last.

## 18. Explicitly not doing

Not part of the product unless a real need appears (see roadmap backlog for the deferred ones):

- restart the current stage, "+5 minutes";
- a queue of plans;
- per-plan transition mode; per-type session length;
- nested groups in plans; breaks placed by hand;
- always-on-top window, tray icon, desktop notifications;
- following the OS theme.

## 19. Assumptions to confirm

Decided by default while writing; to be confirmed before implementing the related stage:

1. Skipped sessions count toward N for long breaks (the break pattern stays as previewed).
2. Skipping a break moves straight to the next session.
3. Stop asks for confirmation in Flow too, not only in plans.
4. Flow is not resumed after an interruption; the interrupted stage is recorded as `interrupted`.
5. Value limits: durations 1–180 min, N 1–20, row count 1–20, repeat 1–20.
6. Deleting a plan keeps its runs in history (the plan name comes from the snapshot).
