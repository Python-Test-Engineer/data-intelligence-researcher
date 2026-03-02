"""Phase 1 — EDA & Preprocessing
Validates data/sales_dummy.csv, removes dirty rows, writes output/PROJECT_01/dirty.csv.
"""
from __future__ import annotations

import warnings
from pathlib import Path

import pandas as pd

RANDOM_SEED = 42
OUTPUT_DIR = Path("output/PROJECT_01")
INPUT_FILE = Path("data/sales_dummy.csv")
REQUIRED_COLUMNS = {"date", "region", "product", "units_sold", "revenue", "cost"}


def load_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise ValueError(f"Input file not found: {path}")
    df = pd.read_csv(path)
    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {missing}")
    return df


def flag_dirty_rows(df: pd.DataFrame) -> pd.DataFrame:
    """Return rows removed as dirty, each with a 'reason' column."""
    dirty_frames: list[pd.DataFrame] = []

    def _collect(idx: pd.Index, reason: str) -> None:
        if idx.empty:
            return
        rows = df.loc[idx].copy()
        rows["reason"] = reason
        dirty_frames.append(rows)

    # Track which indices have already been flagged to avoid double-counting
    flagged: set[int] = set()

    # 1. Missing required fields
    null_mask = df[list(REQUIRED_COLUMNS)].isnull().any(axis=1)
    null_idx = df.index[null_mask]
    _collect(null_idx, "missing_required_field")
    flagged.update(null_idx.tolist())

    # 2. Invalid date (on non-null rows)
    remaining = df.drop(index=list(flagged))
    bad_date_idx = remaining.index[pd.to_datetime(remaining["date"], errors="coerce").isna()]
    _collect(bad_date_idx, "invalid_date")
    flagged.update(bad_date_idx.tolist())

    # Work on clean-so-far rows for numeric checks
    valid = df.drop(index=list(flagged))

    # 3. Non-positive units_sold
    idx = valid.index[valid["units_sold"] <= 0]
    _collect(idx, "non_positive_units")
    flagged.update(idx.tolist())

    # 4. Non-positive revenue
    idx = valid.index[valid["revenue"] <= 0]
    _collect(idx, "non_positive_revenue")
    flagged.update(idx.tolist())

    # 5. Non-positive cost
    idx = valid.index[valid["cost"] <= 0]
    _collect(idx, "non_positive_cost")
    flagged.update(idx.tolist())

    # 6. Cost exceeds revenue (only on numerically valid rows)
    valid2 = df.drop(index=list(flagged))
    idx = valid2.index[valid2["cost"] > valid2["revenue"]]
    _collect(idx, "cost_exceeds_revenue")
    flagged.update(idx.tolist())

    # 7. Exact duplicates (all but first occurrence, across full df)
    dup_idx = df.index[df.duplicated(keep="first")]
    unflagged_dups = dup_idx.difference(pd.Index(list(flagged)))
    _collect(unflagged_dups, "duplicate")

    if not dirty_frames:
        return pd.DataFrame(columns=list(df.columns) + ["reason"])

    return pd.concat(dirty_frames)


def _flag_subset(
    full_df: pd.DataFrame,
    subset: pd.DataFrame,
    mask: pd.Series,
    reason: str,
    collector: list[pd.DataFrame],
) -> None:
    rows = subset[mask].copy()
    rows["reason"] = reason
    collector.append(rows)


def save_dirty(dirty: pd.DataFrame, path: Path) -> None:
    dirty.to_csv(path, index=False)
    if dirty.empty:
        warnings.warn("No dirty rows found — dirty.csv is empty.", stacklevel=2)
    else:
        print(f"  Dirty rows written: {len(dirty)}")


def print_summary(df_raw: pd.DataFrame, df_clean: pd.DataFrame) -> None:
    print("\n" + "=" * 50)
    print("PHASE 1 — EDA SUMMARY")
    print("=" * 50)
    print(f"Total rows loaded   : {len(df_raw)}")
    print(f"Dirty rows removed  : {len(df_raw) - len(df_clean)}")
    print(f"Clean rows remaining: {len(df_clean)}")
    print("\nMissing % per column (clean data):")
    for col in df_clean.columns:
        pct = df_clean[col].isnull().mean() * 100
        print(f"  {col:<15} {pct:.1f}%")
    print("=" * 50)


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print("Loading data...")
    df = load_csv(INPUT_FILE)
    print(f"  Loaded {len(df)} rows, {len(df.columns)} columns")

    print("Flagging dirty rows...")
    dirty = flag_dirty_rows(df)

    dirty_path = OUTPUT_DIR / "dirty.csv"
    save_dirty(dirty, dirty_path)

    dirty_idx = set(dirty.index) if not dirty.empty else set()
    df_clean = df.drop(index=list(dirty_idx)).reset_index(drop=True)

    print_summary(df, df_clean)
    print(f"\nDirty CSV saved to: {dirty_path}")


if __name__ == "__main__":
    main()
