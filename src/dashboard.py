"""Web Analytics Traffic Acquisition — Shiny for Python Dashboard.

Run with:
    uv run shiny run src/dashboard.py --reload
"""

from pathlib import Path

import pandas as pd
from shiny import App, render, ui
from shiny.ui import navbar_options
import faicons

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
OUTPUT_DIR = (Path(__file__).parent.parent / "output" / "PROJECT_02").resolve()
TABLES_DIR = OUTPUT_DIR / "tables"
PLOTS_DIR  = OUTPUT_DIR / "plots"

# ---------------------------------------------------------------------------
# Load data once at startup
# ---------------------------------------------------------------------------
ch  = pd.read_csv(TABLES_DIR / "channel_summary.csv")
cty = pd.read_csv(TABLES_DIR / "country_summary.csv")
sm  = pd.read_csv(TABLES_DIR / "source_medium_summary.csv")
dev = pd.read_csv(TABLES_DIR / "device_summary.csv")
mt  = pd.read_csv(TABLES_DIR / "monthly_trend.csv")
pg  = pd.read_csv(TABLES_DIR / "page_summary.csv")

# Headline KPIs
TOTAL_SESSIONS  = int(ch["Sessions"].sum())
TOTAL_PAGEVIEWS = int(ch["Pageviews"].sum())
TOP_CHANNEL     = str(ch.iloc[0]["Channel Grouping"])
TOP_COUNTRY     = str(cty.iloc[0]["Country"])
TOP_SOURCE      = str(sm.iloc[0]["Source Medium"])

mobile_row  = dev[dev["Device Category"] == "Mobile"]
MOBILE_PCT  = round(float(mobile_row["Sessions"].values[0]) / dev["Sessions"].sum() * 100, 1) if len(mobile_row) else 0.0
GOOGLE_BR_FLAG = "google.com.br" in TOP_SOURCE

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def chart_card(title: str, img_name: str, caption: str = "") -> ui.Tag:
    """A card containing a full-width plot image."""
    return ui.card(
        ui.card_header(title),
        ui.img(
            src=f"plots/{img_name}",
            style="width:100%; border-radius:4px;",
            alt=title,
        ),
        ui.p(caption, style="color:#666; font-size:0.82rem; margin:6px 8px 4px;") if caption else None,
        full_screen=True,
    )


def fmt_int(n: int) -> str:
    return f"{n:,}"


