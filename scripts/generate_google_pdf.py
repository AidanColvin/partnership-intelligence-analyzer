"""Generate a formatted partnership intelligence PDF for Google."""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, KeepTogether
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY

OUTPUT_PATH = "/Users/aidancolvin/partnership-intelligence-analyzer/data/processed/company-profiles/google/deliverable.pdf"

# ── Color palette ──────────────────────────────────────────────────────────────
GOOGLE_BLUE  = colors.HexColor("#1a73e8")
DARK_NAVY    = colors.HexColor("#1a1f36")
MID_GRAY     = colors.HexColor("#5f6368")
LIGHT_GRAY   = colors.HexColor("#f8f9fa")
ACCENT_GREEN = colors.HexColor("#137333")
RULE_COLOR   = colors.HexColor("#dadce0")


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
            fontSize=13, leading=17, textColor=GOOGLE_BLUE,
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
            fontSize=9, leading=13, textColor=ACCENT_GREEN,
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
    story.append(Paragraph("Google LLC / Alphabet Inc.", s["cover_title"]))
    story.append(Paragraph(
        "University of North Carolina at Chapel Hill &mdash; Office of Innovation and Commercialization",
        s["cover_sub"],
    ))
    story.append(Spacer(1, 0.1 * inch))
    story.append(Paragraph(
        "Prepared: May 2026 &#160;&#160;|&#160;&#160; Slug: google &#160;&#160;|&#160;&#160; Classification: Internal Use",
        s["cover_meta"],
    ))
    story.append(Spacer(1, 0.25 * inch))
    story.append(rule())

    # ── COMPANY OVERVIEW ──────────────────────────────────────────────────────
    story += section("Company Overview", s)
    story.append(Paragraph(
        "Google, through parent company Alphabet, is one of the world's largest technology companies, "
        "with businesses spanning search, digital advertising, cloud infrastructure, enterprise AI, "
        "productivity software, consumer devices, YouTube, Android, and research-driven innovation. "
        "Its 2026 public profile shows a company that is not just defending legacy products, but "
        "successfully monetizing AI across consumer and enterprise surfaces at scale.",
        s["body"],
    ))
    story.append(Paragraph(
        "The company's current position is shaped by two reinforcing dynamics. First, core businesses "
        "such as Search and advertising remain strong despite industry concerns that generative AI could "
        "disrupt search behavior &mdash; Alphabet stated search queries reached an all-time high in "
        "Q1 2026, and search revenue grew 19 percent year over year. Second, Google Cloud is becoming "
        "a major AI commercialization engine, with Q1 2026 revenue rising 63 percent year over year to "
        "$20.03 billion and management citing strong growth in enterprise AI solutions and infrastructure. "
        "Together, those facts show a company scaling AI without sacrificing its incumbent revenue base.",
        s["body"],
    ))
    story.append(Paragraph(
        "Google is especially relevant for partnership, talent, and institutional strategy discussions "
        "because it combines massive distribution with strong applied research, productization capability, "
        "and infrastructure depth. It also deepens its healthcare and research positioning through "
        "AI-enabled health tools, clinician education initiatives, and large-scale public health "
        "information distribution, including more than 1 trillion global views of health-related "
        "videos on YouTube.",
        s["body"],
    ))
    story.append(Paragraph(
        "<i>Sources: CNBC Alphabet Q1 2026 earnings coverage [web:70]; Google health AI updates [page:1].</i>",
        s["caution"],
    ))

    # ── BASIC COMPANY INFORMATION ─────────────────────────────────────────────
    story += section("Basic Company Information", s)
    story.append(kv_table([
        ("Full Name",         "Alphabet Inc. (parent) / Google LLC (operating)"),
        ("Headquarters",      "Mountain View, California, United States"),
        ("Website",           "https://www.google.com"),
        ("Investor Relations","https://abc.xyz/investor/"),
        ("SEC Filings",       "https://abc.xyz/investor/sec-filings/"),
        ("Company Type",      "Public Parent / Operating Subsidiary Structure"),
        ("Tickers",           "GOOGL / GOOG (Nasdaq)"),
        ("Industry",          "Internet Services / Digital Advertising / Cloud / Enterprise AI / Consumer Technology"),
        ("Core Business Areas","Google Services, Google Cloud, and other Alphabet research and technology bets"),
        ("Scale",             "Large Enterprise"),
    ], s))
    story.append(Paragraph(
        "Google's public reports portal covers transparency, sustainability, Android security, "
        "copyright removals, encryption, and economic impact &mdash; reflecting the breadth of the "
        "company's operational scope as an infrastructure, policy, and platform company whose decisions "
        "shape information access, research visibility, and enterprise technology adoption at global scale.",
        s["body"],
    ))
    story.append(Paragraph(
        "<i>Sources: Alphabet Investor Relations [web:44]; Alphabet SEC filings [web:82]; "
        "Google reports portal [web:77].</i>",
        s["caution"],
    ))

    # ── Q1 2026 FINANCIAL AND OPERATING POSITION ──────────────────────────────
    story += section("Q1 2026 Financial and Operating Position", s)
    story.append(KeepTogether([
        highlight_box(
            "<b>Q1 2026 Key Metrics:</b> Total revenue +20% YoY (fastest quarterly growth since 2022) &nbsp;|&nbsp; "
            "Net income $62B (+81% YoY) &nbsp;|&nbsp; "
            "Advertising revenue $77.25B &nbsp;|&nbsp; "
            "YouTube advertising revenue $9.88B &nbsp;|&nbsp; "
            "Search revenue +19% YoY &nbsp;|&nbsp; "
            "Search queries at all-time high &nbsp;|&nbsp; "
            "Google Cloud revenue +63% YoY to $20.03B &nbsp;|&nbsp; "
            "Cloud backlog ~$460B &nbsp;|&nbsp; "
            "2026 capex guidance increased to up to $190B.",
            s,
        )
    ]))
    story.append(Spacer(1, 6))

    story.append(Paragraph("Cloud and AI Demand Signals", s["subsection_heading"]))
    story += bullets([
        "Products built on Google's generative AI models grew nearly 800 percent year over year "
        "(TechCrunch, attributing company commentary).",
        "AI token usage through Google's API rose to 16 billion tokens per minute, up from "
        "10 billion in Q4 2025.",
        "New customer acquisition doubled year over year; Google signed multiple billion-dollar-plus deals.",
        "Cloud growth was driven by Gemini Enterprise and broader AI solutions, as well as core "
        "GCP infrastructure demand.",
        "Alphabet increased 2026 capital expenditure expectations to as much as $190 billion and "
        "expects to significantly increase spending again in 2027.",
    ], s)
    story.append(Paragraph(
        "<b>Note on sources:</b> Revenue and net income figures from CNBC Q1 2026 earnings coverage. "
        "Token throughput, customer acquisition, and generative AI product growth from TechCrunch "
        "reporting on Google Cloud Q1 2026. These should be attributed as company commentary and "
        "third-party reporting, not audited disclosures.",
        s["caution"],
    ))
    story.append(Paragraph(
        "<i>Sources: CNBC Alphabet Q1 2026 [web:70]; TechCrunch Google Cloud Q1 2026 [web:83]; "
        "Alphabet Investor FAQ; Alphabet Q1 2026 SEC Exhibit.</i>",
        s["caution"],
    ))

    # ── SEGMENT STRUCTURE ─────────────────────────────────────────────────────
    story += section("Segment Structure", s)

    story.append(Paragraph("Google Services", s["subsection_heading"]))
    story += bullets([
        "Google Search &amp; other (search revenue +19% YoY in Q1 2026; queries at all-time high)",
        "YouTube ads ($9.88B in Q1 2026; 1 trillion+ global health-related video views)",
        "Google subscriptions, platforms, and devices",
        "Android",
        "Chrome",
        "Pixel and other devices",
        "Maps",
        "Photos",
        "Play",
    ], s)

    story.append(Paragraph("Google Cloud", s["subsection_heading"]))
    story += bullets([
        "Google Cloud Platform (GCP) infrastructure services",
        "AI Infrastructure",
        "Vertex AI",
        "Gemini Enterprise",
        "Data and analytics",
        "Cybersecurity",
        "Google Workspace communication and collaboration tools",
        "Other enterprise services",
    ], s)

    story.append(Paragraph("Alphabet-Level Activities", s["subsection_heading"]))
    story += bullets([
        "AI-focused shared R&amp;D activities",
        "Development costs of general AI models",
        "Corporate shared costs and initiatives",
        "Google.org and philanthropic initiatives including AI for Science",
    ], s)
    story.append(Paragraph(
        "Centralized AI model development at the Alphabet level supports describing Google as a "
        "platform company with shared AI investment and distributed commercialization across segments. "
        "Google Cloud includes most of Alphabet's AI services and products, per CNBC's Q1 2026 coverage.",
        s["body"],
    ))
    story.append(Paragraph(
        "<i>Sources: Alphabet Investor FAQ; CNBC Alphabet Q1 2026 [web:70].</i>",
        s["caution"],
    ))

    # ── STRATEGIC THEMES ──────────────────────────────────────────────────────
    story += section("Strategic Themes", s)
    story += bullets([
        "Enterprise AI infrastructure and Vertex AI / Gemini Enterprise commercialization",
        "Cloud platform growth led by enterprise AI solutions at scale",
        "Consumer AI integration sustaining and growing Search and YouTube",
        "Data and analytics at scale across consumer and enterprise surfaces",
        "Developer ecosystem leverage and API-driven AI distribution",
        "Shared AI model R&amp;D at the Alphabet level",
        "Productivity and workflow AI (Google Workspace)",
        "Consumer-to-enterprise platform integration",
        "Cybersecurity and enterprise trust",
        "Infrastructure capacity and large-scale compute (capex up to $190B in 2026)",
        "Health information access and clinician education at global scale",
        "Scientific and research collaboration through Google.org AI for Science",
    ], s)
    story.append(Paragraph(
        "<i>Sources: CNBC Alphabet Q1 2026 [web:70]; TechCrunch Google Cloud [web:83]; "
        "Google health AI updates [page:1]; Google.org AI for Science [web:78].</i>",
        s["caution"],
    ))

    # ── AI, CLOUD, AND RESEARCH STRATEGY ─────────────────────────────────────
    story += section("AI, Cloud, and Research Strategy", s)
    story.append(Paragraph(
        "Google's 2026 operating profile is built around a feedback loop between frontier AI development, "
        "consumer-scale deployment, and enterprise monetization. On the enterprise side, Cloud growth is "
        "driven by Google Cloud Platform, Gemini Enterprise, infrastructure demand, and AI-enabled "
        "customer expansion. On the consumer side, AI enhancements are increasing search usage and helping "
        "drive all-time-high query volume.",
        s["body"],
    ))
    story.append(Paragraph(
        "Very few companies can simultaneously train advanced AI systems, distribute them directly to "
        "billions of users through consumer products, and sell the same core capabilities as enterprise "
        "infrastructure. Google's position in Search, YouTube, Android, Cloud, and Workspace gives it "
        "a multi-surface commercialization model that is difficult for competitors to replicate. It also "
        "means the company's R&amp;D and product decisions have unusually broad downstream implications "
        "for healthcare information, scientific collaboration, knowledge discovery, and enterprise digital "
        "transformation.",
        s["body"],
    ))

    story.append(Paragraph("Google.org AI for Science Initiative", s["subsection_heading"]))
    story.append(Paragraph(
        "Google.org's AI for Science initiative is a $30 million global program intended to accelerate "
        "breakthroughs in health and life sciences as well as climate resilience and environmental "
        "science. It offers funding, technical support, and Google Cloud credits to qualifying "
        "researchers and institutions. This is especially relevant in academic or research partnership "
        "contexts because it shows Google is willing to support external research ecosystems not only "
        "with tools, but also with capital and direct technical collaboration.",
        s["body"],
    ))
    story.append(Paragraph(
        "<i>Sources: CNBC Alphabet Q1 2026 [web:70]; TechCrunch Google Cloud [web:83]; "
        "Google.org AI for Science [web:78].</i>",
        s["caution"],
    ))

    # ── HEALTH, CLINICAL, AND PUBLIC-INFORMATION INFRASTRUCTURE ───────────────
    story += section("Health, Clinical, and Public-Information Infrastructure", s)
    story.append(Paragraph(
        "Google's 2026 health strategy makes the company much more than a generic technology partner. "
        "The following signals come from Google's March 2026 health update (The Check Up) and related "
        "public announcements.",
        s["body"],
    ))

    story.append(Paragraph("Scale of Health Information Reach", s["subsection_heading"]))
    story += bullets([
        "People ask more than <b>1 billion health questions in Google Search every day</b>.",
        "Health-related videos on YouTube have surpassed <b>1 trillion views globally</b>.",
        "These figures underscore Google's role as a primary health information infrastructure "
        "for global populations, independent of any clinical product or partnership.",
    ], s)

    story.append(Paragraph("Clinician Education and Rural Health", s["subsection_heading"]))
    story += bullets([
        "At The Check Up in March 2026, Google announced a <b>$10 million Google.org commitment</b> "
        "to help organizations reimagine clinician education in the AI era.",
        "Google stated it is exploring rural health work with leaders in Arkansas, including the "
        "<b>Alice L. Walton School of Medicine</b> and <b>Heartland Whole Health Institute</b>, as "
        "part of a broader AI effort to improve healthcare accessibility through clinician education, "
        "care delivery, and health research.",
        "These initiatives show Google applying AI and information infrastructure to real-world "
        "healthcare delivery models and regional partnership frameworks, not just consumer products.",
    ], s)

    story.append(Paragraph("Personal Health Tools and Medical Record Integration", s["subsection_heading"]))
    story += bullets([
        "Fitbit's Personal Health Coach is receiving enhanced sleep tracking, CGM (continuous glucose "
        "monitor) connectivity through Health Connect, and the ability to securely link medical records "
        "including lab results and medications for more personalized wellness guidance.",
        "Linked medical-record information is stated to be securely stored, not used for ads, "
        "and remains under user control.",
        "This positions Google as a company attempting to bridge consumer wellness, clinical data "
        "access, education, and AI interpretation within a single integrated ecosystem.",
    ], s)
    story.append(Paragraph(
        "<i>Source: Google health AI updates at The Check Up, March 2026 [page:1]; "
        "Google for Health [web:85].</i>",
        s["caution"],
    ))

    # ── ALIGNMENT WITH UNC RESEARCH ───────────────────────────────────────────
    story += section("Alignment with UNC Research", s)
    story.append(Paragraph(
        "No direct named UNC-Google institutional partnership has been identified from the current "
        "source set. The following represents strategic alignment based on documented Google capabilities "
        "and UNC research strengths. A second research pass targeting named UNC personnel and "
        "institutional agreements is recommended before making partnership claims.",
        s["body"],
    ))

    story.append(Paragraph("Three Strategic Framing Pillars for UNC", s["subsection_heading"]))
    story += bullets([
        "<b>Clinician education and rural health:</b> Google's investments in AI for clinician "
        "education and rural health suggest interest in partners that can combine healthcare delivery, "
        "education, and research at scale. UNC's academic medical center, Gillings School of Public "
        "Health, and regional health programs are well aligned.",
        "<b>Cloud and data science infrastructure:</b> Google Cloud's enterprise AI momentum makes "
        "institutions with strong data science, engineering, and health research capabilities "
        "particularly relevant. RENCI and UNC Research Computing are strong candidates.",
        "<b>Public health information quality:</b> Google's reach through Search and YouTube creates "
        "a natural alignment with research institutions focused on trustworthy communication, "
        "medical evidence translation, and population health impact.",
    ], s)

    story.append(Paragraph("Specific UNC Research Fit Areas", s["subsection_heading"]))
    story += bullets([
        "<b>Biomedical informatics:</b> Cloud-hosted data processing, model development, and secure "
        "analytics architectures relevant to health and research settings",
        "<b>Public health analytics:</b> Alignment with Google's strengths in large, complex, "
        "multi-source dataset processing and population-level health signals",
        "<b>Computer science and applied AI:</b> UNC CS and AI research aligned with Google's "
        "platform, infrastructure, model, and developer-tool capabilities",
        "<b>RENCI and research computing:</b> Natural targets for cloud, data engineering, or "
        "AI-adjacent infrastructure collaboration",
        "<b>Clinical research and implementation science:</b> Relevant to Google's interest in "
        "validating and operationalizing AI tools in real care and learning environments",
        "<b>Health communication and patient education:</b> Relevant to Google's public-health "
        "information mission and YouTube health content quality goals",
    ], s)

    story.append(Paragraph("Recommended Enrichment Targets for Follow-Up Research", s["subsection_heading"]))
    story += bullets([
        "RENCI (Renaissance Computing Institute)",
        "UNC Department of Computer Science",
        "UNC Biomedical Informatics program",
        "UNC Gillings School of Global Public Health &mdash; data analytics and health communication groups",
        "UNC Research Computing and data-intensive science infrastructure teams",
        "UNC health data science groups",
        "UNC School of Medicine &mdash; clinical informatics and digital health programs",
    ], s)

    # ── TALKING POINTS ────────────────────────────────────────────────────────
    story += section("Talking Points", s)

    story.append(Paragraph("Organizational Context", s["subsection_heading"]))
    story += bullets([
        "Google is no longer just a dominant search and advertising company. Its 2026 results show "
        "a business sustaining growth in core advertising while rapidly expanding Cloud and AI-driven "
        "enterprise revenue &mdash; a combination that gives it control over key layers of the AI "
        "stack: user demand, product interfaces, model deployment, cloud infrastructure, and research "
        "partnerships.",
        "Q1 2026 revenue growth of 20 percent YoY was the fastest quarterly rate since 2022, "
        "alongside net income of $62 billion, up 81 percent.",
        "Cloud backlog of approximately $460 billion signals long-duration enterprise commitments "
        "being built around infrastructure and applied AI.",
        "Planned capex of up to $190 billion in 2026 signals both the intensity of the AI race and "
        "Google's willingness to invest aggressively to expand model capacity, data-center "
        "infrastructure, and enterprise service delivery.",
    ], s)

    story.append(Paragraph("Research and Innovation Relevance", s["subsection_heading"]))
    story += bullets([
        "Google Cloud's enterprise AI momentum, combined with Google.org's $30 million AI for "
        "Science initiative, signals that the company sees long-term value in scientific workflows, "
        "technical collaboration, and domain-specific research acceleration.",
        "For academic partners, the strongest fit is likely in areas combining computation, applied "
        "AI, data platforms, and measurable real-world outcomes.",
        "Products built on Google's generative AI models grew nearly 800 percent year over year, "
        "indicating that the ecosystem around Google's AI capabilities is expanding rapidly.",
    ], s)

    story.append(Paragraph("Alignment with Academic Health Systems", s["subsection_heading"]))
    story += bullets([
        "Google's 2026 health agenda is especially compatible with academic medicine: clinician "
        "education, rural health transformation, personal health coaching, medical-record integration, "
        "and health information quality at global scale.",
        "Academic health systems can offer Google what consumer platforms alone cannot: validated "
        "clinical environments, training ecosystems, research oversight, and disease-specific expertise.",
        "Google increasingly values institutional relationships that can test, validate, and "
        "operationalize AI tools in real care and learning environments rather than only in "
        "consumer software contexts.",
        "The company is especially relevant for collaboration in biomedical informatics, patient "
        "education, health AI evaluation, digital health, and evidence-based care delivery.",
    ], s)

    # ── RISK AND CAUTION NOTES ────────────────────────────────────────────────
    story += section("Risk and Caution Notes", s)
    story += bullets([
        "Do not overstate direct healthcare operating or clinical pipeline exposure from Google "
        "without additional sources; Google's health positioning is platform- and information-based, "
        "not therapeutic.",
        "Do not imply existing UNC-Google partnerships without evidence from a dedicated follow-up "
        "research pass.",
        "Keep Gemini Enterprise momentum, token throughput, and generative AI growth figures "
        "attributed to company commentary and third-party reporting (CNBC, TechCrunch) rather "
        "than audited financial disclosures.",
        "Treat investor materials as primary evidence for segment structure, scale, and "
        "strategic direction.",
        "The rural health initiatives (Arkansas, Alice L. Walton School of Medicine) are public "
        "announcements from The Check Up event; confirm status before using in formal outreach.",
        "This profile is designed to reduce hallucination risk in downstream report generation; "
        "maintain source discipline in all derivative documents.",
    ], s)

    # ── EXPECTED REPORT ANGLE ─────────────────────────────────────────────────
    story += section("Expected Report Angle and Positioning", s)
    story.append(highlight_box(
        "<b>Positioning Summary:</b> Google should be framed as (1) a large-scale AI and cloud "
        "platform company sustaining core revenue while rapidly monetizing AI across enterprise "
        "and consumer surfaces, (2) an enterprise infrastructure and analytics partner candidate "
        "with a $460B Cloud backlog and growing Gemini Enterprise demand, (3) a technically "
        "credible fit for UNC computing, informatics, and data-intensive research ecosystems, "
        "(4) an emerging health information and clinician education partner with demonstrated "
        "investment in AI for health and rural care delivery, and (5) a weaker fit for direct "
        "therapeutic or wet-lab collaboration than Pfizer, but potentially stronger for cloud, "
        "data, AI, digital health infrastructure, and public health communication collaboration.",
        s,
    ))

    # ── REFERENCES ────────────────────────────────────────────────────────────
    story += section("References", s)
    refs = [
        ("[web:70]",  "CNBC: Alphabet Q1 2026 earnings coverage",
                      "https://www.cnbc.com/2026/04/29/alphabet-googl-q1-2026-earnings.html"),
        ("[page:1]",  "Google: How Google is using AI to improve health for everyone (The Check Up, March 2026)",
                      "https://blog.google/innovation-and-ai/technology/health/google-check-up-health-ai-updates-2026/"),
        ("[web:44]",  "Alphabet Investor Relations",
                      "https://abc.xyz/investor/"),
        ("[web:82]",  "Alphabet SEC Filings",
                      "https://abc.xyz/investor/sec-filings/"),
        ("[web:77]",  "Google Reports Portal",
                      "https://about.google/company-info/reports/"),
        ("[web:78]",  "Google.org Impact Challenge: AI for Science",
                      "https://google.org/impact-challenges/ai-science"),
        ("[web:83]",  "TechCrunch: Google Cloud surpasses $20B (Q1 2026 growth and AI demand)",
                      "https://techcrunch.com/2026/04/29/google-cloud-surpasses-20b-but-says-growth-was-capacity-constrained/"),
        ("[web:85]",  "Google for Health (1 trillion YouTube health video views)",
                      "https://x.com/GoogleForHealth"),
        ("(prior)",   "Alphabet Investor FAQ",
                      "https://abc.xyz/investor/faqs-and-general-information/"),
        ("(prior)",   "Alphabet Q1 2026 SEC Exhibit 99.1",
                      "https://www.sec.gov/Archives/edgar/data/1652044/000165204426000043/googexhibit991q12026.htm"),
    ]
    for num, title, url in refs:
        story.append(Paragraph(f"<b>{num}</b> {title} &mdash; {url}", s["ref"]))

    story.append(Spacer(1, 0.3 * inch))
    story.append(rule())
    story.append(Paragraph(
        "Partnership Intelligence Profile &mdash; Google LLC / Alphabet Inc. &mdash; Internal Use Only &mdash; May 2026",
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
        title="Partnership Intelligence Profile — Google LLC / Alphabet Inc.",
        author="UNC Office of Innovation and Commercialization",
        subject="Google Partnership Intelligence",
    )
    doc.build(build_story(s))
    print(f"PDF written to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
