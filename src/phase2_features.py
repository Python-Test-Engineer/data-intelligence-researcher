"""Phase 2 — Feature Engineering
Loads and cleans data/sales_dummy.csv, computes derived columns,
and saves features.csv and sales_summary.csv to output/PROJECT_01/.
"""
from __future__ import annotations

import warnings
from pathlib import Path

import pandas as pd

RANDOM_SEED = 42
OUTPUT_DIR = Path("output/PROJECT_01")
INPUT_FILE = Path("data/sales_dummy.csv")
REQUIRED_COLUMNS = {"date", "region", "product", "units_sold", "revenue", "cost"}


def load_and_clean(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise ValueError(f"Input file not found: {path}")
    df = pd.read_csv(path)
    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    flagged: set[int] = set()

    # 1. Null fields
    null_mask = df[list(REQUIRED_COLUMNS)].isnull().any(axis=1)
    flagged.update(df.index[null_mask].tolist())

    # 2. Invalid date
    remaining = df.drop(index=list(flagged))
    bad_date = remaining.index[pd.to_datetime(remaining["date"], errors="coerce").isna()]
    flagged.update(bad_date.tolist())

    valid = df.drop(index=list(flagged))

    # 3–5. Non-positive numeric values
    for col, reason in [("units_sold", "non_positive_units"),
                        ("revenue", "non_positive_revenue"),
                        ("cost", "non_positive_cost")]:
        idx = valid.index[valid[col] <= 0]
        flagged.update(idx.tolist())

    valid2 = df.drop(index=list(flagged))

    # 6. Cost exceeds revenue
    bad_cost = valid2.index[valid2["cost"] > valid2["revenue"]]
    flagged.update(bad_cost.tolist())

    # 7. Duplicates
    dup_idx = df.index[df.duplicated(keep="first")]
    flagged.update(dup_idx.difference(pd.Index(list(flagged))).tolist())

    clean = df.drop(index=list(flagged)).reset_index(drop=True)
    print(f"  Clean rows after removing dirty: {len(clean)} / {len(df)}")
    return clean


def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["date"] = pd.to_datetime(df["date"])
    df["profit"] = df["revenue"] - df["cost"]
    df["profit_margin"] = (df["profit"] / df["revenue"]).round(4)
    return df


def build_summary(df: pd.DataFrame) -> pd.DataFrame:
    summary = (
        df.groupby(["region", "product"], as_index=False)
        .agg(
            total_revenue=("revenue", "sum"),
            total_profit=("profit", "sum"),
            total_units=("units_sold", "sum"),
            avg_profit_margin=("profit_margin", "mean"),
        )
    )
    summary["avg_profit_margin"] = summary["avg_profit_margin"].round(4)
    return summary


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print("Loading and cleaning data...")
    df_clean = load_and_clean(INPUT_FILE)

    print("Engineering features...")
    df_features = engineer_features(df_clean)

    print("Building summary table...")
    df_summary = build_summary(df_features)

    features_path = OUTPUT_DIR / "features.csv"
    summary_path = OUTPUT_DIR / "sales_summary.csv"

    df_features.to_csv(features_path, index=False)
    df_summary.to_csv(summary_path, index=False)

    print(f"\n  features.csv  saved: {df_features.shape[0]} rows × {df_features.shape[1]} cols")
    print(f"  sales_summary.csv saved: {df_summary.shape[0]} rows × {df_summary.shape[1]} cols")
    print(f"\nOutputs written to: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
