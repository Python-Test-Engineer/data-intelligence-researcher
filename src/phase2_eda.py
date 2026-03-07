"""Phase 2 - EDA & Visualisation for Web Analytics Traffic Acquisition."""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd
import seaborn as sns

# Constants
OUTPUT_DIR = Path("output/PROJECT_02")
CLEAN_CSV = OUTPUT_DIR / "analytics_clean.csv"
PLOTS_DIR = OUTPUT_DIR / "plots"
EDA_CSV = OUTPUT_DIR / "eda_summary.csv"

DPI = 150
FIG_SIZE_BAR = (12, 6)
FIG_SIZE_PIE = (8, 8)
PALETTE = sns.color_palette("tab10")
SEQ_PALETTE = "Blues_r"


def load_data() -> pd.DataFrame:
    if not CLEAN_CSV.exists():
        raise FileNotFoundError(f"Clean CSV not found: {CLEAN_CSV}")
    df = pd.read_csv(CLEAN_CSV, parse_dates=["Date"], low_memory=False)
    return df


def save_fig(fig: plt.Figure, name: str) -> None:
    path = PLOTS_DIR / name
    fig.savefig(path, dpi=DPI, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {name}")


def style_axes(ax: plt.Axes, title: str, xlabel: str = "", ylabel: str = "") -> None:
    ax.set_title(title, fontsize=13, pad=10)
    ax.set_xlabel(xlabel, fontsize=11)
    ax.set_ylabel(ylabel, fontsize=11)
    ax.yaxis.grid(True, linestyle="--", alpha=0.6)
    ax.xaxis.grid(False)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


def chart_01_monthly_trend(df: pd.DataFrame, df_sess: pd.DataFrame) -> dict:
    monthly_pv = df.groupby("YearMonth")["Pageviews"].sum().reset_index()
    monthly_sess = df_sess.groupby("YearMonth")["Sessions"].sum().reset_index()
    merged = monthly_pv.merge(monthly_sess, on="YearMonth", how="left").fillna(0)
    merged = merged.sort_values("YearMonth")

    fig, ax = plt.subplots(figsize=FIG_SIZE_BAR)
    ax.plot(range(len(merged)), merged["Pageviews"], label="Pageviews", color=PALETTE[0], linewidth=2)
    ax.plot(range(len(merged)), merged["Sessions"], label="Sessions", color=PALETTE[1], linewidth=2)
    step = max(1, len(merged) // 12)
    ax.set_xticks(range(0, len(merged), step))
    ax.set_xticklabels(merged["YearMonth"].iloc[::step], rotation=45, ha="right", fontsize=8)
    ax.legend()
    style_axes(ax, "Monthly sessions and pageviews (2017-2019)", "Month", "Count")
    save_fig(fig, "01_monthly_sessions_pageviews.png")
    top = merged.loc[merged["Sessions"].idxmax(), "YearMonth"]
    return {"chart_file": "01_monthly_sessions_pageviews.png", "metric": "Sessions",
            "top_value": int(merged["Sessions"].max()), "top_label": top, "note": "Peak session month"}


def chart_02_yoy(df: pd.DataFrame, df_sess: pd.DataFrame) -> dict:
    yoy_pv = df.groupby("Year")["Pageviews"].sum()
    yoy_sess = df_sess.groupby("Year")["Sessions"].sum()
    years = sorted(set(yoy_pv.index) | set(yoy_sess.index))
    x = np.arange(len(years))
    width = 0.35

    fig, ax = plt.subplots(figsize=FIG_SIZE_BAR)
    ax.bar(x - width/2, [yoy_pv.get(y, 0) for y in years], width, label="Pageviews", color=PALETTE[0])
    ax.bar(x + width/2, [yoy_sess.get(y, 0) for y in years], width, label="Sessions", color=PALETTE[1])
    ax.set_xticks(x)
    ax.set_xticklabels(years)
    ax.legend()
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"{v:,.0f}"))
    style_axes(ax, "Year-over-year sessions and pageviews", "Year", "Count")
    save_fig(fig, "02_yoy_sessions.png")
    top_year = max(years, key=lambda y: yoy_sess.get(y, 0))
    return {"chart_file": "02_yoy_sessions.png", "metric": "Sessions",
            "top_value": int(yoy_sess.get(top_year, 0)), "top_label": str(top_year), "note": "Best year by sessions"}


