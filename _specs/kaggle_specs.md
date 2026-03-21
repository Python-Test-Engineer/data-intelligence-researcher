# Technical Spec — Neuroblastoma Gene Expression EDA

**Plan source:** `_plans/kaggle_plan.md`
**Dataset(s):** `data/data.csv`
**Output directory:** `output/PROJECT_01/`
**Date:** 2026-03-21

---

## 1. Overview

Five sequential Python scripts perform a fully exploratory analysis of a 100-patient neuroblastoma gene expression dataset. Phase 1 validates data integrity and removes dirty rows. Phase 2 produces univariate distribution plots for all numeric and categorical columns. Phase 3 produces bivariate comparisons, a correlation heatmap, grouped box plots, cross-tabulations, and per-gene Mann-Whitney U statistical tests. Phase 4 performs PCA and hierarchical clustering across the 16 gene expression features. Phase 5 assembles every output (plots, tables, statistical results) into a single self-contained HTML report with base64-embedded images and inline CSS. No predictive modelling is performed.

---

## 2. Environment

- Python **3.12** via `uv`
- Run commands: `uv run python src/<script>.py`
- Add dependencies: `uv add <package>`

**Dependencies to add:**
```
pandas
matplotlib
seaborn
scipy
scikit-learn
jinja2
```

**Global constant (defined at top of every script):**
```
RANDOM_SEED = 42
OUTPUT_DIR  = "output/PROJECT_01"
DATA_PATH   = "data/data.csv"
```

---

## 3. Script Architecture

| Script | Location | Responsibility | Primary Outputs |
|---|---|---|---|
| `phase1_clean.py` | `src/` | Load, validate types, detect dirty rows, summary stats | `dirty.csv`, `summary_stats.csv` |
| `phase2_univariate.py` | `src/` | Distribution plots for all columns, MYCN bimodality | `uni_*.png` |
| `phase3_bivariate.py` | `src/` | Correlation heatmap, grouped comparisons, statistical tests | `bi_*.png`, `stat_tests.csv` |
| `phase4_multivariate.py` | `src/` | PCA (scree, scatter, loadings) and clustermap | `multi_*.png`, `pca_variance.csv` |
| `phase5_report.py` | `src/` | Assemble all outputs into HTML report | `report.html` |

All scripts are **independently runnable** in phase order.

---

## 4. Data Contract

### 4.1 Input Schema — `data/data.csv`

| Column | dtype | Expected Values | Nullable |
|---|---|---|---|
| `patient_id` | str | `NB001`–`NB100`, unique | No |
| `age_months` | int | 1–240 | No |
| `stage` | str | `{1, 2A, 2B, 3, 4, 4S}` | No |
| `risk_group` | str | `{low, intermediate, high}` | No |
| `mycn_amplified` | int | `{0, 1}` | No |
| `expr_MYCN` | float | log2 scale, expected 2–20 | No |
| `expr_ALK` | float | log2 scale, expected 2–20 | No |
| `expr_PHOX2B` | float | log2 scale, expected 2–20 | No |
| `expr_TH` | float | log2 scale, expected 2–20 | No |
| `expr_CHGB` | float | log2 scale, expected 2–20 | No |
| `expr_DBH` | float | log2 scale, expected 2–20 | No |
| `expr_NTRK1` | float | log2 scale, expected 2–20 | No |
| `expr_NTRK2` | float | log2 scale, expected 2–20 | No |
| `expr_MDM2` | float | log2 scale, expected 2–20 | No |
| `expr_CDK4` | float | log2 scale, expected 2–20 | No |
| `expr_BIRC5` | float | log2 scale, expected 2–20 | No |
| `expr_CCND1` | float | log2 scale, expected 2–20 | No |
| `expr_MYC` | float | log2 scale, expected 2–20 | No |
| `expr_TERT` | float | log2 scale, expected 2–20 | No |
| `expr_ATRX` | float | log2 scale, expected 2–20 | No |
| `expr_TP53` | float | log2 scale, expected 2–20 | No |
| `efs_months` | float | > 0 | No |
| `event` | int | `{0, 1}` | No |