# ---------------------------------------------------------------------------
# UI
# ---------------------------------------------------------------------------
app_ui = ui.page_navbar(
    # ── Overview ────────────────────────────────────────────────────────────
    ui.nav_panel(
        "Overview",
        ui.layout_columns(
            ui.value_box(
                "Total Sessions",
                fmt_int(TOTAL_SESSIONS),
                showcase=faicons.icon_svg("users"),
                theme="primary",
            ),
            ui.value_box(
                "Total Pageviews",
                fmt_int(TOTAL_PAGEVIEWS),
                showcase=faicons.icon_svg("eye"),
                theme="secondary",
            ),
            ui.value_box(
                "Top Channel",
                TOP_CHANNEL,
                showcase=faicons.icon_svg("chart-bar"),
                theme="success",
            ),
            ui.value_box(
                "Top Country",
                TOP_COUNTRY,
                showcase=faicons.icon_svg("earth-americas"),
                theme="info",
            ),
            ui.value_box(
                "Mobile Share",
                f"{MOBILE_PCT}%",
                showcase=faicons.icon_svg("mobile-screen"),
                theme="warning",
            ),
            ui.value_box(
                "Date Range",
                "May 2017 – Aug 2019",
                showcase=faicons.icon_svg("calendar"),
                theme="light",
            ),
            col_widths=[2, 2, 2, 2, 2, 2],
        ),
        ui.hr(),
        ui.layout_columns(
            chart_card("Monthly sessions & pageviews", "01_monthly_sessions_pageviews.png",
                       "Full analysis window, May 2017 – August 2019."),
            chart_card("Year-over-year comparison", "02_yoy_sessions.png",
                       "Sessions and pageviews grouped by calendar year."),
            col_widths=[6, 6],
        ),
        ui.layout_columns(
            chart_card("Channel share over time", "05_channel_area_over_time.png",
                       "Monthly session share by channel grouping."),
            col_widths=[12],
        ),
        ui.layout_columns(
            ui.card(
                ui.card_header("Anomaly Notice"),
                ui.p(
                    ui.strong("google.com.br / Referral"),
                    " is the single largest source/medium combination with over 114,000 rows. "
                    "This is disproportionately high and may indicate a GA tagging "
                    "misconfiguration or bot/spam traffic. Investigate before using these "
                    "figures for acquisition decisions.",
                    style="color:#856404; background:#fff3cd; padding:10px; "
                          "border-radius:4px; font-size:0.9rem; margin:0;",
                ),
            ) if GOOGLE_BR_FLAG else ui.div(),
            col_widths=[12],
        ),
    ),

    # ── Traffic Trends ───────────────────────────────────────────────────────
    ui.nav_panel(
        "Traffic Trends",
        ui.layout_columns(
            chart_card("Monthly sessions & pageviews (2017–2019)",
                       "01_monthly_sessions_pageviews.png"),
            chart_card("Year-over-year sessions & pageviews",
                       "02_yoy_sessions.png"),
            col_widths=[6, 6],
        ),
        ui.card(
            ui.card_header("Monthly trend data"),
            ui.output_data_frame("tbl_monthly"),
        ),
    ),

    # ── Channel Analysis ─────────────────────────────────────────────────────
    ui.nav_panel(
        "Channel Analysis",
        ui.layout_columns(
            chart_card("Sessions by channel grouping", "03_channel_bar.png"),
            chart_card("Session share by channel", "04_channel_pie.png"),
            col_widths=[7, 5],
        ),
        ui.layout_columns(
            chart_card("Monthly channel share over time", "05_channel_area_over_time.png"),
            chart_card("Bounce rate by channel", "06_channel_bounce_rate.png"),
            col_widths=[7, 5],
        ),
        ui.card(
            ui.card_header("Channel summary table"),
            ui.output_data_frame("tbl_channel"),
        ),
    ),

    # ── Geographic ───────────────────────────────────────────────────────────
    ui.nav_panel(
        "Geographic",
        ui.layout_columns(
            chart_card("Sessions by country — world map", "08_country_choropleth.png",
                       "Colour intensity represents session volume."),
            col_widths=[12],
        ),
        ui.layout_columns(
            chart_card("Top 15 countries by sessions", "07_top15_countries.png"),
            chart_card("Top 5 countries by channel", "09_top5_country_channel.png"),
            col_widths=[5, 7],
        ),
        ui.card(
            ui.card_header("Country summary (top 30)"),
            ui.output_data_frame("tbl_country"),
        ),
    ),

    # ── Source / Medium ──────────────────────────────────────────────────────
    ui.nav_panel(
        "Source / Medium",
        ui.layout_columns(
            chart_card("Top 20 source/medium by sessions", "10_top20_source_medium.png"),
            col_widths=[12],
        ),
        ui.layout_columns(
            chart_card("Top 15 referral sources", "11_referral_sources.png"),
            chart_card("Paid search: sessions & bounce rate", "12_paid_search_sources.png"),
            col_widths=[6, 6],
        ),
        ui.card(
            ui.card_header("Source / medium summary (top 30)"),
            ui.output_data_frame("tbl_source_medium"),
        ),
    ),

    # ── Device Analysis ──────────────────────────────────────────────────────
    ui.nav_panel(
        "Device Analysis",
        ui.layout_columns(
            chart_card("Pageview share by device", "13_device_split_pie.png"),
            chart_card("Monthly mobile share of sessions", "14_device_mobile_trend.png"),
            col_widths=[4, 8],
        ),
        ui.layout_columns(
            chart_card("Bounce rate & load time by device", "15_device_bounce_loadtime.png"),
            col_widths=[12],
        ),
        ui.card(
            ui.card_header("Device summary table"),
            ui.output_data_frame("tbl_device"),
        ),
    ),

    # ── Page Performance ─────────────────────────────────────────────────────
    ui.nav_panel(
        "Page Performance",
        ui.layout_columns(
            chart_card("Top 20 pages by pageviews", "16_top20_pages_by_pageviews.png"),
            chart_card("Top 20 pages by exit rate", "17_top20_pages_by_exit_rate.png"),
            col_widths=[6, 6],
        ),
        ui.layout_columns(
            chart_card("Page load time distribution",
                       "18_page_load_distribution.png",
                       "Capped at 99th percentile. 13 extreme outliers (>10,000 ms) excluded from axis."),
            col_widths=[12],
        ),
        ui.card(
            ui.card_header("Page summary (top 50 by pageviews)"),
            ui.p("Page titles are anonymised IDs.",
                 style="color:#666; font-size:0.82rem; margin:4px 0 8px;"),
            ui.output_data_frame("tbl_pages"),
        ),
    ),

    # ── Data Tables ──────────────────────────────────────────────────────────
    ui.nav_panel(
        "Data Tables",
        ui.navset_tab(
            ui.nav_panel("Channels",     ui.output_data_frame("tbl_ch_raw")),
            ui.nav_panel("Countries",    ui.output_data_frame("tbl_cty_raw")),
            ui.nav_panel("Source/Med",   ui.output_data_frame("tbl_sm_raw")),
            ui.nav_panel("Devices",      ui.output_data_frame("tbl_dev_raw")),
            ui.nav_panel("Monthly Trend",ui.output_data_frame("tbl_mt_raw")),
            ui.nav_panel("Pages",        ui.output_data_frame("tbl_pg_raw")),
        ),
    ),

    # ── shell ────────────────────────────────────────────────────────────────
    title=ui.span(
        faicons.icon_svg("chart-line"),
        " Web Analytics — Traffic Acquisition",
    ),
    navbar_options=navbar_options(bg="#1a1a2e"),
    id="main_nav",
)


