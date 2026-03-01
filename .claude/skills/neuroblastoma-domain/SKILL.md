# Skill: Neuroblastoma Domain Knowledge

Use this skill whenever making analytical, modelling, or interpretation decisions in the neuroblastoma research workflow. It ensures oncologically correct choices at every phase.

---

## Disease Overview

Neuroblastoma is the most common extracranial solid tumour in children, arising from neural crest cells of the sympathetic nervous system. It accounts for ~15% of paediatric cancer deaths despite representing only ~8% of childhood cancers. Outcomes range from spontaneous regression (infants, low-risk) to highly aggressive disease with <30% 5-year survival (high-risk, relapsed).

---

## Key Biological Features

### Genomic Markers
| Marker | Clinical Significance |
|--------|-----------------------|
| **MYCN amplification** (>10 copies) | Strongest adverse prognostic marker; defines high-risk regardless of stage |
| **1p deletion** (1p36 LOH) | Adverse; often co-occurs with MYCN amplification |
| **11q aberration** (unbalanced) | Adverse; marks a distinct high-risk subgroup without MYCN amplification |
| **17q gain** | Adverse; most frequent chromosomal change in neuroblastoma |
| **ALK mutation/amplification** | Targetable; present in ~14% of high-risk cases |
| **ATRX mutation** | Associated with older children, poor prognosis |
| **DNA ploidy** (hyperdiploid vs diploid) | Hyperdiploid (triploid) is favourable in infants |
| **Segmental chromosomal aberrations (SCAs)** | Multiple SCAs = worse prognosis even at low stage |

### Tumour Biology Classification
- **Favourable histology**: Schwannian stroma-rich, maturing or well-differentiated, low MKI
- **Unfavourable histology**: Poorly differentiated, high MKI, undifferentiated — per Shimada classification

---

## Risk Stratification

### INRG (International Neuroblastoma Risk Group) Classification
The standard pre-treatment risk schema used in research and clinical trials. Based on:
- **INRG Stage** (L1, L2, M, MS) — not the older INSS staging
- Age at diagnosis
- Histological grade
- DNA ploidy
- MYCN status
- 11q aberration status

| INRG Risk Group | Definition |
|-----------------|------------|
| Very Low | L1, no MYCN amp, any histology |
| Low | L2, age <18mo, favourable features |
| Intermediate | L2, age ≥18mo, or M <18mo without MYCN amp |
| High | M, age ≥18mo; or MYCN amp regardless of stage |

> **Important**: Many older datasets use INSS staging (I–IV, IVS). When using INSS data, be explicit about which staging system is in use and do not conflate L1/L2 with Stage I/II/III.

---

## Clinical Endpoints

| Endpoint | Definition | Notes |
|----------|------------|-------|
| **Event-Free Survival (EFS)** | Time from diagnosis to first event (relapse, progression, secondary malignancy, death) or censoring | Primary endpoint in most trials |
| **Overall Survival (OS)** | Time from diagnosis to death or censoring | Secondary endpoint |
| **Response rate** | CR/PR/MR/NR per INRG criteria at end of induction | Short-term surrogate |

For time-to-event endpoints, use **Cox proportional hazards** or **Kaplan-Meier** methods. Binary classification (alive/dead at fixed time point) is a simplification — flag this if used and justify the cutoff.

---

## Common Datasets

| Dataset | Source | Contents | Notes |
|---------|--------|----------|-------|
| **TARGET Neuroblastoma** | NCI GDC | mRNA, miRNA, WGS, clinical (~250 samples) | Largest US cohort; INRG annotated |
| **SEQC / SEQC-NB** | GEO: GSE49711 | Affymetrix expression (498 samples + 240 validation) | Largest published expression cohort |
| **Kocak (GSE45547)** | GEO | Affymetrix (649 samples, German cohort) | Well-annotated for MYCN, 11q, risk |
| **CAMDA NB** | CAMDA | RNA-seq, clinical | Challenge dataset |
| **INRG Data Commons** | INRG | Multi-cohort, multi-omic | Requires consortium access |

> Gene expression datasets are typically log2-normalised. Confirm normalisation method before analysis. RMA is standard for Affymetrix; TPM/FPKM for RNA-seq.

---

## Feature Engineering Guidance

### Gene Expression
- Apply log2 transformation if raw counts are provided
- Use variance filtering to reduce dimensionality before modelling (top 1000–5000 most variable genes is common)
- Consider pathway-level aggregation (GSVA, ssGSEA) for interpretability
- Watch for batch effects when combining cohorts — apply ComBat or similar correction

### Clinical Features
- Age at diagnosis is highly non-linear — consider log transform or categorical bins (<12mo, 12–18mo, >18mo)
- Stage and risk group are ordinal — do not treat as continuous
- MYCN status is binary (amplified vs not) — never impute; missing = exclude or flag

### Leakage risks
- **Risk group** often encodes the target — do not use as a feature when predicting survival
- **Treatment received** (e.g. high-dose chemotherapy, ASCT) is post-diagnosis and may encode outcome — treat with caution
- **Response to induction** is post-treatment — leakage if predicting EFS from baseline features

---

## Modelling Considerations

### For survival endpoints (EFS/OS)
- Prefer **Cox proportional hazards** (lifelines `CoxPHFitter`, scikit-survival)
- Evaluate with **concordance index (C-index)** — equivalent of AUROC for survival
- Use **time-dependent ROC** (AUROC at specific timepoints, e.g. 3-year, 5-year EFS)
- Check proportional hazards assumption for key covariates

### For binary classification (e.g. high-risk vs non-high-risk)
- Use **stratified k-fold CV** — class imbalance is common (high-risk ~40–50% in most cohorts)
- Report **AUROC, AUPRC, sensitivity, specificity** — accuracy alone is misleading with imbalance
- MYCN amplification alone gives ~0.70 AUROC as a baseline — beat this or justify why you didn't

### Sample sizes
- Most neuroblastoma cohorts are small (n=50–500). Prefer **LOOCV or 5-fold CV** over 80/20 splits for small datasets. External validation on a held-out cohort is strongly preferred over internal-only validation.

---

## Reporting Standards

When summarising results, always report:
- Cohort size (n), with MYCN amplification rate, median age, risk group distribution
- C-index or AUROC with 95% CI (bootstrap preferred)
- Kaplan-Meier curves stratified by predicted risk group if applicable
- Any cohort-merging steps and batch correction applied
- Comparison to a clinically meaningful baseline (MYCN status alone, INRG risk group)
