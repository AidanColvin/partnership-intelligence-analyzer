"""Generate a formatted partnership intelligence PDF for Pfizer."""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, KeepTogether
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY

OUTPUT_PATH = "/Users/aidancolvin/partnership-intelligence-analyzer/data/processed/company-profiles/pfizer/deliverable.pdf"

# ── Color palette ──────────────────────────────────────────────────────────────
PFIZER_BLUE  = colors.HexColor("#0093d0")
DARK_NAVY    = colors.HexColor("#1a1f36")
MID_GRAY     = colors.HexColor("#5f6368")
LIGHT_GRAY   = colors.HexColor("#f2f8fc")
ACCENT_TEAL  = colors.HexColor("#00617f")
RULE_COLOR   = colors.HexColor("#cce4f0")


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
            fontSize=13, leading=17, textColor=PFIZER_BLUE,
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
            fontSize=9, leading=13, textColor=ACCENT_TEAL,
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
    story.append(Paragraph("Pfizer Inc.", s["cover_title"]))
    story.append(Paragraph(
        "University of North Carolina at Chapel Hill &mdash; Office of Innovation and Commercialization",
        s["cover_sub"],
    ))
    story.append(Spacer(1, 0.1 * inch))
    story.append(Paragraph(
        "Prepared: May 2026 &#160;&#160;|&#160;&#160; Slug: pfizer &#160;&#160;|&#160;&#160; Classification: Internal Use",
        s["cover_meta"],
    ))
    story.append(Spacer(1, 0.25 * inch))
    story.append(rule())

    # ── COMPANY OVERVIEW ──────────────────────────────────────────────────────
    story += section("Company Overview", s)
    story.append(Paragraph(
        "Pfizer Inc. is one of the world's largest biopharmaceutical companies, with a business spanning "
        "the discovery, development, manufacturing, and commercialization of medicines and vaccines. Its "
        "current strategic profile shows a company navigating the normalization of COVID-era revenues while "
        "simultaneously investing in oncology, vaccines, metabolic disease, rare disease, and other pipeline "
        "areas intended to drive future growth.",
        s["body"],
    ))
    story.append(Paragraph(
        "Pfizer's 2026 posture is shaped by both financial discipline and scientific ambition. In its "
        "full-year 2025 update, Pfizer stated that its 2026 guidance includes approximately $5 billion in "
        "expected COVID-19 product revenue and approximately $1.5 billion in anticipated year-over-year "
        "revenue decline from products losing exclusivity. At the same time, it emphasized continuing "
        "investment in pipeline advancement and major development milestones &mdash; showing that the "
        "company's future narrative is no longer tied to pandemic concentration but to diversified R&amp;D "
        "productivity and portfolio replacement.",
        s["body"],
    ))
    story.append(Paragraph(
        "This makes Pfizer especially relevant in partnership or research discussions that depend on "
        "translational science, clinical development, and large-scale therapeutic execution.",
        s["body"],
    ))
    story.append(Paragraph(
        "<i>Sources: Pfizer full-year 2025 results and 2026 guidance [web:54]; Pfizer pipeline catalysts page [page:1].</i>",
        s["caution"],
    ))

    # ── BASIC COMPANY INFORMATION ─────────────────────────────────────────────
    story += section("Basic Company Information", s)
    story.append(kv_table([
        ("Full Name",      "Pfizer Inc."),
        ("Ticker",         "PFE (NYSE)"),
        ("Headquarters",   "New York, New York, United States"),
        ("Industry",       "Biopharmaceuticals and Vaccines"),
        ("Business Model", "Research, development, manufacturing, and commercialization of medicines and vaccines"),
        ("R&D Investment", "$10.4 billion internal R&D spend in 2025; ~$8.8 billion in business development "
                           "(Metsera acquisition and 3SBio in-licensing)"),
        ("Key R&D Sites",  "Pearl River, NY (global vaccine R&D); Cambridge, MA (broader R&D network)"),
    ], s))

    # ── FINANCIAL AND OPERATING POSITION ──────────────────────────────────────
    story += section("Financial and Operating Position", s)

    story.append(Paragraph("Full-Year 2025 Results", s["subsection_heading"]))
    story.append(KeepTogether([
        highlight_box(
            "<b>FY 2025 Key Metrics:</b> Revenue $62.6B (&#8722;2% operationally YoY) &nbsp;|&nbsp; "
            "Ex-Paxlovid and Comirnaty revenue +6% operationally &nbsp;|&nbsp; "
            "Adjusted diluted EPS $3.22 &nbsp;|&nbsp; "
            "2026 guidance: $59.5B&#8211;$62.5B revenue, adj. EPS $2.80&#8211;$3.00 &nbsp;|&nbsp; "
            "~20 pivotal trial starts planned for 2026.",
            s,
        )
    ]))
    story.append(Spacer(1, 6))

    story.append(Paragraph("Q1 2026 Results (reported May 5, 2026)", s["subsection_heading"]))
    story.append(KeepTogether([
        highlight_box(
            "<b>Q1 2026 Key Metrics:</b> Revenue $14.451B &nbsp;|&nbsp; "
            "Eliquis +13% YoY to $2.16B &nbsp;|&nbsp; "
            "Padcev +39% to $591M &nbsp;|&nbsp; "
            "Abrysvo +37% to $180M &nbsp;|&nbsp; "
            "Comirnaty &#8722;59% to $232M &nbsp;|&nbsp; "
            "Paxlovid &#8722;62% to $186M &nbsp;|&nbsp; "
            "Recently launched and acquired products +22% operationally &nbsp;|&nbsp; "
            "Full-year 2026 guidance reaffirmed.",
            s,
        )
    ]))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "These figures illustrate the underlying revenue-mix transition. Pandemic-era assets are declining, "
        "while recently launched and acquired products are growing rapidly. Pfizer's message to investors "
        "centers on pipeline-driven replacement of older revenue streams.",
        s["body"],
    ))
    story.append(Paragraph(
        "<i>Sources: Pfizer FY 2025 results [web:54]; Pfizer Q1 2026 results [web:60]; CNBC Q1 2026 "
        "coverage [web:64].</i>",
        s["caution"],
    ))

    # ── PIPELINE AND RESEARCH STRATEGY ───────────────────────────────────────
    story += section("Pipeline and Research Strategy", s)
    story.append(Paragraph(
        "Pfizer's 2026 catalyst slate spans an unusually broad set of anticipated milestones. The company "
        "lists expected regulatory decisions, data readouts, and pivotal study starts across multiple "
        "disease areas, indicating that it is managing a diversified late-stage development portfolio "
        "rather than depending on a narrow set of assets.",
        s["body"],
    ))

    story.append(Paragraph("Disease Areas with 2026 Catalysts", s["subsection_heading"]))
    story += bullets([
        "Hemophilia A/B with inhibitors (HYMPAVZI)",
        "Bladder cancer &mdash; multiple settings (PADCEV)",
        "HER2-positive metastatic breast cancer maintenance (TUKYSA)",
        "Relapsed or refractory multiple myeloma (ELREXFIO)",
        "Lyme disease (vaccine candidate)",
        "Metastatic castration-resistant prostate cancer (mevrometostat)",
        "Non-small cell lung cancer (sigvotatug vedotin)",
        "Metastatic castration-sensitive prostate cancer (TALZENNA + XTANDI)",
        "Obesity and weight management (berobenatide / Metsera ultra-long-acting programs)",
        "Vitiligo (LITFULO)",
        "Migraine (NURTEC pivotal study start)",
        "Pneumococcal infection (PCV25)",
        "Colorectal cancer, endometrial cancer, urothelial cancer (PD-1xVEGF / PF-08634404 from 3SBio)",
    ], s)

    story.append(Paragraph("Key 2026 Pivotal Trial Activity", s["subsection_heading"]))
    story.append(Paragraph(
        "Pfizer plans to initiate approximately 20 pivotal trials in 2026, including ten studies related "
        "to ultra-long-acting obesity programs obtained through the Metsera acquisition and four trials "
        "for PF-08634404, a PD-1/VEGF bispecific in-licensed from 3SBio. This volume of planned clinical "
        "starts signals sustained demand for high-capability trial ecosystems, disease-specific expertise, "
        "biomarker strategy, and development operations.",
        s["body"],
    ))
    story.append(Paragraph(
        "<i>Sources: Pfizer FY 2025 results [web:54]; Pfizer 2026 pipeline catalysts page [page:1].</i>",
        s["caution"],
    ))

    # ── VACCINES, CLINICAL RESEARCH, AND SCIENTIFIC INFRASTRUCTURE ────────────
    story += section("Vaccines, Clinical Research, and Scientific Infrastructure", s)
    story.append(Paragraph(
        "Pfizer continues to maintain a significant public emphasis on vaccines and clinical research. "
        "Its vaccine clinical-trials site states it has active clinical trials for adults and children "
        "across multiple vaccine areas. Pearl River, New York is identified as the primary location for "
        "Pfizer's global vaccine research and development work, and Cambridge, Massachusetts is part of "
        "its broader R&amp;D network.",
        s["body"],
    ))
    story.append(Paragraph(
        "Vaccines require multidisciplinary execution across immunology, infectious disease, maternal and "
        "pediatric health, epidemiology, clinical-trial recruitment, and regulatory science. Pfizer's "
        "continued visibility in vaccine infrastructure suggests a company that benefits from strong "
        "connections to academic medicine, health systems, and research universities with patient-facing "
        "trial capacity and deep disease-area expertise.",
        s["body"],
    ))
    story.append(Paragraph(
        "<i>Sources: Pfizer vaccine clinical trials page [web:59]; Pfizer science page [web:65]; "
        "Pfizer research sites [web:69].</i>",
        s["caution"],
    ))

    # ── OPERATIONAL EFFICIENCY AND TRANSFORMATION ─────────────────────────────
    story += section("Operational Efficiency and Digital Transformation", s)
    story.append(Paragraph(
        "Pfizer's public disclosures show that pipeline growth is being paired with operational redesign. "
        "In an April 2025 SEC filing, Pfizer stated it expected approximately $1.2 billion in additional "
        "anticipated savings from its cost realignment program by end of 2027, largely driven by enhanced "
        "digital enablement, automation, artificial intelligence, and business-process simplification.",
        s["body"],
    ))
    story.append(KeepTogether([
        highlight_box(
            "<b>Cost Realignment Program:</b> ~$4.5B net cost savings target by end of 2025 &nbsp;|&nbsp; "
            "~$5.7B total net cost savings through 2027 &nbsp;|&nbsp; "
            "Additional $1.2B anticipated savings from digital enablement, automation, and AI &nbsp;|&nbsp; "
            "Business-process simplification as a named driver.",
            s,
        )
    ]))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "This positions Pfizer as more than a drug-development company. It is also investing in digital "
        "infrastructure and operating-model simplification. For institutional collaboration, this means "
        "the strongest partnership value may come from combining scientific strength with scalable "
        "execution, health data capabilities, and process-improvement support.",
        s["body"],
    ))
    story.append(Paragraph(
        "<i>Source: Pfizer SEC filing on cost realignment and digital enablement [web:67].</i>",
        s["caution"],
    ))

    # ── ALIGNMENT WITH UNC RESEARCH ───────────────────────────────────────────
    story += section("Alignment with UNC Research", s)
    story.append(Paragraph(
        "No direct named UNC-Pfizer partnership has been identified from the current source set. "
        "The following represents strategic alignment based on Pfizer's documented priorities and "
        "UNC's likely research strengths. A second research pass targeting named UNC personnel and "
        "institutional agreements is recommended before making partnership claims.",
        s["body"],
    ))

    story.append(Paragraph("Three Strategic Framing Pillars", s["subsection_heading"]))
    story += bullets([
        "<b>Translational and clinical development:</b> An academic medical center can support "
        "translational and clinical-development workflows directly relevant to Pfizer's oncology, "
        "vaccine, and immunology pipeline priorities.",
        "<b>Trial ecosystem capacity:</b> Pfizer's approximately 20 planned pivotal trial starts in "
        "2026 signal sustained demand for high-capability trial ecosystems and disease-specific "
        "expertise. UNC's clinical research infrastructure is well positioned here.",
        "<b>Digital enablement and health analytics:</b> Pfizer's emphasis on digital enablement and "
        "process simplification opens the door to collaboration beyond laboratory science, including "
        "clinical operations, implementation science, and health analytics.",
    ], s)

    story.append(Paragraph("Specific UNC Research Fit Areas", s["subsection_heading"]))
    story += bullets([
        "Oncology: UNC Lineberger Comprehensive Cancer Center &mdash; relevance to Pfizer's broad "
        "oncology pipeline across solid tumors and hematology",
        "Vaccines and infectious disease: UNC infectious disease and public health groups aligned with "
        "Pfizer's Lyme disease vaccine, pneumococcal, and broader vaccine programs",
        "Immunology: aligned with Pfizer's hemophilia, myeloma, and autoimmune pipeline areas",
        "Translational medicine: UNC School of Medicine and clinical research programs supporting "
        "biomarker development and early-phase trial infrastructure",
        "Clinical operations and implementation science: relevant to Pfizer's operational efficiency "
        "and digital enablement priorities",
        "Health analytics and real-world evidence: relevant to post-launch evidence generation for "
        "Pfizer's growing portfolio of recently launched and acquired products",
    ], s)

    # ── TALKING POINTS ────────────────────────────────────────────────────────
    story += section("Talking Points", s)

    story.append(Paragraph("Organizational Context", s["subsection_heading"]))
    story += bullets([
        "Pfizer is operating in a transition period where commercial durability and pipeline execution "
        "are both central to performance. Its 2026 guidance reflects lower COVID revenue and "
        "exclusivity-related pressure, but it is simultaneously pointing investors toward a diversified "
        "set of late-stage pipeline and launch drivers.",
        "The company's near-term priorities likely include clinical execution, regulatory readiness, "
        "selective partnership development, and disciplined capital deployment.",
        "Pfizer's $10.4 billion in 2025 R&amp;D investment and $8.8 billion in business development "
        "activity signal a company that is aggressively combining internal discovery with external "
        "sourcing to shape its future pipeline.",
    ], s)

    story.append(Paragraph("Research and Innovation Relevance", s["subsection_heading"]))
    story += bullets([
        "Pfizer's 2026 catalyst slate spans oncology, rare disease, vaccines, migraine, metabolic "
        "disease, immunology, and infectious disease &mdash; a breadth that suggests valuing ecosystems "
        "capable of connecting discovery science, translational validation, biomarker development, "
        "clinical recruitment, and operational execution.",
        "The most compelling partnership fit is likely an institution that can support both scientific "
        "differentiation and efficient patient-facing development work.",
        "Pfizer's planned volume of pivotal trial starts makes trial-site capacity and investigator "
        "expertise a practical, near-term partnership consideration.",
    ], s)

    story.append(Paragraph("Alignment with Academic Health Systems", s["subsection_heading"]))
    story += bullets([
        "Pfizer's vaccine infrastructure, clinical-trial orientation, and distributed research network "
        "make it especially compatible with academic medical centers and major research universities.",
        "Such institutions can be valuable not only as sources of science, but also as sources of "
        "investigators, patients, trial sites, translational data, and real-world evidence capabilities.",
        "Pfizer is particularly relevant for collaborations in oncology, infectious disease, "
        "immunology, translational medicine, and evidence-based care innovation.",
    ], s)

    # ── RISK AND CAUTION NOTES ────────────────────────────────────────────────
    story += section("Risk and Caution Notes", s)
    story += bullets([
        "Do not imply a formal UNC-Pfizer partnership without evidence from a dedicated follow-up "
        "research pass.",
        "Do not overstate pipeline certainty: regulatory decisions and data readouts listed as 2026 "
        "catalysts are anticipated milestones, not guaranteed outcomes.",
        "Revenue figures for specific products (Paxlovid, Comirnaty declines; Padcev, Eliquis growth) "
        "are sourced from Q1 2026 reporting and CNBC coverage &mdash; attribute accordingly.",
        "Cost savings figures are from an April 2025 SEC filing and represent targets, not audited results.",
        "Pfizer is a biopharmaceutical partner, not a technology or cloud partner; do not conflate with "
        "Google/Apple positioning around data infrastructure or AI platforms.",
    ], s)

    # ── EXPECTED REPORT ANGLE ─────────────────────────────────────────────────
    story += section("Expected Report Angle and Positioning", s)
    story.append(highlight_box(
        "<b>Positioning Summary:</b> Pfizer should be framed as (1) a global biopharmaceutical company "
        "in active portfolio transition from pandemic-era concentration to diversified pipeline execution, "
        "(2) a strong candidate for translational science, clinical development, oncology, vaccine, and "
        "immunology collaboration, (3) a meaningful fit for UNC's academic medical center and clinical "
        "research infrastructure, and (4) a different type of partner than Google or Apple &mdash; with "
        "stronger relevance to wet-lab science, clinical trials, translational medicine, and therapeutic "
        "pipeline execution than to digital infrastructure or consumer platform collaboration.",
        s,
    ))

    # ── REFERENCES ────────────────────────────────────────────────────────────
    story += section("References", s)
    refs = [
        ("[web:54]",  "Pfizer reports solid full-year 2025 results and reaffirms 2026 guidance (Yahoo Finance)",
                      "https://finance.yahoo.com/news/pfizer-reports-solid-full-2025-114500250.html"),
        ("[page:1]",  "Pfizer Pipeline | Key Anticipated 2026 Catalysts",
                      "https://www.pfizer.com/pfizer-pipeline-key-anticipated-2026-catalysts"),
        ("[web:60]",  "Pfizer reports strong first-quarter results and reaffirms 2026 guidance (Las Vegas Sun)",
                      "https://lasvegassun.com/news/2026/may/05/pfizer-reports-strong-first-quarter-results-and-re/"),
        ("[web:64]",  "CNBC Q1 2026 Pfizer earnings coverage",
                      "https://www.cnbc.com/2026/05/05/pfizer-pfe-earnings-q1-2026.html"),
        ("[web:65]",  "Pfizer Science page",
                      "https://www.pfizer.com/science"),
        ("[web:59]",  "Pfizer vaccine clinical trials page",
                      "https://www.pfizerclinicaltrials.com/our-research/vaccines"),
        ("[web:69]",  "Pfizer research sites / centers page",
                      "https://www.pfizer.com/science/centers"),
        ("[web:67]",  "Pfizer SEC filing on cost realignment and digital enablement (April 2025)",
                      "https://www.sec.gov/Archives/edgar/data/78003/000007800325000111/pfe-20250429.htm"),
    ]
    for num, title, url in refs:
        story.append(Paragraph(f"<b>{num}</b> {title} &mdash; {url}", s["ref"]))

    story.append(Spacer(1, 0.3 * inch))
    story.append(rule())
    story.append(Paragraph(
        "Partnership Intelligence Profile &mdash; Pfizer Inc. &mdash; Internal Use Only &mdash; May 2026",
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
        title="Partnership Intelligence Profile — Pfizer Inc.",
        author="UNC Office of Innovation and Commercialization",
        subject="Pfizer Partnership Intelligence",
    )
    doc.build(build_story(s))
    print(f"PDF written to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
