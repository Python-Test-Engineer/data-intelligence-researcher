# Insight Report: revenue_by_category.png

![image](../charts/revenue_by_category.png)

**Chart type:** Treemap
**Variables displayed:** Tile area: Revenue sum ($) per product category; Colour intensity: Revenue magnitude (darker = higher); Labels: Category name + revenue value
**Generated:** 2026-03-18

---

## Key Observation

Web Dev ($32,523) and Software ($31,385) dominate the revenue mix, together accounting for roughly 65% of total revenue ($63,908 of $97,658). Consulting ($20,025) and Training ($13,725) occupy the remaining 35%. The treemap visually emphasises the near-parity between the two leading categories -- their tiles are almost identical in size -- while the sharp drop to Consulting and then Training is immediately apparent.

## Business / Scientific Implication

The business has a dual-pillar revenue structure: Web Dev and Software are equally load-bearing and neither can be neglected without a ~33% revenue hit. Consulting punches above its order count (8 orders producing $20K = $2,503 AOV, the highest of any category), making it the margin leader despite lower volume. Strategic investment should consider scaling Consulting's pipeline -- each incremental Consulting deal is worth ~$500 more than an average Web Dev or Software deal. Training at $13,725 is the weakest category and may need repositioning or bundling with higher-value offerings.

## Deeper Analysis

The revenue gap between the top two categories is only $1,138 (3.5%) -- statistically negligible at this sample size. This near-parity means any month where Web Dev loses one deal or Software gains one could flip the ranking. The more meaningful structural observation is the 2:1 revenue ratio between the top tier (Web Dev + Software at ~$32K each) and the bottom tier (Consulting + Training at ~$17K average). Consulting achieves its $20K on just 8 orders, compared to 16 each for Web Dev and Software -- half the volume for 62% of the revenue. This efficiency is the hidden story the treemap reveals through colour intensity (Consulting is noticeably lighter, indicating lower absolute revenue) but masks in tile positioning. Training's small tile at $13,725 across 8 orders yields the lowest AOV ($1,716), suggesting it may function as a loss leader or entry point rather than a profit centre.

## Confidence Assessment

**Confidence:** High
**Rationale:** Revenue sums from validated clean data; four distinct categories with clear separation in the visual.

## Suggested Next Steps

1. Calculate gross margin per category (not just revenue) to determine if Consulting's high AOV translates to higher profitability or if delivery costs erode the advantage.
2. Explore bundling Training with Software or Web Dev engagements to lift Training's effective AOV and reduce standalone dependence on a low-revenue category.
