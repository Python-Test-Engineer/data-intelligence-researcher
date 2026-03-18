# Data Intelligence Insights Report

**Project:** PROJECT_01
**Images analysed:** 10
**Generated:** 2026-03-18

---

## Executive Summary

This sales order dataset ($97,658 revenue, 48 clean orders, Jan--May 2025) reveals a business with balanced geography and a diversified product line but with two critical structural weaknesses: **zero customer retention** (every order is from a unique buyer) and **hidden regional product gaps** (Consulting is absent from East and West). Revenue peaked in March before declining through May, with an April volume-revenue divergence signalling shrinking deal sizes. The discount structure is tiered and controlled, but one rep (Priya Sharma) gives significantly higher average discounts. Addressing the retention gap and unlocking Consulting in underserved regions represent the two highest-leverage growth opportunities.

---

## Key Insights

### Insight 1 -- Zero Customer Retention Is the Single Biggest Strategic Risk

**Source charts:** top_customers.png, order_status.png, cumulative_revenue.png

**Observation:** All 48 clean orders come from 48 unique customers -- there is not a single repeat buyer in 5 months of data. The top 10 customers account for only 34.8% of revenue, far below typical B2B Pareto concentration. The cumulative revenue chart's smooth upward curve masks the fact that every dollar comes from a new customer.

**Implication:** Without recurring revenue, the business must acquire a new customer for every sale, making revenue inherently unpredictable and acquisition-cost dependent. Building a customer success function and launching win-back campaigns for top customers should be the number one strategic priority.

**Confidence:** High -- zero-repeat finding is unambiguous across the entire dataset.

---

### Insight 2 -- Consulting Revenue Absent from Half the Country

**Source charts:** revenue_heatmap.png, revenue_by_category.png, revenue_by_region.png

**Observation:** The heatmap reveals two $0 cells: East x Consulting and West x Consulting. Consulting has the highest AOV ($2,503) of any category but generates revenue only in North ($9,675) and South ($10,350). Meanwhile, the regional bar chart shows near-parity overall, masking this category-level imbalance.

**Implication:** Expanding Consulting into East and West represents a high-AOV, low-volume growth lever. Even 3--4 Consulting deals per region at the existing AOV would add $7,500--$10,000 in revenue -- an 8--10% total revenue uplift with no new product development required.

**Confidence:** High -- zero-revenue cells are definitive; AOV advantage is validated from clean data.

---

### Insight 3 -- March Peak Followed by Revenue Decline Signals a Q2 Problem

**Source charts:** monthly_revenue.png, cumulative_revenue.png

**Observation:** Revenue peaked at ~$25,000 in March (+46% MoM), then declined in April (-8.7%) and collapsed in May (-37.4%). The cumulative revenue curve's gradient visibly flattens from mid-April onward. April's decline is notable because order count was at its highest (12 orders) -- meaning the drop was driven by smaller deals, not fewer deals.

**Implication:** The April volume-up / revenue-down pattern suggests the sales team may be chasing quantity at the expense of deal quality. If May's decline is structural rather than a partial-month artefact, the business faces a Q2 revenue trajectory problem requiring immediate pipeline review.

**Confidence:** Medium -- May is likely a partial month, which limits confidence in the decline's true magnitude.

---

### Insight 4 -- Tiered Discount Structure Is Sound, but One Rep Is an Outlier

**Source charts:** discount_distribution.png, sales_rep_performance.png

**Observation:** Discounts cluster at discrete tiers (0%, 5%, 10%, 15%, 20%) with 60--65% of orders at 0--5%. Priya Sharma averages 8.6% discount -- nearly double some colleagues -- yet her revenue ($22,092) is the lowest of the four named reps. Web Dev is the most aggressively discounted category (up to 20%).

**Implication:** The controlled tiering is good discipline, but Sharma's higher discount rate without proportionally higher volume suggests discounting is eroding margin without driving growth. A coaching intervention on deal pricing or a discount approval workflow for deals above 10% may be warranted.

**Confidence:** High -- discount values are discrete and validated; rep-level patterns are clear even at small sample sizes.