def chart_03_channel_bar(df_sess: pd.DataFrame) -> dict:
    ch = df_sess.groupby("Channel Grouping")["Sessions"].sum().sort_values(ascending=True)
    fig, ax = plt.subplots(figsize=FIG_SIZE_BAR)
    colors = sns.color_palette(SEQ_PALETTE, len(ch))
    ch.plot(kind="barh", ax=ax, color=colors)
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"{v:,.0f}"))
    style_axes(ax, "Total sessions by channel grouping", "Sessions", "Channel")
    save_fig(fig, "03_channel_bar.png")
    return {"chart_file": "03_channel_bar.png", "metric": "Sessions",
            "top_value": int(ch.iloc[-1]), "top_label": ch.index[-1], "note": "Top channel by sessions"}


def chart_04_channel_pie(df_sess: pd.DataFrame) -> dict:
    ch = df_sess.groupby("Channel Grouping")["Sessions"].sum().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=FIG_SIZE_PIE)
    ax.pie(ch.values, labels=ch.index, autopct="%1.1f%%", colors=PALETTE[:len(ch)], startangle=90)
    ax.set_title("Session share by channel grouping", fontsize=13)
    save_fig(fig, "04_channel_pie.png")
    return {"chart_file": "04_channel_pie.png", "metric": "Session share %",
            "top_value": round(ch.iloc[0] / ch.sum() * 100, 1), "top_label": ch.index[0],
            "note": "Dominant channel share"}


def chart_05_channel_area(df_sess: pd.DataFrame) -> dict:
    pivot = df_sess.groupby(["YearMonth", "Channel Grouping"])["Sessions"].sum().unstack(fill_value=0)
    pivot = pivot.sort_index()
    pivot_pct = pivot.div(pivot.sum(axis=1), axis=0) * 100

    fig, ax = plt.subplots(figsize=FIG_SIZE_BAR)
    pivot_pct.plot(kind="area", ax=ax, stacked=True, color=PALETTE[:len(pivot_pct.columns)], alpha=0.85)
    step = max(1, len(pivot_pct) // 12)
    ax.set_xticks(range(0, len(pivot_pct), step))
    ax.set_xticklabels(pivot_pct.index[::step], rotation=45, ha="right", fontsize=8)
    ax.legend(loc="upper left", fontsize=8, bbox_to_anchor=(1, 1))
    ax.set_ylim(0, 100)
    style_axes(ax, "Monthly session share by channel grouping (%)", "Month", "Share (%)")
    save_fig(fig, "05_channel_area_over_time.png")
    return {"chart_file": "05_channel_area_over_time.png", "metric": "Session share %",
            "top_value": round(pivot_pct[pivot_pct.columns[0]].mean(), 1),
            "top_label": pivot_pct.columns[0], "note": "Avg monthly share of top channel"}


def chart_06_bounce_rate(df_sess: pd.DataFrame) -> dict:
    br = df_sess.groupby("Channel Grouping")["Bounce Rate"].mean().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=FIG_SIZE_BAR)
    br.plot(kind="bar", ax=ax, color=PALETTE[:len(br)])
    ax.set_xticklabels(ax.get_xticklabels(), rotation=30, ha="right")
    ax.yaxis.set_major_formatter(mticker.PercentFormatter(xmax=1))
    style_axes(ax, "Mean bounce rate by channel grouping", "Channel", "Bounce rate")
    save_fig(fig, "06_channel_bounce_rate.png")
    return {"chart_file": "06_channel_bounce_rate.png", "metric": "Bounce Rate",
            "top_value": round(float(br.iloc[0]), 3), "top_label": br.index[0],
            "note": "Highest bounce rate channel"}


