# Technical Spec — Web Analytics Traffic Acquisition

**Plan source:** _plans/analytics.md
**Dataset(s):** data/analytics.csv
**Output directory:** output/PROJECT_02/
**Date:** 2026-03-07

---

## 1. Overview

Four sequential scripts load a UTF-16 LE tab-separated Google Analytics export, clean and enrich it, produce a suite of acquisition-focused EDA plots, generate six aggregated summary tables, and render a self-contained Markdown report. No modelling is performed — the deliverable is exploratory insight. All generated files land in `output/PROJECT_02/`.

---

## 2. Environment

- Python 3.12 via `uv`
- Dependencies to add with `uv add`:
  ```
  pandas matplotlib seaborn plotly kaleido
  ```
- `numpy` is assumed present as a transitive dependency of pandas.

---

## 3. Script Architecture

| Script | Location | Responsibility |
|--------|----------|----------------|
| `phase1_etl.py` | `src/` | Load raw file, fix encoding/BOM, deduplicate, remove dirty rows, derive metrics, save `analytics_clean.csv` and `dirty.csv` |
| `phase2_eda.py` | `src/` | Produce all EDA plots (PNG) and `eda_summary.csv` |
| `phase3_tables.py` | `src/` | Produce six aggregated CSV summary tables |
| `phase4_report.py` | `src/` | Assemble and write `report_analytics.md` |

Run in order:
```bash
uv run python src/phase1_etl.py
uv run python src/phase2_eda.py
uv run python src/phase3_tables.py
uv run python src/phase4_report.py
```

---

## 4. Data Contract

### 4.1 Raw Input — `data/analytics.csv`

| Column (raw name) | Resolved name | Type | Nullable | Notes |
|---|---|---|---|---|
| `hannel Grouping` (BOM-truncated) | `Channel Grouping` | str | No | Rename on load; 7 unique values |
| `Country` | `Country` | str | Yes (0.52%) | Fill nulls → `"Unknown"` |
| `Date` | `Date` | str → datetime | No | Format `M/D/YYYY` |
| `Device Category` | `Device Category` | str | No | Desktop / Mobile / Tablet |
| `Page Title` | `Page Title` | str | Yes (0.10%) | Anonymised IDs; fill nulls → `"Unknown"` |
| `Source Medium` | `Source Medium` | str | No | 262 unique values |
| `Bounces` | `Bounces` | int64 | No | Range 0–89 |
| `Exits` | `Exits` | int64 | No | Range 0–94 |
| `Page Load Time` | `Page Load Time` | int64 | No | Sum of ms; 13 rows > 100k ms |
| `Pageviews` | `Pageviews` | int64 | No | 18 rows = 0 (dirty) |
| `Sessions` | `Sessions` | int64 | No | 141,017 rows = 0 (keep) |
| `Time on Page` | `Time on Page` | int64 | No | Sum of seconds |
| `Unique Pageviews` | `Unique Pageviews` | int64 | No | Range 0–190 |
| `Total duration` | `Total duration` | int64 | No | Sum of session seconds |

**Loading procedure** (critical — non-standard encoding):
1. Open file in binary mode (`rb`).
2. Skip the first 2 bytes (`0xB8 0xC0` non-standard BOM).
3. Decode remaining bytes with `utf-16-le`.
4. Wrap decoded string in `io.StringIO` and pass to `pd.read_csv(..., sep='\t')`.
5. Rename column index 0 from `"hannel Grouping"` to `"Channel Grouping"`.

### 4.2 Dirty-Row Rules

Rows are **removed, never fixed**, and appended to `output/PROJECT_02/dirty.csv` with a `reason` column.

| Rule | Condition | `reason` value |
|------|-----------|----------------|
| Zero pageviews | `Pageviews == 0` | `"pageviews_zero"` |

Expected dirty count: ~18 rows.

### 4.3 Deduplication

Drop fully duplicate rows **before** dirty-row extraction. Expected to remove ~10,807 rows. Log count to stdout.

### 4.4 Derived Columns (added to clean dataframe)

| New column | Formula | Guard condition |
|---|---|---|
| `Avg Page Load Time (ms)` | `Page Load Time / Pageviews` | `Pageviews > 0`; else `NaN` |
| `Bounce Rate` | `Bounces / Sessions` | `Sessions > 0`; else `NaN` |
| `Exit Rate` | `Exits / Pageviews` | `Pageviews > 0`; else `NaN` |
| `Avg Time on Page (s)` | `Time on Page / (Pageviews - Exits)` | `(Pageviews - Exits) > 0`; else `NaN` |
| `page_load_outlier` | `Avg Page Load Time (ms) > 10000` | Always; boolean |
| `Year` | `Date.dt.year` | — |
| `Month` | `Date.dt.month` | — |
| `YearMonth` | `Date.dt.to_period('M')` stored as string `YYYY-MM` | — |

