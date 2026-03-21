"""
Shiny for Python dashboard — auto-discovers highest PROJECT_XX output folder.
"""

import base64
import random
from pathlib import Path

import pandas as pd
from shiny import App, reactive, render, ui
from shinywidgets import output_widget, render_widget
import plotly.express as px

# ---------------------------------------------------------------------------
# Resolve output folder
# ---------------------------------------------------------------------------
_candidates = sorted(Path("output").glob("PROJECT_*"))
OUTPUT_DIR = _candidates[-1]
PROJECT_NAME = OUTPUT_DIR.name

PORT = random.randint(8000, 8999)

# ---------------------------------------------------------------------------
# Discover available files
# ---------------------------------------------------------------------------
PLOTS_DIR = OUTPUT_DIR / "plots"
REPORT_HTML = OUTPUT_DIR / "report.html"
SUMMARY_CSV = OUTPUT_DIR / "summary_stats.csv"
DIRTY_CSV = OUTPUT_DIR / "dirty.csv"
CLEAN_CSV = OUTPUT_DIR / "clean.csv"

plots = sorted(PLOTS_DIR.glob("*.png")) if PLOTS_DIR.exists() else []
has_plots = len(plots) > 0
has_report = REPORT_HTML.exists()
has_summary = SUMMARY_CSV.exists()
has_dirty = DIRTY_CSV.exists()
has_clean = CLEAN_CSV.exists()

# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------
df_summary = pd.read_csv(SUMMARY_CSV) if has_summary else pd.DataFrame()
df_dirty = pd.read_csv(DIRTY_CSV) if has_dirty else pd.DataFrame()
df_clean = pd.read_csv(CLEAN_CSV, nrows=5000) if has_clean else pd.DataFrame()

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def encode_png(path: Path) -> str:
    return "data:image/png;base64," + base64.b64encode(path.read_bytes()).decode()


def kpi_card(title: str, value: str, icon: str = "bi-bar-chart-fill", color: str = "primary"):
    return ui.div(
        ui.div(
            ui.tags.i(class_=f"bi {icon}", style="font-size:2rem;"),
            ui.h2(value, class_="mt-1 mb-0 fw-bold"),
            ui.p(title, class_="text-muted mb-0 small"),
            class_="card-body text-center py-3",
        ),
        class_=f"card border-{color} mb-3 h-100",
    )


# ---------------------------------------------------------------------------
# Overview tab UI
# ---------------------------------------------------------------------------
def overview_ui():
    total_rows = 110521
    dirty_rows = len(df_dirty) if has_dirty else 0

    kpi_row = ui.row(
        ui.column(3, kpi_card("Total Appointments", f"{total_rows:,}", "bi-calendar-check-fill", "primary")),
        ui.column(3, kpi_card("Unique Patients", "62,298", "bi-people-fill", "info")),
        ui.column(3, kpi_card("Overall No-Show Rate", "20.19%", "bi-x-circle-fill", "warning")),
        ui.column(3, kpi_card("Dirty Rows Removed", str(dirty_rows), "bi-trash3-fill", "danger")),
    )

    if has_report:
        report_html_content = REPORT_HTML.read_text(encoding="utf-8", errors="replace")
        # Embed as a sandboxed iframe using srcdoc
        report_section = ui.div(
            ui.h4("Project Report", class_="mt-4 mb-3"),
            ui.tags.iframe(
                srcdoc=report_html_content,
                style="width:100%; height:680px; border:1px solid #555; border-radius:6px;",
                sandbox="allow-scripts allow-same-origin",
            ),
            class_="mt-2",
        )
    else:
        report_section = ui.p("No report.html found.", class_="text-muted mt-4")

    return ui.div(
        ui.h3("Medical Appointment No-Show Analysis", class_="mb-1"),
        ui.p("Brazil hospital appointments dataset — 110,527 records across 81 neighbourhoods in Vitoria, ES.", class_="text-muted mb-4"),
        kpi_row,
        ui.hr(),
        report_section,
        class_="p-3",
    )


# ---------------------------------------------------------------------------
# Charts Gallery tab UI
# ---------------------------------------------------------------------------
CHART_LABELS = {
    "01_age_distribution": "Age Distribution",
    "02_lead_days_distribution": "Lead Days Distribution",
    "03_noshow_overall": "No-Show Overall",
    "04_binary_flags_prevalence": "Binary Flags Prevalence",
    "05_gender_split": "Gender Split",
    "06_top20_neighbourhoods": "Top 20 Neighbourhoods",
    "07_appointments_by_weekday": "Appointments by Weekday",
    "08_appointments_over_time": "Appointments Over Time",
    "09_noshow_by_gender": "No-Show by Gender",
    "10_noshow_by_age_group": "No-Show by Age Group",
    "11_noshow_by_lead_days": "No-Show by Lead Days",
    "12_noshow_by_sms": "No-Show by SMS",
    "13_noshow_by_conditions": "No-Show by Conditions",
    "14_noshow_by_weekday": "No-Show by Weekday",
    "15_noshow_by_neighbourhood": "No-Show by Neighbourhood",
    "16_noshow_by_month": "No-Show by Month",
    "17_repeat_patient_noshow": "Repeat Patient No-Show",
    "18_correlation_heatmap": "Correlation Heatmap",
    "19_sms_paradox": "SMS Paradox",
    "20_age_condition_heatmap": "Age × Condition Heatmap",
    "21_neighbourhood_inequality": "Neighbourhood Inequality",
    "22_same_day_profile": "Same-Day Profile",
    "23_scholarship_analysis": "Scholarship Analysis",
    "24_patient_appointment_counts": "Patient Appointment Counts",
    "25_weekly_noshow_timeseries": "Weekly No-Show Time Series",
}


