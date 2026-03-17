---
description: "Build and launch an interactive Shiny Dash dashboard from a PROJECT_XX output folder. Usage: /dashboard output/PROJECT_XX"
allowed-tools: Read, Glob, Grep, Bash(uv run python *), Bash(uv add *), Write, AskUserQuestion
argument: "Path to an output folder, e.g. output/PROJECT_02 — REQUIRED"
hint: "Provide the output folder path as an argument, e.g. /dashboard output/PROJECT_02"
---

**Argument required:** path to a project output folder, e.g. `output/PROJECT_02`. Find the PROJECT with the largest _XX number and add 1 to create PROJECT_YY where YY is one up from XX.

If no argument is given, list available folders:

```
Glob: output/PROJECT_*
```

Then stop and ask the user to re-run with the correct folder path.

---

## Your role

You are an experienced data visualisation engineer. Your job is to:

1. Inspect the output folder at `$ARGUMENTS`
2. Discover all available data files (CSVs, PNGs, report.txt, parquets)
3. Install any missing dependencies
4. Write a production-quality **Plotly Dash** multi-page dashboard in `src/dashboard.py`
5. Run it and confirm it launches successfully

---

## Step 1 — Discover the output folder contents

Scan `$ARGUMENTS` for:
- `tables/*.csv` — structured data tables
- `model/*.csv` — model metrics
- `*.parquet` — clean datasets
- `plots/*.png` — static charts already generated
- `report.txt` — text summary
- `dirty.csv` — removed rows

Build a manifest of what is available.

---

## Step 2 — Install dependencies

```bash
uv add dash dash-bootstrap-components plotly pandas
```

---

## Step 3 — Write `src/dashboard.py`

### Architecture

Build a **multi-tab Dash app** using `dash-bootstrap-components`. One tab per data domain:

| Tab | Content |
|-----|---------|
| **Overview** | KPI cards (total rows, dirty rows, date range, loss rate), report.txt rendered as pre-formatted text |
| **Profitability** | Interactive bar + scatter charts from `profit_by_category.csv`; filterable by Category |
| **Discount Analysis** | Scatter of Discount vs Profit (from parquet) with colour-coded loss/profit; breakeven table |
| **RFM Segments** | Pie chart of segments; sortable DataTable of RFM scores with search |
| **Statistics** | DataTable of statistical test results; correlation heatmap image |
| **Models** | Bar chart of CV AUROC and F1 per model; inline PNG images for feature importance + ROC curves |
| **Charts Gallery** | All 16 static PNG plots displayed in a responsive image grid |

### Design rules

- Use `dash_bootstrap_components.themes.DARKLY` theme
- All charts built with `plotly.express` or `plotly.graph_objects` — **not** matplotlib (those are already saved PNGs)
- For PNGs: serve them as static assets via `app.server.static_folder` or encode as base64 inline
- KPI cards: use `dbc.Card` with a large number and a subtitle
- DataTables: use `dash.dash_table.DataTable` with `filter_action="native"`, `sort_action="native"`, `page_size=15`
- All chart containers: `style={"height": "500px"}` minimum
- App title: `"Superstore Analytics Dashboard — {PROJECT_XX}"`
- Port: `8050`; `debug=False` when run as script

### Constants at top of file

```python
OUTPUT_DIR = Path("$ARGUMENTS")
PROJECT_NAME = OUTPUT_DIR.name   # e.g. "PROJECT_02"
PORT = 8050
```

### PNG serving

Encode each PNG as base64 for inline embedding (avoids static file server complexity on Windows):

```python
import base64
def encode_image(path: Path) -> str:
    return "data:image/png;base64," + base64.b64encode(path.read_bytes()).decode()
```

### Layout skeleton

```python
app.layout = dbc.Container([
    dbc.Row(dbc.Col(html.H1(f"Superstore Analytics — {PROJECT_NAME}"))),
    dbc.Tabs([
        dbc.Tab(label="Overview",        tab_id="overview"),
        dbc.Tab(label="Profitability",   tab_id="profit"),
        dbc.Tab(label="Discount",        tab_id="discount"),
        dbc.Tab(label="RFM Segments",    tab_id="rfm"),
        dbc.Tab(label="Statistics",      tab_id="stats"),
        dbc.Tab(label="Models",          tab_id="models"),
        dbc.Tab(label="Charts Gallery",  tab_id="gallery"),
    ], id="tabs", active_tab="overview"),
    html.Div(id="tab-content"),
], fluid=True)
```

Use a single callback `@app.callback(Output("tab-content", "children"), Input("tabs", "active_tab"))` to render each tab's content lazily.

---

## Step 4 — Run the dashboard

```bash
uv run python src/dashboard.py
```

The app should start and print:
```
Dash is running on http://127.0.0.1:8050/
```

Run in **background** so it does not block. Then open the URL in the browser:

```bash
start http://127.0.0.1:8050
```

(On Windows use `start`, on macOS use `open`, on Linux use `xdg-open`.)

---

## Step 5 — Confirm and report

Tell the user:
- The URL to open: `http://127.0.0.1:8050`
- Which tabs are available and what data each shows
- The script location: `src/dashboard.py`
- Any files that were missing and therefore skipped

If the app fails to start, read the full traceback, fix the root cause, and re-run once. Do not retry the same failing command more than twice.
