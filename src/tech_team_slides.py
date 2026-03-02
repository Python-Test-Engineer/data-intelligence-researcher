"""
Generate a 5-slide PDF deck of discovery questions for the tech team.
Topic: UI upgrade + AI chat interface over their database.
Output: tech-team-discovery.pdf (project root)
"""

import pathlib
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame,
    Paragraph, Spacer, HRFlowable, Table, TableStyle,
    NextPageTemplate, PageBreak,
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
BASE   = pathlib.Path(__file__).parent.parent
OUTPUT = BASE / "tech-team-discovery.pdf"

# ---------------------------------------------------------------------------
# Palette
# ---------------------------------------------------------------------------
NAVY    = colors.HexColor("#0d1b40")
BLUE    = colors.HexColor("#1a56db")
LBLUE   = colors.HexColor("#e8f0fe")
ACCENT  = colors.HexColor("#f59e0b")   # amber — used for question numbers
DGREY   = colors.HexColor("#374151")
MGREY   = colors.HexColor("#6b7280")
LGREY   = colors.HexColor("#f3f4f6")
WHITE   = colors.white

# ---------------------------------------------------------------------------
# Page geometry  (A4 landscape = 297 × 210 mm)
# ---------------------------------------------------------------------------
W, H = A4[1], A4[0]           # swap for landscape
MARGIN_X = 1.8 * cm
MARGIN_TOP = 1.6 * cm
MARGIN_BOT = 1.4 * cm

# ---------------------------------------------------------------------------
# Styles
# ---------------------------------------------------------------------------
def S(name, **kw):
    return ParagraphStyle(name, **kw)

SLIDE_NUM  = S("snum",  fontName="Helvetica", fontSize=8,
               textColor=MGREY, alignment=TA_RIGHT)
SLIDE_TAG  = S("stag",  fontName="Helvetica-Bold", fontSize=8,
               textColor=BLUE,  alignment=TA_LEFT)
TITLE      = S("title", fontName="Helvetica-Bold", fontSize=28,
               textColor=WHITE, leading=34, spaceAfter=6)
SUBTITLE   = S("sub",   fontName="Helvetica", fontSize=14,
               textColor=colors.HexColor("#cbd5e1"), leading=18)
H1         = S("h1",    fontName="Helvetica-Bold", fontSize=20,
               textColor=NAVY,  leading=26, spaceAfter=4)
H2         = S("h2",    fontName="Helvetica-Bold", fontSize=12,
               textColor=BLUE,  leading=16, spaceAfter=2, spaceBefore=10)
BODY       = S("body",  fontName="Helvetica", fontSize=10,
               textColor=DGREY, leading=15, spaceAfter=3)
QNUM       = S("qnum",  fontName="Helvetica-Bold", fontSize=10,
               textColor=ACCENT)
QTXT       = S("qtxt",  fontName="Helvetica", fontSize=10,
               textColor=DGREY, leading=15)
HINT       = S("hint",  fontName="Helvetica-Oblique", fontSize=8,
               textColor=MGREY, leading=12)
FOOTER_L   = S("ftl",   fontName="Helvetica", fontSize=7,
               textColor=MGREY, alignment=TA_LEFT)
FOOTER_R   = S("ftr",   fontName="Helvetica", fontSize=7,
               textColor=MGREY, alignment=TA_RIGHT)