### 4.5 Output Files

| File | Description |
|------|-------------|
| `output/PROJECT_02/dirty.csv` | Removed rows + `reason` column |
| `output/PROJECT_02/analytics_clean.csv` | Deduplicated, cleaned, enriched dataset |
| `output/PROJECT_02/plots/*.png` | All EDA charts (see Phase 2) |
| `output/PROJECT_02/eda_summary.csv` | Aggregated stats backing EDA charts |
| `output/PROJECT_02/tables/channel_summary.csv` | Channel-level aggregates |
| `output/PROJECT_02/tables/country_summary.csv` | Country-level aggregates (top 30) |
| `output/PROJECT_02/tables/source_medium_summary.csv` | Source/medium aggregates (top 30) |
| `output/PROJECT_02/tables/device_summary.csv` | Device-level aggregates |
| `output/PROJECT_02/tables/monthly_trend.csv` | Monthly sessions & pageviews by channel |
| `output/PROJECT_02/tables/page_summary.csv` | Page-level aggregates (top 50 by pageviews) |
| `output/PROJECT_02/report_analytics.md` | Final Markdown report |

---

## 5. Phase Specs

### Phase 1 — ETL & Preprocessing (`src/phase1_etl.py`)

**Inputs:** `data/analytics.csv`
**Outputs:** `output/PROJECT_02/dirty.csv`, `output/PROJECT_02/analytics_clean.csv`

Steps:
1. Create `output/PROJECT_02/` directory if it does not exist (`exist_ok=True`).
2. Load raw file using the binary-skip + utf-16-le procedure described in §4.1.
3. Assert all 14 expected column names are present (after rename); raise `ValueError` if not.
4. Assert row count is in range [200_000, 300_000]; raise `ValueError` if not (sanity check).
5. Log initial shape to stdout.
6. **Deduplicate:** call `df.drop_duplicates()`, log rows removed.
7. **Dirty extraction:** filter `Pageviews == 0`, assign `reason = "pageviews_zero"`, write to `dirty.csv` (include all original columns + `reason`).
8. Drop dirty rows from working dataframe.
9. **Null fill:** `Country` → `"Unknown"`, `Page Title` → `"Unknown"`.
10. **Date parse:** `pd.to_datetime(df['Date'], format='%m/%d/%Y')`.
11. **Derive columns** per §4.4.
12. Log final clean shape to stdout.
13. Save `analytics_clean.csv` (index=False, encoding=utf-8).

---

### Phase 2 — EDA & Visualisation (`src/phase2_eda.py`)

**Inputs:** `output/PROJECT_02/analytics_clean.csv`
**Outputs:** `output/PROJECT_02/plots/*.png`, `output/PROJECT_02/eda_summary.csv`

Create `output/PROJECT_02/plots/` if absent. Use `matplotlib`/`seaborn` for all charts except the choropleth. All PNGs saved at 150 dpi, `bbox_inches='tight'`.

#### Chart inventory

