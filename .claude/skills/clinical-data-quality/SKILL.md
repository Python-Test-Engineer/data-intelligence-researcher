# Skill: Clinical Data Quality — Neuroblastoma Datasets

Use this skill when deciding whether a row is dirty and should be removed. Dirty rows are **never fixed** — they are removed and written to `output/PROJECT_XX/dirty.csv` with a `reason` column describing exactly why.

---

## Core Rule

> If a row cannot be trusted to represent a real patient with reliable data, remove it. Imputing clinical data introduces assumptions that can corrupt survival analysis and inflate apparent model performance.

---

## Universal Dirty-Row Rules

Apply these to any clinical dataset regardless of study:

| Rule | Condition | Reason value |
|------|-----------|--------------|
| Negative survival time | `survival_time_days < 0` | `negative_survival_time` |
| Zero survival with no event | `survival_time_days == 0 AND event == 0` | `zero_survival_censored` |
| Age out of paediatric range | `age_at_diagnosis_days < 0 OR age_at_diagnosis_days > 6570` (>18 years) | `age_out_of_range` |
| Missing primary target | Target column is null/NaN | `missing_target` |
| Duplicate patient ID | Same patient ID appears more than once | `duplicate_patient_id` |
| All-null feature row | >90% of feature columns are null | `sparse_row` |

---

## Neuroblastoma-Specific Rules

### MYCN Status
| Condition | Reason value |
|-----------|--------------|
| Value not in `{0, 1, "amplified", "not amplified", "NA"}` | `invalid_mycn_value` |
| MYCN amplification copy number < 0 | `negative_copy_number` |

Do **not** impute missing MYCN status — it is a primary biomarker and guessing is clinically unacceptable.

### Staging
| Condition | Reason value |
|-----------|--------------|
| INSS stage not in `{1, 2, 2A, 2B, 3, 4, 4S}` | `invalid_inss_stage` |
| INRG stage not in `{L1, L2, M, MS}` | `invalid_inrg_stage` |
| Both INSS and INRG stages present but contradictory | `contradictory_stage` |

### Risk Group
| Condition | Reason value |
|-----------|--------------|
| Risk group not in expected vocabulary for the dataset | `invalid_risk_group` |
| Risk group contradicts MYCN + stage combination (e.g. MYCN amplified labelled as low-risk) | `contradictory_risk_group` |

Flag contradictions — do not silently correct them.

### Survival / Event Data
| Condition | Reason value |
|-----------|--------------|
| Event column contains values outside `{0, 1}` after encoding | `invalid_event_value` |
| Survival time implausibly long (>10,950 days / 30 years) | `implausible_survival_time` |
| Patient marked as deceased with survival time = 0 | `death_at_zero_time` |

### Gene Expression
| Condition | Reason value |
|-----------|--------------|
| Sample has >20% of genes with expression = 0 (for RNA-seq) | `excessive_zero_expression` |
| Sample is a clear outlier: mean expression >4 SD from cohort mean | `expression_outlier` |
| Sample ID cannot be matched to clinical metadata | `unmatched_expression_sample` |

---

## How to Apply

```python
import pandas as pd
from pathlib import Path

def flag_dirty(df: pd.DataFrame, output_dir: Path) -> pd.DataFrame:
    """Remove dirty rows, write them to dirty.csv, return clean df."""
    dirty_rows = []

    # Example: negative survival time
    mask = df["survival_time_days"] < 0
    dirty_rows.append(df[mask].assign(reason="negative_survival_time"))
    df = df[~mask]

    # ... apply each rule in turn ...

    dirty = pd.concat(dirty_rows, ignore_index=True)
    dirty_path = output_dir / "dirty.csv"

    if dirty_path.exists():
        dirty.to_csv(dirty_path, mode="a", header=False, index=False)
    else:
        dirty.to_csv(dirty_path, index=False)

    print(f"Removed {len(dirty)} dirty rows. Remaining: {len(df)}")
    return df
```

---

## Reporting Dirty Rows

Always print a summary after cleaning:

```
Data quality report
-------------------
Total rows loaded:     N
Dirty rows removed:    X
  negative_survival_time:    n1
  missing_target:            n2
  duplicate_patient_id:      n3
  ...
Clean rows retained:   N - X
Dirty rows written to: output/PROJECT_XX/dirty.csv
```

If >10% of rows are removed, raise a warning and note it in the plan/report — this level of data loss should be reviewed by the researcher before proceeding.

---

## What is NOT a dirty row

Do not remove rows for:
- Missing **non-critical** features (e.g. tumour site, treatment centre) — these can be missing
- Missing expression data for a subset of genes — handle with imputation or feature exclusion, documented in the spec
- Uncommon but valid values (e.g. very long survival times if clinically plausible)

When uncertain, **flag and ask the researcher** rather than silently removing.