def chart_07_top_countries(df_sess: pd.DataFrame) -> dict:
    top = df_sess.groupby("Country")["Sessions"].sum().nlargest(15).sort_values(ascending=True)
    fig, ax = plt.subplots(figsize=FIG_SIZE_BAR)
    top.plot(kind="barh", ax=ax, color=sns.color_palette(SEQ_PALETTE, 15))
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"{v:,.0f}"))
    style_axes(ax, "Top 15 countries by sessions", "Sessions", "Country")
    save_fig(fig, "07_top15_countries.png")
    return {"chart_file": "07_top15_countries.png", "metric": "Sessions",
            "top_value": int(top.iloc[-1]), "top_label": top.index[-1], "note": "Top country by sessions"}


def chart_08_choropleth(df_sess: pd.DataFrame) -> dict:
    try:
        import plotly.express as px
        country_sess = df_sess.groupby("Country")["Sessions"].sum().reset_index()
        fig = px.choropleth(
            country_sess,
            locations="Country",
            locationmode="country names",
            color="Sessions",
            color_continuous_scale="Blues",
            projection="natural earth",
            title="Sessions by country (world map)",
        )
        fig.update_layout(margin={"r": 0, "t": 40, "l": 0, "b": 0})
        out_png = PLOTS_DIR / "08_country_choropleth.png"
        fig.write_image(str(out_png), width=1200, height=600)
        print("  Saved: 08_country_choropleth.png")
        top_country = country_sess.loc[country_sess["Sessions"].idxmax(), "Country"]
        return {"chart_file": "08_country_choropleth.png", "metric": "Sessions",
                "top_value": int(country_sess["Sessions"].max()), "top_label": top_country,
                "note": "Choropleth world map"}
    except Exception as exc:
        print(f"  WARNING: choropleth PNG export failed ({exc}), saving as HTML fallback.")
        import plotly.express as px
        country_sess = df_sess.groupby("Country")["Sessions"].sum().reset_index()
        fig = px.choropleth(country_sess, locations="Country", locationmode="country names",
                            color="Sessions", color_continuous_scale="Blues",
                            projection="natural earth", title="Sessions by country")
        fig.write_html(str(PLOTS_DIR / "08_country_choropleth.html"))
        return {"chart_file": "08_country_choropleth.html", "metric": "Sessions",
                "top_value": int(country_sess["Sessions"].max()),
                "top_label": country_sess.loc[country_sess["Sessions"].idxmax(), "Country"],
                "note": "Choropleth saved as HTML (kaleido unavailable)"}


def chart_09_top5_country_channel(df_sess: pd.DataFrame) -> dict:
    top5 = df_sess.groupby("Country")["Sessions"].sum().nlargest(5).index.tolist()
    sub = df_sess[df_sess["Country"].isin(top5)]
    pivot = sub.groupby(["Country", "Channel Grouping"])["Sessions"].sum().unstack(fill_value=0)
    pivot = pivot.loc[top5]

    fig, ax = plt.subplots(figsize=FIG_SIZE_BAR)
    pivot.plot(kind="bar", ax=ax, color=PALETTE[:len(pivot.columns)])
    ax.set_xticklabels(ax.get_xticklabels(), rotation=30, ha="right")
    ax.legend(loc="upper right", fontsize=8, bbox_to_anchor=(1.15, 1))
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"{v:,.0f}"))
    style_axes(ax, "Sessions by channel for top 5 countries", "Country", "Sessions")
    save_fig(fig, "09_top5_country_channel.png")
    return {"chart_file": "09_top5_country_channel.png", "metric": "Sessions",
            "top_value": int(pivot.values.max()), "top_label": top5[0],
            "note": "Top country x channel breakdown"}


