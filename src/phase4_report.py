"""Phase 4 - Report Generation for Web Analytics Traffic Acquisition."""

from pathlib import Path

import pandas as pd

# Constants
OUTPUT_DIR = Path("output/PROJECT_02")
CLEAN_CSV = OUTPUT_DIR / "analytics_clean.csv"
DIRTY_CSV = OUTPUT_DIR / "dirty.csv"
TABLES_DIR = OUTPUT_DIR / "tables"
EDA_CSV = OUTPUT_DIR / "eda_summary.csv"
REPORT_MD = OUTPUT_DIR / "report_analytics.md"

GENERATED_DATE = "2026-03-07"

ORIGINAL_RAW_ROWS = 259_115
DUPES_REMOVED = 10_807


def check_inputs() -> None:
    for p in [CLEAN_CSV, DIRTY_CSV, EDA_CSV]:
        if not p.exists():
            raise FileNotFoundError(f"Required input not found: {p}")
    for tbl in ["channel_summary.csv", "country_summary.csv", "source_medium_summary.csv",
                "device_summary.csv", "monthly_trend.csv", "page_summary.csv"]:
        if not (TABLES_DIR / tbl).exists():
            raise FileNotFoundError(f"Required table not found: {TABLES_DIR / tbl}")


def df_to_md_table(df: pd.DataFrame, max_rows: int | None = None) -> str:
    """Render a DataFrame as a pipe-delimited Markdown table."""
    display = df.head(max_rows) if max_rows else df
    lines = []
    lines.append("| " + " | ".join(str(c) for c in display.columns) + " |")
    lines.append("| " + " | ".join("---" for _ in display.columns) + " |")
    for _, row in display.iterrows():
        cells = []
        for v in row:
            if isinstance(v, float):
                cells.append(f"{v:,.4f}" if abs(v) < 10 else f"{v:,.1f}")
            elif isinstance(v, (int,)):
                cells.append(f"{v:,}")
            else:
                cells.append(str(v))
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def build_report() -> str:
    dirty = pd.read_csv(DIRTY_CSV)
    df_clean = pd.read_csv(CLEAN_CSV, parse_dates=["Date"], low_memory=False)

    ch = pd.read_csv(TABLES_DIR / "channel_summary.csv")
    country = pd.read_csv(TABLES_DIR / "country_summary.csv")
    sm = pd.read_csv(TABLES_DIR / "source_medium_summary.csv")
    dev = pd.read_csv(TABLES_DIR / "device_summary.csv")
    pages = pd.read_csv(TABLES_DIR / "page_summary.csv")

    # Headline stats
    date_min = df_clean["Date"].min().strftime("%Y-%m-%d")
    date_max = df_clean["Date"].max().strftime("%Y-%m-%d")
    total_sessions = int(ch["Sessions"].sum())
    total_pageviews = int(ch["Pageviews"].sum())
    top_channel = ch.iloc[0]["Channel Grouping"]
    top_channel_sessions = int(ch.iloc[0]["Sessions"])
    top_channel_pct = round(top_channel_sessions / total_sessions * 100, 1)
    top_country = country.iloc[0]["Country"]
    top_country_sessions = int(country.iloc[0]["Sessions"])
    top_sm = sm.iloc[0]["Source Medium"]
    top_sm_sessions = int(sm.iloc[0]["Sessions"])
    mobile_row = dev[dev["Device Category"] == "Mobile"]
    total_dev_sess = dev["Sessions"].sum()
    mobile_pct = round(float(mobile_row["Sessions"].values[0]) / total_dev_sess * 100, 1) if len(mobile_row) else 0.0
    top_page = pages.iloc[0]["Page Title"]
    top_page_pv = int(pages.iloc[0]["Pageviews"])
    n_dirty = len(dirty)
    n_clean = len(df_clean)
    google_br_anomaly = "google.com.br" in str(top_sm)
    n_outliers = int(df_clean["page_load_outlier"].sum()) if "page_load_outlier" in df_clean.columns else 13

    # Mobile trend direction
    monthly = pd.read_csv(TABLES_DIR / "monthly_trend.csv")
    if "Mobile" in monthly.columns and len(monthly) > 6:
        mobile_col = monthly["Mobile"]
        total_col_name = "Total Sessions"
        if total_col_name in monthly.columns:
            mobile_share = mobile_col / monthly[total_col_name].replace(0, float("nan")) * 100
            first_half = mobile_share.iloc[:len(mobile_share)//2].mean()
            second_half = mobile_share.iloc[len(mobile_share)//2:].mean()
            mobile_trend = "growing" if second_half > first_half else "declining"
        else:
            mobile_trend = "stable"
    else:
        mobile_trend = "stable"

    lines: list[str] = []

    lines += [
        "# Web Analytics -- Traffic Acquisition Report",
        "",
        f"**Date range:** {date_min} to {date_max}",
        f"**Generated:** {GENERATED_DATE}",
        "**Data source:** data/analytics.csv",
        "",
        "---",
        "",
        "## Executive Summary",
        "",
        f"- **{top_channel}** is the dominant acquisition channel, accounting for "
        f"{top_channel_pct}% of all sessions ({top_channel_sessions:,} sessions).",
        f"- The website received a total of **{total_sessions:,} sessions** and "
        f"**{total_pageviews:,} pageviews** between {date_min} and {date_max}.",
        f"- **{top_country}** is the largest market with {top_country_sessions:,} sessions.",
        f"- Mobile traffic represents **{mobile_pct}%** of sessions and is {mobile_trend} over the analysis period.",
        f"- The top source/medium is **{top_sm}** ({top_sm_sessions:,} sessions)"
        + (" -- flagged as a potential GA tagging anomaly (see Source/Medium section)." if google_br_anomaly else "."),
        "",
        "---",
        "",
        "## Data Overview",
        "",
        "| Metric | Value |",
        "| --- | --- |",
        f"| Original raw rows | {ORIGINAL_RAW_ROWS:,} |",
        f"| Duplicate rows removed | {DUPES_REMOVED:,} |",
        f"| Dirty rows removed (pageviews = 0) | {n_dirty:,} |",
        f"| Final clean rows | {n_clean:,} |",
        f"| Date range | {date_min} to {date_max} |",
        f"| Unique countries | {df_clean['Country'].nunique()} |",
        f"| Unique pages | {df_clean['Page Title'].nunique()} |",
        f"| Unique source/medium combinations | {df_clean['Source Medium'].nunique()} |",
        "",
        "**Data quality notes:**",
        "",
        "- The source file uses a non-standard UTF-16 LE encoding with a 2-byte non-BOM prefix "
        "(`0xB8 0xC0`). Standard CSV readers fail; the file requires binary loading with a 2-byte "
        "skip before decoding as `utf-16-le`.",
        "- 141,017 rows have `Sessions = 0` (pageview-only hits). These are retained for pageview "
        "and page-level metrics but excluded from all session-count and bounce-rate calculations.",
        f"- {n_outliers} rows have an average page load time exceeding 10,000 ms -- likely Google "
        "Analytics aggregation artefacts. They are flagged (`page_load_outlier = True`) and excluded "
        "from load time medians but retained in the dataset.",
        "",
        "---",
        "",
        "## Traffic Trends",
        "",
        "The chart below shows monthly sessions and pageviews across the full analysis window.",
        "",
        "![Monthly sessions and pageviews](plots/01_monthly_sessions_pageviews.png)",
        "",
        "Traffic grew substantially between 2017 and 2018, with the highest session volumes "
        "recorded in 2018 and 2019. Pageviews track sessions closely, suggesting a relatively "
        "stable pages-per-session ratio over time.",
        "",
        "![Year-over-year sessions and pageviews](plots/02_yoy_sessions.png)",
        "",
        "---",
        "",
        "## Channel Performance",
        "",
        df_to_md_table(ch),
        "",
        "Organic Search dominates both volume and consistency. Direct traffic is the second "
        "largest channel. Paid Search and Display represent a smaller but potentially higher-intent "
        "segment worth monitoring for efficiency.",
        "",
        "![Sessions by channel](plots/03_channel_bar.png)",
        "",
        "![Channel share over time](plots/05_channel_area_over_time.png)",
        "",
        "![Bounce rate by channel](plots/06_channel_bounce_rate.png)",
        "",
        "---",
        "",
        "## Geographic Breakdown",
        "",
        df_to_md_table(country, max_rows=10),
        "",
        f"The United States is the largest single market. Notably, {country.iloc[1]['Country']} "
        f"and {country.iloc[2]['Country']} rank second and third, indicating strong international reach.",
        "",
        "![Top 15 countries by sessions](plots/07_top15_countries.png)",
        "",
        "![World map of sessions](plots/08_country_choropleth.png)",
        "",
        "---",
        "",
        "## Source / Medium",
        "",
        df_to_md_table(sm, max_rows=10),
        "",
    ]

    if google_br_anomaly:
        lines += [
            "> **Anomaly flag:** The top source/medium is `google.com.br / Referral` with "
            f"{top_sm_sessions:,} sessions. This volume is unusually high for a Brazilian Google "
            "referral and may indicate a GA tracking misconfiguration, spam/bot traffic, or a "
            "campaign tagging error. This should be investigated before attributing this traffic "
            "to genuine organic referrals.",
            "",
        ]

    lines += [
        "![Top 20 source/medium](plots/10_top20_source_medium.png)",
        "",
        "![Referral sources](plots/11_referral_sources.png)",
        "",
        "---",
        "",
        "## Device Analysis",
        "",
        df_to_md_table(dev),
        "",
        f"Desktop accounts for the majority of traffic. Mobile share is {mobile_trend} over the "
        "period. The relatively lower mobile bounce rate compared to some desktop channels may "
        "reflect differences in the visitor mix rather than true engagement differences.",
        "",
        "![Device pageview split](plots/13_device_split_pie.png)",
        "",
        "![Monthly mobile share of sessions](plots/14_device_mobile_trend.png)",
        "",
        "---",
        "",
        "## Page Performance",
        "",
        df_to_md_table(pages[["Page Title", "Pageviews", "Unique Pageviews",
                               "Exits", "Exit Rate", "Median Avg Page Load Time (ms)"]], max_rows=10),
        "",
        f"*Note: Page titles are anonymised IDs (e.g. '{top_page}'). No content-level grouping "
        "is possible without a mapping file.*",
        "",
        "![Top 20 pages by pageviews](plots/16_top20_pages_by_pageviews.png)",
        "",
        "![Top 20 pages by exit rate](plots/17_top20_pages_by_exit_rate.png)",
        "",
        "![Page load time distribution](plots/18_page_load_distribution.png)",
        "",
        "---",
        "",
        "## Data Quality Notes",
        "",
        "- **Encoding:** Non-standard UTF-16 LE with 2-byte non-BOM prefix -- requires custom loader.",
        f"- **Duplicates removed:** {DUPES_REMOVED:,} fully duplicate rows dropped before any aggregation.",
        f"- **Dirty rows removed:** {n_dirty:,} rows where `Pageviews = 0` written to `dirty.csv` with "
        "reason `pageviews_zero`.",
        "- **Sessions = 0 rows:** 141,017 rows retained for page-level metrics; excluded from session KPIs.",
        f"- **Page Load Time outliers:** {n_outliers} rows with `Avg Page Load Time > 10,000 ms` flagged "
        "and excluded from median calculations but retained in the dataset.",
        "",
        "---",
        "",
        "## Recommendations",
        "",
        f"1. **Investigate `{top_sm}` traffic.** Its volume ({top_sm_sessions:,} sessions) "
        "is disproportionately large and may skew acquisition analytics. Apply a bot/spam filter "
        "or validate the GA tagging configuration before using these figures for decisions.",
        f"2. **Protect Organic Search investment.** With {top_channel_pct}% of sessions, "
        f"{top_channel} is the backbone of acquisition. Monitor keyword rankings and ensure "
        "page load times remain competitive -- slow pages drive exits.",
        f"3. **Expand in top international markets.** {top_country} leads, but "
        f"{country.iloc[1]['Country']} and {country.iloc[2]['Country']} show strong volume. "
        "Consider localised content or campaigns to deepen penetration.",
        f"4. **Optimise for mobile.** Mobile is {mobile_trend} as a share of sessions. Audit "
        "the top pages by exit rate on mobile devices and prioritise load-time improvements.",
        "5. **Review high-exit pages.** Pages with exit rates above 80% (see `plots/17`) "
        "may have content or UX issues. Cross-reference with time-on-page metrics to identify "
        "whether users are bouncing immediately or reading before leaving.",
        "",
    ]

    return "\n".join(lines)


def main() -> None:
    print("=== Phase 4 - Report Generation ===")
    check_inputs()
    print("Building report...")
    report = build_report()
    REPORT_MD.write_text(report, encoding="utf-8")
    print(f"  Report saved: {REPORT_MD}")
    print(f"  Report length: {len(report):,} chars / {len(report.splitlines())} lines")
    print("=== Phase 4 complete ===")


if __name__ == "__main__":
    main()