### 4.2 Dirty-Row Rules

Rows are **removed, never fixed**. All removed rows are appended to `output/PROJECT_01/dirty.csv` with a `reason` column (plain-English string).

| Rule | Reason string |
|---|---|
| Any `expr_*` column < 0 | `"negative gene expression value in <col>"` |
| `age_months` < 1 or > 240 | `"age_months out of valid range [1, 240]"` |
| `efs_months` <= 0 | `"efs_months must be positive"` |
| `event` not in {0, 1} | `"event value not in {0, 1}"` |
| `stage` not in `{1, 2A, 2B, 3, 4, 4S}` | `"stage not in valid set"` |
| `risk_group` not in `{low, intermediate, high}` | `"risk_group not in valid set"` |
| `mycn_amplified` not in {0, 1} | `"mycn_amplified not in {0, 1}"` |
| Duplicate `patient_id` | `"duplicate patient_id"` — keep first occurrence, mark subsequent rows |

A single row may match multiple rules; record all reasons joined by `"; "`.

### 4.3 Clean DataFrame Contract

Subsequent phases load `data/data.csv` and exclude `patient_id` values present in `dirty.csv`. This exclusion logic must be re-applied in **every script** (phases 2–5) before any analysis — do not persist the clean DataFrame to disk between phases.

**Helper pattern** (not code — intent only):
```
load data.csv
if dirty.csv exists:
    load dirty patient_ids
    drop those rows from df
proceed with clean df
```

### 4.4 Output File Registry

| File | Phase | Description |
|---|---|---|
| `output/PROJECT_01/dirty.csv` | 1 | Removed rows with `reason` column |
| `output/PROJECT_01/summary_stats.csv` | 1 | Per-column descriptive statistics |
| `output/PROJECT_01/uni_gene_distributions.png` | 2 | 4×4 grid of histograms+KDE for all 16 genes |
| `output/PROJECT_01/uni_age_distribution.png` | 2 | Age histogram+KDE with mean/median annotations |
| `output/PROJECT_01/uni_efs_by_event.png` | 2 | EFS histogram stratified by event status (overlaid) |
| `output/PROJECT_01/uni_categorical_bars.png` | 2 | 2×2 bar charts for stage, risk_group, mycn_amplified, event |
| `output/PROJECT_01/uni_gene_boxplots_by_event.png` | 2 | 4×4 grid of gene box plots split by event (0 vs 1) |
| `output/PROJECT_01/uni_mycn_bimodality.png` | 2 | expr_MYCN KDE overlay: amplified vs non-amplified |
| `output/PROJECT_01/bi_correlation_heatmap.png` | 3 | Pearson correlation matrix (16 genes + age + efs) |
| `output/PROJECT_01/bi_gene_by_riskgroup.png` | 3 | Grouped box plots: each gene × risk group |
| `output/PROJECT_01/bi_key_genes_by_stage.png` | 3 | Box plots for MYCN, NTRK1, ALK across stages |
| `output/PROJECT_01/bi_riskgroup_event.png` | 3 | Stacked bar: risk_group × event |
| `output/PROJECT_01/bi_stage_event.png` | 3 | Stacked bar: stage × event |
| `output/PROJECT_01/bi_mycn_amp_event.png` | 3 | Stacked bar: mycn_amplified × event |
| `output/PROJECT_01/bi_age_by_event.png` | 3 | Box plot: age_months split by event |
| `output/PROJECT_01/stat_tests.csv` | 3 | Gene-level Mann-Whitney U results with Bonferroni correction |
| `output/PROJECT_01/multi_pca_scree.png` | 4 | Scree plot: variance explained per PCA component |
| `output/PROJECT_01/multi_pca_scatter_riskgroup.png` | 4 | PC1 vs PC2 scatter coloured by risk_group |
| `output/PROJECT_01/multi_pca_scatter_event.png` | 4 | PC1 vs PC2 scatter coloured by event |
| `output/PROJECT_01/multi_pca_scatter_mycn.png` | 4 | PC1 vs PC2 scatter coloured by mycn_amplified |
| `output/PROJECT_01/multi_pca_loadings.png` | 4 | Bar chart of gene loadings for PC1 and PC2 |
| `output/PROJECT_01/multi_clustermap.png` | 4 | Hierarchical clustering heatmap with row annotations |
| `output/PROJECT_01/pca_variance.csv` | 4 | Component index, explained variance ratio, cumulative variance |
| `output/PROJECT_01/report.html` | 5 | Self-contained HTML report with all findings |

