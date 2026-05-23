"""Generate a formatted partnership intelligence PDF for Eli Lilly and Company."""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, KeepTogether
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY

OUTPUT_PATH = "/Users/aidancolvin/partnership-intelligence-analyzer/data/processed/company-profiles/eli-lilly/deliverable.pdf"

# ── Color palette ──────────────────────────────────────────────────────────────
LILLY_RED    = colors.HexColor("#C8102E")
DARK_NAVY    = colors.HexColor("#1a1f36")
MID_GRAY     = colors.HexColor("#5f6368")
LIGHT_RED    = colors.HexColor("#fdf2f4")
ACCENT_DARK  = colors.HexColor("#8b0d1f")
RULE_COLOR   = colors.HexColor("#f0c0c8")


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
            fontSize=13, leading=17, textColor=LILLY_RED,
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
    story.append(Paragraph("Eli Lilly and Company", s["cover_title"]))
    story.append(Paragraph(
        "University of North Carolina at Chapel Hill &mdash; Office of Innovation and Commercialization",
        s["cover_sub"],
    ))
    story.append(Spacer(1, 0.1 * inch))
    story.append(Paragraph(
        "Prepared: May 2026 &#160;&#160;|&#160;&#160; Slug: eli-lilly &#160;&#160;|&#160;&#160; Classification: Internal Use",
        s["cover_meta"],
    ))
    story.append(Spacer(1, 0.25 * inch))
    story.append(rule())

    # ── COMPANY OVERVIEW ──────────────────────────────────────────────────────
    story += section("Company Overview", s)
    story.append(Paragraph(
        "Eli Lilly and Company is a large public biopharmaceutical company headquartered in Indianapolis, "
        "Indiana, focused on discovering, developing, manufacturing, and commercializing medicines across "
        "cardiometabolic health, oncology, immunology, and neuroscience.",
        s["body"],
    ))
    story.append(Paragraph(
        "Lilly's current strategic profile is shaped by three reinforcing strengths: first, major "
        "commercial scale in diabetes and obesity medicines; second, a broad clinical pipeline spanning "
        "small molecules, biologics, and select genetic or radioligand-related platforms; and third, "
        "unusually strong capital capacity generated by recent product growth.",
        s["body"],
    ))
    story.append(Paragraph(
        "The company is especially relevant for partnership discussions because it combines large-scale "
        "therapeutic commercialization with sustained investment in translational R&amp;D, clinical "
        "development infrastructure, and disease areas that overlap meaningfully with UNC capabilities "
        "in obesity, diabetes, endocrinology, oncology, neuroscience, biomedical data science, and "
        "clinical research operations.",
        s["body"],
    ))
    story.append(Paragraph(
        "<i>Sources: Lilly 2024 Form 10-K [web:95]; Lilly pipeline site [web:91]; Lilly science site [web:93].</i>",
        s["caution"],
    ))

    # ── BASIC COMPANY INFORMATION ─────────────────────────────────────────────
    story += section("Basic Company Information", s)
    story.append(kv_table([
        ("Full Name",      "Eli Lilly and Company"),
        ("Headquarters",   "Indianapolis, Indiana, United States"),
        ("Website",        "https://www.lilly.com"),
        ("Company Type",   "Public Company"),
        ("Ticker",         "LLY (NYSE)"),
        ("Industry",       "Biopharmaceuticals / Prescription Medicines"),
        ("Scale",          "Large global enterprise with marketed products across multiple therapeutic "
                           "areas and a broad clinical pipeline"),
    ], s))

    story.append(Paragraph("Operating and Financial Position", s["subsection_heading"]))
    story.append(Paragraph(
        "Lilly's 2024 annual filing shows that the company's revenue base is materially driven by "
        "cardiometabolic products, including Mounjaro, Zepbound, and Trulicity, with additional "
        "contributions from oncology, immunology, and neuroscience products.",
        s["body"],
    ))
    story.append(KeepTogether([
        highlight_box(
            "<b>Q1 2026 (earnings-period reporting, not audited):</b> Third-party investor coverage "
            "reported revenue of approximately $19.8 billion and noted continued growth tied to obesity "
            "and diabetes demand. These figures should be treated as current-period reporting rather "
            "than audited year-end disclosure.",
            s,
        )
    ]))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "Lilly's current public profile is best understood as a biopharma company with both blockbuster "
        "commercial execution and an unusually active late-stage and mid-stage pipeline, especially in "
        "obesity, diabetes, and adjacent cardiometabolic disease.",
        s["body"],
    ))
    story.append(Paragraph(
        "<i>Sources: Lilly 2024 Form 10-K [web:95]; Lilly pipeline site [web:91]; annualreports mirror "
        "[web:96]; Q1 2026 earnings coverage [web:98][web:99].</i>",
        s["caution"],
    ))

    # ── PLATFORM AND PORTFOLIO STRUCTURE ──────────────────────────────────────
    story += section("Platform and Portfolio Structure", s)
    story.append(Paragraph(
        "Lilly does not present its business as a technology-style segment structure. Its public "
        "reporting is best understood through therapeutic and product concentration across "
        "cardiometabolic health, oncology, immunology, and neuroscience.",
        s["body"],
    ))

    story.append(Paragraph("Core Portfolio Areas", s["subsection_heading"]))
    story += bullets([
        "<b>Cardiometabolic health:</b> Mounjaro, Zepbound, Trulicity, Jardiance, insulin products, "
        "and related metabolic assets.",
        "<b>Oncology:</b> Verzenio, Cyramza, Erbitux, and pipeline oncology candidates.",
        "<b>Immunology:</b> Taltz, Ebglyss-related activity, Olumiant-related disclosures, and "
        "additional pipeline programs.",
        "<b>Neuroscience:</b> Emgality, neuroscience pipeline programs, and ongoing CNS-focused "
        "development.",
    ], s)
    story.append(Paragraph(
        "This portfolio mix matters because it gives Lilly both near-term commercial strength and "
        "multiple research-facing entry points for academic collaboration, especially where clinical "
        "validation, translational science, biomarkers, or patient populations matter.",
        s["body"],
    ))
    story.append(Paragraph(
        "<i>Sources: Lilly 2024 Form 10-K [web:95]; Lilly pipeline site [web:91]; Lilly science "
        "site [web:93].</i>",
        s["caution"],
    ))

    # ── PIPELINE AND R&D PROFILE ───────────────────────────────────────────────
    story += section("Pipeline and R&D Profile", s)
    story.append(Paragraph(
        "Lilly's public pipeline page states that the company's clinical development portfolio includes "
        "both new molecular entities and new indications or line extensions. The pipeline spans Phase 1, "
        "Phase 2, Phase 3, and regulatory review activity. Lilly explicitly notes that some molecules "
        "are undisclosed for competitive reasons, which is common in large-cap biopharma pipeline "
        "management.",
        s["body"],
    ))
    story.append(Paragraph(
        "Lilly's R&amp;D positioning is not limited to one franchise. Public materials show active "
        "development across obesity, diabetes, oncology, immunology, neuroscience, and additional "
        "therapeutic areas, supporting the view that Lilly remains a diversified innovation-oriented "
        "medicine company rather than a single-franchise obesity story.",
        s["body"],
    ))
    story.append(Paragraph(
        "<i>Sources: Lilly Clinical Development Pipeline [page:2][web:91]; Lilly 2024 Form 10-K [web:95].</i>",
        s["caution"],
    ))

    story.append(Paragraph("Obesity and Cardiometabolic Signals", s["subsection_heading"]))
    story.append(KeepTogether([
        highlight_box(
            "<b>Tirzepatide Platform:</b> Mounjaro (tirzepatide) approved for type 2 diabetes &nbsp;|&nbsp; "
            "Zepbound (tirzepatide) approved for chronic weight management in adults with obesity or "
            "overweight plus at least one weight-related condition (FDA) &nbsp;|&nbsp; "
            "Tirzepatide activates both GLP-1 and GIP receptors &nbsp;|&nbsp; "
            "Retatrutide (next-generation asset) additional late-stage data expected 2025, per CNBC "
            "reporting &nbsp;|&nbsp; "
            "Company is building a broad long-duration metabolic franchise, not a single product story.",
            s,
        )
    ]))
    story.append(Spacer(1, 6))

    story.append(Paragraph("R&D and Development Interpretation", s["subsection_heading"]))
    story.append(Paragraph(
        "Taken together, these sources support framing Lilly as a company with a strong commercial "
        "base, heavy pipeline density, and particular strategic relevance in obesity, diabetes, "
        "cardiometabolic disease, and translational therapeutic development. That profile makes Lilly "
        "potentially relevant to UNC not only as a licensing or sponsored-research prospect, but also "
        "as a clinically oriented partner for biomarker development, trial collaboration, "
        "disease-specific research, and evidence-generation programs.",
        s["body"],
    ))
    story.append(Paragraph(
        "<i>Sources: Lilly 2024 Form 10-K [web:95]; Lilly pipeline site [web:91]; FDA Zepbound approval "
        "[web:104]; CNBC retatrutide reporting [web:102].</i>",
        s["caution"],
    ))

    # ── UNC CONNECTION ────────────────────────────────────────────────────────
    story += section("Alignment with UNC Research", s)
    story.append(Paragraph(
        "No direct named UNC&ndash;Lilly institutional partnership has been identified from the current "
        "source set. This section should be treated as a strategic alignment assessment rather than "
        "evidence of a formal active UNC&ndash;Lilly relationship. A second-pass enrichment workflow "
        "should specifically target named UNC faculty, sponsored research databases, "
        "clinicaltrials.gov investigator sites, alumni networks, licensing records, and jointly "
        "authored publications before any direct partnership claim is made in downstream outreach.",
        s["body"],
    ))

    story.append(Paragraph("Strategic Fit with UNC", s["subsection_heading"]))
    story += bullets([
        "<b>Obesity, diabetes, and metabolism research:</b> Lilly's commercial and pipeline emphasis "
        "in GLP-1/GIP and next-generation obesity therapeutics aligns naturally with UNC clinical, "
        "endocrinology, nutrition, and metabolic disease expertise.",
        "<b>Clinical trials and translational medicine:</b> Lilly's large development footprint "
        "suggests fit with academic medical centers able to support trial execution, biomarker work, "
        "and real-world evidence generation.",
        "<b>Oncology collaboration:</b> Lilly's marketed oncology portfolio and oncology pipeline "
        "create potential relevance for UNC cancer biology, translational oncology, and clinical "
        "oncology programs at UNC Lineberger.",
        "<b>Neuroscience and CNS development:</b> Lilly's neuroscience portfolio and pipeline make "
        "it relevant to academic collaborators working in neurology, psychiatry, and "
        "neurodegenerative disease.",
        "<b>Biomedical informatics and data science:</b> Large-scale clinical development and "
        "outcome tracking can support collaboration opportunities around trial analytics, patient "
        "stratification, and evidence generation.",
    ], s)

    story.append(Paragraph("Recommended Enrichment Targets for Follow-Up Research", s["subsection_heading"]))
    story += bullets([
        "UNC School of Medicine obesity and endocrinology groups",
        "UNC metabolic disease and diabetes investigators",
        "UNC Lineberger Comprehensive Cancer Center",
        "UNC neuroscience and neurodegeneration groups",
        "UNC biomedical informatics and clinical data science teams",
        "UNC clinical trials offices and translational research infrastructure",
    ], s)
    story.append(Paragraph(
        "These are recommended internal targeting categories, not verified existing Lilly relationships.",
        s["caution"],
    ))

    # ── TALKING POINTS ────────────────────────────────────────────────────────
    story += section("Talking Points", s)

    story.append(Paragraph("Organizational Context", s["subsection_heading"]))
    story += bullets([
        "Lilly should be framed as one of the strongest current large-cap biopharma growth stories "
        "because its recent profile combines blockbuster commercial demand, especially in "
        "cardiometabolic medicines, with a still-expanding clinical pipeline.",
        "Its relevance is not limited to market momentum. Public materials show a company with "
        "durable therapeutic depth across obesity, diabetes, oncology, immunology, and neuroscience, "
        "making it more structurally diversified than a single-product narrative would suggest.",
        "Academic institutions generally gain the most from biopharma relationships when the company "
        "has both cash-generating marketed assets and a deep enough pipeline to sustain multi-year "
        "scientific engagement &mdash; Lilly meets both criteria.",
    ], s)

    story.append(Paragraph("Research and Innovation Relevance", s["subsection_heading"]))
    story += bullets([
        "Lilly's pipeline structure and therapeutic spread make it especially relevant to academic "
        "environments that can contribute translational science, disease-area expertise, patient "
        "access, mechanistic biology, biomarker development, and trial execution.",
        "Its strongest externally visible innovation signals are concentrated in obesity and diabetes, "
        "but the company's public materials support a broader framing that includes oncology, "
        "immunology, and neuroscience research opportunity spaces as well.",
        "For UNC, that means the highest-confidence framing is focused collaboration around disease "
        "areas where Lilly already has commercial momentum and clear ongoing development activity, "
        "not a generic innovation partnership pitch.",
    ], s)

    story.append(Paragraph("Alignment with UNC Research (Talking Points)", s["subsection_heading"]))
    story += bullets([
        "<b>Cardiometabolic and translational medicine:</b> Lilly's obesity and diabetes franchise "
        "makes it particularly relevant to UNC programs working on metabolic disease, outcomes "
        "research, implementation science, and patient-centered clinical research.",
        "<b>Oncology and neuroscience:</b> Lilly's marketed assets and ongoing development support "
        "the view that UNC could be relevant as a research, clinical, or biomarker-validation "
        "partner rather than only as a licensing source.",
        "<b>Research operations and data-intensive clinical collaboration:</b> Large biopharma "
        "development increasingly depends on high-quality academic clinical environments, patient "
        "populations, and evidence-generation capabilities &mdash; a natural UNC strength.",
    ], s)

    # ── RISK AND CAUTION NOTES ────────────────────────────────────────────────
    story += section("Risk and Caution Notes", s)
    story += bullets([
        "Do not imply a formal UNC&ndash;Lilly partnership without a dedicated institution-specific "
        "evidence pass targeting named faculty, sponsored research databases, and clinicaltrials.gov "
        "investigator sites.",
        "Do not reduce Lilly to an &ldquo;obesity company.&rdquo; That framing is incomplete and "
        "weakens credibility because Lilly's public reporting and pipeline materials clearly show "
        "broader strength across oncology, immunology, neuroscience, and additional disease areas.",
        "Do not overstate pipeline certainty. Lilly's own pipeline page explicitly states that there "
        "are significant risks and uncertainties in pharmaceutical R&amp;D and that investigational "
        "molecules may be delayed, discontinued, or fail to reach market.",
        "When using quarter-specific 2026 performance numbers, attribute them to earnings-period "
        "reporting and not to audited annual reporting unless directly tied to an SEC filing.",
    ], s)

    # ── EXPECTED REPORT ANGLE ─────────────────────────────────────────────────
    story += section("Expected Report Angle and Positioning", s)
    story.append(highlight_box(
        "<b>Positioning Summary:</b> Eli Lilly should be framed as (1) a large-scale global "
        "biopharmaceutical company with major current strength in cardiometabolic medicines and "
        "meaningful diversification across oncology, immunology, and neuroscience; (2) a "
        "strategically strong fit for UNC in obesity, diabetes, translational medicine, oncology, "
        "neuroscience, and clinical research infrastructure; (3) a more therapeutics- and "
        "pipeline-oriented partner than Apple or Google, with stronger relevance to clinical "
        "development, disease-area science, and drug-development collaboration; and (4) a company "
        "whose strongest outreach angle should emphasize translational science, clinical trials, "
        "biomarker strategy, and disease-specific academic expertise rather than generic "
        "innovation language.",
        s,
    ))

    # ── REFERENCES ────────────────────────────────────────────────────────────
    story += section("References", s)
    refs = [
        ("[web:95]",  "Eli Lilly 2024 Annual Report / Form 10-K (SEC)",
                      "https://www.sec.gov/Archives/edgar/data/59478/000005947825000067/lly-20241231.htm"),
        ("[web:91 / page:2]", "Lilly Clinical Development Pipeline",
                      "https://www.lilly.com/science/research-development/pipeline"),
        ("[web:93]",  "Lilly Science / R&D overview",
                      "https://www.lilly.com/science"),
        ("[web:94]",  "Lilly corporate website",
                      "https://www.lilly.com"),
        ("[web:96]",  "AnnualReports mirror for Eli Lilly filings",
                      "https://www.annualreports.com/Company/eli-lilly-co"),
        ("[web:104]", "FDA approval announcement for Zepbound",
                      "https://www.fda.gov/news-events/press-announcements/fda-approves-new-medication-chronic-weight-management"),
        ("[web:100]", "Additional FDA / clinical reporting on tirzepatide obesity indication",
                      "https://www.tctmd.com/news/fda-grants-tirzepatide-new-indication-obesity-management"),
        ("[web:102]", "CNBC reporting on retatrutide and Lilly obesity pipeline timing",
                      "https://www.cnbc.com/2025/02/06/eli-lilly-to-release-weight-loss-drug-retatrutide-data-in-2025.html"),
        ("[web:98]",  "Q1 2026 earnings-period coverage (YouTube)",
                      "https://www.youtube.com/watch?v=YsFts6q5WQQ"),
        ("[web:99]",  "Earnings transcript coverage (Investing.com)",
                      "https://www.investing.com/news/transcripts/earnings-call-transcript-eli-lilly-beats-expectations-in-q1-2026-93CH-4650548"),
        ("[web:101]", "Investor-material aggregator noting Q1 2026 revenue growth",
                      "https://quartr.com/companies/eli-lilly-and-company_5159"),
    ]
    for num, title, url in refs:
        story.append(Paragraph(f"<b>{num}</b> {title} &mdash; {url}", s["ref"]))

    story.append(Spacer(1, 0.3 * inch))
    story.append(rule())
    story.append(Paragraph(
        "Partnership Intelligence Profile &mdash; Eli Lilly and Company &mdash; Internal Use Only &mdash; May 2026",
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
        title="Partnership Intelligence Profile — Eli Lilly and Company",
        author="UNC Office of Innovation and Commercialization",
        subject="Eli Lilly Partnership Intelligence",
    )
    doc.build(build_story(s))
    print(f"PDF written to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
