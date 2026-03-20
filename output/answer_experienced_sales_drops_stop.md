---
question: "why have we experienced sales drops if at all and what could we do to stop this"
generated: 2026-03-20
project: PROJECT_01
---

### Answer

Yes — two consecutive months of sales drops have occurred after a March 2025 peak. April fell **-8.7%** ($22,790) despite the highest order count of any month, meaning the drop was caused by **shrinking deal sizes**, not fewer deals. May then fell a further **-37.4%** ($14,270) with both order volume and revenue collapsing simultaneously, signalling a **pipeline problem**. Three structural fixes are supported by the evidence: stop discounting without results (one rep is discounting heavily with no revenue gain), launch a customer retention programme (zero repeat buyers means every slow month is unmitigated), and expand Consulting into East and West regions where it is entirely absent.

---

### Supporting Evidence

- **`summary_stats.csv` — `monthly_revenue`** — Exact MoM figures: Jan $18,555 → Feb $17,074 (-8.0%) → **Mar $24,969 (+46.2%)** → Apr $22,790 (-8.7%) → May $14,270 (-37.4%). April's AOV dropped from $2,270 to $1,899 while order count rose to 12 — the only month where volume and revenue moved in opposite directions.

- **`monthly_revenue.png`** — The chart visually confirms the divergence: the revenue line (blue) drops from its March peak while the order count bars rise in April, then both collapse in May. The divergence between the two series in April is the clearest visual signal in the dataset.

- **`cumulative_revenue.png`** — The gradient of the filled area curve steepens through mid-March (~$35K to ~$60K in ~3 weeks) then visibly flattens from late April onward, plateauing through May.

- **`insights/insights.md` — Insight 4** — Priya Sharma averages **8.6% discount**, nearly three times James Okafor's 2.9%, yet her revenue ($22,092) is the lowest of all named reps. Discounting is not converting into proportional revenue.

- **`summary_stats.csv` — `kpis`** — `repeat_customer_count = 0`, `one_time_customer_count = 48`. Every single order across 5 months is from a unique buyer. With no recurring revenue base, any drop in new acquisitions produces an immediate and unmitigated revenue fall.

- **`summary_stats.csv` — `region_category_heatmap`** — East × Consulting = **$0**, West × Consulting = **$0**. Consulting carries the highest AOV of any category ($2,503) but is entirely absent from two of four regions.

---

### Confidence

**Medium-High** — The timing and mechanics of the drops are clearly supported by validated transaction data. The *root cause* of April's AOV compression (whether discounting, product mix shift, or customer profile) is strongly indicated but requires deal-level breakdown from `clean.csv` to confirm conclusively.

---

### Caveats & Limitations

May is almost certainly a **partial month** — the cumulative chart shows data running only to ~May 18. Normalised to a full month, May's estimated revenue is ~$19,100, reducing the apparent decline from -37.4% to approximately -16%. The trend is still negative, but the headline figure overstates the severity.

---

### Suggested Follow-up

Filter `clean.csv` to April orders and group by `sales_rep` × `product` × `discount` to determine whether the AOV compression was concentrated in one rep or one product — this single query would identify the precise mechanism behind the most actionable of the two drops.