def chart_10_source_medium(df_sess: pd.DataFrame) -> dict:
    top = df_sess.groupby("Source Medium")["Sessions"].sum().nlargest(20).sort_values(ascending=True)
    fig, ax = plt.subplots(figsize=(12, 8))
    top.plot(kind="barh", ax=ax, color=sns.color_palette(SEQ_PALETTE, 20))
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"{v:,.0f}"))
    style_axes(ax, "Top 20 source/medium combinations by sessions", "Sessions", "Source Medium")
    save_fig(fig, "10_top20_source_medium.png")
    return {"chart_file": "10_top20_source_medium.png", "metric": "Sessions",
            "top_value": int(top.iloc[-1]), "top_label": top.index[-1],
            "note": "Top source/medium by sessions"}


def chart_11_referral_sources(df_sess: pd.DataFrame) -> dict:
    referral = df_sess[df_sess["Channel Grouping"] == "Referral"]
    top = referral.groupby("Source Medium")["Sessions"].sum().nlargest(15).sort_values(ascending=True)
    fig, ax = plt.subplots(figsize=(12, 7))
    top.plot(kind="barh", ax=ax, color=sns.color_palette(SEQ_PALETTE, 15))
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"{v:,.0f}"))
    style_axes(ax, "Top 15 referral source/medium by sessions", "Sessions", "Source Medium")
    save_fig(fig, "11_referral_sources.png")
    return {"chart_file": "11_referral_sources.png", "metric": "Sessions",
            "top_value": int(top.iloc[-1]), "top_label": top.index[-1],
            "note": "Top referral source"}


def chart_12_paid_search(df_sess: pd.DataFrame) -> dict:
    paid = df_sess[df_sess["Channel Grouping"] == "Paid Search"]
    agg = paid.groupby("Source Medium").agg(
        Sessions=("Sessions", "sum"),
        Bounce_Rate=("Bounce Rate", "mean"),
    ).nlargest(15, "Sessions").sort_values("Sessions", ascending=False)

    fig, ax1 = plt.subplots(figsize=FIG_SIZE_BAR)
    x = np.arange(len(agg))
    ax1.bar(x - 0.2, agg["Sessions"], width=0.4, color=PALETTE[0], label="Sessions")
    ax1.set_ylabel("Sessions")
    ax2 = ax1.twinx()
    ax2.bar(x + 0.2, agg["Bounce_Rate"], width=0.4, color=PALETTE[1], label="Bounce Rate", alpha=0.7)
    ax2.set_ylabel("Bounce Rate")
    ax2.yaxis.set_major_formatter(mticker.PercentFormatter(xmax=1))
    ax1.set_xticks(x)
    ax1.set_xticklabels(agg.index, rotation=40, ha="right", fontsize=7)
    ax1.yaxis.grid(True, linestyle="--", alpha=0.6)
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper right")
    ax1.set_title("Paid search sources: sessions and bounce rate", fontsize=13)
    ax1.spines["top"].set_visible(False)
    save_fig(fig, "12_paid_search_sources.png")
    return {"chart_file": "12_paid_search_sources.png", "metric": "Sessions",
            "top_value": int(agg["Sessions"].iloc[0]), "top_label": agg.index[0],
            "note": "Top paid search source"}


def chart_13_device_pie(df: pd.DataFrame) -> dict:
    dev = df.groupby("Device Category")["Pageviews"].sum().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=FIG_SIZE_PIE)
    ax.pie(dev.values, labels=dev.index, autopct="%1.1f%%", colors=PALETTE[:3], startangle=90)
    ax.set_title("Pageview share by device category", fontsize=13)
    save_fig(fig, "13_device_split_pie.png")
    return {"chart_file": "13_device_split_pie.png", "metric": "Pageview share %",
            "top_value": round(dev.iloc[0] / dev.sum() * 100, 1), "top_label": dev.index[0],
            "note": "Dominant device by pageviews"}