---

## 5. Phase Specs

---

### Phase 1 — Data Quality & Cleaning (`src/phase1_clean.py`)

**Inputs:** `data/data.csv`
**Outputs:** `output/PROJECT_01/dirty.csv`, `output/PROJECT_01/summary_stats.csv`

**Steps:**

1. **Setup:** Create `output/PROJECT_01/` directory if it does not exist. Define `GENE_COLS` as the list of 16 `expr_*` column names. Define `EXPECTED_STAGES = {"1","2A","2B","3","4","4S"}`, `EXPECTED_RISKS = {"low","intermediate","high"}`.

2. **Load:** Read `data/data.csv` with pandas. Assert all 23 expected columns are present; raise `ValueError` naming any missing column.

3. **Type coercion:** Cast numeric columns to `float64`; cast `mycn_amplified` and `event` to `int64`. Log a warning (do not raise) if any cast produces NaN.

4. **Dirty-row detection:** Apply each rule in §4.2 in order. Build a dict mapping `patient_id` → list of reason strings. A row may accumulate multiple reasons. After checking all rules, produce a dirty DataFrame containing original rows plus a `reason` column (joined reasons string). Write to `dirty.csv`.

5. **Clean DataFrame:** Drop all dirty rows from working `df`.

6. **Summary statistics — numeric columns:** For each numeric column compute: `count`, `missing_pct` (always 0 post-drop), `mean`, `std`, `min`, `p25`, `p50`, `p75`, `max`. One row per column. Save to `summary_stats.csv`.

7. **Summary statistics — categorical columns:** For `stage`, `risk_group`, `mycn_amplified`, `event`: compute value counts and percentages. Append to `summary_stats.csv` as additional rows with `N/A` for numeric-only fields.

8. **Print to stdout:** A readable table of shape, dirty row count, and clean row count.

---

### Phase 2 — Univariate Analysis (`src/phase2_univariate.py`)

**Inputs:** `data/data.csv`, `output/PROJECT_01/dirty.csv`
**Outputs:** 6 PNG files (see §4.4 `uni_*`)

**Plotting style:** Use `seaborn` style `"whitegrid"` globally. Figure DPI = 150. All axes must have a title, labelled x-axis, labelled y-axis. Save each figure with `bbox_inches="tight"`.

**Steps:**

1. Load and clean data (apply dirty-row exclusion per §4.3).

2. **Gene distribution grid** (`uni_gene_distributions.png`):
   - 4×4 subplot grid, one subplot per gene (order matches `GENE_COLS` list).
   - Each subplot: histogram (bins=20, alpha=0.6) + KDE overlay.
   - Subplot title = gene name (e.g. `MYCN`).
   - Super-title: `"Gene Expression Distributions (log2)"`.

3. **Age distribution** (`uni_age_distribution.png`):
   - Single figure. Histogram (bins=20) + KDE.
   - Annotate mean with a dashed vertical line labelled `f"Mean: {mean:.1f}"`.
   - Annotate median with a dotted vertical line labelled `f"Median: {median:.1f}"`.

4. **EFS by event** (`uni_efs_by_event.png`):
   - Single figure. Two overlaid histograms (alpha=0.5): one for `event=0` (censored), one for `event=1` (relapse/death).
   - KDE overlays for each group. Legend showing group labels and n.

5. **Categorical bar charts** (`uni_categorical_bars.png`):
   - 2×2 subplot grid. One subplot each for `stage`, `risk_group`, `mycn_amplified`, `event`.
   - Horizontal bar chart. Show count on bar. Colour bars by category using a qualitative palette.

