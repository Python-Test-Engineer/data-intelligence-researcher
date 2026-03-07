# Research Plan — Web Analytics Traffic Acquisition

**Idea source:** _ideas/analytics.md
**Dataset(s):** data/analytics.csv
**Date:** 2026-03-07

---

## 1. Research Question

The primary goal is to understand **which traffic acquisition channels, geographic markets, source/medium combinations, and device types are driving sessions and pageviews** to the website over the period May 2017 – August 2019. The analysis will surface trends over time, identify top-performing and underperforming segments, and produce a clear internal report with supporting visualisations.

---

## 2. Dataset Summary

### File Format

- **Encoding:** UTF-16 LE with a non-standard 2-byte prefix (`0xB8 0xC0`) rather than the standard BOM. Must be read by skipping the first 2 bytes and decoding as `utf-16-le`.
- **Delimiter:** Tab (`\t`)
- **Shape:** 259,115 rows × 14 columns
- **Date range:** 2017-05-17 to 2019-08-31

### Column Reference

| Column            | Type        | Missing | Notes                                                                 |
|-------------------|-------------|---------|-----------------------------------------------------------------------|
| Channel Grouping  | categorical | 0%      | 7 values. First char cut by BOM — must be renamed on load.           |
| Country           | categorical | 0.52%   | 188 unique countries. 1,342 nulls to retain as "Unknown".            |
| Date              | string→date | 0%      | Format `M/D/YYYY`. Parse to datetime.                                |
| Device Category   | categorical | 0%      | Desktop / Mobile / Tablet.                                           |
| Page Title        | categorical | 0.10%   | Anonymised IDs (e.g. "Page Title 496"). 1,852 unique. Treat as IDs. |
| Source Medium     | categorical | 0%      | 262 unique combinations.                                             |
| Bounces           | integer     | 0%      | Count of single-page sessions. Range 0–89.                           |
| Exits             | integer     | 0%      | Count of exits from this page. Range 0–94.                           |
| Page Load Time    | integer     | 0%      | Sum of load times in ms. 13 rows exceed 100,000 ms (outliers).      |
| Pageviews         | integer     | 0%      | Total pageviews. 18 rows = 0.                                        |
| Sessions          | integer     | 0%      | Total sessions. 141,017 rows = 0 (pageview-only rows — keep).       |
| Time on Page      | integer     | 0%      | Sum of seconds on page. Max 17,844.                                  |
| Unique Pageviews  | integer     | 0%      | Range 0–190.                                                         |
| Total duration    | integer     | 0%      | Sum of session durations in seconds. 34 rows > 1,000,000.            |

### Key Observations

- **Channel split:** Organic Search dominates (118,595 rows / ~46%), then Direct (58,316), Social (32,479), Referral (29,699), Paid Search (18,417), Display (1,605), Other (4).
- **Top countries:** United States (80,571), India (30,389), France (20,205), UK (12,321), Germany (9,268), Switzerland (9,088).
- **Device split:** Desktop 82%, Mobile 14%, Tablet 3%. Mobile share warrants investigation over time.
- **Top sources:** google.com.br/Referral, indiegogo.com/Referral, amazon.co.jp/Referral, cnet.com/Referral.
- **Duplicate rows:** 10,807 fully duplicate rows present — must be dropped before aggregation.
- **Page Load Time outliers:** 13 rows with values 103k–425k ms (plausible GA aggregation artefacts; will be capped/flagged).
- **Sessions = 0:** 141,017 rows are pageview-only. Kept but excluded from session-level metrics.
- **Pageviews = 0:** 18 rows. These are dirty and will be removed to `dirty.csv`.

---

## 3. Proposed Phases

### Phase 1 — ETL & Preprocessing

**Objectives:** produce a clean, analysis-ready dataframe and a dirty log.

Steps:
1. **Load** — skip 2-byte non-standard BOM, decode `utf-16-le`, parse as TSV, rename `Channel Grouping`.
2. **Deduplicate** — drop 10,807 fully duplicate rows.
3. **Parse dates** — convert `Date` column to `datetime`.
4. **Dirty removal** — rows where `Pageviews == 0` (18 rows) are removed and written to `output/PROJECT_XX/dirty.csv` with `reason = "pageviews_zero"`.
5. **Null handling** — fill `Country` nulls with `"Unknown"`; fill `Page Title` nulls with `"Unknown"`.
6. **Derived columns:**
   - `Avg Page Load Time (ms)` = `Page Load Time / Pageviews` (only where `Pageviews > 0`)
   - `Bounce Rate` = `Bounces / Sessions` (only where `Sessions > 0`)
   - `Exit Rate` = `Exits / Pageviews`
   - `Avg Time on Page (s)` = `Time on Page / (Pageviews - Exits)` (standard GA formula)
   - `Year`, `Month`, `YearMonth` extracted from `Date`
7. **Outlier flagging** — add boolean column `page_load_outlier` for rows where `Avg Page Load Time > 10,000 ms` (extreme artefacts; note in report but retain).
8. **Save clean CSV** to `output/PROJECT_XX/analytics_clean.csv`.

