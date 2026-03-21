# Research Plan — Neuroblastoma Gene Expression Exploratory Analysis

**Idea source:** `_ideas/kaggle_ideas.md`
**Dataset(s):** `data/data.csv`
**Date:** 2026-03-21

---

## 1. Research Question

Perform a thorough exploratory data analysis (EDA) of a neuroblastoma gene expression dataset containing clinical variables, expression levels for 16 cancer-relevant genes, and event-free survival outcomes. The goal is to uncover patterns, distributions, correlations, and group differences that would prepare a researcher for interview questions ranging from basic descriptive statistics to advanced analytical reasoning. **No predictive modelling** — this is purely exploratory. The primary outcome of interest is the binary `event` column (relapse/death vs. censored), evaluated by **AUROC** should modelling be pursued in a future phase.

---

## 2. Dataset Summary

| Column | Type | Missing % | Notes |
|---|---|---|---|
| `patient_id` | Categorical (ID) | 0% | 100 unique values — primary key |
| `age_months` | Numeric | 0% | Range 1–89, mean 30.1, std 19.4 |
| `stage` | Categorical | 0% | 6 levels: 1, 2A, 2B, 3, 4, 4S. Stage 4 dominates (50%) |
| `risk_group` | Categorical | 0% | 3 levels: high (45%), low (30%), intermediate (25%) |
| `mycn_amplified` | Binary (0/1) | 0% | 20% amplified |
| `expr_MYCN` | Numeric (log2) | 0% | Range 4.78–15.08, mean 8.86 — bimodal expected (amplified vs. not) |
| `expr_ALK` | Numeric (log2) | 0% | Range 2.11–13.05, mean 8.19 |
| `expr_PHOX2B` | Numeric (log2) | 0% | Range 2.85–12.40, mean 7.44 |
| `expr_TH` | Numeric (log2) | 0% | Range 2.72–11.36, mean 7.63 |
| `expr_CHGB` | Numeric (log2) | 0% | Range 2.85–10.82, mean 7.25 |
| `expr_DBH` | Numeric (log2) | 0% | Range 3.86–11.70, mean 7.40 |
| `expr_NTRK1` | Numeric (log2) | 0% | Range 2.85–12.68, mean 8.13 — elevated in low-risk |
| `expr_NTRK2` | Numeric (log2) | 0% | Range 2.78–14.25, mean 7.47 |
| `expr_MDM2` | Numeric (log2) | 0% | Range 3.16–12.98, mean 8.51 |
| `expr_CDK4` | Numeric (log2) | 0% | Range 3.27–12.44, mean 8.18 |
| `expr_BIRC5` | Numeric (log2) | 0% | Range 3.96–13.29, mean 7.66 |
| `expr_CCND1` | Numeric (log2) | 0% | Range 2.14–13.49, mean 7.42 |
| `expr_MYC` | Numeric (log2) | 0% | Range 4.14–12.82, mean 7.72 |
| `expr_TERT` | Numeric (log2) | 0% | Range 3.44–11.75, mean 7.37 |
| `expr_ATRX` | Numeric (log2) | 0% | Range 3.80–11.91, mean 7.54 |
| `expr_TP53` | Numeric (log2) | 0% | Range 2.54–12.75, mean 7.13 |
| `efs_months` | Numeric | 0% | Range 1.0–85.4, mean 29.1, std 20.3 |
| `event` | Binary (0/1) | 0% | **Target variable.** 47% event, 53% censored — reasonably balanced |

### Key Observations

- **Zero missing values** across all 23 columns — no imputation needed.
- **No duplicate patient IDs** — each row is a unique patient.
- **Stage 4 dominates** at 50% of patients, reflecting real-world neuroblastoma epidemiology.
- **High-risk group is the largest** (45%), consistent with the stage distribution.
- **MYCN amplification** is present in 20% of patients — expect bimodal `expr_MYCN` distribution.
- **Event rate is ~47%** — well-balanced for binary classification; no oversampling needed.
- All gene expression values are on a **log2 scale** with broadly similar ranges (roughly 2–15).
- **NTRK1** appears elevated in low-risk patients — a known favourable prognostic marker in neuroblastoma.
- **ALK, MDM2, CDK4** show elevated expression in high-risk patients.

---

## 3. Proposed Phases

### Phase 1 — Data Quality & Cleaning
- **Validate data types:** Confirm all numeric columns parse correctly; verify categorical levels match expected values.
- **Dirty row detection:** Flag any rows with impossible values (negative expression, negative age, `efs_months` < 0, `event` not in {0,1}, stage not in valid set). Save flagged rows to `output/PROJECT_XX/dirty.csv` with a `reason` column.
- **Descriptive statistics:** Generate a summary table of all columns (count, mean, std, min, Q25, Q50, Q75, max for numerics; value counts for categoricals).

