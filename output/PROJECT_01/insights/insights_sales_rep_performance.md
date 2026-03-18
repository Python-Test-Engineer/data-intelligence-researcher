# Insight Report: sales_rep_performance.png

![image](../charts/sales_rep_performance.png)

**Chart type:** Grouped/stacked bar chart with dual axes
**Variables displayed:** X-axis: Sales Rep; Left Y-axis: Revenue ($); Right Y-axis: Order Count; Colour: Revenue (blue) vs Order Count (red/pink)
**Generated:** 2026-03-18

---

## Key Observation

Sarah Mitchell leads on both revenue ($25,539) and order count (~13), followed closely by James Okafor ($24,172, ~12 orders). Tom Richards and Priya Sharma are tightly clustered at $22,855 and $22,092 respectively. A fifth bar -- "(unknown)" -- shows a single $3,000 order with no assigned rep. The total spread between the top four reps is only $3,447 (13.5%), indicating a balanced but slightly top-heavy team.

## Business / Scientific Implication

The team is performing within a narrow band, which is positive for operational resilience -- no single rep departure would devastate revenue. However, Sarah Mitchell's lead is driven by volume (13 orders vs 11--12 for others) rather than deal size, since her AOV ($1,965) is actually the lowest of the four reps. James Okafor achieves nearly the same revenue with 12 orders, implying a higher AOV ($2,014). Management should recognise that Mitchell's strength is pipeline generation while Okafor's is deal value -- different coaching approaches are needed. The "(unknown)" order ($3,000) represents a data quality issue that should be resolved to ensure accurate rep attribution.

## Deeper Analysis

The dual-axis overlay reveals a subtle but important pattern: the revenue bars and order count bars are almost proportional for Mitchell, Okafor, and Richards, meaning their AOV is consistent (~$1,965--$2,078). Priya Sharma breaks this pattern -- her revenue bar is slightly shorter relative to her order count bar, suggesting she may be giving higher discounts (confirmed by her 8.6% average discount, the highest of any rep per the summary stats). The "(unknown)" bar at $3,000 with a single order is an outlier in the visualisation -- it has the highest AOV of any "rep" ($3,000) but is clearly a data quality gap rather than performance. A casual reader might focus on Mitchell as "the best performer," but her lead is 1 additional deal over Okafor -- at this sample size, that advantage could easily reverse next month.

## Confidence Assessment

**Confidence:** Medium
**Rationale:** Revenue and order counts are validated, but with only 11--13 orders per rep, individual performance rankings are not statistically robust; one large deal would reshuffle the leaderboard.

## Suggested Next Steps

1. Investigate Priya Sharma's higher average discount rate (8.6%) -- determine if it correlates with specific product categories or customer segments, and whether it is eroding margin without delivering proportional volume.
2. Resolve the "(unknown)" rep attribution for the $3,000 order to ensure complete sales tracking and accurate commission calculations.