# ---------------------------------------------------------------------------
# Slide data
# ---------------------------------------------------------------------------
SLIDES = [
    # ── Slide 1: Title ──────────────────────────────────────────────────────
    {
        "type": "title",
        "tag":  "Discovery Session",
        "title": "UI Upgrade &\nAI Chat Interface",
        "subtitle": "Questions to align the team and define the path forward",
        "footer": "Prepared for the Tech Team  •  2026",
    },

    # ── Slide 2: The database & current app ─────────────────────────────────
    {
        "type": "questions",
        "tag":  "Foundation  |  Slide 2 of 6",
        "heading": "Understanding Your Database & App",
        "intro": "Before designing anything we need a clear picture of what exists today.",
        "questions": [
            ("1", "What database are you running — and what does the schema look like?",
             "e.g. PostgreSQL, MySQL, SQL Server. How many tables? Any views or stored procs we should know about?"),
            ("2", "Who are the primary users of the site — internal staff, customers, or both?",
             "This shapes access controls, tone of the UI, and what the chat interface is allowed to expose."),
            ("3", "What kinds of questions do users currently struggle to answer from the site?",
             "These become the first use-cases for the chat interface and the priority areas for the UI redesign."),
            ("4", "Are there any data sensitivity or compliance constraints we need to respect?",
             "e.g. PII, GDPR, financial data. Determines what the AI can read and return."),
        ],
    },

    # ── Slide 3: UI redesign ────────────────────────────────────────────────
    {
        "type": "questions",
        "tag":  "UI Upgrade  |  Slide 3 of 6",
        "heading": "Scoping the UI Redesign",
        "intro": "A clear brief prevents scope creep and sets realistic expectations.",
        "questions": [
            ("1", "What is the current front-end stack, and is it staying or changing?",
             "e.g. vanilla HTML/CSS, React, Django templates. Knowing this decides whether we restyle or rebuild."),
            ("2", "Do you have brand guidelines, a design system, or a reference site you want to match?",
             "If yes, brings assets to the next meeting. If no, we should agree on palette and component library first."),
            ("3", "Which three pages or workflows cause the most friction for users right now?",
             "Focus the redesign effort where it has the highest immediate impact."),
            ("4", "Is this a full redesign, a visual refresh, or adding new components (e.g. chat panel)?",
             "Helps us decide between a phased rollout vs. a big-bang release and estimate effort correctly."),
        ],
    },

    # ── Slide 4: Infrastructure & deployment ────────────────────────────────
    {
        "type": "questions",
        "tag":  "Infrastructure  |  Slide 4 of 6",
        "heading": "Deployment & Infrastructure",
        "intro": "Understanding how and where the app runs is critical before adding new components.",
        "questions": [
            ("1", "Where is the site currently hosted — on-prem, cloud, or shared hosting?",
             "e.g. AWS, Azure, GCP, self-hosted server, Heroku. Determines latency, scaling options, and cost model for the chat feature."),
            ("2", "Is the app containerised? Are you using Docker, Kubernetes, or Docker Compose?",
             "Containerised apps make it much easier to add a new AI service alongside the existing stack without disrupting production."),
            ("3", "How are deployments done today — CI/CD pipeline, manual FTP, or something else?",
             "Automated pipelines (GitHub Actions, GitLab CI, etc.) let us ship UI changes and the chat service safely and repeatedly."),
            ("4", "What is the backend language and framework powering the site?",
             "e.g. Django, Laravel, Node/Express, .NET, Rails. The chat integration will need to hook into this layer to query the database."),
        ],
    },

    # ── Slide 5: Chat interface ──────────────────────────────────────────────
    {
        "type": "questions",
        "tag":  "AI Chat  |  Slide 5 of 6",
        "heading": "Designing the Chat Interface",
        "intro": "The chat feature needs well-defined boundaries before any code is written.",
        "questions": [
            ("1", "Should the chat generate and run SQL, or only retrieve pre-approved answers?",
             "Free SQL is powerful but risky on production data. Pre-approved queries are safer but need curation."),
            ("2", "What level of technical sophistication do the users have?",
             "Non-technical users need plain-English answers; power users may want the underlying query shown."),
            ("3", "Where does the chat live — embedded in a page, a floating panel, or its own screen?",
             "This drives the UI layout decision and how it integrates with the existing navigation."),
            ("4", "What is the acceptable latency and how should failures be handled?",
             "Chat over a large DB can be slow. Do users expect instant results or is a loading state acceptable?"),
            ("5", "Who is responsible for monitoring, moderating, and improving the chat over time?",
             "AI chat needs ongoing oversight — bad answers erode trust quickly if nobody owns quality."),
        ],
    },

    # ── Slide 5: Priorities & next steps ────────────────────────────────────
    {
        "type": "questions",
        "tag":  "Next Steps  |  Slide 6 of 6",
        "heading": "Priorities & Decisions",
        "intro": "Leaving this meeting with clear owners and a sequenced plan.",
        "questions": [
            ("1", "Which comes first — UI redesign or chat interface, or do they run in parallel?",
             "Parallel tracks need separate owners. Sequential work is safer but slower."),
            ("2", "What does 'done' look like for a first release, and what can be deferred to v2?",
             "Define the MVP now so the team has a finish line, not an endless backlog."),
            ("3", "Who is the single decision-maker when the team disagrees on direction?",
             "Avoids design-by-committee delays. One owner per workstream is ideal."),
            ("4", "Do we have API access to Claude already, or does that need to be procured?",
             "Claude API keys and usage limits need to be in place before development starts."),
        ],
        "cta": "ACTION: Assign an owner to each question above before the next meeting.",
    },
]

