"""Phase 1 — ETL & Preprocessing for Web Analytics Traffic Acquisition."""

import io
from pathlib import Path

import pandas as pd

# Constants
DATA_PATH = Path("data/analytics.csv")
OUTPUT_DIR = Path("output/PROJECT_02")
CLEAN_CSV = OUTPUT_DIR / "analytics_clean.csv"
DIRTY_CSV = OUTPUT_DIR / "dirty.csv"

EXPECTED_COLUMNS = [
    "Channel Grouping", "Country", "Date", "Device Category", "Page Title",
    "Source Medium", "Bounces", "Exits", "Page Load Time", "Pageviews",
    "Sessions", "Time on Page", "Unique Pageviews", "Total duration",
]
MIN_ROWS = 200_000
MAX_ROWS = 300_000


def load_raw(path: Path) -> pd.DataFrame:
    """Load UTF-16 LE TSV with non-standard 2-byte BOM prefix."""
    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {path}")
    with path.open("rb") as f:
        raw = f.read()
    # Skip 2-byte non-standard BOM (0xB8 0xC0), decode as utf-16-le
    text = raw[2:].decode("utf-16-le")
    df = pd.read_csv(io.StringIO(text), sep="\t")
    # Fix BOM-truncated first column name
    cols = list(df.columns)
    cols[0] = "Channel Grouping"
    df.columns = cols
    return df


def validate(df: pd.DataFrame) -> None:
    """Assert expected columns and row count range."""
    missing_cols = set(EXPECTED_COLUMNS) - set(df.columns)
    if missing_cols:
        raise ValueError(f"Missing expected columns: {missing_cols}")
    if not (MIN_ROWS <= len(df) <= MAX_ROWS):
        raise ValueError(f"Row count {len(df)} outside expected range [{MIN_ROWS}, {MAX_ROWS}]")


def deduplicate(df: pd.DataFrame) -> pd.DataFrame:
    """Drop fully duplicate rows and log count."""
    before = len(df)
    df = df.drop_duplicates()
    removed = before - len(df)
    print(f"  Deduplication: removed {removed:,} duplicate rows ({before:,} -> {len(df):,})")
    return df


def extract_dirty(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Split dirty rows (Pageviews == 0) from clean rows."""
    mask_dirty = df["Pageviews"] == 0
    dirty = df[mask_dirty].copy()
    dirty["reason"] = "pageviews_zero"
    clean = df[~mask_dirty].copy()
    print(f"  Dirty rows (Pageviews == 0): {len(dirty):,} rows -> dirty.csv")
    return clean, dirty


def fill_nulls(df: pd.DataFrame) -> pd.DataFrame:
    """Fill nullable categorical nulls with 'Unknown'."""
    df["Country"] = df["Country"].fillna("Unknown")
    df["Page Title"] = df["Page Title"].fillna("Unknown")
    return df


def parse_dates(df: pd.DataFrame) -> pd.DataFrame:
    """Parse Date column from M/D/YYYY string to datetime."""
    df["Date"] = pd.to_datetime(df["Date"], format="%m/%d/%Y")
    return df


def derive_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Add derived metric and time columns."""
    # Guarded divisions -> NaN when denominator is 0
    df["Avg Page Load Time (ms)"] = df["Page Load Time"].where(
        df["Pageviews"] > 0
    ) / df["Pageviews"].replace(0, float("nan"))

    df["Bounce Rate"] = df["Bounces"].where(
        df["Sessions"] > 0
    ) / df["Sessions"].replace(0, float("nan"))

    df["Exit Rate"] = df["Exits"].where(
        df["Pageviews"] > 0
    ) / df["Pageviews"].replace(0, float("nan"))

    denom = (df["Pageviews"] - df["Exits"]).replace(0, float("nan"))
    df["Avg Time on Page (s)"] = df["Time on Page"].where(denom.notna()) / denom

    df["page_load_outlier"] = df["Avg Page Load Time (ms)"] > 10_000

    df["Year"] = df["Date"].dt.year
    df["Month"] = df["Date"].dt.month
    df["YearMonth"] = df["Date"].dt.to_period("M").astype(str)

    return df


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print("=== Phase 1 — ETL & Preprocessing ===")

    print("Loading raw file...")
    df = load_raw(DATA_PATH)
    print(f"  Raw shape: {df.shape}")

    print("Validating schema and row count...")
    validate(df)
    print("  Validation passed.")

    print("Deduplicating...")
    df = deduplicate(df)

    print("Extracting dirty rows...")
    df, dirty = extract_dirty(df)

    print("Filling nulls...")
    df = fill_nulls(df)

    print("Parsing dates...")
    df = parse_dates(df)

    print("Deriving columns...")
    df = derive_columns(df)

    print(f"  Final clean shape: {df.shape}")

    print("Saving outputs...")
    dirty.to_csv(DIRTY_CSV, index=False, encoding="utf-8")
    df.to_csv(CLEAN_CSV, index=False, encoding="utf-8")
    print(f"  dirty.csv  -> {DIRTY_CSV} ({len(dirty):,} rows)")
    print(f"  clean.csv  -> {CLEAN_CSV} ({len(df):,} rows)")

    print("=== Phase 1 complete ===")


if __name__ == "__main__":
    main()