def chart_14_mobile_trend(df_sess: pd.DataFrame) -> dict:
    total = df_sess.groupby("YearMonth")["Sessions"].sum()
    mobile = df_sess[df_sess["Device Category"] == "Mobile"].groupby("YearMonth")["Sessions"].sum()
    share = (mobile / total * 100).fillna(0).sort_index()

    fig, ax = plt.subplots(figsize=FIG_SIZE_BAR)
    x = range(len(share))
    ax.plot(x, share.values, color=PALETTE[2], linewidth=2)
    ax.fill_between(x, share.values, alpha=0.2, color=PALETTE[2])
    step = max(1, len(share) // 12)
    ax.set_xticks(range(0, len(share), step))
    ax.set_xticklabels(share.index[::step], rotation=45, ha="right", fontsize=8)
    ax.yaxis.set_major_formatter(mticker.PercentFormatter())
    style_axes(ax, "Monthly mobile share of sessions (%)", "Month", "Mobile share (%)")
    save_fig(fig, "14_device_mobile_trend.png")
    return {"chart_file": "14_device_mobile_trend.png", "metric": "Mobile share %",
            "top_value": round(float(share.max()), 1), "top_label": share.idxmax(),
            "note": "Peak mobile share month"}


def chart_15_device_metrics(df_sess: pd.DataFrame) -> dict:
    br = df_sess.groupby("Device Category")["Bounce Rate"].mean()
    lt = df_sess[~df_sess["page_load_outlier"]].groupby("Device Category")["Avg Page Load Time (ms)"].median()
    devices = br.index.tolist()
    x = np.arange(len(devices))
    width = 0.35

    fig, ax1 = plt.subplots(figsize=FIG_SIZE_BAR)
    ax1.bar(x - width/2, br.values, width, color=PALETTE[0], label="Bounce Rate")
    ax1.set_ylabel("Bounce Rate")
    ax1.yaxis.set_major_formatter(mticker.PercentFormatter(xmax=1))
    ax2 = ax1.twinx()
    ax2.bar(x + width/2, lt.reindex(devices).fillna(0).values, width, color=PALETTE[1],
            label="Median Load Time (ms)", alpha=0.8)
    ax2.set_ylabel("Median Page Load Time (ms)")
    ax1.set_xticks(x)
    ax1.set_xticklabels(devices)
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper right")
    ax1.set_title("Bounce rate and median page load time by device", fontsize=13)
    ax1.yaxis.grid(True, linestyle="--", alpha=0.6)
    ax1.spines["top"].set_visible(False)
    save_fig(fig, "15_device_bounce_loadtime.png")
    return {"chart_file": "15_device_bounce_loadtime.png", "metric": "Bounce Rate",
            "top_value": round(float(br.max()), 3), "top_label": br.idxmax(),
            "note": "Highest bounce rate device"}


def chart_16_top_pages(df: pd.DataFrame) -> dict:
    top = df.groupby("Page Title")["Pageviews"].sum().nlargest(20).sort_values(ascending=True)
    fig, ax = plt.subplots(figsize=(12, 8))
    top.plot(kind="barh", ax=ax, color=sns.color_palette(SEQ_PALETTE, 20))
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"{v:,.0f}"))
    style_axes(ax, "Top 20 pages by total pageviews", "Pageviews", "Page Title")
    save_fig(fig, "16_top20_pages_by_pageviews.png")
    return {"chart_file": "16_top20_pages_by_pageviews.png", "metric": "Pageviews",
            "top_value": int(top.iloc[-1]), "top_label": top.index[-1],
            "note": "Most viewed page"}


def chart_17_exit_rate(df: pd.DataFrame) -> dict:
    # Min 100 pageviews to qualify
    page_agg = df.groupby("Page Title").agg(Pageviews=("Pageviews", "sum"), Exits=("Exits", "sum"))
    qualified = page_agg[page_agg["Pageviews"] >= 100].copy()
    qualified["Exit Rate"] = qualified["Exits"] / qualified["Pageviews"]
    top = qualified.nlargest(20, "Exit Rate")["Exit Rate"].sort_values(ascending=True)

    fig, ax = plt.subplots(figsize=(12, 8))
    top.plot(kind="barh", ax=ax, color=sns.color_palette("Reds_r", 20))
    ax.xaxis.set_major_formatter(mticker.PercentFormatter(xmax=1))
    style_axes(ax, "Top 20 pages by exit rate (min 100 pageviews)", "Exit Rate", "Page Title")
    save_fig(fig, "17_top20_pages_by_exit_rate.png")
    return {"chart_file": "17_top20_pages_by_exit_rate.png", "metric": "Exit Rate",
            "top_value": round(float(top.iloc[-1]), 3), "top_label": top.index[-1],
            "note": "Highest exit rate page"}


