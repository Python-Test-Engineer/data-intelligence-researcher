# Insight Report: revenue_by_product.png

![image](../charts/revenue_by_product.png)

**Chart type:** Vertical bar chart, coloured by product category
**Variables displayed:** X-axis: Product name; Y-axis: Revenue ($); Colour: Category (Consulting, Web Dev, Software, Training)
**Generated:** 2026-03-18

---

## Key Observation

Data Cleansing Service (Consulting, $20,025) is the single highest-revenue product, followed by Dashboard Build (Web Dev, $18,370). The spread from highest to lowest product is only $6,300 ($20,025 to $13,725), with all six products falling within a relatively narrow $13K--$20K band. Every product has exactly 8 orders, meaning revenue differences are driven entirely by unit price and discount variation, not volume.

## Business / Scientific Implication

The uniform order count (8 per product) is a remarkable finding: the sales team is distributing deals evenly across the product line, whether by design or coincidence. This means the revenue ranking is purely a function of pricing power. Data Cleansing Service commands the highest effective price per deal ($2,503 AOV), while AI Training Workshop is the lowest ($1,716). Product management should consider whether Training's lower price reflects market positioning or underpricing -- a $200 price increase per Training deal would add $1,600 to total revenue without any volume change.

## Deeper Analysis

The category-colour coding reveals a clear tiering: Consulting (blue) leads, followed by Web Dev (orange) products with a within-category split (Dashboard Build at $18,370 vs. Web Starter Package at $14,152 -- a $4,218 gap despite the same order count). This within-category variance is larger than some between-category gaps, suggesting product-level pricing matters more than category-level strategy. The two Software products (Data Analytics Pro $16,440 and Insight Reporting Suite $14,945) are mid-pack and closely spaced. AI Training Workshop sits alone as the single Training product and the revenue laggard. The even distribution of 8 orders per product across 48 total orders is suspiciously uniform for real-world data -- this could indicate the dataset was generated or balanced, which would be important context for interview questions about data provenance.

## Confidence Assessment

**Confidence:** High
**Rationale:** Clean revenue values with exact 8-order-per-product uniformity clearly visible; category colouring is unambiguous.

## Suggested Next Steps

1. Investigate why Web Starter Package lags Dashboard Build by $4,218 despite equal volume -- is it purely unit price, or are discounts more aggressive on the Starter product?
2. Evaluate whether AI Training Workshop should be repositioned as an upsell/add-on rather than a standalone product to capture higher effective revenue per engagement.
