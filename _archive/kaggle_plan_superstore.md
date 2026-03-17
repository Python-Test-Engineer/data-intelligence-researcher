# Research Plan — Superstore Sales EDA & Analytics

**Idea source:** _ideas/kaggle_ideas.md
**Dataset(s):** data/kaggle.csv, data/web_traffic.csv
**Date:** 2026-03-17

---

## 1. Research Question

The researcher wants a comprehensive exploratory analysis of the Superstore retail dataset (`kaggle.csv`) — covering ETL, statistical analysis, visualisation, and reporting — in preparation for a technical interview spanning easy to very hard questions.

---

## 2. Dataset Summary

### 2a — kaggle.csv (Superstore Sales)

| Column | Type | Missing % | Notes |
|---|---|---|---|
| Row ID | int64 | 0% | Synthetic row key — drop before modelling |
| Order ID | str | 0% | Links line items to orders |
| Order Date | str→datetime | 0% | Range: 2014-01-03 to 2017-12-30 |
| Ship Date | str→datetime | 0% | Used to derive `days_to_ship` |
| Ship Mode | str (4 cats) | 0% | Standard Class dominates (60%) |
| Customer ID | str | 0% | Identifier — useful for repeat-purchase analysis |
| Customer Name | str | 0% | PII-adjacent; drop from models |
| Segment | str (3 cats) | 0% | Consumer 52%, Corporate 30%, Home Office 18% |
| Country | str | 0% | All USA — column is constant, drop |
| City | str | 0% | 531 unique cities |
| State | str | 0% | 49 unique states |
| Postal Code | int64 | 0% | Numeric but geo — treat as categorical |
| Region | str (4 cats) | 0% | West 32%, East 28%, Central 23%, South 16% |
| Product ID | str | 0% | Identifier |
| Category | str (3 cats) | 0% | Office Supplies 60%, Furniture 21%, Technology 18% |
| Sub-Category | str (17 cats) | 0% | Binders & Paper dominate volume |
| Product Name | str | 0% | 1,850 unique products — high cardinality |
| Sales | float64 | 0% | Mean $230, max $22,638, right-skewed |
| Quantity | int64 | 0% | Range 1–14, mean ~4 |
| Discount | float64 | 0% | Range 0–0.8; 856 rows >50% discount |
| Profit | float64 | 0% | Mean $29, range -$6,600 to +$8,400 |

**Key observations:**
- No missing values; no duplicate rows — clean on arrival.
- 1,871 rows (18.7%) have negative profit; the majority coincide with high discounts.
- `Country` is constant (United States) — safe to drop.
- `Sales` and `Profit` are heavily right-skewed; log transforms likely needed for modelling.
- Date range spans four full calendar years — seasonal and trend decomposition is viable.
- `Tables` sub-category is known to be a chronic loss-maker in this dataset.


**Key observations:**
- No missing values; no duplicates.
- `Page Views = 0` (check count) may represent bots or tracking failures — flag as dirty.
- `Conversion Rate` is effectively binary (1 or <1 in 11.4% of rows) — if used as a target, treat as classification.
- Dataset is small (2,000 rows); limited power for complex models.

---

## 3. Proposed Phases

### Phase 1 — ETL & Preprocessing

**Superstore:**
- Parse `Order Date` and `Ship Date` as datetime
- Engineer `days_to_ship = Ship Date - Order Date`
- Engineer `profit_margin = Profit / Sales`
- Drop constant column `Country`; drop PII columns (`Customer Name`) before modelling
- Flag dirty rows: rows where `Sales <= 0` or `Profit` is extreme outlier (>3 IQR) → `output/PROJECT_XX/dirty.csv`
- Encode categoricals: ordinal encode `Ship Mode`; one-hot encode `Segment`, `Category`, `Region`

**Web traffic:**
- Flag rows where `Page Views == 0` as dirty
- Bin `Previous Visits` into 0 / 1–2 / 3+ cohorts
- Derive binary `converted` column from `Conversion Rate` (1 = converted, 0 = not)

### Phase 2 — EDA & Visualisation

All plots saved to `output/PROJECT_XX/`.

| # | Chart | Insight target |
|---|---|---|
| 1 | Profit distribution (histogram + KDE) | Skewness, loss tail |
| 2 | Profit by Category (box plot) | Category-level P&L |
| 3 | Profit by Sub-Category (bar chart, sorted) | Which sub-cats lose money |
| 4 | Discount vs Profit scatter (with regression line) | Discount cannibalisation |
| 5 | Sales & Profit over time (monthly line chart) | Seasonality & trend |
| 6 | Region × Segment heatmap (avg profit margin) | Geographic & segment mix |
| 7 | Ship Mode vs Profit margin (violin) | Logistics cost signal |
| 8 | Top 10 / Bottom 10 products by profit | SKU-level winners/losers |
| 9 | Customer repeat-purchase distribution | RFM preparation |