# ---------------------------------------------------------------------------
# Drawing helpers
# ---------------------------------------------------------------------------

def draw_title_slide(canvas, slide, W, H):
    """Full-bleed navy background title slide."""
    canvas.setFillColor(NAVY)
    canvas.rect(0, 0, W, H, fill=1, stroke=0)

    # Amber accent bar on left
    canvas.setFillColor(ACCENT)
    canvas.rect(0, 0, 0.6 * cm, H, fill=1, stroke=0)

    # Tag line top-right
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.HexColor("#94a3b8"))
    canvas.drawRightString(W - MARGIN_X, H - 0.9 * cm, slide["tag"])

    # Title
    y = H * 0.62
    canvas.setFont("Helvetica-Bold", 34)
    canvas.setFillColor(WHITE)
    for line in slide["title"].split("\n"):
        canvas.drawString(MARGIN_X + 0.8 * cm, y, line)
        y -= 42

    # Subtitle
    canvas.setFont("Helvetica", 14)
    canvas.setFillColor(colors.HexColor("#94a3b8"))
    canvas.drawString(MARGIN_X + 0.8 * cm, y - 8, slide["subtitle"])

    # Horizontal rule
    y -= 28
    canvas.setStrokeColor(ACCENT)
    canvas.setLineWidth(1.5)
    canvas.line(MARGIN_X + 0.8 * cm, y, W * 0.55, y)

    # Footer
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.HexColor("#64748b"))
    canvas.drawString(MARGIN_X + 0.8 * cm, MARGIN_BOT, slide["footer"])


