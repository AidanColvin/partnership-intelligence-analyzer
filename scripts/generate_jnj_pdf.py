"""Generate a formatted partnership intelligence PDF for Johnson & Johnson."""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, KeepTogether
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY

OUTPUT_PATH = "/Users/aidancolvin/partnership-intelligence-analyzer/data/processed/company-profiles/jnj/deliverable.pdf"

# ── Color palette ──────────────────────────────────────────────────────────────
JNJ_RED      = colors.HexColor("#CC0000")
DARK_NAVY    = colors.HexColor("#1a1f36")
MID_GRAY     = colors.HexColor("#5f6368")
LIGHT_RED    = colors.HexColor("#fff5f5")
ACCENT_DARK  = colors.HexColor("#8B0000")
RULE_COLOR   = colors.HexColor("#f0c0c0")


def build_styles():
    base = getSampleStyleSheet()

    return {
        "cover_title": ParagraphStyle(
            "cover_title", parent=base["Title"],
            fontSize=28, leading=34, textColor=DARK_NAVY,
            spaceAfter=6, alignment=TA_LEFT,
        ),
        "cover_sub": ParagraphStyle(
            "cover_sub", parent=base["Normal"],
            fontSize=13, leading=18, textColor=MID_GRAY,
            spaceAfter=4, alignment=TA_LEFT,
        ),
        "cover_meta": ParagraphStyle(
            "cover_meta", parent=base["Normal"],
            fontSize=10, leading=14, textColor=MID_GRAY,
            spaceAfter=2, alignment=TA_LEFT,
        ),
        "section_heading": ParagraphStyle(
            "section_heading", parent=base["Heading1"],
            fontSize=13, leading=17, textColor=JNJ_RED,
            spaceBefore=18, spaceAfter=6,
            fontName="Helvetica-Bold",
        ),
        "subsection_heading": ParagraphStyle(
            "subsection_heading", parent=base["Heading2"],
            fontSize=11, leading=15, textColor=DARK_NAVY,
            spaceBefore=10, spaceAfter=4,
            fontName="Helvetica-Bold",
        ),
        "body": ParagraphStyle(
            "body", parent=base["Normal"],
            fontSize=10, leading=15, textColor=DARK_NAVY,
            spaceAfter=6, alignment=TA_JUSTIFY,
        ),
        "bullet": ParagraphStyle(
            "bullet", parent=base["Normal"],
            fontSize=10, leading=15, textColor=DARK_NAVY,
            leftIndent=14, firstLineIndent=-10, spaceAfter=4,
        ),
        "label": ParagraphStyle(
            "label", parent=base["Normal"],
            fontSize=9, leading=13, textColor=MID_GRAY,
            fontName="Helvetica-Bold", spaceAfter=1,
        ),
        "value": ParagraphStyle(
            "value", parent=base["Normal"],
            fontSize=10, leading=14, textColor=DARK_NAVY,
            spaceAfter=6,
        ),
        "caution": ParagraphStyle(
            "caution", parent=base["Normal"],
            fontSize=9, leading=13, textColor=ACCENT_DARK,
            leftIndent=10, spaceAfter=4, fontName="Helvetica-Oblique",
        ),
        "ref": ParagraphStyle(
            "ref", parent=base["Normal"],
            fontSize=8, leading=12, textColor=MID_GRAY,
            spaceAfter=3,
        ),
        "footer": ParagraphStyle(
            "footer", parent=base["Normal"],
            fontSize=8, leading=11, textColor=MID_GRAY,
            alignment=TA_CENTER,
        ),
    }


def rule():
    return HRFlowable(width="100%", thickness=0.5, color=RULE_COLOR, spaceAfter=6, spaceBefore=2)


def section(title, s):
    return [rule(), Paragraph(title, s["section_heading"])]


def bullets(items, s):
    return [Paragraph(f"&#8226;&#160; {item}", s["bullet"]) for item in items]


def kv_table(pairs, s):
    rows = [[Paragraph(label, s["label"]), Paragraph(value, s["value"])] for label, value in pairs]
    tbl = Table(rows, colWidths=[1.6 * inch, 4.9 * inch])
    tbl.setStyle(TableStyle([
        ("VALIGN",        (0, 0), (-1, -1), "TOP"),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING",    (0, 0), (-1, -1), 2),
    ]))
    return tbl