### Phase 3 — Statistical Analysis

- **Correlation matrix** of numeric features (Sales, Quantity, Discount, Profit, days_to_ship, profit_margin)
- **ANOVA / Kruskal-Wallis** — test whether mean profit differs across Region, Segment, Category
- **Chi-square test** — Segment × Ship Mode independence
- **Discount threshold analysis** — breakeven discount level per category (where avg profit turns negative)
- **RFM scoring** — Recency, Frequency, Monetary value per customer; segment into quartile tiers
- **Time-series decomposition** (STL) — trend + seasonality of monthly sales

### Phase 4 — Feature Engineering & Modelling

**Target:** `is_loss` (binary: 1 if Profit < 0) — classification task to predict which orders will lose money.

**Features to include:**
- `Category`, `Sub-Category`, `Segment`, `Region`, `Ship Mode`
- `Sales`, `Quantity`, `Discount`
- `days_to_ship`, `order_month`, `order_year`, `order_dayofweek`
- `profit_margin` (exclude if leakage concerns apply)

**Models:**
1. Logistic Regression — baseline, interpretable coefficients
2. Random Forest — handles non-linearity, provides feature importances
3. XGBoost — strong benchmark for tabular data

**Cross-validation:** Stratified 5-fold (class imbalance ~19% positive).

**Metrics:** AUROC, F1-score (macro), precision/recall for the loss class, confusion matrix.

**Outputs:** Feature importance chart, ROC curve, classification report CSV.

### Phase 5 — Reporting

All outputs saved to `output/PROJECT_XX/`:

```
output/PROJECT_XX/
├── dirty.csv                    # Removed rows with reason column
├── superstore_eda.html          # Interactive EDA report (or PDF)
├── plots/
│   ├── profit_distribution.png
│   ├── profit_by_subcategory.png
│   ├── discount_vs_profit.png
│   ├── sales_over_time.png
│   ├── region_segment_heatmap.png
│   └── ... (all charts above)
├── tables/
│   ├── rfm_scores.csv
│   ├── profit_by_category.csv
│   ├── discount_breakeven.csv
│   └── statistical_tests.csv
└── model/
    ├── feature_importances.png
    ├── roc_curve.png
    └── classification_report.csv
```

---

## 4. Open Questions / Assumptions

- **Dataset identity assumed:** `kaggle.csv` = Superstore Final dataset from Kaggle (Vivek468); `web_traffic.csv` = Anthony Therrien website traffic dataset. Both are confirmed by `kagggle.md`.
- **Interview scope:** Assumed to cover all difficulty levels (EDA through ML). Plan covers this breadth.
- **Profit margin leakage:** `profit_margin = Profit / Sales` is derived from the target-adjacent column `Profit`. Will exclude from the model or treat with care and document explicitly.
- **Web traffic conversion rate:** Treating as near-binary (1.0 = converted). If the float values represent partial attribution, the modelling approach changes.
- **No external validation data:** Analysis is self-contained within the two CSV files.
- **`Country` column:** Constant (all USA) — safe to drop; confirmed by inspection.

---

## 5. Risks & Mitigations

| Risk | Mitigation |
|---|---|
| High discount rows dominate loss signal | Analyse discount as continuous and bucketed; document breakeven points |
| Class imbalance (~19% loss rows) | Use stratified k-fold; report F1 and AUROC, not just accuracy |
| Right-skewed Sales/Profit distributions | Apply log1p transform for modelling; use median in summaries |
| `Tables` sub-category chronic losses may overwhelm signal | Investigate separately; consider sub-category fixed effects |
| Web traffic `Conversion Rate` near-constant | Document limitation; if used as target, use binary classification with appropriate class weights |
| `Page Views = 0` rows | Flag as dirty, remove, save to `dirty.csv` with reason = "zero_page_views" |
| Encoding high-cardinality `Product Name` | Exclude from baseline model; use target-encoding or embeddings only if justified |

---

## 6. Interview Preparation — Question Tiers

### Easy
- What is the average profit margin by category?
- Which region has the highest total sales?
- How many unique customers are there?
- What is the most common ship mode?

### Intermediate
- Is there a statistically significant difference in profit across regions?
- At what discount level does profit turn negative on average?
- Which sub-categories are consistently unprofitable?
- How would you detect and handle outliers in the `Sales` column?

### Hard
- How would you build an RFM model for customer segmentation from this data?
- Design a model to predict whether an order will be loss-making before it ships. What features would you use and why? How would you handle leakage?
- How would you decompose the time-series of monthly sales into trend and seasonality? What conclusions would you draw?
- If you wanted to recommend an optimal discount strategy per sub-category, how would you frame this as an optimisation problem?

---

*Plan ready for `/spec _plans/kaggle_plan.md`.*
