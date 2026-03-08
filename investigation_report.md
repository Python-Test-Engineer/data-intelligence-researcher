# Case Report: Dataset Investigation

## Executive Summary
This investigation analysed **30** records across **4** numeric column(s). After removing **3** dirty row(s), the clean dataset contains **27** rows (90.0% pass rate). Across 4 numeric column(s), the overall mean is 313.62. revenue has the highest average at 1169.36.

---

## Data Quality

- **Total rows ingested:** 30
- **Dirty rows removed:** 3 (10.0%)
- **Clean rows retained:** 27 (90.0%)
- **Issues detected:** anomalous value in 'units_sold' (9999); anomalous value in 'revenue' (999700.01); missing value in 'rep_name'; duplicate row

### Issue Breakdown
  - anomalous value: **2** occurrence(s)
  - missing value: **1** occurrence(s)
  - duplicate row: **1** occurrence(s)

---

## Statistical Analysis

### Summary Table
| Column | Mean | Std Dev | Min | Max | Median | CV |
|--------|------|---------|-----|-----|--------|----|
| units_sold | 26.96 | 15.25 | 6.0 | 61.0 | 26.0 | 56.6% |
| unit_price | 54.8 | 28.6 | 29.99 | 99.99 | 49.99 | 52.2% |
| revenue | 1169.36 | 404.62 | 599.94 | 2049.59 | 1099.78 | 34.6% |
| discount_pct | 3.33 | 3.92 | 0.0 | 10.0 | 0.0 | 117.7% |

### Top Performers (by mean)
  1. **revenue** — avg 1169.36
  2. **unit_price** — avg 54.8
  3. **units_sold** — avg 26.96

### Lowest Performers (by mean)
  1. **discount_pct** — avg 3.33
  2. **units_sold** — avg 26.96
  3. **unit_price** — avg 54.8

### Overall
- **Overall mean across all numeric columns:** 313.62
- **Highest average column:** **revenue** at 1169.36

## Variability Alert
The following columns show high coefficient of variation (CV > 40%), indicating significant spread or potential data inconsistency:
- **units_sold** (CV: 56.6%)
- **unit_price** (CV: 52.2%)
- **discount_pct** (CV: 117.7%)

---

## Key Findings

- revenue leads with an average of 1169.36; the overall mean is 313.62 and values span a range of 1166.03.
- Data quality stands at **90.0%** after cleaning.
- **revenue** consistently leads as the strongest numeric signal in this dataset.
- High variability detected in: **units_sold**, **unit_price**, **discount_pct** — warrants deeper investigation.

---

## Recommended Next Steps

1. **Improve upstream data capture** — missing values suggest gaps in data entry or collection pipelines. Enforce mandatory fields at source.
2. **Implement range validation** — anomalous values were detected. Add min/max constraints at the point of entry or ETL layer.
3. **Deduplicate at source** — duplicate rows indicate a merging or ingestion issue. Add unique-key enforcement before loading.
4. **Investigate high-variance columns** — units_sold, unit_price, discount_pct show wide spread. Segment by category or time period to understand drivers.
5. **Trend analysis** — extend this report with time-series breakdowns of **revenue** to identify seasonal patterns or growth trajectories.
6. **Correlation study** — compute pairwise correlations between numeric columns to surface relationships that may drive the key metric.
7. **Automated monitoring** — schedule this pipeline to run on new data drops and alert stakeholders when quality thresholds are breached.

---

*— Assembled by the Data Science Detective Agency*