6. **Gene box plots by event** (`uni_gene_boxplots_by_event.png`):
   - 4×4 subplot grid. Each subplot: box plot of one gene, split into two groups (`event=0`, `event=1`).
   - Use a two-colour palette. Subplot title = gene name.
   - Super-title: `"Gene Expression by Event Status"`.

7. **MYCN bimodality** (`uni_mycn_bimodality.png`):
   - Single figure. Two KDE curves overlaid: `mycn_amplified=0` vs `mycn_amplified=1`.
   - Vertical dashed lines at mean of each group. Legend with group labels and n.
   - Title: `"MYCN Expression: Amplified vs Non-Amplified"`.

---

### Phase 3 — Bivariate & Group Comparisons (`src/phase3_bivariate.py`)

**Inputs:** `data/data.csv`, `output/PROJECT_01/dirty.csv`
**Outputs:** 7 PNG files, `output/PROJECT_01/stat_tests.csv` (see §4.4 `bi_*`)

**Steps:**

1. Load and clean data (apply dirty-row exclusion per §4.3).

2. **Correlation heatmap** (`bi_correlation_heatmap.png`):
   - Compute Pearson correlation matrix for `GENE_COLS + ["age_months", "efs_months"]`.
   - Plot as a lower-triangle seaborn heatmap with `annot=True`, `fmt=".2f"`, `vmin=-1`, `vmax=1`, `cmap="coolwarm"`.
   - Annotate pairs with |r| > 0.5 with a border or bold annotation (post-hoc annotation via `ax.texts` styling is acceptable).
   - Title: `"Pearson Correlation Matrix — Gene Expression + Clinical Numerics"`.

3. **Gene expression by risk group** (`bi_gene_by_riskgroup.png`):
   - Figure with 4×4 subplots. Each subplot: box plot of one gene, `x=risk_group`, order `["low","intermediate","high"]`.
   - Three-colour qualitative palette. Super-title: `"Gene Expression by Risk Group"`.

4. **Key genes by stage** (`bi_key_genes_by_stage.png`):
   - 1×3 subplots for `expr_MYCN`, `expr_NTRK1`, `expr_ALK`.
   - Box plots with `x=stage`, order `["1","2A","2B","3","4","4S"]`.
   - Title per subplot = gene name. Super-title: `"Key Gene Expression by Disease Stage"`.

5. **Clinical × event cross-tabulations:**
   - `bi_riskgroup_event.png`: Stacked 100% bar chart, `x=risk_group`, stacks = `event`. Annotate each segment with percentage. Also print chi-square test result (χ², p-value) as figure subtitle.
   - `bi_stage_event.png`: Same pattern for `x=stage`. Chi-square test subtitle.
   - `bi_mycn_amp_event.png`: Same pattern for `x=mycn_amplified`. Fisher's exact test subtitle (use `scipy.stats.fisher_exact` on the 2×2 table). Label x-ticks as `"Not Amplified"` / `"Amplified"`.
   - `bi_age_by_event.png`: Box plot of `age_months` split by `event`. Mann-Whitney U test result as subtitle. Label groups `"Censored (event=0)"` / `"Relapse/Death (event=1)"`.

6. **Per-gene Mann-Whitney U tests** (`stat_tests.csv`):
   - For each gene in `GENE_COLS`: split into `event=0` and `event=1` groups, run `scipy.stats.mannwhitneyu` with `alternative="two-sided"`.
   - Compute Bonferroni-corrected significance threshold: `alpha_corrected = 0.05 / len(GENE_COLS)` = 0.003125.
   - Output CSV with columns: `gene`, `statistic`, `p_value`, `bonferroni_significant` (bool), `mean_event0`, `mean_event1`, `mean_diff` (event1 − event0).
   - Sort by `p_value` ascending.
   - Print summary to stdout: how many genes significant before and after correction.

---

### Phase 4 — Multivariate Exploration (`src/phase4_multivariate.py`)

