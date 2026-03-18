# Insight Report: revenue_heatmap.png

![image](../charts/revenue_heatmap.png)

**Chart type:** Heatmap (matrix)
**Variables displayed:** Y-axis: Region (West, South, North, East); X-axis: Category (Consulting, Software, Training, Web Dev); Cell values and colour: Revenue sum ($)
**Generated:** 2026-03-18

---

## Key Observation

The heatmap reveals two $0 cells -- East x Consulting and West x Consulting -- meaning Consulting revenue is entirely concentrated in North ($9,675) and South ($10,350). This is the most striking structural finding: half the regions have zero Consulting penetration. The hottest cells are West x Software ($11,840) and South x Web Dev ($11,410), representing the peak revenue concentrations in the matrix.

## Business / Scientific Implication

The Consulting gap in East and West represents an immediate growth opportunity. Consulting has the highest AOV ($2,503) of any category, so even adding 2--3 Consulting deals per region could generate $5,000--$7,500 in incremental revenue. Sales leadership should investigate whether the gap is due to (a) no Consulting capability in those regions, (b) no market demand, or (c) simply no sales effort. If it's (c), reallocating one Consulting-experienced rep or running a targeted campaign could unlock a dormant revenue pocket.

## Deeper Analysis

Beyond the two zero cells, the heatmap reveals distinct regional specialisations that were invisible in the aggregate regional bar chart. South's revenue is bipolar -- heavy in Consulting ($10,350) and Web Dev ($11,410) but weak in Software ($4,557) and almost negligible in Training ($855). West is the mirror opposite -- strongest in Software ($11,840) with zero Consulting. North is the most balanced region ($5,940--$9,675 range across all four categories). East substitutes Software ($8,124) and Web Dev ($8,118) for its missing Consulting, creating a near-identical pair. South's Training cell at $855 is the lowest non-zero value in the matrix -- effectively a dead zone that suggests Training does not resonate with South's customer base. The diagonal pattern (high Consulting in South/North, high Software in West/East) suggests regional market composition differences, not random allocation.

## Confidence Assessment

**Confidence:** High
**Rationale:** Zero-revenue cells and revenue concentrations are unambiguous in the annotated heatmap; the 4x4 matrix covers all region-category intersections completely.

## Suggested Next Steps

1. Pilot a Consulting sales initiative in East and West regions, starting with the highest-AOV product (Data Cleansing Service) to test whether demand exists.
2. Investigate why South generates only $855 in Training -- determine if this is a demand issue or a coverage gap, and whether bundling Training with South's strong Consulting pipeline could lift both.
