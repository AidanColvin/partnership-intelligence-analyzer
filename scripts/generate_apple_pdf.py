"""Generate a formatted partnership intelligence PDF for Apple."""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, KeepTogether
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY

OUTPUT_PATH = "/Users/aidancolvin/partnership-intelligence-analyzer/data/processed/company-profiles/apple/deliverable.pdf"

# ── Color palette ──────────────────────────────────────────────────────────────
APPLE_GRAY   = colors.HexColor("#555555")
DARK_NAVY    = colors.HexColor("#1a1f36")
MID_GRAY     = colors.HexColor("#6e6e73")
LIGHT_GRAY   = colors.HexColor("#f5f5f7")
ACCENT_BLUE  = colors.HexColor("#0071e3")
RULE_COLOR   = colors.HexColor("#d2d2d7")


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
            fontSize=13, leading=17, textColor=ACCENT_BLUE,
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
            fontSize=9, leading=13, textColor=APPLE_GRAY,
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
        ("VALIGN",         (0, 0), (-1, -1), "TOP"),
        ("BOTTOMPADDING",  (0, 0), (-1, -1), 4),
        ("TOPPADDING",     (0, 0), (-1, -1), 2),
    ]))
    return tbl


def highlight_box(text, s, bg=LIGHT_GRAY):
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
    story.append(Paragraph("Apple Inc.", s["cover_title"]))
    story.append(Paragraph(
        "University of North Carolina at Chapel Hill &mdash; Office of Innovation and Commercialization",
        s["cover_sub"],
    ))
    story.append(Spacer(1, 0.1 * inch))
    story.append(Paragraph(
        "Prepared: May 2026 &#160;&#160;|&#160;&#160; Slug: apple &#160;&#160;|&#160;&#160; Classification: Internal Use",
        s["cover_meta"],
    ))
    story.append(Spacer(1, 0.25 * inch))
    story.append(rule())

    # ── COMPANY OVERVIEW ──────────────────────────────────────────────────────
    story += section("Company Overview", s)
    story.append(Paragraph(
        "Apple Inc. is a large public technology company headquartered in Cupertino, California. "
        "The company designs and sells consumer hardware, operating systems, developer platforms, "
        "semiconductors, subscription services, and health-related digital features across a tightly "
        "integrated device ecosystem.",
        s["body"],
    ))
    story.append(Paragraph(
        "Apple is relevant for partnership discussions because it combines platform-scale engineering, "
        "on-device and large-scale machine learning, consumer health surfaces, privacy-centered product "
        "design, and research-enabling frameworks that align with UNC capabilities in biomedical informatics, "
        "digital health, computer science, behavioral measurement, and clinical research infrastructure.",
        s["body"],
    ))
    story.append(Paragraph(
        "<i>Sources: Apple Investor Relations [1]; Apple newsroom Q1 and Q2 2026 releases [2][3]; "
        "Apple Machine Learning Research [4].</i>",
        s["caution"],
    ))

    # ── BASIC COMPANY INFORMATION ─────────────────────────────────────────────
    story += section("Basic Company Information", s)
    story.append(kv_table([
        ("Full Name",         "Apple Inc."),
        ("Headquarters",      "Cupertino, California, United States"),
        ("Website",           "https://www.apple.com"),
        ("Investor Relations","https://investor.apple.com/investor-relations/default.aspx"),
        ("Company Type",      "Public Company"),
        ("Ticker",            "AAPL (Nasdaq)"),
        ("Industry",          "Consumer Technology / Devices / Software / Services / Digital Health"),
        ("Scale",             "Large Enterprise"),
    ], s))

    # ── BUSINESS SIGNALS ──────────────────────────────────────────────────────
    story += section("Business Signals: Fiscal Q1 and Q2 2026", s)

    story.append(Paragraph("Fiscal Q1 2026 (reported January 29, 2026)", s["subsection_heading"]))
    story.append(KeepTogether([
        highlight_box(
            "<b>Q1 2026 Key Metrics:</b> Revenue $143.8B (+16% YoY) &nbsp;|&nbsp; "
            "Diluted EPS $2.84 (+19% YoY) &nbsp;|&nbsp; "
            "Best-ever iPhone quarter &nbsp;|&nbsp; "
            "Services all-time revenue record &nbsp;|&nbsp; "
            "Installed base exceeded 2.5 billion active devices.",
            s,
        )
    ]))
    story.append(Spacer(1, 6))

    story.append(Paragraph("Fiscal Q2 2026 (reported April 30, 2026)", s["subsection_heading"]))
    story.append(KeepTogether([
        highlight_box(
            "<b>Q2 2026 Key Metrics:</b> Revenue $111.2B (+17% YoY) &nbsp;|&nbsp; "
            "Diluted EPS $2.01 (+22% YoY) &nbsp;|&nbsp; "
            "Best March quarter ever &nbsp;|&nbsp; "
            "Double-digit growth across every geographic segment &nbsp;|&nbsp; "
            "Services achieved another all-time record &nbsp;|&nbsp; "
            "Operating cash flow over $28B &nbsp;|&nbsp; "
            "Cash dividend increased to $0.27/share &nbsp;|&nbsp; "
            "Additional $100B share repurchase authorized.",
            s,
        )
    ]))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "These results support a profile centered on platform scale, sustained product demand, "
        "services momentum, and significant financial capacity for continued platform investment.",
        s["body"],
    ))
    story.append(Paragraph(
        "<i>Sources: Apple Q1 2026 newsroom release [3]; Apple Q2 2026 newsroom release [2].</i>",
        s["caution"],
    ))

    # ── SEGMENT / PLATFORM STRUCTURE ──────────────────────────────────────────
    story += section("Platform Structure", s)
    story.append(Paragraph(
        "Apple does not publish a formal segment structure equivalent to Alphabet's reporting segments. "
        "The platform is best framed through the interaction of its core product and ecosystem layers.",
        s["body"],
    ))

    story.append(Paragraph("Core Platform Layers", s["subsection_heading"]))
    story += bullets([
        "Hardware products: iPhone, Mac, iPad, Apple Watch, and other devices",
        "Operating systems and platform ecosystems (iOS, macOS, watchOS, etc.)",
        "Services and subscriptions (App Store, Apple Music, iCloud, Apple TV+, Apple Fitness+, etc.)",
        "Developer-facing software ecosystems",
        "Silicon and performance optimization (Apple Silicon, Neural Engine)",
        "Health-related user experiences and data interfaces",
    ], s)

    story.append(Paragraph("Health-Adjacent Public Platform Surfaces", s["subsection_heading"]))
    story += bullets([
        "Apple in Healthcare",
        "Health on Apple Watch",
        "Health Records on iPhone",
    ], s)
    story.append(Paragraph(
        "<i>Source: Apple Investor Relations site navigation [1].</i>",
        s["caution"],
    ))

    story.append(Paragraph("Research-Enabling Framework: ResearchKit", s["subsection_heading"]))
    story.append(Paragraph(
        "ResearchKit is an open-source software framework released by Apple that enables investigators "
        "to create mobile apps for informed consent, surveys, and active-task data capture using "
        "smartphone-based measurements. Published descriptions support its use in longitudinal medical "
        "research, behavioral measurement, and decentralized study designs.",
        s["body"],
    ))
    story.append(Paragraph(
        "<i>Source: Apple ResearchKit — PMC literature [5].</i>",
        s["caution"],
    ))

    # ── STRATEGIC THEMES ──────────────────────────────────────────────────────
    story += section("Strategic Themes", s)
    story += bullets([
        "Integrated hardware-software-services ecosystem",
        "Consumer-scale platform distribution (2.5B+ active devices)",
        "On-device intelligence and Neural Engine integration",
        "Machine learning research across fundamental and applied domains",
        "Privacy-preserving product design as structural differentiator",
        "Digital health and wearable data surfaces",
        "Mobile and sensor-based research enablement (ResearchKit model)",
        "Semiconductor and performance integration (Apple Silicon)",
        "Services monetization at scale",
        "User-centered, longitudinal data collection potential",
    ], s)
    story.append(Paragraph(
        "<i>Sources: Apple Q1 and Q2 2026 newsroom releases [2][3]; Apple Investor Relations [1]; "
        "Apple ML Research [4]; ResearchKit literature [5].</i>",
        s["caution"],
    ))

    # ── AI / TECHNOLOGY SIGNALS ───────────────────────────────────────────────
    story += section("AI and Technology Signals", s)
    story.append(Paragraph(
        "Apple's machine learning research page states that Apple advances AI and ML through fundamental "
        "research shared via publications and conference engagement. Apple's integrated-device model supports "
        "framing around efficient, productized AI rather than only cloud-native AI.",
        s["body"],
    ))
    story.append(Paragraph("ICLR 2026 Research Contributions (Named Topics)", s["subsection_heading"]))
    story += bullets([
        "Large-scale training for recurrent neural networks",
        "Improved state space models",
        "Unified image understanding and generation",
        "3D scene generation from a single photo",
        "Protein folding",
    ], s)
    story.append(Paragraph(
        "<b>Caution:</b> The strongest verified AI claims are Apple's named ICLR 2026 research topics and "
        "the public statement about advancing AI through fundamental research. Do not overstate proprietary "
        "generative AI product claims unless separately sourced. Frame Apple as strong in ML research, "
        "integrated deployment environments, and productized intelligence.",
        s["caution"],
    ))
    story.append(Paragraph(
        "<i>Source: Apple Machine Learning Research at ICLR 2026 [4].</i>",
        s["caution"],
    ))

    # ── ALIGNMENT WITH UNC RESEARCH ───────────────────────────────────────────
    story += section("Alignment with UNC Research", s)
    story.append(Paragraph(
        "No direct named UNC-Apple partnership has been identified from the current source set. "
        "The following represents strategic alignment based on documented Apple capabilities and UNC "
        "research strengths. A second research pass targeting named UNC personnel and institutional "
        "agreements is recommended before making partnership claims.",
        s["body"],
    ))

    story.append(Paragraph("Strategic Fit Areas", s["subsection_heading"]))
    story += bullets([
        "<b>Biomedical informatics and health data science:</b> UNC biomedical informatics groups align "
        "with Apple's health-data surfaces, especially where device-linked data must be analyzed, "
        "interpreted, and integrated into research or clinical workflows.",
        "<b>Digital health and clinical research:</b> UNC digital health and clinical research groups "
        "are well positioned to evaluate wearable-based monitoring, mobile outcomes capture, and "
        "decentralized study designs that fit Apple's ecosystem model.",
        "<b>Computer science and applied ML:</b> UNC CS and applied AI groups align with Apple's ML "
        "research directions, including efficient training methods, multimodal modeling, and scientific "
        "ML-adjacent work such as protein folding.",
        "<b>Public health, behavior, and implementation research:</b> UNC programs can support questions "
        "of usability, adherence, real-world adoption, and population-level evidence generation for "
        "digital tools deployed through consumer platforms.",
        "<b>Mobile health and sensor-based research:</b> ResearchKit-like frameworks suggest strong fit "
        "with longitudinal studies, behavioral measurement, and decentralized research designs.",
    ], s)

    story.append(Paragraph("Recommended Enrichment Targets for Follow-Up Research", s["subsection_heading"]))
    story += bullets([
        "UNC Biomedical Informatics program",
        "UNC digital health research groups",
        "UNC mobile health and sensor-based health research",
        "UNC Gillings School of Global Public Health &mdash; data analytics groups",
        "UNC clinical research programs using patient-generated or device-derived data",
        "UNC Department of Computer Science and applied machine learning faculty",
        "UNC health behavior and implementation science groups",
    ], s)
    story.append(Paragraph(
        "<i>Sources: Apple health platform [1]; ResearchKit literature [5]; Apple ML Research [4].</i>",
        s["caution"],
    ))

    # ── TALKING POINTS ────────────────────────────────────────────────────────
    story += section("Talking Points", s)

    story.append(Paragraph("Organizational Context", s["subsection_heading"]))
    story += bullets([
        "Apple operates one of the world's largest integrated device ecosystems, with an installed base "
        "of more than 2.5 billion active devices.",
        "Fiscal Q1 and Q2 2026 results show strong revenue growth, record iPhone and Services performance, "
        "and significant operating cash flow, indicating both market scale and financial capacity for "
        "continued platform investment.",
        "Apple's services momentum and platform breadth make it more than a hardware company; it should "
        "be framed as an ecosystem operator with recurring digital engagement surfaces.",
        "Apple's public healthcare navigation and wearable-health positioning suggest that health-related "
        "functionality is a meaningful part of its broader platform story.",
        "Apple's ML research posture indicates continued investment in foundational technical capabilities "
        "deployed through tightly controlled end-user products.",
    ], s)

    story.append(Paragraph("Alignment with UNC Research (Talking Points)", s["subsection_heading"]))
    story += bullets([
        "UNC can be positioned as a strong partner for clinical validation, wearable-based monitoring "
        "research, and digital health implementation in Apple's research-framework ecosystem.",
        "Apple may be a stronger fit for digital health, sensing, mobile measurement, platform usability, "
        "and applied ML collaboration than for wet-lab or therapeutic pipeline collaboration.",
        "The strongest defensible outreach angle emphasizes mobile measurement, decentralized research "
        "design, and health data science &mdash; not biopharma-style clinical pipelines.",
    ], s)

    # ── RISK AND CAUTION NOTES ────────────────────────────────────────────────
    story += section("Risk and Caution Notes", s)
    story += bullets([
        "Do not imply a formal UNC-Apple partnership without evidence from a dedicated follow-up research pass.",
        "Do not overstate Apple's healthcare activities beyond the public platform and framework signals "
        "available in the supplied sources.",
        "Do not turn this into a biopharma-style profile; the strongest facts support platform, device, "
        "research-framework, and ML positioning.",
        "Keep frontier AI discussion tied to Apple's published ML research and conference presence rather "
        "than speculative product claims.",
        "This profile is designed to reduce hallucination risk in downstream report generation; maintain "
        "source discipline in all derivative documents.",
    ], s)

    # ── EXPECTED REPORT ANGLE ─────────────────────────────────────────────────
    story += section("Expected Report Angle and Positioning", s)
    story.append(highlight_box(
        "<b>Positioning Summary:</b> Apple should be framed as (1) a large-scale integrated platform "
        "company, (2) a strong candidate for digital health, wearable, mobile measurement, and "
        "research-enablement collaboration, (3) a meaningful fit for UNC informatics, clinical research, "
        "behavioral measurement, and applied machine learning ecosystems, and (4) a different type of "
        "partner than Pfizer or Sanofi &mdash; with stronger relevance to platform technology, user-facing "
        "health systems, and device-enabled data collection than to therapeutics pipelines.",
        s,
    ))

    # ── REFERENCES ────────────────────────────────────────────────────────────
    story += section("References", s)
    refs = [
        ("[1]", "Apple Investor Relations",
         "https://investor.apple.com/investor-relations/default.aspx"),
        ("[2]", "Apple reports second quarter results (April 30, 2026)",
         "https://www.apple.com/newsroom/2026/04/apple-reports-second-quarter-results/"),
        ("[3]", "Apple reports first quarter results (January 29, 2026)",
         "https://www.apple.com/newsroom/2026/01/apple-reports-first-quarter-results/"),
        ("[4]", "Apple Machine Learning Research at ICLR 2026",
         "https://machinelearning.apple.com/research/iclr-2026"),
        ("[5]", "Apple's ResearchKit: smart data collection for the smartphone era? (PMC)",
         "https://pmc.ncbi.nlm.nih.gov/articles/PMC4535444/"),
    ]
    for num, title, url in refs:
        story.append(Paragraph(f"<b>{num}</b> {title} &mdash; {url}", s["ref"]))

    story.append(Spacer(1, 0.3 * inch))
    story.append(rule())
    story.append(Paragraph(
        "Partnership Intelligence Profile &mdash; Apple Inc. &mdash; Internal Use Only &mdash; May 2026",
        s["footer"],
    ))

    return story


def main():
    s = build_styles()
    doc = SimpleDocTemplate(
        OUTPUT_PATH,
        pagesize=letter,
        leftMargin=0.9 * inch,
        rightMargin=0.9 * inch,
        topMargin=0.85 * inch,
        bottomMargin=0.85 * inch,
        title="Partnership Intelligence Profile — Apple Inc.",
        author="UNC Office of Innovation and Commercialization",
        subject="Apple Partnership Intelligence",
    )
    doc.build(build_story(s))
    print(f"PDF written to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