def gallery_ui():
    if not has_plots:
        return ui.p("No PNG charts found in plots/.", class_="text-muted p-3")

    rows = []
    row_items = []
    for i, p in enumerate(plots):
        stem = p.stem
        label = CHART_LABELS.get(stem, stem.replace("_", " ").title())
        encoded = encode_png(p)
        card = ui.column(
            4,
            ui.div(
                ui.tags.img(
                    src=encoded,
                    style="width:100%; border-radius:4px; cursor:pointer;",
                    title=label,
                    **{"data-bs-toggle": "modal", "data-bs-target": f"#modal-{i}"},
                ),
                ui.p(label, class_="text-center small mt-1 mb-0 text-muted"),
                ui.tags.div(
                    ui.tags.div(
                        ui.tags.div(
                            ui.tags.div(
                                ui.tags.button(
                                    ui.HTML("&times;"),
                                    class_="btn-close btn-close-white",
                                    **{"data-bs-dismiss": "modal"},
                                ),
                                class_="modal-header border-0 justify-content-end",
                            ),
                            ui.tags.div(
                                ui.tags.img(src=encoded, style="width:100%; border-radius:4px;"),
                                ui.tags.p(label, class_="text-center mt-2 text-muted"),
                                class_="modal-body",
                            ),
                            class_="modal-content bg-dark",
                        ),
                        class_="modal-dialog modal-xl modal-dialog-centered",
                    ),
                    class_="modal fade",
                    id=f"modal-{i}",
                    tabindex="-1",
                ),
                class_="mb-4",
            ),
        )
        row_items.append(card)
        if len(row_items) == 3:
            rows.append(ui.row(*row_items))
            row_items = []

    if row_items:
        rows.append(ui.row(*row_items))

    return ui.div(
        ui.h4(f"{len(plots)} Charts", class_="mb-1"),
        ui.p("Click any chart to expand it in full size.", class_="text-muted small mb-4"),
        *rows,
        class_="p-3",
    )


# ---------------------------------------------------------------------------
# Data Tables tab UI
# ---------------------------------------------------------------------------
def tables_ui():
    panels = []

    if has_clean:
        panels.append(
            ui.nav_panel(
                "Clean Data (first 5,000 rows)",
                ui.output_data_frame("tbl_clean"),
            )
        )
    if has_summary:
        panels.append(
            ui.nav_panel(
                "Summary Stats",
                ui.output_data_frame("tbl_summary"),
            )
        )
    if has_dirty:
        panels.append(
            ui.nav_panel(
                "Dirty Rows",
                ui.output_data_frame("tbl_dirty"),
            )
        )

    if not panels:
        return ui.p("No CSV files found.", class_="text-muted p-3")

    return ui.div(
        ui.navset_tab(*panels, id="data_tabs"),
        class_="p-3",
    )


# ---------------------------------------------------------------------------
# Statistics tab UI
# ---------------------------------------------------------------------------
def statistics_ui():
    if not has_summary:
        return ui.p("No summary_stats.csv found.", class_="text-muted p-3")
    return ui.div(
        ui.h4("Summary Statistics", class_="mb-3"),
        ui.row(
            ui.column(5, ui.output_data_frame("tbl_stats_full")),
            ui.column(7, output_widget("chart_stats")),
        ),
        class_="p-3",
    )


# ---------------------------------------------------------------------------
# Dirty Data tab UI
# ---------------------------------------------------------------------------
def dirty_ui():
    if not has_dirty:
        return ui.p("No dirty.csv found.", class_="text-muted p-3")
    return ui.div(
        ui.h4("Removed Rows Analysis", class_="mb-3"),
        ui.row(
            ui.column(5, output_widget("chart_dirty_reasons")),
            ui.column(7, ui.output_data_frame("tbl_dirty_full")),
        ),
        class_="p-3",
    )


# ---------------------------------------------------------------------------
# App UI
# ---------------------------------------------------------------------------
nav_panels = [ui.nav_panel("Overview", overview_ui())]
if has_plots:
    nav_panels.append(ui.nav_panel("Charts Gallery", gallery_ui()))
