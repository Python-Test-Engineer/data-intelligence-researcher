"""Phase 3 - Aggregated Summary Tables for Web Analytics Traffic Acquisition."""

from pathlib import Path

import pandas as pd

# Constants
OUTPUT_DIR = Path("output/PROJECT_02")
CLEAN_CSV = OUTPUT_DIR / "analytics_clean.csv"
TABLES_DIR = OUTPUT_DIR / "tables"


def load_data() -> pd.DataFrame:
    if not CLEAN_CSV.exists():
        raise FileNotFoundError(f"Clean CSV not found: {CLEAN_CSV}")
    return pd.read_csv(CLEAN_CSV, parse_dates=["Date"], low_memory=False)


def make_channel_summary(df_all: pd.DataFrame, df_sess: pd.DataFrame) -> pd.DataFrame:
    pv = df_all.groupby("Channel Grouping").agg(
        Pageviews=("Pageviews", "sum"),
        Bounces=("Bounces", "sum"),
        Avg_Time_on_Page=("Avg Time on Page (s)", "mean"),
    )
    sess = df_sess.groupby("Channel Grouping").agg(
        Sessions=("Sessions", "sum"),
    )
    result = sess.join(pv, how="outer").fillna(0)
    result["Bounce Rate"] = result["Bounces"] / result["Sessions"].replace(0, float("nan"))
    result = result.rename(columns={"Avg_Time_on_Page": "Avg Time on Page (s)"})
    result = result[["Sessions", "Pageviews", "Bounces", "Bounce Rate", "Avg Time on Page (s)"]]
    result["Bounce Rate"] = result["Bounce Rate"].round(4)
    result["Avg Time on Page (s)"] = result["Avg Time on Page (s)"].round(1)
    return result.sort_values("Sessions", ascending=False).reset_index()


def make_country_summary(df_all: pd.DataFrame, df_sess: pd.DataFrame) -> pd.DataFrame:
    pv = df_all.groupby("Country")["Pageviews"].sum()
    sess = df_sess.groupby("Country")["Sessions"].sum()
    top30_countries = sess.nlargest(30).index.tolist()

    device_counts = df_all.groupby(["Country", "Device Category"]).size().unstack(fill_value=0)
    device_totals = device_counts.sum(axis=1)
    device_pct = device_counts.div(device_totals, axis=0) * 100
    device_pct = device_pct.rename(columns={
        "Desktop": "Desktop %", "Mobile": "Mobile %", "Tablet": "Tablet %"
    })

    result = pd.DataFrame({"Sessions": sess, "Pageviews": pv}).loc[top30_countries]
    for col in ["Desktop %", "Mobile %", "Tablet %"]:
        result[col] = device_pct.get(col.replace(" %", ""), pd.Series(dtype=float)).reindex(top30_countries).round(1)

    return result.sort_values("Sessions", ascending=False).reset_index()


def make_source_medium_summary(df_sess: pd.DataFrame) -> pd.DataFrame:
    agg = df_sess.groupby("Source Medium").agg(
        Sessions=("Sessions", "sum"),
        Pageviews=("Pageviews", "sum"),
        Bounces=("Bounces", "sum"),
    )
    top30 = agg.nlargest(30, "Sessions").copy()
    top30["Bounce Rate"] = (top30["Bounces"] / top30["Sessions"].replace(0, float("nan"))).round(4)
    return top30.sort_values("Sessions", ascending=False).reset_index()


def make_device_summary(df_all: pd.DataFrame, df_sess: pd.DataFrame) -> pd.DataFrame:
    pv = df_all.groupby("Device Category")["Pageviews"].sum()
    sess = df_sess.groupby("Device Category")["Sessions"].sum()
    br = df_sess.groupby("Device Category")["Bounce Rate"].mean().round(4)

    no_outlier = df_all[~df_all["page_load_outlier"] & df_all["Avg Page Load Time (ms)"].notna()]
    median_lt = no_outlier.groupby("Device Category")["Avg Page Load Time (ms)"].median().round(1)

    result = pd.DataFrame({
        "Sessions": sess,
        "Pageviews": pv,
        "Bounce Rate": br,
        "Median Avg Page Load Time (ms)": median_lt,
    })
    return result.sort_values("Sessions", ascending=False).reset_index()


def make_monthly_trend(df_all: pd.DataFrame, df_sess: pd.DataFrame) -> pd.DataFrame:
    total_pv = df_all.groupby("YearMonth")["Pageviews"].sum().rename("Total Pageviews")
    total_sess = df_sess.groupby("YearMonth")["Sessions"].sum().rename("Total Sessions")

    channel_pivot = df_sess.groupby(["YearMonth", "Channel Grouping"])["Sessions"].sum().unstack(fill_value=0)

    result = pd.concat([total_sess, total_pv], axis=1).join(channel_pivot, how="left").fillna(0)
    return result.sort_index().reset_index()


def make_page_summary(df_all: pd.DataFrame) -> pd.DataFrame:
    agg = df_all.groupby("Page Title").agg(
        Pageviews=("Pageviews", "sum"),
        Unique_Pageviews=("Unique Pageviews", "sum"),
        Exits=("Exits", "sum"),
    )
    top50 = agg.nlargest(50, "Pageviews").copy()
    top50["Exit Rate"] = (top50["Exits"] / top50["Pageviews"].replace(0, float("nan"))).round(4)
    top50 = top50.rename(columns={"Unique_Pageviews": "Unique Pageviews"})

    no_outlier = df_all[~df_all["page_load_outlier"] & df_all["Avg Page Load Time (ms)"].notna()]
    median_lt = no_outlier.groupby("Page Title")["Avg Page Load Time (ms)"].median().round(1)
    top50["Median Avg Page Load Time (ms)"] = median_lt.reindex(top50.index)

    return top50.sort_values("Pageviews", ascending=False).reset_index()


def main() -> None:
    TABLES_DIR.mkdir(parents=True, exist_ok=True)
    print("=== Phase 3 - Aggregated Tables ===")

    print("Loading clean data...")
    df_all = load_data()
    df_sess = df_all[df_all["Sessions"] > 0].copy()
    print(f"  df_all: {len(df_all):,} | df_sess: {len(df_sess):,}")

    tables = {
        "channel_summary.csv": make_channel_summary(df_all, df_sess),
        "country_summary.csv": make_country_summary(df_all, df_sess),
        "source_medium_summary.csv": make_source_medium_summary(df_sess),
        "device_summary.csv": make_device_summary(df_all, df_sess),
        "monthly_trend.csv": make_monthly_trend(df_all, df_sess),
        "page_summary.csv": make_page_summary(df_all),
    }

    for fname, tbl in tables.items():
        path = TABLES_DIR / fname
        tbl.to_csv(path, index=False, encoding="utf-8")
        print(f"  {fname}: {tbl.shape[0]} rows x {tbl.shape[1]} cols")

    print("=== Phase 3 complete ===")


if __name__ == "__main__":
    main()
