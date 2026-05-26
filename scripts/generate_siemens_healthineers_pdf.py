"""Generate a formatted partnership intelligence PDF for Siemens Healthineers AG."""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, KeepTogether
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
import os

OUTPUT_PATH = "/Users/aidancolvin/partnership-intelligence-analyzer/public/reports/siemens-healthineers.pdf"

# ── Color palette ──────────────────────────────────────────────────────────────
SH_TEAL      = colors.HexColor("#009B9E")
DARK_NAVY    = colors.HexColor("#1a1f36")
MID_GRAY     = colors.HexColor("#5f6368")
LIGHT_TEAL   = colors.HexColor("#e6f7f7")
ACCENT_DARK  = colors.HexColor("#006E72")
RULE_COLOR   = colors.HexColor("#99d9da")


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
            fontSize=13, leading=17, textColor=SH_TEAL,
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
    tbl = Table(rows, colWidths=[1.8 * inch, 4.7 * inch])
    tbl.setStyle(TableStyle([
        ("VALIGN",        (0, 0), (-1, -1), "TOP"),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING",    (0, 0), (-1, -1), 2),
    ]))
    return tbl


def highlight_box(text, s, bg=LIGHT_TEAL):
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
    story.append(Paragraph("Siemens Healthineers AG", s["cover_title"]))
    story.append(Paragraph(
        "University of North Carolina at Chapel Hill &mdash; Office of Innovation and Commercialization",
        s["cover_sub"],
    ))
    story.append(Spacer(1, 0.1 * inch))
    story.append(Paragraph(
        "Prepared: May 2026 &#160;&#160;|&#160;&#160; Slug: siemens-healthineers "
        "&#160;&#160;|&#160;&#160; Classification: Internal Use",
        s["cover_meta"],
    ))
    story.append(Spacer(1, 0.25 * inch))
    story.append(rule())

    # ── COMPANY OVERVIEW ──────────────────────────────────────────────────────
    story += section("Company Overview", s)
    story.append(Paragraph(
        "Siemens Healthineers AG is a German-headquartered global medical technology company "
        "active in imaging, diagnostics, cancer care, and minimally invasive therapies, augmented "
        "by digital health and artificial intelligence. Its business spans hardware systems, "
        "laboratory diagnostics, radiation oncology through its Varian subsidiary, digital health "
        "platforms, and a growing portfolio of AI-embedded clinical applications, all organized "
        "around an explicit mission to improve access to care for underserved populations worldwide.",
        s["body"],
    ))
    story.append(Paragraph(
        "The company's 2026 strategic posture is shaped by a November 2025 Capital Markets Day "
        "announcement in which it introduced a new strategy phase — \"Elevating Health Globally\" "
        "— targeting four of the most prevalent non-communicable diseases: stroke, cancer, "
        "cardiovascular diseases, and neurodegenerative diseases. This is a deliberate narrowing "
        "of clinical focus paired with a structural reorganization of reporting segments to align "
        "around Imaging (prevention and detection), Precision Therapy (treatment), and Diagnostics. "
        "The reorganization reflects a company that increasingly sees itself as a full-pathway "
        "partner in disease management, not only a device supplier.",
        s["body"],
    ))
    story.append(Paragraph(
        "Siemens Healthineers is especially relevant for UNC because of its active investment in "
        "North Carolina, its documented Value Partnerships model with U.S. academic health systems, "
        "and its deep alignment with clinical imaging infrastructure, radiation oncology, and health "
        "AI — all areas where UNC Health and the UNC research enterprise have substantial and "
        "growing capabilities.",
        s["body"],
    ))
    story.append(Paragraph(
        "<i>Sources: Siemens Healthineers FY2025 annual press release [1]; Capital Markets Day "
        "\"Elevating Health Globally\" [2]; Siemens Healthineers Company page [3].</i>",
        s["caution"],
    ))

    # ── BASIC COMPANY INFORMATION ─────────────────────────────────────────────
    story += section("Basic Company Information", s)
    story.append(kv_table([
        ("Full Name",           "Siemens Healthineers AG"),
        ("Headquarters",        "Erlangen, Germany"),
        ("Website",             "https://www.siemens-healthineers.com"),
        ("Investor Relations",  "https://www.siemens-healthineers.com/investor-relations"),
        ("Company Type",        "Public (Aktiengesellschaft)"),
        ("Ticker",              "FWB: SHL (DAX component)"),
        ("Industry",            "Medical Technology / Imaging / Diagnostics / Cancer Care / Digital Health"),
        ("Segments",            "Imaging; Precision Therapy; Diagnostics (restructured beginning FY2026)"),
        ("Revenue (FY2025)",    "~EUR 23.4 billion (fiscal year ended September 30, 2025)"),
        ("Employees",           "~74,000 worldwide"),
        ("CEO",                 "Dr. Bernd Montag"),
        ("CFO",                 "Dr. Jochen Schmitz"),
        ("Primary Shareholder", "Siemens AG (majority; deconsolidation announced November 2025)"),
        ("Key U.S. R&D Spend",  "~$900 million annually"),
        ("Key U.S. Facilities", "Malvern, PA (Americas HQ); Palo Alto, CA (Varian); "
                                "Charlotte, NC (Experience Center, under construction)"),
    ], s))
    story.append(Paragraph(
        "<i>Sources: Siemens Healthineers FY2025 annual press release [1]; "
        "Siemens Healthineers U.S. investment press release [4]; Capital Markets Day [2].</i>",
        s["caution"],
    ))

    # ── FINANCIAL POSITION ────────────────────────────────────────────────────
    story += section("Financial and Operating Position", s)

    story.append(Paragraph("Full Fiscal Year 2025 (ended September 30, 2025)", s["subsection_heading"]))
    story.append(KeepTogether([highlight_box(
        "<b>FY2025 Key Metrics:</b> Revenue ~EUR 23.4B (+3.7% comparable YoY) &nbsp;|&nbsp; "
        "Adjusted EBIT margin 17.4% &nbsp;|&nbsp; Adjusted EBIT ~EUR 3.9B &nbsp;|&nbsp; "
        "Free cash flow EUR 2.7B &nbsp;|&nbsp; FY2026 guidance: comparable revenue growth 5-6%, "
        "adjusted basic EPS EUR 2.20-EUR 2.40 &nbsp;|&nbsp; Order backlog EUR 36B at fiscal year end.",
        s,
    )]))
    story.append(Spacer(1, 6))

    story.append(Paragraph("Q1 FY2026 (ended December 31, 2025)", s["subsection_heading"]))
    story.append(KeepTogether([highlight_box(
        "<b>Q1 FY2026 Key Metrics:</b> Adjusted basic EPS EUR 0.49 (approximately flat YoY despite "
        "tariff and currency headwinds) &nbsp;|&nbsp; Imaging and Precision Therapy core delivered "
        "higher profit and profitability &nbsp;|&nbsp; Diagnostics comparable revenue declined 3.1% "
        "due to structural changes in China market &nbsp;|&nbsp; Full-year FY2026 guidance confirmed.",
        s,
    )]))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "These figures reflect a company in a period of managed portfolio transition: strong, "
        "profitable imaging and precision therapy performance offset by near-term pressure in "
        "diagnostics from a changing China market environment. Siemens Healthineers has disclosed "
        "that tariffs will have a pretax impact of up to EUR 300 million in FY2026, a headwind "
        "driving the decision to accelerate domestic U.S. manufacturing.",
        s["body"],
    ))
    story.append(Paragraph(
        "<i>Sources: Siemens Healthineers FY2025 annual press release [1]; "
        "Siemens Healthineers Q1 FY2026 press release [5]; MedTech Dive [6].</i>",
        s["caution"],
    ))

    # ── BUSINESS SEGMENTS ─────────────────────────────────────────────────────
    story += section("Business Segments and Product Platform", s)

    story.append(Paragraph("Imaging (Prevention and Detection)", s["subsection_heading"]))
    story.append(Paragraph(
        "The Imaging segment covers computed tomography (CT), magnetic resonance imaging (MRI), "
        "molecular imaging (PET-CT, PET-MR), X-ray, digital radiography, and multimodality data "
        "integration. Imaging generated approximately EUR 11.8 billion in FY2024 revenue, with "
        "approximately 45% recurring as of 2025. Beginning in FY2026, Imaging is the company's "
        "primary segment for disease prevention and early detection, directly enabling the "
        "four-disease strategic focus.",
        s["body"],
    ))

    story.append(Paragraph("Precision Therapy (Treatment)", s["subsection_heading"]))
    story.append(Paragraph(
        "Precision Therapy is a newly consolidated segment combining Varian (radiation oncology), "
        "Advanced Therapies (image-guided minimally invasive procedures), and Ultrasound. Varian "
        "— acquired by Siemens Healthineers in 2021 — is the world's leading radiation oncology "
        "platform and operates manufacturing from Palo Alto, CA following the relocation of Varian "
        "production back to the U.S. in 2025. Precision Therapy targets high-single-digit revenue "
        "growth annually with margin expansion of approximately 100 basis points per year through FY2030.",
        s["body"],
    ))

    story.append(Paragraph("Diagnostics (Laboratory and Point-of-Care)", s["subsection_heading"]))
    story.append(Paragraph(
        "The Diagnostics segment covers laboratory automation, immunoassay systems, hematology "
        "analyzers, molecular diagnostics, and point-of-care testing, with approximately 90% "
        "recurring revenue as of 2025. The segment is currently undergoing a transition in China "
        "and pursuing its own operational restructuring separate from Imaging and Precision Therapy.",
        s["body"],
    ))

    story.append(Paragraph("Digital and AI Platform", s["subsection_heading"]))
    story.append(Paragraph(
        "<b>teamplay digital health platform:</b> A vendor-, device-, and system-neutral cloud and "
        "edge-computing platform connecting more than 5,000 institutions and 23,000 connected "
        "systems across 60+ countries. The platform hosts AI-Rad Companion applications, clinical "
        "analytics tools, and third-party AI integrations. It supports HIPAA compliance, "
        "ISO 27001 certification, and hybrid deployment models (cloud plus on-edge).",
        s["body"],
    ))
    story.append(Paragraph(
        "<b>AI-Rad Companion:</b> A suite of FDA-cleared AI-powered clinical software assistants "
        "for imaging interpretation. Multiple modules have received FDA 510(k) clearance, covering "
        "chest CT (pulmonary and cardiovascular), brain MR morphometry, prostate MR biopsy support, "
        "and organ contouring for radiation therapy planning (AI-Rad Companion Organs RT). All "
        "applications are DICOM-compliant and vendor-neutral.",
        s["body"],
    ))
    story.append(Paragraph(
        "<b>AI Data Infrastructure:</b> Siemens Healthineers operates an AI data lake containing "
        "more than two billion data points drawn from clinical images, lab results, genomics, and "
        "patient histories sourced from all five continents. Data undergoes anonymization before "
        "use in AI development.",
        s["body"],
    ))
    story.append(Paragraph(
        "<i>Sources: Siemens Healthineers AI page [7]; teamplay platform page [8]; "
        "Capital Markets Day [2]; MedTech Dive [6].</i>",
        s["caution"],
    ))

    # ── STRATEGIC THEMES ──────────────────────────────────────────────────────
    story += section("Strategic Themes", s)
    story += bullets([
        "EUR 23.4 billion in FY2025 revenue across a global portfolio serving 180+ countries with "
        "direct representation in 70+, and a EUR 36 billion order backlog at fiscal year end.",
        "\"Elevating Health Globally\" strategy (November 2025) explicitly focused on four "
        "non-communicable diseases — stroke, cancer, cardiovascular disease, and neurodegenerative "
        "disease — with AI as the primary clinical lever.",
        "Segment reorganization beginning FY2026: Imaging (prevention/detection), Precision Therapy "
        "(treatment, combining Varian, Advanced Therapies, Ultrasound), and Diagnostics operating "
        "independently. FY2027-2030 targets: 6-9% annual revenue growth from Imaging and Precision "
        "Therapy combined; 5-7% group growth; double-digit EPS growth.",
        "Value Partnerships model connecting Siemens Healthineers with more than 200 major customers "
        "globally — a multi-year, multi-million-dollar engagement structure combining equipment, "
        "consulting, research collaboration, and workforce development, expanding into "
        "disease-specific \"Value Programs.\"",
        "$150 million in new U.S. investments (May 2025) including a 60,000 sq ft Siemens "
        "Healthineers Experience Center at The Pearl, Charlotte, NC — part of a $141 million "
        "commitment to Charlotte's research and innovation district.",
        "~$900 million in U.S. R&D spending annually, plus more than $1 billion invested in U.S. "
        "facilities, acquisitions, and strategic partnerships since 2019.",
        "Deconsolidation from Siemens AG announced November 2025; Siemens Healthineers will operate "
        "fully independently as a standalone public company.",
        "Tariff and supply chain risk actively managed: up to EUR 300 million pretax tariff impact "
        "projected for FY2026; partially addressed by domestic U.S. manufacturing relocation for Varian.",
    ], s)
    story.append(Paragraph(
        "<i>Sources: Siemens Healthineers FY2025 annual press release [1]; Capital Markets Day [2]; "
        "U.S. investment press release [4]; Siemens Healthineers Company page [3].</i>",
        s["caution"],
    ))

    # ── AI AND TECHNOLOGY SIGNALS ─────────────────────────────────────────────
    story += section("AI and Technology Signals", s)
    story.append(Paragraph(
        "Siemens Healthineers' AI posture in 2026 is defined by clinical deployment at scale "
        "rather than platform ambition. Its AI development operates through an industrial "
        "\"AI factory\" model: large, diverse, and continuously expanding datasets feeding "
        "proprietary algorithms embedded directly into imaging and therapy hardware and accessible "
        "through the teamplay cloud platform.",
        s["body"],
    ))

    story.append(Paragraph("AI Development Infrastructure", s["subsection_heading"]))
    story.append(Paragraph(
        "Siemens Healthineers' AI data lake holds more than two billion data points aggregated "
        "from public clinical registries, medical associations, and trusted research partners "
        "across all five continents. Data is rigorously anonymized and enriched with clinical "
        "annotations before use. The company describes this as a continuously expanding repository "
        "that enables iterative refinement of AI models as population diversity and clinical scope increase.",
        s["body"],
    ))

    story.append(Paragraph("Named AI Products and Regulatory Status", s["subsection_heading"]))
    story += bullets([
        "<b>AI-Rad Companion Chest CT</b> — FDA 510(k) cleared (2019); automatically identifies "
        "abnormalities in lungs, heart, and aorta; vendor-neutral (validated on GE and Philips "
        "equipment in addition to Siemens hardware).",
        "<b>AI-Rad Companion Brain MR for Morphometry Analysis</b> — FDA cleared; segments "
        "approximately 30 brain regions, measures volumes, and compares to normative reference data "
        "from the Alzheimer's Disease Neuroimaging Initiative (ADNI).",
        "<b>AI-Rad Companion Prostate MR for Biopsy Support</b> — FDA cleared; supports targeted "
        "MRI-ultrasound fusion biopsy.",
        "<b>AI-Rad Companion Organs RT</b> — FDA cleared (2020); automates contouring of organs "
        "at risk for radiation therapy planning using deep-learning algorithms.",
    ], s)

    story.append(Paragraph("Digital Twin and Emerging Modalities", s["subsection_heading"]))
    story.append(Paragraph(
        "Siemens Healthineers is actively developing digital patient twin capabilities — "
        "computational models of individual patient anatomy and physiology intended to support "
        "treatment planning and predictive monitoring. This includes work on modeling internal "
        "organ anatomy and represents an emerging area of investment with direct relevance to "
        "precision oncology and neurodegenerative disease monitoring.",
        s["body"],
    ))
    story.append(KeepTogether([highlight_box(
        "<b>Caution:</b> Frame Siemens Healthineers as a clinical AI company with FDA-cleared "
        "products at scale, not as a foundation model or large language model developer. Its AI "
        "advantage is domain-specific imaging intelligence and a proprietary clinical data lake, "
        "not general-purpose AI infrastructure.",
        s,
    )]))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "<i>Sources: Siemens Healthineers AI page [7]; Siemens Healthineers FY2025 press release [1]; "
        "FDA clearance press releases [9][10][11].</i>",
        s["caution"],
    ))

    # ── PARTNERSHIP INFRASTRUCTURE ────────────────────────────────────────────
    story += section("Health System and Partnership Infrastructure", s)

    story.append(Paragraph("Value Partnerships Model", s["subsection_heading"]))
    story.append(Paragraph(
        "Siemens Healthineers' Value Partnerships are multi-year, multi-dimensional agreements "
        "with health systems that bundle equipment procurement, consulting, clinical operations "
        "improvement, research collaboration, and workforce development. The company currently "
        "holds Value Partnerships with more than 200 major customers globally and is expanding "
        "the model into disease-specific \"Value Programs\" targeting the four priority "
        "non-communicable disease areas.",
        s["body"],
    ))

    story.append(Paragraph("Named U.S. Academic Health System Value Partnerships", s["subsection_heading"]))
    story += bullets([
        "<b>Ohio State University Wexner Medical Center (November 2024):</b> 10-year, $105 million "
        "Value Partnership for translational research in diagnostic and therapeutic imaging, AI and "
        "machine learning in radiology and radiation oncology, and access to care for underserved "
        "patients. Dedicated Siemens Healthineers scientists embedded with Ohio State clinical and "
        "research teams at a new center for imaging excellence.",
        "<b>University of Missouri System and MU Health Care:</b> 10-year, $133 million Value "
        "Partnership including equipment for the NextGen Precision Health Institute, joint research "
        "projects in precision medicine, and curricula co-development in data science, machine "
        "learning, and AI for healthcare.",
        "<b>University Hospitals Cleveland and Case Western Reserve University (May 2024):</b> "
        "10-year strategic alliance building on a 40-year collaboration; focused on oncology, "
        "cardiovascular, neurovascular, Alzheimer's disease, theranostics, and novel MR "
        "technology development.",
        "<b>OU Health and University of Oklahoma Health Sciences:</b> 10-year Value Partnership "
        "including the MAGNETOM Terra 7 Tesla MRI (one of five in the Midwest) and NAEOTOM Alpha "
        "photon-counting CT scanner.",
    ], s)

    story.append(Paragraph("North Carolina Presence", s["subsection_heading"]))
    story += bullets([
        "<b>$141 million commitment to The Pearl, Charlotte, NC</b> — a research and innovation "
        "district. Construction of a 60,000 sq ft Siemens Healthineers Experience Center is "
        "underway as of May 2025. North Carolina Governor Josh Stein cited the investment as "
        "evidence of North Carolina's research and health education leadership.",
        "<b>Atrium Health Value Partnership</b> (Charlotte-based, serving NC, SC, GA, and AL): "
        "a multi-year Value Partnership involving more than $140 million in equipment purchases — "
        "advanced imaging technology, radiation oncology, and precision endovascular robotics — "
        "with a focus on rural and underserved communities in the southeastern U.S.",
    ], s)
    story.append(Paragraph(
        "<i>Sources: Ohio State Value Partnership press release [12]; University Hospitals strategic "
        "alliance press release [13]; U.S. investment press release [4]; Atrium Health Value "
        "Partnership [14]; Capital Markets Day [2].</i>",
        s["caution"],
    ))

    # ── UNC ALIGNMENT ─────────────────────────────────────────────────────────
    story += section("Alignment with UNC Research", s)
    story.append(Paragraph(
        "No direct named UNC-Siemens Healthineers institutional partnership has been identified "
        "from the current source set. The following represents strategic alignment based on "
        "documented Siemens Healthineers capabilities, its active North Carolina footprint, and "
        "UNC's known research and clinical strengths. A dedicated follow-up research pass targeting "
        "named UNC faculty, UNC Health equipment contracts, sponsored research records, and any "
        "existing CHIP or NC TraCS engagements with Siemens is recommended before making "
        "partnership claims.",
        s["body"],
    ))

    story.append(Paragraph("Three Strategic Framing Pillars for UNC", s["subsection_heading"]))
    story += bullets([
        "<b>Clinical imaging infrastructure and AI co-development:</b> Siemens Healthineers' "
        "Value Partnerships model — demonstrated with Ohio State, University Hospitals, and OU "
        "Health — is directly transferable to UNC Health. UNC Health's 17-hospital system, "
        "Epic-integrated infrastructure, and SHIRE AI research environment create a defensible "
        "basis for a Value Partnership combining equipment, AI co-development, and research collaboration.",
        "<b>Oncology and radiation therapy:</b> Varian, a Siemens Healthineers company, is the "
        "world's leading radiation oncology platform. UNC Lineberger Comprehensive Cancer Center "
        "— an NCI-designated center with the ARPA-H EVOLVE trial, decentralized clinical trials, "
        "and 200-plus active trials — is a natural Varian research and clinical deployment site.",
        "<b>Precision medicine and digital health informatics:</b> Siemens Healthineers' AI data "
        "lake, AI-Rad Companion applications, and teamplay digital health platform align with "
        "UNC's CHIP biomedical informatics program, NC TraCS translational science infrastructure, "
        "and SHIRE's multimodal data integration capabilities (imaging, genomics, clinical notes).",
    ], s)

    story.append(Paragraph("Specific UNC Research Fit Areas", s["subsection_heading"]))
    story += bullets([
        "<b>UNC Lineberger Comprehensive Cancer Center:</b> Varian radiation oncology integration, "
        "AI-based treatment planning (AI-Rad Companion Organs RT), and molecular imaging for "
        "PET-guided cancer care trials all align with Lineberger's clinical and research footprint. "
        "The ARPA-H EVOLVE trial's biomarker-adaptive model is particularly compatible with "
        "Siemens' precision oncology positioning.",
        "<b>UNC Health imaging infrastructure:</b> UNC Health operates a statewide system of "
        "17 hospitals and 900-plus clinics. A Value Partnership anchored by AI-enabled imaging "
        "systems (NAEOTOM Alpha photon-counting CT, MAGNETOM MRI systems) would fit within the "
        "same framework Siemens Healthineers has executed with Ohio State and OU Health.",
        "<b>UNC CHIP and SHIRE:</b> The CHIP biomedical informatics program and the SHIRE secure "
        "health informatics environment create a credentialed research infrastructure for "
        "co-developing and validating imaging AI models using UNC Health EHR and imaging data.",
        "<b>NC TraCS and theranostics:</b> University Hospitals' alliance includes a theranostics "
        "focus — combining diagnostics and therapeutics to treat advanced cancers. NC TraCS, as "
        "UNC's NIH-funded CTSA hub, provides the translational and regulatory infrastructure to "
        "support similar theranostics trial development at UNC.",
        "<b>Rural health and access to care:</b> Siemens Healthineers' Atrium Health Value "
        "Partnership focuses explicitly on rural health equity using Siemens imaging and radiation "
        "oncology technology across NC and the Southeast. UNC Health's rural footprint across all "
        "100 NC counties creates a natural complementary geography.",
        "<b>UNC Gillings School and population health informatics:</b> The AI and Public Health "
        "Center (CAIPH) at Gillings aligns with Siemens Healthineers' disease-level population "
        "modeling interests embedded in its AI data lake strategy.",
    ], s)

    story.append(Paragraph("Recommended Enrichment Targets", s["subsection_heading"]))
    story += bullets([
        "UNC Health Department of Radiology and UNC Health Imaging leadership",
        "UNC Lineberger Comprehensive Cancer Center — radiation oncology and molecular imaging programs",
        "UNC CHIP program (biomedical informatics) and SHIRE governance team",
        "NC TraCS clinical research infrastructure team",
        "UNC School of Medicine — clinical informatics and digital health programs",
        "UNC Health Rural Health leadership and UNC Health Southeastern",
    ], s)
    story.append(Paragraph(
        "<i>Sources: Ohio State Value Partnership [12]; University Hospitals alliance [13]; "
        "Capital Markets Day [2]; U.S. investment press release [4].</i>",
        s["caution"],
    ))

    # ── TALKING POINTS ────────────────────────────────────────────────────────
    story += section("Talking Points", s)

    story.append(Paragraph("Organizational Context", s["subsection_heading"]))
    story += bullets([
        "Siemens Healthineers is a EUR 23.4 billion global medical technology company with a "
        "EUR 36 billion order backlog and approximately 74,000 employees — a full-spectrum "
        "MedTech enterprise with a documented track record of multi-year, multi-million-dollar "
        "institutional partnership commitments in U.S. academic health systems.",
        "The company is in a period of strategic consolidation: the \"Elevating Health Globally\" "
        "phase narrows clinical focus to four diseases, restructures segments around Imaging and "
        "Precision Therapy as a synergistic core, and separates Diagnostics for independent optimization.",
        "Siemens Healthineers is simultaneously managing deconsolidation from Siemens AG, "
        "tariff-related cost pressure of up to EUR 300 million in FY2026, and accelerated U.S. "
        "domestic manufacturing — signals of a company actively strengthening its U.S. presence.",
        "The company's $900 million in annual U.S. R&D spending and $141 million committed to "
        "Charlotte's Pearl district represent a level of North Carolina engagement that provides "
        "a direct and credible bridge to UNC outreach.",
    ], s)

    story.append(Paragraph("Research and Innovation Relevance", s["subsection_heading"]))
    story += bullets([
        "Value Partnerships with Ohio State Wexner Medical Center (10-year, $105 million, "
        "November 2024) and University Hospitals Cleveland (10-year, May 2024) demonstrate "
        "the company's current appetite for academic health system investment — embedded research "
        "scientists, joint AI/ML development, clinical imaging excellence centers — all mirroring "
        "what could be structured at UNC.",
        "The AI-Rad Companion suite represents the only FDA-cleared, vendor-neutral imaging AI "
        "platform from a major MedTech company with direct DICOM integration and deployment at "
        "scale across 5,000+ institutions. UNC researchers studying clinical AI validation or "
        "imaging informatics would find this a credible and accessible research substrate.",
        "Siemens Healthineers' four-disease focus — cancer, cardiovascular, stroke, "
        "neurodegenerative — maps directly onto UNC's clinical and translational strengths at "
        "Lineberger (cancer), UNC Hospitals (cardiovascular and neurosciences), and NC TraCS "
        "(clinical trial infrastructure).",
    ], s)

    story.append(Paragraph("Alignment with Academic Health Systems", s["subsection_heading"]))
    story += bullets([
        "Siemens Healthineers' Value Partnerships model is structurally designed for academic "
        "health systems: it is not a one-time equipment sale but an ongoing operating relationship "
        "providing co-funded clinical operations improvement, research collaboration, and "
        "workforce development.",
        "The company's stated intent to expand Value Partnerships into disease-specific "
        "\"Value Programs\" — aligning around the four priority non-communicable diseases — "
        "signals a new phase of engagement in which clinical focus, not just hardware volume, "
        "determines partnership structure.",
        "Siemens Healthineers' North Carolina presence — the Charlotte Experience Center, the "
        "Atrium Health partnership, and the Governor's cited recognition of the investment — "
        "means the company already understands and has made commitments to the North Carolina "
        "healthcare market.",
    ], s)

    # ── RISK AND CAUTION NOTES ────────────────────────────────────────────────
    story += section("Risk and Caution Notes", s)
    story += bullets([
        "Do not imply a formal UNC-Siemens Healthineers partnership without evidence from a "
        "dedicated follow-up research pass targeting named agreements, equipment contracts, or "
        "existing CHIP/NC TraCS engagements.",
        "Siemens Healthineers' fiscal year ends September 30. FY2025 figures cover October 1, "
        "2024 through September 30, 2025. Financial comparisons to calendar-year companies "
        "(Pfizer, Microsoft) should account for this timing difference.",
        "Revenue is reported in euros. Do not convert to USD without specifying the exchange rate "
        "and date; currency effects are a named management concern in FY2026 guidance.",
        "The deconsolidation from Siemens AG — announced November 2025 — is subject to regulatory "
        "approvals. Until completed, governance and strategic decision-making authority may involve "
        "Siemens AG. Confirm current ownership and governance status before formal outreach.",
        "Do not conflate Siemens Healthineers with Siemens AG or Siemens Corporation; these are "
        "legally distinct entities. The Siemens AG investment in North and South Carolina data "
        "center infrastructure (announced March 2026) is a Siemens Corporation initiative, not a "
        "Siemens Healthineers initiative.",
        "Tariff impact projections (up to EUR 300 million pretax in FY2026) are company guidance, "
        "not audited results.",
        "The AI data lake size (2 billion+ data points) is sourced from the Siemens Healthineers "
        "AI innovation page. This is a marketing claim and has not been independently audited.",
    ], s)

    # ── EXPECTED REPORT ANGLE ─────────────────────────────────────────────────
    story += section("Expected Report Angle and Positioning", s)
    story.append(highlight_box(
        "<b>Positioning Summary:</b> Siemens Healthineers should be framed as (1) the world's "
        "leading dedicated medical technology company by scope, with EUR 23.4 billion in FY2025 "
        "revenue, ~74,000 employees, and operations in 180+ countries, now entering a focused "
        "\"Elevating Health Globally\" phase targeting stroke, cancer, cardiovascular disease, and "
        "neurodegenerative disease using AI as its primary clinical lever; (2) the owner and "
        "operator of the Varian radiation oncology platform — the most advanced and widely "
        "deployed radiation therapy system globally — making it the natural partner for UNC "
        "Lineberger's oncology research and clinical programs; (3) an active investor in North "
        "Carolina, with $141 million committed to The Pearl in Charlotte and an existing Atrium "
        "Health Value Partnership serving the southeastern U.S., providing credible geographic "
        "and institutional common ground for UNC engagement; (4) an established model for deep "
        "academic health system partnership through its Value Partnerships framework — currently "
        "deployed at Ohio State, University Hospitals Cleveland, University of Missouri, and "
        "others — which combines equipment investment, embedded research collaboration, AI "
        "co-development, and workforce development in a model directly applicable to UNC Health; "
        "and (5) a different type of partner than Microsoft or Pfizer — with stronger relevance "
        "to clinical imaging hardware, radiation oncology, laboratory diagnostics, imaging AI "
        "validation, and health system operational consulting than to cloud infrastructure, "
        "enterprise software, or therapeutic pipeline development.",
        s,
    ))

    # ── REFERENCES ────────────────────────────────────────────────────────────
    story += section("References", s)
    refs = [
        ("[1]",  "Siemens Healthineers — Q4 and FY2025 results press release (November 5, 2025)",
                 "https://www.siemens-healthineers.com/press/releases/2025q4"),
        ("[2]",  "Siemens Healthineers — Capital Markets Day \"Elevating Health Globally\" (November 17, 2025)",
                 "https://www.siemens-healthineers.com/press/releases/cmd2025"),
        ("[3]",  "Siemens Healthineers — Company / Our Purpose",
                 "https://www.siemens-healthineers.com/company"),
        ("[4]",  "Siemens Healthineers USA — $150 Million U.S. Investment press release (May 2025)",
                 "https://www.siemens-healthineers.com/en-us/press-room/press-releases/us-investments"),
        ("[5]",  "Siemens Healthineers — Q1 FY2026 results press release (February 5, 2026)",
                 "https://www.siemens-healthineers.com/press/releases/2026q1"),
        ("[6]",  "MedTech Dive — Siemens Healthineers $150M U.S. investment (May 2025)",
                 "https://www.medtechdive.com/news/siemens-healthineers-move-production-us-mexico/748194/"),
        ("[7]",  "Siemens Healthineers — Artificial Intelligence innovations page",
                 "https://www.siemens-healthineers.com/innovations/artificial-intelligence"),
        ("[8]",  "Siemens Healthineers — teamplay digital health platform",
                 "https://www.siemens-healthineers.com/digital-health-solutions/teamplay-digital-health-platform"),
        ("[9]",  "Siemens Healthineers USA — FDA clears AI-Rad Companion Chest CT (September 2019)",
                 "https://www.siemens-healthineers.com/en-us/press-room/press-releases/fdaclearsairadcompanion.html"),
        ("[10]", "Siemens Healthineers USA — FDA clears AI-Rad Companion Brain MR and Prostate MR (2020)",
                 "https://www.siemens-healthineers.com/en-us/press-room/press-releases/fdaclearsairadcompanionbrainmr.html"),
        ("[11]", "Siemens Healthineers USA — FDA clears AI-Rad Companion Organs RT (November 2020)",
                 "https://www.siemens-healthineers.com/en-us/press-room/press-releases/fdaclearsairadcompanionorgansrt.html"),
        ("[12]", "Siemens Healthineers — Ohio State University Wexner Medical Center 10-year Value Partnership (November 2024)",
                 "https://www.siemens-healthineers.com/press/releases/ohio-state"),
        ("[13]", "Siemens Healthineers — University Hospitals 10-year strategic alliance (May 2024)",
                 "https://www.siemens-healthineers.com/en-us/press-room/press-releases/university-hospitals-strategic-agreement"),
        ("[14]", "Business Wire — Siemens Healthineers and Atrium Health multi-year Value Partnership (November 2022)",
                 "https://www.businesswire.com/news/home/20221128005184/en/"),
        ("[15]", "Siemens Healthineers — Varian acquisition completion press release",
                 "https://www.siemens-healthineers.com/press/releases/varian-closing"),
        ("[16]", "AuntMinnie — Siemens Healthineers FY2025 Q4 results coverage (November 2025)",
                 "https://www.auntminnie.com/industry-news/market-analysis/news/15771068/"),
    ]
    for num, title, url in refs:
        story.append(Paragraph(f"<b>{num}</b> {title} &mdash; {url}", s["ref"]))

    story.append(Spacer(1, 0.3 * inch))
    story.append(rule())
    story.append(Paragraph(
        "Partnership Intelligence Profile — Siemens Healthineers AG — Internal Use Only — May 2026",
        s["footer"],
    ))

    return story


def main():
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    s = build_styles()
    doc = SimpleDocTemplate(
        OUTPUT_PATH,
        pagesize=letter,
        leftMargin=0.9 * inch,
        rightMargin=0.9 * inch,
        topMargin=0.85 * inch,
        bottomMargin=0.85 * inch,
        title="Partnership Intelligence Profile — Siemens Healthineers AG",
        author="UNC Office of Innovation and Commercialization",
        subject="Siemens Healthineers AG Partnership Intelligence",
    )
    doc.build(build_story(s))
    print(f"PDF written to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