nav_panels.append(ui.nav_panel("Data Tables", tables_ui()))
if has_summary:
    nav_panels.append(ui.nav_panel("Statistics", statistics_ui()))
if has_dirty:
    nav_panels.append(ui.nav_panel("Dirty Data", dirty_ui()))

app_ui = ui.page_navbar(
    ui.head_content(
        ui.tags.link(
            rel="stylesheet",
            href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css",
        ),
        ui.output_ui("theme_link"),
    ),
    *nav_panels,
    title=ui.span(
        ui.tags.i(class_="bi bi-activity me-2"),
        f"{PROJECT_NAME} — Data Intelligence",
    ),
    header=ui.div(
        ui.output_ui("toggle_icon", inline=True),
        ui.input_action_button(
            "toggle_theme",
            "",
            class_="btn btn-sm ms-2",
            style="border:none; background:transparent; cursor:pointer;",
        ),
        style="display:flex; align-items:center; margin-left:auto; padding-right:1rem;",
    ),
    id="navbar",
    inverse=True,
)


# ---------------------------------------------------------------------------
# Server
# ---------------------------------------------------------------------------
def server(input, output, session):
    theme_dark = reactive.Value(True)

    @reactive.effect
    @reactive.event(input.toggle_theme)
    def _flip_theme():
        theme_dark.set(not theme_dark.get())

    @render.ui
    def theme_link():
        if theme_dark.get():
            href = "https://cdn.jsdelivr.net/npm/bootswatch@5.3.3/dist/darkly/bootstrap.min.css"
        else:
            href = "https://cdn.jsdelivr.net/npm/bootswatch@5.3.3/dist/flatly/bootstrap.min.css"
        return ui.tags.link(rel="stylesheet", href=href)

    @render.ui
    def toggle_icon():
        if theme_dark.get():
            return ui.tags.i(class_="bi bi-sun-fill", style="font-size:1.3rem; color:#ffd700;")
        return ui.tags.i(class_="bi bi-moon-fill", style="font-size:1.3rem; color:#aaa;")

    # --- Data Tables ---
    @render.data_frame
    def tbl_clean():
        return render.DataGrid(df_clean, filters=True, height="500px")

    @render.data_frame
    def tbl_summary():
        return render.DataGrid(df_summary, filters=True)

    @render.data_frame
    def tbl_dirty():
        return render.DataGrid(df_dirty, filters=True)

    # --- Statistics ---
    @render.data_frame
    def tbl_stats_full():
        return render.DataGrid(df_summary)

    @render_widget
    def chart_stats():
        df = df_summary.copy()
        df.columns = ["metric", "value"]
        numeric_rows = []
        for _, row in df.iterrows():
            try:
                v = float(str(row["value"]).replace(",", "").replace("%", ""))
                numeric_rows.append({"metric": row["metric"], "value": v})
            except Exception:
                pass
        if not numeric_rows:
            return px.bar(title="No numeric data")
        df_num = pd.DataFrame(numeric_rows)
        rate_rows = df_num[df_num["metric"].str.contains("rate|%|mean|median", case=False, na=False)]
        if len(rate_rows) < 2:
            rate_rows = df_num.head(10)
        fig = px.bar(
            rate_rows,
            x="value",
            y="metric",
            orientation="h",
            title="Key Metrics at a Glance",
            labels={"value": "Value", "metric": ""},
            color="value",
            color_continuous_scale="Teal",
        )
        fig.update_layout(
            template="plotly_dark" if theme_dark.get() else "plotly_white",
            height=420,
            margin=dict(l=10, r=10, t=40, b=10),
            coloraxis_showscale=False,
            yaxis=dict(tickfont=dict(size=10)),
        )
        return fig

    # --- Dirty Data ---
    @render.data_frame
    def tbl_dirty_full():
        return render.DataGrid(df_dirty, filters=True)

    @render_widget
    def chart_dirty_reasons():
        if df_dirty.empty:
            return px.bar(title="No dirty data")
        df = df_dirty.copy()
        reason_col = "reason" if "reason" in df.columns else df.columns[-1]
        counts = df[reason_col].value_counts().reset_index()
        counts.columns = ["reason", "count"]
        fig = px.bar(
            counts,
            x="count",
            y="reason",
            orientation="h",
            title="Removed Rows by Reason",
            labels={"count": "Rows", "reason": ""},
            color="count",
            color_continuous_scale="Reds",
        )
        fig.update_layout(
            template="plotly_dark" if theme_dark.get() else "plotly_white",
            height=300,
            margin=dict(l=10, r=10, t=40, b=10),
            coloraxis_showscale=False,
        )
        return fig


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
app = App(app_ui, server)

if __name__ == "__main__":
    import uvicorn

    print(f"\n  Dashboard : http://127.0.0.1:{PORT}")
    print(f"  Project   : {PROJECT_NAME}")
    print(f"  Charts    : {len(plots)}")
    print(f"  Output    : {OUTPUT_DIR}\n")

    uvicorn.run(app, host="127.0.0.1", port=PORT)