**Inputs:** `data/data.csv`, `output/PROJECT_01/dirty.csv`
**Outputs:** 5 PNG files, `output/PROJECT_01/pca_variance.csv` (see §4.4 `multi_*`)

**Steps:**

1. Load and clean data (apply dirty-row exclusion per §4.3).

2. **PCA preparation:**
   - Extract the 16 `GENE_COLS` columns into matrix `X`.
   - Apply `sklearn.preprocessing.StandardScaler` (fit + transform on full clean dataset — no train/test split, this is exploratory).
   - Fit `sklearn.decomposition.PCA(n_components=16, random_state=RANDOM_SEED)`.

3. **Scree plot** (`multi_pca_scree.png`):
   - Bar chart of explained variance ratio per component (x = `PC1`…`PC16`).
   - Overlay a line for cumulative explained variance (right y-axis).
   - Annotate the number of components needed to reach 80% and 95% cumulative variance with vertical dashed lines.
   - Title: `"PCA Scree Plot — Gene Expression (n=16 genes)"`.

4. **Save variance CSV** (`pca_variance.csv`):
   - Columns: `component` (PC1…PC16), `explained_variance_ratio`, `cumulative_variance`.

5. **PC1 vs PC2 scatter plots** — three figures using the same 2D transformed coordinates:
   - `multi_pca_scatter_riskgroup.png`: colour = `risk_group`, palette = `{"low":"green","intermediate":"orange","high":"red"}`. Add centroids as large markers with gene label.
   - `multi_pca_scatter_event.png`: colour = `event`, palette = `{0:"steelblue", 1:"crimson"}`, labels `"Censored"` / `"Relapse"`.
   - `multi_pca_scatter_mycn.png`: colour = `mycn_amplified`, palette = `{0:"grey", 1:"purple"}`, labels `"Not Amplified"` / `"Amplified"`.
   - All three: scatter plot with alpha=0.7, size=60, legend, x-label `"PC1 ({var:.1f}% variance)"`, y-label `"PC2 ({var:.1f}% variance)"`.

6. **PCA loadings plot** (`multi_pca_loadings.png`):
   - Two side-by-side horizontal bar charts: PC1 loadings and PC2 loadings.
   - Bars coloured by sign (positive = teal, negative = salmon).
   - Genes sorted by absolute loading magnitude (descending).
   - Title: `"PCA Gene Loadings — PC1 and PC2"`.

7. **Hierarchical clustering heatmap** (`multi_clustermap.png`):
   - Use `seaborn.clustermap` on the StandardScaler-transformed gene expression matrix (patients as rows, genes as columns).
   - `method="ward"`, `metric="euclidean"`.
   - Row colour annotations: two colour bars — one for `risk_group` (low/intermediate/high) and one for `event` (0/1). Use `row_colors` parameter.
   - Add a legend for the row colour bars as an inset.
   - Column clustering: enable. Row clustering: enable.
   - Figure size: (14, 10).
   - Title: `"Hierarchical Clustering — Gene Expression Profiles"`.

---

### Phase 5 — HTML Report (`src/phase5_report.py`)

**Inputs:** all files in `output/PROJECT_01/` (PNGs and CSVs from phases 1–4)
**Outputs:** `output/PROJECT_01/report.html`

**Steps:**

1. Load and clean data (apply dirty-row exclusion per §4.3 — for inline statistics in the report).

2. **Load all artefacts:**
   - Read `summary_stats.csv`, `stat_tests.csv`, `pca_variance.csv`, `dirty.csv` into DataFrames.
   - Collect all PNG files in `OUTPUT_DIR` into a dict keyed by filename stem.
   - Encode each PNG as a base64 data URI: `"data:image/png;base64,<b64string>"`.

3. **Compute inline statistics for the executive summary:**
   - `n_total`, `n_dirty`, `n_clean`.
   - Event rate (%).
   - MYCN amplification rate (%).
   - Number of genes significant before Bonferroni correction.
   - Number of genes significant after Bonferroni correction.
   - Top 3 genes by smallest p-value (from `stat_tests.csv`).
   - Variance explained by PC1 and PC2.
   - Number of PCA components to reach 80% cumulative variance.

