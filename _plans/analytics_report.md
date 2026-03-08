# Analytics Report & ETL/Analysis Plan

**Dataset:** `data/data.csv`
**Rows:** 2,000 | **Columns:** 7
**Date drafted:** 2026-03-08

---

## 1. Dataset Overview

| Column | Type | Range / Values | Notes |
|---|---|---|---|
| `Page Views` | int | 1 – 11+ | Count of pages viewed per session |
| `Session Duration` | float | ~0.01 – 18+ min | Very wide spread; near-zero values likely dirty |
| `Bounce Rate` | float | 0.0 – ~0.68 | Proportion 0–1; values > 1 would be invalid |
| `Traffic Source` | categorical | Organic, Social, Paid, Direct, Referral | 5 categories observed |
| `Time on Page` | float | ~0.01 – 15+ min | May overlap meaningfully with Session Duration |
| `Previous Visits` | int | 0 – 5+ | Repeat-visitor indicator |
| `Conversion Rate` | float | ~0.87 – 1.0 | Mostly exactly 1.0; sub-1.0 values suggest partial or aggregated sessions |

---

## 2. Data Quality Observations (Pre-ETL)

- **Near-zero durations:** Some `Session Duration` and `Time on Page` values are extremely small (e.g. 0.012, 0.033 min). These likely represent bots, session errors, or page refreshes and should be flagged.
- **Conversion Rate variance:** The vast majority of rows have `Conversion Rate = 1.0`. Rows with values < 1.0 (e.g. 0.868, 0.963) are a small minority — the semantics of this column need clarification before deciding on cleaning rules.
- **No date/timestamp column** visible. This limits time-series analysis unless one is present elsewhere or can be reconstructed.
- **No nulls observed** in the sample, but a full null audit is needed across all 2,000 rows.

---

## 3. Proposed ETL Pipeline

### Phase 3.1 — Ingest & Audit
- Load `data.csv` with pandas
- Count nulls, duplicates, and out-of-range values per column
- Compute value distributions and percentiles
- Save audit summary to `output/PROJECT_XX/audit.csv`

### Phase 3.2 — Dirty Row Detection & Removal
Apply the following rules (dirty rows removed, never fixed, saved to `dirty.csv`):

| Rule | Column | Condition |
|---|---|---|
| Missing values | All | Any null |
| Implausible duration | `Session Duration` | < threshold (e.g. < 0.1 min — TBD) |
| Implausible time | `Time on Page` | < threshold (e.g. < 0.1 min — TBD) |
| Invalid bounce rate | `Bounce Rate` | < 0 or > 1 |
| Invalid conversion | `Conversion Rate` | < 0 or > 1 |
| Negative page views | `Page Views` | < 1 |
| Unknown traffic source | `Traffic Source` | Not in known set |

Dirty rows saved to `output/PROJECT_XX/dirty.csv` with a `reason` column.
Clean rows saved to `output/PROJECT_XX/clean.csv`.

### Phase 3.3 — Feature Engineering (optional, post-clarification)
- `engaged` flag: `Session Duration > X` AND `Bounce Rate < Y`
- `returning_visitor` flag: `Previous Visits > 0`
- `converted` binary: `Conversion Rate >= threshold` (if semantics confirmed)
- `pages_per_minute`: `Page Views / Session Duration`

---

## 4. Proposed Analyses

### 4.1 Univariate Distributions
- Histograms for all numeric columns
- Bar chart for `Traffic Source` frequency
- Box plots to surface outliers

### 4.2 Traffic Source Segmentation
- Mean/median of `Session Duration`, `Bounce Rate`, `Page Views`, `Time on Page`, `Conversion Rate` by `Traffic Source`
- Stacked bar: conversion profile per source
- Key question: which source delivers the highest-quality sessions?

### 4.3 Bounce Rate Analysis
- Distribution of bounce rate overall and per traffic source
- Correlation of bounce rate vs. `Session Duration`, `Time on Page`, `Page Views`
- Scatter plot: `Bounce Rate` vs. `Session Duration`, coloured by `Traffic Source`

### 4.4 Conversion Rate Analysis
- Distribution of `Conversion Rate` values (is it truly binary-ish or continuous?)
- `Conversion Rate` vs. all other numeric fields (correlations, scatter matrix)
- By `Traffic Source`: which source converts best?
- By `Previous Visits`: does repeat behaviour predict conversion?

### 4.5 Engagement Analysis
- `Page Views` vs. `Session Duration` scatter (coloured by `Traffic Source`)
- `Time on Page` vs. `Session Duration` — are they correlated? (If yes, possible redundancy)
- Returning vs. new visitors: engagement metrics comparison

### 4.6 Correlation Heatmap
- Pearson correlation matrix for all numeric columns
- Identify multicollinearity (e.g. `Session Duration` ↔ `Time on Page`)

### 4.7 Statistical Tests (if sample size supports)
- ANOVA / Kruskal-Wallis: are means of `Conversion Rate` / `Bounce Rate` significantly different across `Traffic Source`?
- Chi-square test if binary conversion flag is created

---

## 5. Proposed Charts & Plots

| # | Chart | X | Y / Colour | Purpose |
|---|---|---|---|---|
| 1 | Histogram grid | All numerics | — | Distribution overview |
| 2 | Bar chart | `Traffic Source` | Count | Source volume |
| 3 | Box plot | `Traffic Source` | `Session Duration` | Engagement by source |
| 4 | Box plot | `Traffic Source` | `Bounce Rate` | Quality by source |
| 5 | Box plot | `Traffic Source` | `Conversion Rate` | Conversion by source |
| 6 | Scatter | `Session Duration` | `Bounce Rate` | Engagement vs bounce |
| 7 | Scatter | `Page Views` | `Conversion Rate` | Depth vs conversion |
| 8 | Scatter | `Previous Visits` | `Conversion Rate` | Loyalty vs conversion |
| 9 | Heatmap | Numeric cols | Correlation | Multicollinearity |
| 10 | Grouped bar | `Traffic Source` | Mean metrics | Executive summary |
| 11 | Line/violin | `Previous Visits` | `Session Duration` | Repeat-visit engagement |

All plots: saved as PNG to `output/PROJECT_XX/plots/`.

---

## 6. Proposed Reports

### report_summary.md
- Executive summary: top 3–5 insights
- Key metrics table (overall averages)
- Best and worst performing traffic sources

### report_detailed.md (or notebook)
- Full methodology
- All charts embedded
- Statistical test results
- Recommendations for each traffic source

---

## 7. Proposed Script Structure (`src/`)

```
src/
  01_audit.py          # Load, null check, describe, save audit.csv
  02_clean.py          # Apply dirty-row rules, save dirty.csv + clean.csv
  03_eda.py            # All charts and plots (sections 4 & 5)
  04_stats.py          # Correlation, ANOVA, significance tests
  05_report.py         # Generate Markdown/HTML summary report
```

---

## 8. Open Questions (Pending Clarification)

See questions raised to the researcher below.

---

## 9. Assumptions (Until Clarified)

- `Session Duration` and `Time on Page` are in minutes
- `Bounce Rate` is a proportion (0–1), not a percentage (0–100)
- `Conversion Rate = 1.0` means the session converted; values < 1.0 are partial or aggregated
- `Previous Visits` is capped at 5 (or 5+) — needs confirmation
- No other data files exist beyond `data.csv`
