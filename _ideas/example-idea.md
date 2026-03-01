# Example Idea File

This file shows the kind of content to put in an idea file. It does not need to be
formal or structured — rough notes, questions, and bullet points are fine. Claude
will ask clarifying questions during /plan if anything is unclear.

---

## What I want to explore

I want to predict which neuroblastoma patients are likely to relapse within 3 years
of diagnosis, using gene expression data combined with clinical variables.

The dataset is `data/seqc_neuroblastoma.csv`. It contains Affymetrix microarray
expression values for ~500 patients alongside clinical annotations.

## What I think matters

- MYCN amplification is probably the strongest predictor but I want to see if
  expression signatures can add anything on top of it
- I suspect patients under 18 months behave differently — maybe worth stratifying
- Not sure whether to model this as binary (relapsed yes/no at 3 years) or use
  the actual time-to-event data. Leaning towards binary for simplicity but open
  to advice.

## What I want as output

- A model I can apply to new patients
- A plot showing the most important genes/features
- A Kaplan-Meier curve comparing predicted high-risk vs low-risk groups
- A plain-language summary of what the model found

## Things I'm not sure about

- How to handle batch effects if samples came from different centres
- Whether to use all ~54,000 probes or filter to known cancer genes first
- What counts as a good result — is 0.75 AUROC acceptable for this cohort?