4. **HTML structure** — build using Python f-strings or Jinja2 template (either is acceptable; the choice is the implementer's). The HTML must be a single file with:
   - `<head>`: UTF-8 charset, viewport meta, inline `<style>` block with clean, readable CSS (white background, max-width 1100px centred, `font-family: "Segoe UI", sans-serif`, table borders, section headers).
   - Navigation sidebar or jump links at the top for each section.
   - **Section 1 — Executive Summary:** 4–6 bullet points of key findings drawn from the inline statistics computed in step 3.
   - **Section 2 — Dataset Overview:** Rendered HTML table from `summary_stats.csv`.
   - **Section 3 — Data Quality:** Count of dirty rows, rendered table of `dirty.csv` (or `"No dirty rows detected."` if empty).
   - **Section 4 — Univariate Analysis:** Embed all `uni_*.png` images in logical order with captions matching the plot titles. Each image `width="100%"`.
   - **Section 5 — Bivariate Analysis:** Embed all `bi_*.png` images with captions. Include the full `stat_tests.csv` as an HTML table styled with alternating row colours and Bonferroni-significant rows highlighted in yellow.
   - **Section 6 — Multivariate Analysis:** Embed all `multi_*.png` images with captions. Include `pca_variance.csv` as a compact HTML table showing the first 8 components.
   - **Section 7 — Interview Preparation Notes:** A static HTML block (hardcoded in the template) containing 8–10 bullet points covering:
     - How to interpret the correlation heatmap.
     - Why Bonferroni correction is used and its implication here.
     - Clinical significance of MYCN amplification in neuroblastoma.
     - What PCA reveals about gene co-expression structure.
     - Why Mann-Whitney U is preferred over t-test for this dataset size.
     - How event rate balance affects downstream modelling considerations.
     - Limitations of synthetic data.
     - Stage 4 dominance and how it affects group comparisons.
   - Footer with `"Generated by Claude Code — Project 01 — 2026-03-21"`.

5. Write the complete HTML string to `output/PROJECT_01/report.html`.

6. Print to stdout: `"Report saved to output/PROJECT_01/report.html"` and total file size in KB.

---

## 6. Reproducibility

- `RANDOM_SEED = 42` defined at the top of every script that uses randomness (Phase 4 PCA).
- All scripts are independently executable in phase order:
  ```bash
  uv run python src/phase1_clean.py
  uv run python src/phase2_univariate.py
  uv run python src/phase3_bivariate.py
  uv run python src/phase4_multivariate.py
  uv run python src/phase5_report.py
  ```
- Phases 2–5 re-apply dirty-row exclusion from `dirty.csv` on each run — no intermediate cleaned CSV is persisted.

---

## 7. Error Handling

| Condition | Behaviour |
|---|---|
| `data/data.csv` not found | Raise `FileNotFoundError` with message `"data/data.csv not found — place dataset in data/ directory"` |
| Expected column missing from CSV | Raise `ValueError("Missing required column: <col_name>")` |
| `dirty.csv` not found when running phases 2–5 | Assume no dirty rows — log a warning and proceed with full dataset |
| PNG file missing when building report | Log a warning, skip that image, insert a `<p>[image not generated]</p>` placeholder |
| Unexpected categorical value (not in defined set) | Log a `warnings.warn` — do not raise |

---

## 8. Plot Style Standards

Applied consistently across all scripts:
- `seaborn.set_theme(style="whitegrid", context="notebook")`
- Figure DPI: `150`
- Save: `fig.savefig(path, dpi=150, bbox_inches="tight")`
- Close after saving: `plt.close(fig)` — prevents memory accumulation across scripts
- Colour palette for risk group: `{"low": "#2ecc71", "intermediate": "#f39c12", "high": "#e74c3c"}`
- Colour palette for event: `{0: "#3498db", 1: "#e74c3c"}`
- All titles in title case. All axis labels in sentence case.
