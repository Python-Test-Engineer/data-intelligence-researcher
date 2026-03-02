# Research Plan — Sales CSV Analysis with Shiny

**Idea source:** _ideas/test.md
**Dataset(s):** data/sales_dummy.csv
**Date:** 2026-03-02

## 1. Research Question
Build a simple interactive Shiny for Python dashboard that lets users explore weekly sales performance by region and product, tracking revenue, cost, and units sold.

## 2. Dataset Summary
| Column | Type | Missing % | Notes |
|--------|------|-----------|-------|
| date | string (weekly) | 0% | 50 weeks, 2024-01-07 → 2024-12-29 |
| region | categorical | 0% | 4 values: North, South, East, West |
| product | categorical | 0% | 3 values: Widget A, Widget B, Gadget X |
| units_sold | int | 0% | range 10–197, mean 96 |
| revenue | float | 0% | range $531–$4,873, mean $2,620 |
| cost | float | 0% | range $230–$1,974, mean $1,065 |

Key observations:
- No missing values — no dirty-row removal needed
- `profit = revenue - cost` is a useful derived column
- Dataset is small (50 rows) — no performance concerns

## 3. Proposed Phases

### Phase 1 — EDA & Preprocessing
- Load CSV, parse dates, compute `profit` column
- Check for duplicates and impossible values (e.g. cost > revenue)

### Phase 2 — Feature Engineering
- `profit = revenue - cost`
- `profit_margin = profit / revenue`
- Weekly aggregates by region and product

### Phase 3 — Shiny Dashboard
- KPI cards: total revenue, total profit, avg units sold
- Bar chart: revenue by region
- Line chart: weekly revenue trend
- Filter widgets: region multi-select, product multi-select

### Phase 4 — Reporting
- Output: `output/PROJECT_XX/sales_dashboard.py` (Shiny app)
- Output: `output/PROJECT_XX/sales_summary.csv` (aggregated stats)

## 4. Open Questions / Assumptions
- Dummy data used — swap `data/sales_dummy.csv` for real data when available
- Shiny for Python (`shiny` package) assumed, not R Shiny

## 5. Risks & Mitigations
- No dirty rows expected in dummy data; real data should be validated and dirty rows saved to `output/PROJECT_XX/dirty.csv`