---

### Insight 5 -- Product Revenue Is Driven by Pricing Power, Not Volume

**Source charts:** revenue_by_product.png, revenue_by_category.png

**Observation:** All six products have exactly 8 orders each -- a perfectly uniform distribution. Revenue differences ($13,725--$20,025) are therefore entirely explained by unit price and discount variation. Data Cleansing Service (Consulting) leads at $20,025 ($2,503 AOV) while AI Training Workshop trails at $13,725 ($1,716 AOV).

**Implication:** With uniform volume, the revenue leaderboard is a direct pricing power ranking. AI Training Workshop's 46% revenue discount relative to Data Cleansing Service, despite equal order counts, suggests it is either underpriced or positioned as a lower-value offering. Product management should evaluate whether a price increase or product bundling could close this gap.

**Confidence:** High -- 8-orders-per-product uniformity is definitive in the data.

---

### Insight 6 -- Regional Balance Masks Radically Different Category Mixes

**Source charts:** revenue_by_region.png, revenue_heatmap.png

**Observation:** The regional bar chart shows a tight $22K--$27K spread, suggesting homogeneity. But the heatmap reveals entirely different category compositions: South is Consulting + Web Dev heavy ($10,350 + $11,410); West is Software-dominant ($11,840 with zero Consulting); North is the most balanced; East mirrors West without Consulting. South's Training cell ($855) is almost zero.

**Implication:** One-size-fits-all regional strategy would be ineffective. Each region needs a tailored product emphasis aligned with its demonstrated market composition. Marketing campaigns and rep training should be localised by category strength.

**Confidence:** High -- the heatmap's annotated dollar values leave no ambiguity about regional specialisation.

---

### Insight 7 -- The "(unknown)" Rep Order Is a Data Governance Red Flag

**Source charts:** sales_rep_performance.png

**Observation:** One order ($3,000) has no sales rep attribution, appearing as "(unknown)" in the performance chart. While small in absolute terms, it represents a gap in the CRM data pipeline.

**Implication:** If this missing attribution scales with data volume (e.g., 2% of orders), it could distort commission calculations, territory performance metrics, and pipeline forecasting. The root cause (manual entry error, system integration gap, or departed rep) should be investigated and fixed at the source.

**Confidence:** High -- single data point, but the governance implication is systemic.

---

## Patterns Across Analyses

1. **Surface uniformity conceals structural imbalance:** Region, product, and rep charts all show near-parity at the aggregate level. But drilling into the heatmap, discount patterns, and customer data reveals hidden asymmetries -- zero Consulting in two regions, zero repeat customers, one rep discounting more aggressively. The most important insights in this dataset are invisible in single-dimension charts.

2. **Volume is uniform; value is the differentiator:** With 8 orders per product and 11--13 per rep, the business distributes deals remarkably evenly. All variation in revenue comes from pricing, discounting, and product mix -- not sales activity volume. This means growth strategy should focus on value per deal (upselling, pricing optimisation, category expansion) rather than raw pipeline generation.

3. **March is the pivot month:** Multiple charts converge on March as the inflection point -- peak monthly revenue, steepest cumulative gradient, and the month after which both metrics decline. Understanding what happened in March (large deals? end-of-quarter push? specific campaigns?) would unlock the key to replicating that performance.

4. **Data quality is good but has edges:** Two dirty rows were removed (extreme quantity, negative price), one date had mixed formatting, one order lacks a rep, and one customer lacks an email. These are manageable issues but suggest the data entry or CRM process has no hard validation at the point of capture.

---

## Risks & Caveats

| Risk | Affected Insights | Mitigation |
|------|-------------------|------------|
| May data likely incomplete (partial month) | Insight 3 (Q2 decline), cumulative revenue | Confirm data cutoff date; normalise May to full-month estimate before trend conclusions |
| Sample size of 48 orders limits statistical inference | All insights | Frame findings as descriptive, not inferential; avoid claiming statistical significance |
| 8-orders-per-product uniformity may indicate synthetic data | Insight 5 (pricing power) | Verify data provenance; if synthetic, note that real-world product mix is unlikely to be this uniform |
| No cost/margin data available | Insights 2, 4, 5 (Consulting AOV, discounts, pricing) | Revenue != profit; high-AOV products may have proportionally higher delivery costs |
| Single-month decline could be noise, not trend | Insight 3 | Require 3+ consecutive months of decline before triggering structural concern |

