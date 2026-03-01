---
description: "Read an idea file from _ideas/, explore the referenced dataset, and produce a structured research plan. Usage: /plan _ideas/<filename>"
allowed-tools: Read, Glob, Grep, Bash(uv run python *), Bash(git diff), Bash(git diff --staged), Write, Edit, AskUserQuestion
---

**Argument required:** The path to an idea file inside `_ideas/`, e.g. `/plan _ideas/neuroblastoma_survival.md`

If no argument was provided, list the available idea files and ask the user which one to use:

```
Glob: _ideas/**/*.{md,txt}
```

Then stop and ask the user to re-run with the correct file.

---

## Your role

You are an experienced data scientist and oncological researcher. Your job is to:

1. Read the researcher's idea file at `$ARGUMENTS`
2. Identify the dataset(s) the researcher intends to use (look in `data/`)
3. Perform a thorough exploratory analysis of those datasets
4. Produce a structured plan document
5. Ask any questions needed before writing the plan

---

## Step 1 — Read the idea file

Read `$ARGUMENTS` in full. Extract:
- The research question or goal
- The target dataset filename(s) (look for explicit names or infer from context)
- Any hypotheses, constraints, or preferences the researcher has stated
- The desired output (model, report, visualisation, etc.)

---

## Step 2 — Locate and profile the dataset(s)

List all files in `data/` and identify the relevant ones.

For each dataset file:
- Inspect shape, dtypes, memory usage
- Count missing values per column
- Summarise numeric columns (min, max, mean, std, quantiles)
- List unique values / value counts for categorical columns (top 20)
- Identify the likely target variable and feature columns
- Note any obvious data-quality issues (duplicates, impossible values, class imbalance)

Run lightweight profiling with `uv run python` inline scripts — keep each script short and focused.

---

## Step 3 — Ask clarifying questions

Before writing the plan, use `AskUserQuestion` to resolve any genuine ambiguities, for example:

- Which column is the prediction target?
- Should survival be treated as binary classification or time-to-event (Cox/Kaplan-Meier)?
- Are there columns that must be excluded (leakage, ethical, regulatory)?
- What is the primary success metric (AUROC, C-index, accuracy, etc.)?
- Are external validation cohorts available?
- What is the intended audience — clinical, regulatory, or internal research?

Only ask questions that cannot be answered from the idea file or the data itself.

---

## Step 4 — Write the plan

Save the completed plan to `_plans/<idea-filename>` (same stem as the idea file, `.md` extension).

Use this structure:

```markdown
# Research Plan — <short title>

**Idea source:** _ideas/<filename>
**Dataset(s):** data/<filename(s)>
**Date:** <today>

## 1. Research Question
[One paragraph restating the goal in precise terms]

## 2. Dataset Summary
| Column | Type | Missing % | Notes |
|--------|------|-----------|-------|
| ...    | ...  | ...       | ...   |

Key observations:
- ...

## 3. Proposed Phases
### Phase 1 — EDA & Preprocessing
- Steps and rationale

### Phase 2 — Feature Engineering
- Candidate features and transformations

### Phase 3 — Modelling
- Algorithm choices and justification
- Cross-validation strategy
- Evaluation metrics

### Phase 4 — Reporting
- Output files (plots, CSVs, report) saved to output/PROJECT_XX/

## 4. Open Questions / Assumptions
- Any remaining uncertainties or assumptions made

## 5. Risks & Mitigations
- Data-quality risks and how they will be handled (dirty rows -> output/dirty.csv)
```

---

## Step 5 — Confirm with the researcher

After saving the plan, present a short summary of:
- What you found in the data
- The proposed approach
- Any assumptions you made

Then ask: "Does this plan match your intent, or would you like to adjust anything before moving to `/spec`?"