def chart_18_load_time_dist(df: pd.DataFrame) -> dict:
    valid = df[df["Avg Page Load Time (ms)"].notna() & ~df["page_load_outlier"]]["Avg Page Load Time (ms)"]
    n_outliers = df["page_load_outlier"].sum()
    cap = valid.quantile(0.99)
    valid_capped = valid[valid <= cap]

    fig, ax = plt.subplots(figsize=FIG_SIZE_BAR)
    ax.hist(valid_capped, bins=50, color=PALETTE[0], alpha=0.8, edgecolor="white")
    ax.axvline(valid_capped.median(), color="red", linestyle="--", label=f"Median: {valid_capped.median():.0f} ms")
    ax.annotate(f"{int(n_outliers)} outliers > 10,000 ms\nexcluded from axis",
                xy=(0.97, 0.95), xycoords="axes fraction", ha="right", va="top",
                fontsize=9, color="grey",
                bbox=dict(boxstyle="round,pad=0.3", fc="white", alpha=0.7))
    ax.legend()
    style_axes(ax, "Distribution of avg page load time (ms, capped at 99th pct)", "Avg Load Time (ms)", "Frequency")
    save_fig(fig, "18_page_load_distribution.png")
    return {"chart_file": "18_page_load_distribution.png", "metric": "Avg Page Load Time (ms)",
            "top_value": round(float(valid_capped.median()), 1), "top_label": "Median",
            "note": f"{int(n_outliers)} outliers excluded"}


def main() -> None:
    PLOTS_DIR.mkdir(parents=True, exist_ok=True)
    print("=== Phase 2 - EDA & Visualisation ===")
    print("Loading clean data...")
    df = load_data()
    df_sess = df[df["Sessions"] > 0].copy()
    print(f"  Full df: {len(df):,} rows | Session-filtered df: {len(df_sess):,} rows")

    sns.set_theme(style="whitegrid")
    plt.rcParams["figure.facecolor"] = "white"

    summary_rows: list[dict] = []

    print("Generating charts...")
    summary_rows.append(chart_01_monthly_trend(df, df_sess))
    summary_rows.append(chart_02_yoy(df, df_sess))
    summary_rows.append(chart_03_channel_bar(df_sess))
    summary_rows.append(chart_04_channel_pie(df_sess))
    summary_rows.append(chart_05_channel_area(df_sess))
    summary_rows.append(chart_06_bounce_rate(df_sess))
    summary_rows.append(chart_07_top_countries(df_sess))
    summary_rows.append(chart_08_choropleth(df_sess))
    summary_rows.append(chart_09_top5_country_channel(df_sess))
    summary_rows.append(chart_10_source_medium(df_sess))
    summary_rows.append(chart_11_referral_sources(df_sess))
    summary_rows.append(chart_12_paid_search(df_sess))
    summary_rows.append(chart_13_device_pie(df))
    summary_rows.append(chart_14_mobile_trend(df_sess))
    summary_rows.append(chart_15_device_metrics(df_sess))
    summary_rows.append(chart_16_top_pages(df))
    summary_rows.append(chart_17_exit_rate(df))
    summary_rows.append(chart_18_load_time_dist(df))

    print("Saving eda_summary.csv...")
    pd.DataFrame(summary_rows).to_csv(EDA_CSV, index=False, encoding="utf-8")
    print(f"  {len(summary_rows)} charts documented.")
    print("=== Phase 2 complete ===")


if __name__ == "__main__":
    main()