### Phase 2 — Univariate Analysis
- **Distribution plots for each gene** — Histograms with KDE overlays for all 16 gene expression columns.
- **Age distribution** — Histogram with KDE; annotate median and mean.
- **EFS distribution** — Histogram with KDE, stratified by event status.
- **Bar charts** for categorical variables: `stage`, `risk_group`, `mycn_amplified`, `event`.
- **Box plots** of gene expression grouped by `event` — identify genes with visually distinct distributions between event/no-event groups.
- **MYCN bimodality check** — Overlay `expr_MYCN` distributions for MYCN-amplified vs. non-amplified patients.

### Phase 3 — Bivariate & Group Comparisons
- **Correlation heatmap** — Pearson correlation matrix across all 16 gene expression columns plus `age_months` and `efs_months`. Annotate strong correlations (|r| > 0.5).
- **Gene expression by risk group** — Grouped box plots for each gene across low/intermediate/high risk.
- **Gene expression by stage** — Grouped box plots for key genes (MYCN, NTRK1, ALK) across stages.
- **Clinical variable cross-tabs:**
  - `risk_group` × `event` — stacked bar chart + chi-square test.
  - `stage` × `event` — stacked bar chart + chi-square test.
  - `mycn_amplified` × `event` — stacked bar chart + Fisher's exact test.
  - `age_months` × `event` — box plot + Mann-Whitney U test.
- **Statistical tests** — For each gene, run Mann-Whitney U test comparing expression in event=1 vs. event=0. Report p-values and flag significant genes (p < 0.05 after Bonferroni correction for 16 tests).

### Phase 4 — Multivariate Exploration
- **PCA** (Principal Component Analysis) on the 16 gene expression columns:
  - Scree plot showing variance explained per component.
  - 2D scatter of PC1 vs. PC2, coloured by `risk_group`, `event`, and `mycn_amplified` (3 separate plots).
  - Loading plot showing gene contributions to PC1 and PC2.
- **Clustermap** — Hierarchical clustering heatmap of gene expression across patients, with row annotations for risk group and event status.

### Phase 5 — Reporting
- **HTML report** — A single self-contained HTML file consolidating:
  - Executive summary of key findings.
  - All charts and plots embedded inline (base64-encoded PNGs or interactive Plotly).
  - Summary statistics tables.
  - Statistical test results table (gene, test statistic, p-value, significance).
  - Key takeaways section for interview preparation.
- Save to `output/PROJECT_XX/report.html`.

---

## 4. Technical Spec Guidance

The `/spec` phase should produce the following scripts:

| Script | Phase | Purpose | Key Outputs |
|---|---|---|---|
| `phase1_clean.py` | 1 | Load CSV, validate types, detect dirty rows, produce summary stats | `dirty.csv`, `summary_stats.csv` |
| `phase2_univariate.py` | 2 | Distribution plots for all numeric and categorical columns | Multiple PNG files |
| `phase3_bivariate.py` | 3 | Correlation heatmap, grouped comparisons, statistical tests | PNG files, `stat_tests.csv` |
| `phase4_multivariate.py` | 4 | PCA, clustering heatmap | PNG files, `pca_variance.csv` |
| `phase5_report.py` | 5 | Assemble all outputs into a single HTML report | `report.html` |

### Data Contracts Between Scripts
- All scripts read from `data/data.csv` (raw source) or from cleaned intermediate outputs.
- Phase 1 outputs `dirty.csv` — subsequent phases should load `data.csv` and exclude any `patient_id` values found in `dirty.csv`.
- All plots saved as PNG to `output/PROJECT_XX/`.
- Phase 5 reads all PNGs and CSVs from `output/PROJECT_XX/` to assemble the final HTML.

### Libraries
- **pandas** — data manipulation
- **matplotlib + seaborn** — static plots
- **scipy.stats** — statistical tests (Mann-Whitney U, chi-square, Fisher's exact)
- **scikit-learn** — PCA
- **jinja2** or string templating — HTML report generation

---

## 5. Open Questions / Assumptions

- **Assumption:** Gene expression values are already log2-normalised. No additional normalisation (quantile, z-score) will be applied unless distributions suggest otherwise.
- **Assumption:** `patient_id` is excluded from all analyses (identifier only).
- **Assumption:** `efs_months` will be used descriptively (e.g., distributions by group) but not in survival modelling, per the "exploratory only" scope.
- **Assumption:** The interview scope covers both statistical literacy (interpreting p-values, effect sizes) and domain knowledge (neuroblastoma biology, gene function).

---

## 6. Risks & Mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| Small sample size (n=100) | Low statistical power, wide confidence intervals | Acknowledge in report; use non-parametric tests; avoid over-interpretation |
| Multiple testing (16 genes) | Inflated false-positive rate | Apply Bonferroni correction (α = 0.05/16 = 0.003125) |
| Stage 4 dominance (50%) | May bias group-level summaries | Stratify analyses by stage where appropriate |
| Synthetic data limitations | May not reflect real biological complexity | Note in report; focus on methodology rather than biological conclusions |
| No external validation | Cannot assess generalisability | Flag as limitation; recommend external cohort in future phases |
