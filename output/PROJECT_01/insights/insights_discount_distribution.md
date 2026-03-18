# Insight Report: discount_distribution.png

![image](../charts/discount_distribution.png)

**Chart type:** Stacked/overlaid histogram, coloured by product category
**Variables displayed:** X-axis: Discount percentage (0--20%); Y-axis: Order count; Colour: Category (Software, Web Dev, Training, Consulting)
**Generated:** 2026-03-18

---

## Key Observation

Discounts cluster heavily at 0% and 5%, which together account for roughly 60--65% of all orders. The distribution is strongly right-skewed: the 10% bin captures a significant secondary peak (dominated by Web Dev), while the 15% and 20% bins are sparsely populated with only 1--2 orders each. This reveals a tiered discounting structure rather than a continuous negotiation model.

## Business / Scientific Implication

The concentration at 0--5% suggests the sales team defaults to minimal or no discounting on most deals, which is healthy for margin protection. However, Web Dev stands out as the category most frequently discounted at the 10% tier (visually the largest share in that bin), signalling either competitive pricing pressure or a deliberate volume strategy. Finance should review whether the higher-discount Web Dev deals deliver proportional volume to justify the margin erosion.

## Deeper Analysis

Four discrete discount tiers are visible (0%, 5%, 10%, 15--20%), with virtually no orders at intermediate values -- this confirms a structured discount policy rather than ad hoc negotiation. Consulting is almost entirely at 0--5%, consistent with its premium positioning and highest AOV in the dataset. Training appears prominently in the 5% and 10% bins, suggesting moderate flexibility. The 15% and 20% bins are the tail -- only Software and Web Dev appear at 15%, and only Web Dev reaches 20%. A casual reader might see a simple "most orders are low-discount" story, but the category breakdown reveals that discount aggressiveness varies systematically by product line, not randomly by deal. The absence of discounts between 5% and 10% (no 6--9% values) further confirms pre-set tiers.

## Confidence Assessment

**Confidence:** High
**Rationale:** Discrete, validated discount_pct values from clean data; category breakdowns are unambiguous in the visual.

## Suggested Next Steps

1. Correlate discount level with deal close rate and time-to-close to determine if higher discounts actually accelerate sales or simply reduce margin without volume benefit.
2. Analyse whether the 15--20% discount tail is concentrated with specific sales reps (potential policy compliance issue).
