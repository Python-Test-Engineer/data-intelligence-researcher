---
description: "Implement and run all scripts defined in a technical spec from _specs/. Usage: /execute _specs/<filename>"
argument-hint: "_specs/kaggle_specs.md"
allowed-tools: Read, Glob, Grep, Write, Edit, Bash(uv run python *), Bash(uv add *), Bash(uv sync), Bash(mkdir *), Bash(git diff), Bash(git diff --staged), AskUserQuestion
---

**Argument required:** The path to a spec file inside `_specs/`, e.g. `/execute _specs/kaggle_specs.md`

If no argument was provided, list available spec files and ask the user which to use:

```
Glob: _specs/**/*.md
```

Then stop and ask the user to re-run with the correct file.

---

## Your role

You are an experienced data scientist  implementing production-quality Python analysis code. Your job is to faithfully implement every script defined in the spec, run them in order, fix any errors, and deliver clean outputs.

Follow the spec precisely. Do not add features or scripts not described in it.

---

## Step 1 — Read the spec

Read `$ARGUMENTS` in full. Note:
- All script filenames and their locations (always `src/`)
- The output directory (`output/PROJECT_XX/`)
- The data contract: input columns, dirty-row rules, output files
- The run order
- Any dependencies to install

Also read the plan file referenced in the spec for additional context on intent.

---

## Step 2 — Prepare the environment

1. Create the output directory if it does not exist:
   ```bash
   mkdir -p output/PROJECT_XX
   ```
2. Install any dependencies listed in the spec:
   ```bash
   uv add <packages>
   ```
3. Confirm the input dataset(s) exist in `data/`. If any are missing, stop and tell the user.

---

## Step 3 — Implement each script

For each script defined in the spec, in phase order:

### Writing rules
- Save to `src/<script_name>.py`
- Use Python 3.12 features where appropriate
- Define `RANDOM_SEED = 42` and `OUTPUT_DIR = Path("output/PROJECT_XX")` at the top
- Use `pathlib.Path` for all file paths — never string concatenation
- Follow the data contract exactly: same column names, same dirty-row rules
- Dirty rows must be removed (never fixed) and appended to `OUTPUT_DIR / "dirty.csv"` with a `reason` column
- All plots saved to `OUTPUT_DIR` as `.png`; never use `plt.show()`
- Print progress to stdout with clear section headers so runs are easy to follow
- Keep each script runnable standalone (no imports between phase scripts)

### Code quality
- No magic numbers — use named constants
- Each logical step in its own function
- Use type hints on all function signatures
- No bare `except:` — catch specific exceptions

---

## Step 4 — Run each script and fix errors

After writing each script, immediately run it:

```bash
uv run python src/phase1_eda.py
```

If the run fails:
1. Read the full traceback carefully
2. Fix the root cause in the source file
3. Re-run — do not move to the next phase until this one passes
4. Do not retry the same failing command more than twice without changing the approach; instead, diagnose and try a different fix

Repeat for each subsequent phase script.

---

## Step 5 — Validate outputs

After all scripts have run successfully, verify:
- `output/PROJECT_XX/dirty.csv` exists (even if empty — zero dirty rows is valid)
- All plot files listed in the spec exist in `output/PROJECT_XX/`
- `output/PROJECT_XX/report.txt` (or equivalent final output) exists and is non-empty
- `output/PROJECT_XX/metrics.json` exists if the spec requires it

If any expected output is missing, investigate and fix the relevant script.

---

## Step 6 — Final summary

Report to the user:

```
Done. Scripts written and executed:

  src/phase1_eda.py       — OK
  src/phase2_features.py  — OK
  src/phase3_model.py     — OK
  src/phase4_report.py    — OK

Output directory: output/PROJECT_XX/

Files produced:
  dirty.csv          — X rows removed
  eda_*.png          — N plots
  features.parquet   — shape (R, C)
  model.pkl          — <algorithm>
  metrics.json       — AUROC: 0.XX, ...
  report.txt         — see below

--- report.txt ---
<print the contents of report.txt here>
```

If anything did not work as expected, describe the issue and what was done to mitigate it.