def draw_content_slide(canvas, slide, W, H):
    """White content slide with questions."""
    # White background
    canvas.setFillColor(WHITE)
    canvas.rect(0, 0, W, H, fill=1, stroke=0)

    # Navy header band
    header_h = 2.6 * cm
    canvas.setFillColor(NAVY)
    canvas.rect(0, H - header_h, W, header_h, fill=1, stroke=0)

    # Amber left accent bar (header only)
    canvas.setFillColor(ACCENT)
    canvas.rect(0, H - header_h, 0.6 * cm, header_h, fill=1, stroke=0)

    # Slide tag (top-left in header)
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.HexColor("#93c5fd"))
    canvas.drawString(MARGIN_X + 0.8 * cm, H - 1.0 * cm, slide["tag"])

    # Heading in header
    canvas.setFont("Helvetica-Bold", 18)
    canvas.setFillColor(WHITE)
    canvas.drawString(MARGIN_X + 0.8 * cm, H - header_h + 0.55 * cm, slide["heading"])

    # Intro line below header
    canvas.setFont("Helvetica-Oblique", 9)
    canvas.setFillColor(MGREY.clone() if hasattr(MGREY, 'clone') else colors.HexColor("#6b7280"))
    canvas.drawString(MARGIN_X, H - header_h - 0.55 * cm, slide["intro"])

    # Questions
    questions = slide["questions"]
    col_count = 2 if len(questions) >= 4 else 1
    col_w = (W - 2 * MARGIN_X - 0.4 * cm) / col_count
    col_gap = 0.4 * cm

    top_y = H - header_h - 1.3 * cm
    row_h = (top_y - MARGIN_BOT - 0.8 * cm) / (len(questions) // col_count + (len(questions) % col_count))

    for idx, (num, question, hint) in enumerate(questions):
        col = idx % col_count
        row = idx // col_count
        x = MARGIN_X + col * (col_w + col_gap)
        y = top_y - row * row_h

        # Question card background
        card_pad = 0.25 * cm
        card_h = row_h - 0.2 * cm
        canvas.setFillColor(LGREY)
        canvas.roundRect(x, y - card_h + card_pad, col_w - 0.2 * cm, card_h - card_pad,
                         radius=4, fill=1, stroke=0)

        # Number badge
        badge_r = 0.26 * cm
        bx = x + card_pad + badge_r + 0.05 * cm
        by = y - card_pad - badge_r - 0.05 * cm
        canvas.setFillColor(ACCENT)
        canvas.circle(bx, by, badge_r, fill=1, stroke=0)
        canvas.setFont("Helvetica-Bold", 8)
        canvas.setFillColor(WHITE)
        canvas.drawCentredString(bx, by - 3, num)

        # Question text
        text_x = bx + badge_r + 0.2 * cm
        canvas.setFont("Helvetica-Bold", 12)
        canvas.setFillColor(DGREY)
        # Wrap text manually
        max_w = col_w - (text_x - x) - 0.3 * cm
        _draw_wrapped(canvas, question, text_x, y - card_pad - 0.08 * cm,
                      max_w, "Helvetica-Bold", 12, DGREY, 16)

        # Hint text
        canvas.setFont("Helvetica-Oblique", 7.5)
        canvas.setFillColor(MGREY)
        _draw_wrapped(canvas, hint, x + card_pad, y - card_h + card_pad * 2 + 0.15 * cm,
                      col_w - card_pad * 2 - 0.2 * cm, "Helvetica-Oblique", 7.5, MGREY, 10)

    # CTA banner at bottom if present
    if slide.get("cta"):
        canvas.setFillColor(LBLUE)
        canvas.rect(MARGIN_X, MARGIN_BOT - 0.1 * cm,
                    W - 2 * MARGIN_X, 0.65 * cm, fill=1, stroke=0)
        canvas.setFont("Helvetica-Bold", 8.5)
        canvas.setFillColor(BLUE)
        canvas.drawString(MARGIN_X + 0.3 * cm, MARGIN_BOT + 0.12 * cm, slide["cta"])

    # Footer rule
    canvas.setStrokeColor(colors.HexColor("#e5e7eb"))
    canvas.setLineWidth(0.5)
    canvas.line(MARGIN_X, MARGIN_BOT - 0.2 * cm, W - MARGIN_X, MARGIN_BOT - 0.2 * cm)


def _draw_wrapped(canvas, text, x, y, max_w, font, size, color, leading):
    """Very simple word-wrap for canvas text."""
    canvas.setFont(font, size)
    canvas.setFillColor(color)
    words = text.split()
    line = ""
    cy = y
    for word in words:
        test = (line + " " + word).strip()
        if canvas.stringWidth(test, font, size) <= max_w:
            line = test
        else:
            if line:
                canvas.drawString(x, cy, line)
                cy -= leading
            line = word
    if line:
        canvas.drawString(x, cy, line)


# ---------------------------------------------------------------------------
# Build PDF
# ---------------------------------------------------------------------------
def build_pdf():
    from reportlab.pdfgen import canvas as pdfcanvas

    c = pdfcanvas.Canvas(str(OUTPUT), pagesize=(W, H))
    c.setTitle("Tech Team Discovery: UI Upgrade & AI Chat Interface")
    c.setAuthor("Claude Code")
    c.setSubject("Discovery questions for UI redesign and AI chat over database")

    for slide in SLIDES:
        if slide["type"] == "title":
            draw_title_slide(c, slide, W, H)
        else:
            draw_content_slide(c, slide, W, H)
        c.showPage()

    c.save()
    print(f"Saved: {OUTPUT}")


if __name__ == "__main__":
    build_pdf()