# ---------------------------------------------------------------------------
# Server
# ---------------------------------------------------------------------------
def server(input, output, session):

    @render.data_frame
    def tbl_channel():
        return render.DataGrid(ch, filters=True, height="400px")

    @render.data_frame
    def tbl_country():
        return render.DataGrid(cty, filters=True, height="400px")

    @render.data_frame
    def tbl_source_medium():
        return render.DataGrid(sm, filters=True, height="400px")

    @render.data_frame
    def tbl_device():
        return render.DataGrid(dev, height="250px")

    @render.data_frame
    def tbl_monthly():
        return render.DataGrid(mt, filters=True, height="400px")

    @render.data_frame
    def tbl_pages():
        return render.DataGrid(pg, filters=True, height="400px")

    # raw table tab duplicates
    @render.data_frame
    def tbl_ch_raw():
        return render.DataGrid(ch, filters=True, height="500px")

    @render.data_frame
    def tbl_cty_raw():
        return render.DataGrid(cty, filters=True, height="500px")

    @render.data_frame
    def tbl_sm_raw():
        return render.DataGrid(sm, filters=True, height="500px")

    @render.data_frame
    def tbl_dev_raw():
        return render.DataGrid(dev, height="300px")

    @render.data_frame
    def tbl_mt_raw():
        return render.DataGrid(mt, filters=True, height="500px")

    @render.data_frame
    def tbl_pg_raw():
        return render.DataGrid(pg, filters=True, height="500px")


# ---------------------------------------------------------------------------
# App
# ---------------------------------------------------------------------------
app = App(
    ui=app_ui,
    server=server,
    static_assets=OUTPUT_DIR,
)