| Filename | Chart type | Description |
|---|---|---|
| `01_monthly_sessions_pageviews.png` | Dual-line chart | Sessions and Pageviews per month (2017–2019). Use session-filtered df (`Sessions > 0`) for session line; full df for pageviews line. |
| `02_yoy_sessions.png` | Grouped bar chart | Total sessions and pageviews by year (2017, 2018, 2019). |
| `03_channel_bar.png` | Horizontal bar chart | Total sessions by Channel Grouping (descending). Session-filtered df only. |
| `04_channel_pie.png` | Pie chart | Session share by Channel Grouping. |
| `05_channel_area_over_time.png` | Stacked area chart | Monthly session share by channel. Pivot on `YearMonth` × `Channel Grouping`. |
| `06_channel_bounce_rate.png` | Bar chart | Mean `Bounce Rate` by Channel Grouping (session-filtered df). |
| `07_top15_countries.png` | Horizontal bar chart | Top 15 countries by total sessions. |
| `08_country_choropleth.png` | Plotly choropleth (exported PNG via kaleido) | World map coloured by session count. Group countries outside top 30 into `"Other"` for legend clarity; map still plots all. Use `plotly.express.choropleth`. |
| `09_top5_country_channel.png` | Grouped bar chart | Sessions by Channel Grouping for the top 5 countries. |
| `10_top20_source_medium.png` | Horizontal bar chart | Top 20 Source Medium combinations by sessions. |
| `11_referral_sources.png` | Horizontal bar chart | Top 15 referral domains (filter `Channel Grouping == "Referral"`), sessions. |
| `12_paid_search_sources.png` | Bar chart | Sessions and Bounce Rate for Paid Search sources. |
| `13_device_split_pie.png` | Pie chart | Pageview share by Device Category. |
| `14_device_mobile_trend.png` | Line chart | Monthly mobile share (%) of sessions over time. |
| `15_device_bounce_loadtime.png` | Side-by-side bar chart | Bounce Rate and median Avg Page Load Time by Device Category. |
| `16_top20_pages_by_pageviews.png` | Horizontal bar chart | Top 20 Page Titles by total Pageviews. |
| `17_top20_pages_by_exit_rate.png` | Horizontal bar chart | Top 20 Page Titles by Exit Rate (min 100 pageviews to qualify). |
| `18_page_load_distribution.png` | Histogram | Distribution of `Avg Page Load Time (ms)`, capped at 99th percentile. Annotate: `{n} outliers > 10,000 ms excluded from axis`. |

**`eda_summary.csv`** — a single CSV containing one row per chart with columns: `chart_file`, `metric`, `top_value`, `top_label`, `note`. Manually constructed in the script as a list of dicts after computing each chart's aggregation.

#### Styling conventions
- Figure size: default `(12, 6)` for bar/line charts; `(8, 8)` for pies.
- Colour palette: `seaborn.color_palette("tab10")` for categorical; `"Blues_r"` for sequential.
- All axes labelled; titles in sentence case; gridlines on y-axis only.
- For choropleth: `color_continuous_scale="Blues"`, `projection="natural earth"`.

---

### Phase 3 — Aggregated Tables (`src/phase3_tables.py`)

**Inputs:** `output/PROJECT_02/analytics_clean.csv`
**Outputs:** `output/PROJECT_02/tables/*.csv`

Create `output/PROJECT_02/tables/` if absent.

Define two base dataframes at the top of the script:
- `df_all` — full clean dataframe
- `df_sess` — `df_all` filtered to `Sessions > 0` (for session-level metrics)

#### Table specifications

**`channel_summary.csv`**
- Group `df_all` by `Channel Grouping`
- Columns: `Sessions` (sum from df_sess), `Pageviews` (sum), `Bounces` (sum), `Bounce Rate` (= Bounces/Sessions, from df_sess), `Avg Time on Page (s)` (mean, excluding NaN)
- Sort descending by `Sessions`

**`country_summary.csv`**
- Group `df_all` by `Country`; keep top 30 by `Sessions` (summed from df_sess)
- Columns: `Sessions`, `Pageviews`, `Desktop %`, `Mobile %`, `Tablet %`
- Device percentages = count of rows per device / total rows for that country × 100

**`source_medium_summary.csv`**
- Group `df_sess` by `Source Medium`; keep top 30 by `Sessions`
- Columns: `Sessions`, `Pageviews`, `Bounces`, `Bounce Rate`
- Sort descending by `Sessions`

**`device_summary.csv`**
- Group `df_all` by `Device Category`
- Columns: `Sessions` (from df_sess), `Pageviews`, `Bounce Rate` (from df_sess), `Median Avg Page Load Time (ms)` (median of `Avg Page Load Time (ms)`, ignoring NaN and outliers where `page_load_outlier == True`)

**`monthly_trend.csv`**
- Group `df_all` by `YearMonth`
- Columns: `Total Sessions`, `Total Pageviews`, then one column per Channel Grouping value showing sessions (pivot)
- Sort ascending by `YearMonth`

**`page_summary.csv`**
- Group `df_all` by `Page Title`; keep top 50 by `Pageviews`
- Columns: `Pageviews`, `Unique Pageviews`, `Exits`, `Exit Rate`, `Median Avg Page Load Time (ms)` (excluding `page_load_outlier == True` rows)
- Sort descending by `Pageviews`

All tables: save with `index=False`, `encoding='utf-8'`.

---

### Phase 4 — Report Generation (`src/phase4_report.py`)

**Inputs:** `output/PROJECT_02/analytics_clean.csv`, all tables in `output/PROJECT_02/tables/`, `output/PROJECT_02/eda_summary.csv`
**Outputs:** `output/PROJECT_02/report_analytics.md`