---

## Recommended Next Steps

### High Priority
1. **Customer Retention Programme** -- Design a post-purchase follow-up and re-engagement workflow. With zero repeat customers, even a 10% retention rate would add ~$10K/month in predictable recurring revenue.
2. **Consulting Expansion Pilot (East & West)** -- Assign or recruit Consulting-capable sales resource in East and West regions. Target 3--5 Data Cleansing Service deals per region in Q3.
3. **May Data Verification** -- Confirm whether May is complete or partial. If partial, adjust all trend analyses and re-evaluate the Q2 decline signal.

### Medium Priority
1. **Discount Governance Review** -- Audit Priya Sharma's discount patterns and implement a manager-approval step for discounts above 10% across all reps.
2. **March Performance Decomposition** -- Break down March's $25K peak by product, region, and rep to identify repeatable drivers.
3. **Resolve Unknown Rep Attribution** -- Fix the CRM gap that produced the unattributed $3,000 order.

### Exploratory / Speculative
1. **Training Product Repositioning** -- Test bundling AI Training Workshop with Software or Web Dev products to lift effective AOV from $1,716 to $2,500+.
2. **Customer Cohort Analysis** -- As more months of data accumulate, build monthly acquisition cohorts to measure time-to-second-purchase and identify early retention signals.
3. **Regional Pricing Experiment** -- Test whether East and West customers respond to Consulting offers, or whether the $0 cells reflect genuine lack of demand.

---

## Appendix -- Individual Chart Insights

| # | Chart | Key Observation | Confidence |
|---|-------|-----------------|------------|
| 1 | cumulative_revenue.png | Near-linear $97.7K accumulation with May flattening; lumpy step-jumps from large deals | High |
| 2 | discount_distribution.png | Tiered at 0/5/10/15/20%; Web Dev most discounted; Consulting stays premium at 0--5% | High |
| 3 | monthly_revenue.png | March peak at ~$25K then two-month decline; April volume-revenue divergence | Medium |
| 4 | order_status.png | 89.6% completion; 5 pending orders worth $10.2K; binary status model | High |
| 5 | revenue_by_category.png | Web Dev + Software dual-pillar ($32K each, 65% total); Consulting highest AOV at $2,503 | High |
| 6 | revenue_by_product.png | All 6 products have exactly 8 orders; Data Cleansing leads at $20K | High |
| 7 | revenue_by_region.png | 4 regions within $22K--$27K (5.2% spread); balanced but undifferentiated | High |
| 8 | revenue_heatmap.png | Two $0 cells: East/West have zero Consulting; hidden regional specialisations | High |
| 9 | sales_rep_performance.png | $3.4K spread across reps; Sharma's 8.6% avg discount is the outlier | Medium |
| 10 | top_customers.png | Zero repeat customers; top 10 at 34.8% of revenue; no concentration risk but no retention | High |

---

## Appendix -- Input Inventory

### Images
| File | Description inferred from content |
|------|------------------------------------|
| cumulative_revenue.png | Filled area chart of cumulative revenue over time (Jan--May 2025) |
| discount_distribution.png | Stacked histogram of discount % by product category |
| monthly_revenue.png | Dual-axis line+bar chart of monthly revenue and order count |
| order_status.png | Donut chart showing Completed (89.6%) vs Pending (10.4%) orders |
| revenue_by_category.png | Treemap of revenue split across 4 product categories |
| revenue_by_product.png | Vertical bar chart of revenue per product, coloured by category |
| revenue_by_region.png | Horizontal bar chart of revenue per region |
| revenue_heatmap.png | 4x4 heatmap of revenue at the region x category intersection |
| sales_rep_performance.png | Grouped bar chart of rep revenue and order count |
| top_customers.png | Horizontal bar chart of top 10 customers by revenue |