def highlight_box(text, s, bg=LIGHT_RED):
    tbl = Table([[Paragraph(text, s["body"])]], colWidths=[6.5 * inch])
    tbl.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, -1), bg),
        ("LEFTPADDING",   (0, 0), (-1, -1), 10),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 10),
        ("TOPPADDING",    (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    return tbl


def build_story(s):
    story = []

    # ── COVER BLOCK ───────────────────────────────────────────────────────────
    story.append(Spacer(1, 0.3 * inch))
    story.append(Paragraph("Partnership Intelligence Profile", s["cover_sub"]))
    story.append(Paragraph("Johnson &amp; Johnson", s["cover_title"]))
    story.append(Paragraph(
        "University of North Carolina at Chapel Hill &mdash; Office of Innovation and Commercialization",
        s["cover_sub"],
    ))
    story.append(Spacer(1, 0.1 * inch))
    story.append(Paragraph(
        "Prepared: May 2026 &#160;&#160;|&#160;&#160; Slug: jnj &#160;&#160;|&#160;&#160; Classification: Internal Use",
        s["cover_meta"],
    ))
    story.append(Spacer(1, 0.25 * inch))
    story.append(rule())

    # ── COMPANY OVERVIEW ──────────────────────────────────────────────────────
    story += section("Company Overview", s)
    story.append(Paragraph(
        "Johnson &amp; Johnson is a large public healthcare company headquartered in New Brunswick, "
        "New Jersey, with operations organized around Innovative Medicine and MedTech following the "
        "separation of Kenvue. The company develops and commercializes medicines and medical "
        "technologies and publicly frames itself around healthcare innovation across prevention, "
        "treatment, and procedural care.",
        s["body"],
    ))
    story.append(Paragraph(
        "Johnson &amp; Johnson is relevant for partnership discussions because its documented "
        "priorities span therapeutic development, clinical trials, surgery and interventional care, "
        "data-enabled healthcare operations, and applied AI use cases that align with UNC capabilities "
        "in translational medicine, biomedical informatics, clinical research, implementation science, "
        "and medical-device-related evaluation.",
        s["body"],
    ))
    story.append(Paragraph(
        "<i>Sources: Johnson &amp; Johnson Q4 and Full-Year 2025 results [1]; Johnson &amp; Johnson "
        "policies and reports [2]; Johnson &amp; Johnson AI in healthcare page [3].</i>",
        s["caution"],
    ))

    # ── BASIC COMPANY INFORMATION ─────────────────────────────────────────────
    story += section("Basic Company Information", s)
    story.append(kv_table([
        ("Full Name",           "Johnson & Johnson"),
        ("Headquarters",        "New Brunswick, New Jersey, United States"),
        ("Website",             "https://www.jnj.com"),
        ("Investor Relations",  "https://www.investor.jnj.com"),
        ("Company Type",        "Public Company"),
        ("Ticker",              "JNJ (NYSE)"),
        ("Industry",            "Healthcare / Innovative Medicine / MedTech"),
        ("Scale",               "Large Enterprise"),
    ], s))
    story.append(Paragraph(
        "<i>Sources: Johnson &amp; Johnson Q4 and Full-Year 2025 results [1]; Johnson &amp; Johnson "
        "investor relations pages [4]; Johnson &amp; Johnson policies and reports [2].</i>",
        s["caution"],
    ))

    # ── BUSINESS SIGNALS: Q4 AND FULL-YEAR 2025 ───────────────────────────────
    story += section("Business Signals: Fourth Quarter and Full-Year 2025", s)

    story.append(Paragraph("Fourth Quarter 2025", s["subsection_heading"]))
    story.append(KeepTogether([
        highlight_box(
            "<b>Q4 2025 Key Metrics:</b> Sales $24.6B (+9.1% reported, +6.7% operational) &nbsp;|&nbsp; "
            "Net earnings $4.4B &nbsp;|&nbsp; Adjusted operational sales growth of 6.2% excluding "
            "COVID-19 Vaccine &nbsp;|&nbsp; MedTech operational sales growth of 8.2% worldwide.",
            s,
        )
    ]))
    story.append(Spacer(1, 6))

    story.append(Paragraph("Full Year 2025", s["subsection_heading"]))
    story.append(KeepTogether([
        highlight_box(
            "<b>FY 2025 Key Metrics:</b> Sales $94.2B (+6.0% reported, +4.3% operational) &nbsp;|&nbsp; "
            "2026 sales guidance midpoint $100.5B &nbsp;|&nbsp; Multiple innovation milestones across "
            "Innovative Medicine and MedTech including approvals, pipeline advancement, acquisition "
            "activity, and submission of the OTTAVA robotic surgical system.",
            s,
        )
    ]))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "These results support a profile centered on diversified healthcare scale, sustained commercial "
        "performance, and continued investment capacity across therapeutic and device-oriented "
        "innovation areas.",
        s["body"],
    ))
    story.append(Paragraph(
        "<i>Sources: Johnson &amp; Johnson Q4 and Full-Year 2025 results [1]; Johnson &amp; Johnson "
        "Fourth Quarter 2025 Earnings Presentation [5]; Johnson &amp; Johnson 2025 Full-Year "
        "Earnings Infographic [6].</i>",
        s["caution"],
    ))

    # ── PLATFORM STRUCTURE ────────────────────────────────────────────────────
    story += section("Platform Structure", s)
    story.append(Paragraph(
        "Johnson &amp; Johnson's current operating structure is centered on two business segments: "
        "Innovative Medicine and MedTech. This segment framing is used consistently across the "
        "company's investor-facing reporting materials and policy/reporting hub.",
        s["body"],
    ))

    story.append(Paragraph("Core Platform Layers", s["subsection_heading"]))
    story += bullets([
        "<b>Innovative Medicine:</b> pharmaceutical products, therapeutic pipeline programs, and "
        "related clinical development activities.",
        "<b>MedTech:</b> medical technologies and device-based offerings supporting surgical, "
        "interventional, and procedural care environments.",
        "<b>Enterprise enablement capabilities:</b> clinical development infrastructure, data and AI "
        "applications, supply-chain operations, and healthcare-provider engagement systems.",
    ], s)
    story.append(Paragraph(
        "<i>Sources: Johnson &amp; Johnson Q4 and Full-Year 2025 results [1]; Johnson &amp; Johnson "
        "Fourth Quarter 2025 Earnings Presentation [5]; Johnson &amp; Johnson policies and reports [2].</i>",
        s["caution"],
    ))

    # ── STRATEGIC THEMES ──────────────────────────────────────────────────────
    story += section("Strategic Themes", s)
    story += bullets([
        "Diversified healthcare model spanning Innovative Medicine and MedTech.",
        "Continued innovation through therapeutic approvals, acquisitions, and MedTech submissions "
        "including the OTTAVA robotic surgical system.",
        "Large-scale clinical, commercial, and global operating footprint with 2026 sales guidance "
        "midpoint of $100.5B.",
        "Applied AI and advanced analytics embedded in healthcare research and operational workflows.",
        "Relevance to clinical, translational, device, and health-system-facing collaboration rather "
        "than consumer-platform engagement.",
    ], s)
    story.append(Paragraph(
        "<i>Sources: Johnson &amp; Johnson Q4 and Full-Year 2025 results [1]; Johnson &amp; Johnson "
        "Fourth Quarter 2025 Earnings Presentation [5]; Johnson &amp; Johnson AI in healthcare page [3].</i>",
        s["caution"],
    ))

    # ── AI AND TECHNOLOGY SIGNALS ─────────────────────────────────────────────
    story += section("AI and Technology Signals", s)
    story.append(Paragraph(
        "Johnson &amp; Johnson publicly states that it is using AI and machine learning in areas "
        "such as clinical trial site identification, trial diversity efforts, anatomy-informed "
        "procedural planning, surgical support, and supply-chain risk prediction. The company's "
        "public materials support framing its AI posture as applied and healthcare-specific, with "
        "emphasis on research, development, clinical operations, and MedTech workflows rather than "
        "unsupported claims about general-purpose frontier model leadership.",
        s["body"],
    ))
    story.append(KeepTogether([
        highlight_box(
            "<b>Caution:</b> The strongest verified AI claims are the official company statements "
            "describing specific use cases and should be kept separate from speculative claims about "
            "proprietary capabilities not documented in the cited materials.",
            s,
        )
    ]))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "<i>Sources: Johnson &amp; Johnson AI in healthcare page [3]; Johnson &amp; Johnson policies "
        "and reports [2]; Johnson &amp; Johnson investor relations materials [4].</i>",
        s["caution"],
    ))

    # ── UNC ALIGNMENT ─────────────────────────────────────────────────────────
    story += section("Alignment with UNC Research", s)
    story.append(Paragraph(
        "No direct named UNC&ndash;Johnson &amp; Johnson partnership has been identified from the "
        "current source set. The following represents strategic alignment based on documented "
        "Johnson &amp; Johnson capabilities and UNC research strengths. A second research pass "
        "targeting named UNC personnel, centers, sponsored research activity, licensing records, "
        "alumni links, and institutional agreements is recommended before making partnership claims.",
        s["body"],
    ))

    story.append(Paragraph("Strategic Fit Areas", s["subsection_heading"]))
    story += bullets([
        "<b>Translational medicine and clinical research:</b> Johnson &amp; Johnson's documented "
        "scale in therapeutic development and trial activity aligns with UNC strengths in "
        "translational and clinical research environments.",
        "<b>Biomedical informatics and health data science:</b> the company's use of AI and "
        "analytics in trials and operations aligns with UNC capabilities in informatics, analytics, "
        "and health data interpretation.",
        "<b>Medical devices and procedural innovation:</b> Johnson &amp; Johnson's MedTech "
        "portfolio creates plausible fit with UNC surgical, intervention-oriented, and "
        "device-evaluation ecosystems.",
        "<b>Public health and implementation science:</b> AI-supported site selection and trial "
        "representation themes fit UNC strengths in population health, implementation research, "
        "and equitable study design.",
        "<b>Drug development support and computational bioscience:</b> applied AI and Innovative "
        "Medicine priorities create potential alignment with UNC translational bioscience and "
        "data-driven therapeutic research support capabilities.",
    ], s)

    story.append(Paragraph("Recommended Enrichment Targets for Follow-Up Research", s["subsection_heading"]))
    story += bullets([
        "UNC School of Medicine clinical and translational research programs",
        "UNC Eshelman School of Pharmacy drug development and translational science groups",
        "UNC biomedical informatics and health data science programs",
        "UNC Gillings School of Global Public Health analytics and implementation science groups",
        "UNC surgery, interventional, and device-evaluation research programs",
    ], s)
    story.append(Paragraph(
        "<i>Sources: Johnson &amp; Johnson AI in healthcare page [3]; Johnson &amp; Johnson Q4 and "
        "Full-Year 2025 results [1]; Johnson &amp; Johnson policies and reports [2].</i>",
        s["caution"],
    ))

    # ── TALKING POINTS ────────────────────────────────────────────────────────
    story += section("Talking Points", s)

    story.append(Paragraph("Organizational Context", s["subsection_heading"]))
    story += bullets([
        "Johnson &amp; Johnson should be framed as a diversified healthcare company operating across "
        "two major segments, Innovative Medicine and MedTech, rather than as a single-category "
        "life sciences company.",
        "Fourth-quarter and full-year 2025 results support a profile centered on scale, durable "
        "commercialization capacity, and continued innovation investment.",
        "The company's public materials support a partnership narrative grounded in healthcare "
        "delivery, therapeutics, clinical development, and medical technology rather than "
        "consumer digital ecosystems.",
        "Johnson &amp; Johnson's official AI framing is practical and healthcare-specific, "
        "focusing on discovery, trials, surgery, and supply-chain operations.",
        "This mix of pharmaceutical, MedTech, and data-enabled operating capabilities makes the "
        "company relevant to multiple UNC research domains without requiring speculative claims.",
    ], s)

    story.append(Paragraph("Alignment with UNC Research", s["subsection_heading"]))
    story += bullets([
        "UNC can be positioned as a strong academic partner for clinical validation, translational "
        "medicine, health data analysis, and implementation research relevant to Johnson &amp; "
        "Johnson's documented operating priorities.",
        "Johnson &amp; Johnson may be a stronger fit for translational science, clinical studies, "
        "and device-adjacent evaluation than for consumer digital health collaboration.",
        "The strongest defensible outreach angle emphasizes therapeutic pipelines, MedTech "
        "evaluation, clinical trial support, and data-enabled care research &mdash; not consumer "
        "platform or app-layer collaboration.",
    ], s)

    # ── RISK AND CAUTION NOTES ────────────────────────────────────────────────
    story += section("Risk and Caution Notes", s)
    story += bullets([
        "Do not imply a formal UNC&ndash;Johnson &amp; Johnson partnership without evidence from "
        "a dedicated follow-up research pass.",
        "Do not overstate Johnson &amp; Johnson's AI capabilities beyond the specific use cases "
        "documented in public materials.",
        "Do not frame this as a consumer digital health or platform partnership; the strongest "
        "facts support clinical, translational, and device-oriented positioning.",
        "Keep AI discussion tied to Johnson &amp; Johnson's published use cases in trials, "
        "surgery, and supply-chain operations rather than speculative frontier model claims.",
        "This profile is designed to reduce hallucination risk in downstream report generation; "
        "maintain source discipline in all derivative documents.",
    ], s)

    # ── EXPECTED REPORT ANGLE ─────────────────────────────────────────────────
    story += section("Expected Report Angle and Positioning", s)
    story.append(highlight_box(
        "<b>Positioning Summary:</b> Johnson &amp; Johnson should be framed as (1) a diversified "
        "healthcare company with significant scale across both pharmaceutical and medical technology "
        "segments; (2) a strong candidate for clinical research, translational science, MedTech "
        "evaluation, and health data science collaboration; (3) a meaningful fit for UNC capabilities "
        "in biomedical informatics, implementation science, translational medicine, and "
        "device-adjacent research; and (4) a different type of partner than Apple or Google &mdash; "
        "with stronger relevance to therapeutic pipelines, clinical trials, and procedural care "
        "innovation than to consumer platforms or general-purpose AI infrastructure.",
        s,
    ))

    # ── REFERENCES ────────────────────────────────────────────────────────────
    story += section("References", s)
    refs = [
        ("[1]", "Johnson & Johnson Q4 and Full-Year 2025 results",
                "https://www.investor.jnj.com/investor-news/news-details/2026/Johnson--Johnson-reports-Q4-and-Full-Year-2025-results/default.aspx"),
        ("[2]", "Johnson & Johnson policies and reports",
                "https://www.jnj.com/policies-reports"),
        ("[3]", "Johnson & Johnson AI in healthcare",
                "https://www.jnj.com/innovation/artificial-intelligence-in-healthcare"),
        ("[4]", "Johnson & Johnson SEC filings and investor relations",
                "https://www.investor.jnj.com/financials/sec-filings/default.aspx"),
        ("[5]", "Johnson & Johnson Fourth Quarter 2025 Earnings Presentation",
                "https://www.investor.jnj.com/events-and-presentations/presentations/presentation-details/2026/Johnson--Johnson-Fourth-Quarter-2025-Earnings-Presentation/default.aspx"),
        ("[6]", "Johnson & Johnson 2025 Full-Year Earnings Infographic",
                "https://www.investor.jnj.com"),
        ("[7]", "Johnson & Johnson latest news — Q4 and Full-Year 2025 Earnings",
                "https://www.jnj.com/latest-news/2025-fourth-quarter-and-full-year-earnings"),
    ]
    for num, title, url in refs:
        story.append(Paragraph(f"<b>{num}</b> {title} &mdash; {url}", s["ref"]))

    story.append(Spacer(1, 0.3 * inch))
    story.append(rule())
    story.append(Paragraph(
        "Partnership Intelligence Profile &mdash; Johnson &amp; Johnson &mdash; Internal Use Only &mdash; May 2026",
        s["footer"],
    ))

    return story


def main():
    import os
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    s = build_styles()
    doc = SimpleDocTemplate(
        OUTPUT_PATH,
        pagesize=letter,
        leftMargin=0.9 * inch,
        rightMargin=0.9 * inch,
        topMargin=0.85 * inch,
        bottomMargin=0.85 * inch,
        title="Partnership Intelligence Profile — Johnson & Johnson",
        author="UNC Office of Innovation and Commercialization",
        subject="Johnson & Johnson Partnership Intelligence",
    )
    doc.build(build_story(s))
    print(f"PDF written to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
