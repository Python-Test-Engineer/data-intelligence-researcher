# Insight Report: order_status.png

![image](../charts/order_status.png)

**Chart type:** Donut chart
**Variables displayed:** Segments: Order status (Completed, Pending); Values: Order count as percentage of total
**Generated:** 2026-03-18

---

## Key Observation

89.6% of orders (43 of 48) are Completed, with 10.4% (5 orders) still Pending. The completion rate is healthy for a B2B sales operation, but the Pending slice represents ~$10,190 in unrealised revenue -- roughly 10.4% of the total pipeline value. The donut chart shows a clean two-state system with no cancelled, refunded, or failed statuses.

## Business / Scientific Implication

A 10.4% pending rate is operationally manageable but strategically important -- converting all 5 pending orders would add $10K to recognised revenue. Operations should prioritise these pending orders for follow-up, especially if they are concentrated in recent months (which would explain the May revenue dip visible in other charts). The absence of any "Cancelled" or "Failed" status is noteworthy: either cancellations are not tracked, or the business has a zero-churn pipeline, which warrants verification.

## Deeper Analysis

The simplicity of this two-state breakdown is itself an insight. Most mature B2B operations would have 3--5 statuses (e.g., Pending, In Progress, Completed, Cancelled, Refunded). The binary Completed/Pending model suggests either (a) the business is early-stage and hasn't needed more granular tracking, or (b) the dataset has been simplified. If pending orders are disproportionately from May, the 10.4% rate could actually represent a much higher recent-month pending rate masked by the denominator of all 5 months. A casual reader sees "90% complete, looks great" -- but the more actionable question is whether the pending orders are aging (stale pipeline) or recent (normal processing lag). Without a "days pending" metric, this chart alone cannot distinguish between the two.

## Confidence Assessment

**Confidence:** High
**Rationale:** Binary status field with no missing values; percentages directly computed from clean validated data.

## Suggested Next Steps

1. Cross-reference pending orders by month and region to determine if they cluster in May (pipeline lag) or are distributed (systemic completion issue).
2. Add a "days since order" metric to pending orders to identify stale pipeline items that may need escalation or write-off.