**Outputs:**
- `output/PROJECT_XX/dirty.csv`
- `output/PROJECT_XX/analytics_clean.csv`

---

### Phase 2 — Exploratory Data Analysis

**Objectives:** answer the core acquisition questions and surface anomalies.

#### 2a. Traffic Volume Over Time
- Monthly sessions and pageviews trend line (2017–2019).
- Year-over-year comparison bar chart.
- Annotate any notable spikes or drops.

#### 2b. Channel Acquisition Analysis
- Sessions and pageviews by Channel Grouping — stacked bar and pie chart.
- Channel share over time (stacked area chart by month).
- Bounce rate by channel (bar chart).

#### 2c. Geographic Analysis
- Top 15 countries by sessions — horizontal bar chart.
- Heatmap or choropleth of sessions by country (world map).
- Country × Channel Grouping breakdown for top 5 countries.

#### 2d. Source / Medium Deep Dive
- Top 20 source/medium combinations by sessions.
- Referral source breakdown — which domains drive the most traffic.
- Paid Search sources breakdown (sessions, bounce rate).

#### 2e. Device Category Analysis
- Device split (Desktop / Mobile / Tablet) over time.
- Mobile share trend — is it growing?
- Bounce rate and page load time by device.

#### 2f. Page-Level Analysis
- Top 20 pages by pageviews and unique pageviews.
- Top 20 pages by exits (exit rate = exits / pageviews).
- Page load time distribution — histogram, flag the 13 extreme outliers.

**Outputs:**
- `output/PROJECT_XX/plots/` — one PNG per chart (named descriptively)
- `output/PROJECT_XX/eda_summary.csv` — aggregated stats used in charts

---

### Phase 3 — Aggregated Metrics Tables

Produce summary CSV tables for inclusion in the report:

| Table | Dimensions | Metrics |
|-------|-----------|---------|
| `channel_summary.csv` | Channel Grouping | Sessions, Pageviews, Bounce Rate, Avg Time on Page |
| `country_summary.csv` | Country (top 30) | Sessions, Pageviews, Device split % |
| `source_medium_summary.csv` | Source Medium (top 30) | Sessions, Pageviews, Bounce Rate |
| `device_summary.csv` | Device Category | Sessions, Pageviews, Bounce Rate, Avg Load Time |
| `monthly_trend.csv` | YearMonth | Sessions, Pageviews, by Channel |
| `page_summary.csv` | Page Title (top 50) | Pageviews, Unique Pageviews, Exits, Exit Rate, Avg Load Time |

All tables saved to `output/PROJECT_XX/tables/`.

---

### Phase 4 — Report Generation

**Objective:** produce a self-contained Markdown report tying findings together.

Structure of `output/PROJECT_XX/report_analytics.md`:

1. **Executive Summary** — 3–5 bullet headline findings.
2. **Data Overview** — shape, date range, dirty rows removed.
3. **Traffic Trends** — time-series narrative with embedded chart references.
4. **Channel Performance** — which channels deliver volume and quality.
5. **Geographic Breakdown** — top markets and notable patterns.
6. **Source / Medium** — top referrers and paid vs organic.
7. **Device Analysis** — desktop dominance, mobile trend.
8. **Page Performance** — top pages, slowest pages, high-exit pages.
9. **Data Quality Notes** — duplicates dropped, outliers flagged, encoding quirks.
10. **Recommendations** — 3–5 data-driven actions for the team.

---

## 4. Open Questions / Assumptions

- **Page Title anonymisation is permanent** — treated as opaque IDs throughout. No content grouping or category roll-up is possible without a mapping file.
- **Sessions = 0 rows are kept** — they contribute to pageview, exit, and page load metrics but are excluded from session-count and bounce-rate calculations.
- **GA aggregation artefacts** — very high Page Load Time values (up to 425,164 ms) are assumed to be GA aggregation artefacts, not real page loads. They are flagged but not removed (they don't violate business logic).
- **Currency of data** — the dataset ends August 2019. Trends observed may not reflect current behaviour; report will clearly note the time window.
- **Source Medium label "google.com.br / Referral"** — unusually large volume (114k rows) suggests a potential GA tagging misconfiguration or bot traffic. Will note this in the report as an anomaly.
- **"(Other)" channel (4 rows)** — negligible; grouped with Direct or noted as unknown in visuals.

---

## 5. Risks & Mitigations

| Risk | Mitigation |
|------|-----------|
| Non-standard file encoding breaks load | Hardcode 2-byte skip + `utf-16-le` decode in ETL script; document in code comments |
| Duplicate rows inflate all metrics | Drop before any aggregation; log count in report |
| Sessions=0 rows skew session-level KPIs | Separate dataframes for session vs pageview metrics; document clearly |
| Page Load Time outliers distort averages | Use median alongside mean; cap at 99th percentile for visualisations |
| google.com.br Referral dominance may be bot/spam traffic | Flag in report; optionally produce a version of charts excluding it |
| 188 countries → visual clutter | Limit geographic charts to top 15–30; group remainder as "Other" |