The script reads the clean CSV and all tables, computes a small set of headline statistics, then assembles and writes a Markdown file. No plotting occurs in this script.

#### Headline statistics to compute

| Stat | Source |
|---|---|
| Total rows (raw), after dedup, after dirty removal | Read from dirty.csv (len) and clean CSV (len) |
| Date range (min, max) | Clean CSV `Date` column |
| Total sessions | `channel_summary.csv` Sessions sum |
| Total pageviews | `channel_summary.csv` Pageviews sum |
| Top channel by sessions | `channel_summary.csv` row 0 |
| Top country by sessions | `country_summary.csv` row 0 |
| Top source/medium by sessions | `source_medium_summary.csv` row 0 |
| Mobile share % (overall) | `device_summary.csv` Mobile row / total |
| Top page by pageviews | `page_summary.csv` row 0 |
| google.com.br anomaly flag | If `source_medium_summary.csv` row 0 contains "google.com.br" |

#### Report structure

```
# Web Analytics — Traffic Acquisition Report

**Date range:** YYYY-MM-DD to YYYY-MM-DD
**Generated:** 2026-03-07
**Data source:** data/analytics.csv

## Executive Summary
- [3–5 bullet headline findings derived from headline statistics]

## Data Overview
- Raw rows, duplicates removed, dirty rows removed, final clean rows
- Data quality notes: encoding quirk, BOM issue, Sessions=0 retention

## Traffic Trends
- Prose paragraph referencing `plots/01_monthly_sessions_pageviews.png`
- Prose paragraph referencing `plots/02_yoy_sessions.png`

## Channel Performance
- Inline table from `channel_summary.csv` (all channels)
- Reference `plots/03_channel_bar.png`, `plots/05_channel_area_over_time.png`, `plots/06_channel_bounce_rate.png`

## Geographic Breakdown
- Top 10 country table from `country_summary.csv`
- Reference `plots/07_top15_countries.png`, `plots/08_country_choropleth.png`

## Source / Medium
- Top 10 source/medium table from `source_medium_summary.csv`
- Flag google.com.br anomaly if present
- Reference `plots/10_top20_source_medium.png`, `plots/11_referral_sources.png`

## Device Analysis
- Inline table from `device_summary.csv`
- Reference `plots/13_device_split_pie.png`, `plots/14_device_mobile_trend.png`

## Page Performance
- Top 10 pages table from `page_summary.csv`
- Reference `plots/16_top20_pages_by_pageviews.png`, `plots/17_top20_pages_by_exit_rate.png`
- Note: page titles are anonymised IDs

## Data Quality Notes
- Non-standard UTF-16 LE encoding with 2-byte non-BOM prefix
- Duplicate rows removed: N
- Dirty rows removed: N (pageviews_zero)
- Sessions=0 rows retained for pageview metrics, excluded from session metrics
- Page Load Time outliers (> 10,000 ms): 13 rows flagged, retained

## Recommendations
- [3–5 actionable items derived from findings, written by the script as templated strings
   populated with real values, e.g. top channel, anomalous source, mobile trend direction]
```

Inline tables in the report use pipe-delimited Markdown format. Chart references use relative Markdown image links: `![caption](plots/01_monthly_sessions_pageviews.png)`.

---

## 6. Reproducibility

- No random seed required (no stochastic operations).
- All scripts read from fixed input paths; output paths are constants defined at the top of each script.
- Scripts are independently runnable in phase order.

---

## 7. Error Handling

- Each script asserts its required input files exist; raises `FileNotFoundError` with a clear message if not.
- Phase 1 asserts column names and row count range.
- Division-by-zero in derived metrics guarded by boolean masks (`where` conditions); result is `NaN`, not an exception.
- Choropleth export (kaleido): if export fails, catch exception, log a warning, and save the plotly figure as HTML instead (`plots/08_country_choropleth.html`).

---

## 8. Constants (defined at top of each script)

```
DATA_PATH  = "data/analytics.csv"
OUTPUT_DIR = "output/PROJECT_02"
PLOTS_DIR  = "output/PROJECT_02/plots"
TABLES_DIR = "output/PROJECT_02/tables"
CLEAN_CSV  = "output/PROJECT_02/analytics_clean.csv"
DIRTY_CSV  = "output/PROJECT_02/dirty.csv"
REPORT_MD  = "output/PROJECT_02/report_analytics.md"
EDA_CSV    = "output/PROJECT_02/eda_summary.csv"
```
