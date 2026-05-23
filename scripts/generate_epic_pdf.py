"""Generate a formatted partnership intelligence PDF for Epic Systems Corporation."""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, KeepTogether
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY

OUTPUT_PATH = "/Users/aidancolvin/partnership-intelligence-analyzer/data/processed/company-profiles/epic/deliverable.pdf"

# ── Color palette ──────────────────────────────────────────────────────────────
EPIC_RED     = colors.HexColor("#E31837")
DARK_NAVY    = colors.HexColor("#1a1f36")
MID_GRAY     = colors.HexColor("#5f6368")
LIGHT_RED    = colors.HexColor("#fff5f5")
ACCENT_DARK  = colors.HexColor("#a01020")
RULE_COLOR   = colors.HexColor("#f5c0c8")


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
            fontSize=13, leading=17, textColor=EPIC_RED,
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
    story.append(Paragraph("Epic Systems Corporation", s["cover_title"]))
    story.append(Paragraph(
        "University of North Carolina at Chapel Hill &mdash; Office of Innovation and Commercialization",
        s["cover_sub"],
    ))
    story.append(Spacer(1, 0.1 * inch))
    story.append(Paragraph(
        "Prepared: May 2026 &#160;&#160;|&#160;&#160; Slug: epic &#160;&#160;|&#160;&#160; Classification: Internal Use",
        s["cover_meta"],
    ))
    story.append(Spacer(1, 0.25 * inch))
    story.append(rule())

    # ── COMPANY OVERVIEW ──────────────────────────────────────────────────────
    story += section("Company Overview", s)
    story.append(Paragraph(
        "Epic Systems Corporation is a large private healthcare software company headquartered "
        "in Verona, Wisconsin. Founded in 1979, Epic develops and maintains electronic health "
        "record systems, patient engagement platforms, clinical analytics tools, and a growing "
        "portfolio of AI capabilities for health systems, hospitals, and clinics.",
        s["body"],
    ))
    story.append(Paragraph(
        "Epic is relevant for partnership discussions for a reason no other company in this "
        "profile set shares: UNC Health is an active, long-term Epic customer with a documented "
        "history of co-developing and early-adopting Epic AI features. Beyond the UNC Health "
        "operational relationship, Epic is relevant because its Cosmos research database "
        "&mdash; covering more than 300 million deidentified patient records from 1,760-plus "
        "participating hospitals &mdash; represents one of the largest structured clinical "
        "research datasets in existence, with a documented publication program and an AI "
        "development initiative that creates direct alignment with UNC capabilities in "
        "biomedical informatics, clinical research infrastructure, health data science, "
        "implementation science, and applied machine learning.",
        s["body"],
    ))
    story.append(Paragraph(
        "<i>Sources: Epic Systems corporate site [1]; Becker's Hospital Review [2]; "
        "Epic Cosmos [3].</i>",
        s["caution"],
    ))

    # ── BASIC COMPANY INFORMATION ─────────────────────────────────────────────
    story += section("Basic Company Information", s)
    story.append(kv_table([
        ("Full Name",          "Epic Systems Corporation"),
        ("Headquarters",       "Verona, Wisconsin, United States"),
        ("Website",            "https://www.epic.com"),
        ("Developer Platform", "https://open.epic.com"),
        ("FHIR Resources",     "https://fhir.epic.com"),
        ("Cosmos Research",    "https://cosmos.epic.com"),
        ("Company Type",       "Private Company (no SEC filings)"),
        ("Ticker",             "N/A (privately held)"),
        ("Industry",           "Healthcare Software / Electronic Health Records / Clinical AI"),
        ("Scale",              "Large Enterprise (privately held)"),
        ("Founded",            "1979"),
        ("CEO",                "Judith Faulkner"),
    ], s))
    story.append(Paragraph(
        "<i>Sources: Epic Systems corporate site [1]; Becker's Hospital Review [2].</i>",
        s["caution"],
    ))

    # ── BUSINESS SIGNALS ─────────────────────────────────────────────────────
    story += section("Business Signals: Revenue and Market Position 2024–2026", s)

    story.append(Paragraph("Revenue", s["subsection_heading"]))
    story.append(KeepTogether([highlight_box(
        "<b>Revenue:</b> $5.7B in 2024 (confirmed by company spokesperson to Becker's Hospital "
        "Review), up from $4.9B in 2023 and $1.2B in 2012. Epic is privately held and does not "
        "publish quarterly earnings, investor relations filings, or audited annual financial "
        "statements. All revenue figures should be attributed to company-confirmed disclosures "
        "reported by Becker's Hospital Review.",
        s,
    )]))
    story.append(Spacer(1, 6))

    story.append(Paragraph("Market Position", s["subsection_heading"]))
    story += bullets([
        "43.7% of U.S. acute care EHR market as of year-end 2025, up from 42.3% at year-end 2024 "
        "(KLAS Research, published May 2026).",
        "54.9% of U.S. acute care hospital beds by market share in 2024; Oracle Health 22.1%; "
        "Meditech 12.7%.",
        "Active in 3,620 U.S. hospitals and health systems as of August 2025.",
        "Net gain of 176 acute care multispecialty hospitals in 2024 &mdash; largest single-year "
        "net gain on record. Oracle Health lost a net 74 hospital sites in the same period.",
        "Won nearly 70% of new hospital contracts executed in 2024.",
        "Gained 77 multispecialty hospitals in 2025 despite a 40% industry-wide decline in EHR "
        "purchase decisions.",
        "New customers announced at UGM 2025 include UAB Medicine, Indiana University Health, "
        "Baptist Health South Florida, and MedStar Health.",
    ], s)
    story.append(Paragraph(
        "<i>Sources: Becker's Hospital Review [2]; Fierce Healthcare [5]; Dark Daily [6]; "
        "Sacra [7].</i>",
        s["caution"],
    ))

    # ── PLATFORM STRUCTURE ────────────────────────────────────────────────────
    story += section("Platform Structure", s)
    story.append(Paragraph(
        "Epic operates as a vertically integrated clinical platform. Its core EHR, patient "
        "engagement, analytics, interoperability, and research systems are built on a proprietary "
        "data architecture (Chronicles) and accessed through a common client interface "
        "(Hyperspace). All external integration is conducted through APIs.",
        s["body"],
    ))

    story.append(Paragraph("Core Platform Layers", s["subsection_heading"]))
    story += bullets([
        "<b>Epic EHR (Hyperspace):</b> Clinical documentation, ordering, and workflow system "
        "deployed at 3,620 U.S. hospitals and health systems as of August 2025.",
        "<b>MyChart:</b> Patient-facing portal and mobile application with more than 180 million "
        "active U.S. users. MyChart Central &mdash; a single Epic-issued patient ID connecting "
        "records across provider organizations &mdash; was rolling out as of September 2025.",
        "<b>Cosmos:</b> Deidentified opt-in research database covering more than 300 million "
        "patients globally, 16 billion+ clinical encounters across four countries, from 1,760+ "
        "participating hospitals. Epic's primary platform for population-level research, "
        "comparative effectiveness, and foundation model development.",
        "<b>Caboodle and Clarity:</b> Enterprise data warehouse and reporting database layers "
        "supporting population health analytics, quality reporting, and research. Clarity data "
        "model made available for developer licensing in 2025.",
        "<b>Care Everywhere:</b> Health information exchange network for clinical data sharing "
        "between Epic organizations and external health systems.",
        "<b>Community Connect:</b> Hosted extension model enabling smaller hospitals and "
        "ambulatory practices to run on a host Epic instance. Captured nearly 70% of standalone "
        "hospital EHR decisions in 2024.",
        "<b>Health Grid:</b> Connectivity layer for exchanging data with payers, specialty "
        "diagnostic labs, medical devices, and telehealth companies.",
    ], s)

    story.append(Paragraph("Developer and Interoperability Platform", s["subsection_heading"]))
    story += bullets([
        "<b>open.epic:</b> Public developer platform providing free resources, technical "
        "documentation, API specifications, and sandbox access.",
        "<b>Epic on FHIR (fhir.epic.com):</b> 450-plus FHIR APIs across 55 resources. "
        "Argonaut Project and Da Vinci Project membership. International Patient Summary FHIR "
        "support added May 2025.",
        "<b>Showroom (formerly App Orchard):</b> Curated app marketplace for third-party "
        "developers that have passed Epic's technical, security, and HIPAA compliance review.",
    ], s)
    story.append(Paragraph(
        "<i>Sources: open.epic [8]; Epic FHIR documentation [9]; Fierce Healthcare [10]; "
        "Epic Cosmos [3]; Epic UGM 2025 coverage [11].</i>",
        s["caution"],
    ))

    # ── STRATEGIC THEMES ──────────────────────────────────────────────────────
    story += section("Strategic Themes", s)
    story += bullets([
        "Dominant and expanding EHR market position: 43.7% of U.S. acute care hospitals and "
        "approximately 55% of U.S. acute care hospital beds as of year-end 2025.",
        "Revenue growth from $4.9B in 2023 to $5.7B in 2024 confirming sustained demand.",
        "Cosmos as a research and AI asset: 300 million deidentified patient records from "
        "1,760+ hospitals, active academic publication program, new AI model development "
        "initiative announced at UGM 2025.",
        "Broad AI development across 160&ndash;200 features spanning clinical documentation, "
        "revenue cycle, patient engagement, diagnostic support, and disease monitoring.",
        "450-plus FHIR APIs, SMART on FHIR, Care Everywhere, Argonaut and Da Vinci Project "
        "membership, and International Patient Summary support.",
        "Active partnership with Microsoft and Nuance for ambient clinical documentation AI "
        "embedded in Epic, with UNC Health among early deployment sites.",
        "ERP expansion: Epic is developing an enterprise resource planning suite to extend its "
        "footprint from clinical into operational and financial systems.",
    ], s)
    story.append(Paragraph(
        "<i>Sources: Becker's Hospital Review [2]; KLAS Research via Fierce Healthcare [5]; "
        "Epic Cosmos [3]; CNBC [13]; Fierce Healthcare [14].</i>",
        s["caution"],
    ))

    # ── AI AND TECHNOLOGY SIGNALS ─────────────────────────────────────────────
    story += section("AI and Technology Signals", s)
    story.append(Paragraph(
        "Epic's AI posture as of August 2025 is defined by scale of proprietary data assets, "
        "broad integration across existing workflows, and a deliberate shift from third-party "
        "model reliance toward internally trained foundation models. At UGM 2025, CEO Judith "
        "Faulkner stated: &ldquo;We&rsquo;ve got somewhere between 160 and 200 AI projects "
        "going. Some of them are completed and some are in process.&rdquo;",
        s["body"],
    ))

    story.append(Paragraph("Cosmos AI and CoMET", s["subsection_heading"]))
    story.append(Paragraph(
        "Epic announced proprietary foundation models called Cosmos AI at UGM 2025, trained "
        "on the Cosmos deidentified patient dataset, and launched the Cosmos AI Lab to allow "
        "researchers and data scientists to explore the models.",
        s["body"],
    ))
    story.append(KeepTogether([highlight_box(
        "<b>CoMET (Generative Medical Event Models):</b> A model that &mdash; analogously to "
        "how large language models predict the next token &mdash; predicts the next medical "
        "event in a patient's trajectory, such as readmission risk, future diagnoses, or "
        "clinical deterioration. Executives stated the models improve in predictive accuracy "
        "as the Cosmos dataset grows. Epic is evaluating use cases including proactive risk "
        "identification and real-world evidence generation for clinical decision support.",
        s,
    )]))
    story.append(Spacer(1, 6))

    story.append(Paragraph("Named AI Features and Agents (UGM 2025)", s["subsection_heading"]))
    story += bullets([
        "<b>Art for Clinicians:</b> An ambient AI clinical assistant supporting documentation "
        "and clinical workflow.",
        "<b>Emmie:</b> An AI-powered patient-facing chatbot for engagement, scheduling, and "
        "care navigation.",
        "<b>Penny:</b> An AI revenue management assistant for revenue cycle automation.",
        "<b>Ambient AI Charting:</b> Integrated with Microsoft Nuance Dragon Ambient eXperience "
        "(DAX) for ambient clinical documentation. UNC Health is among the health systems "
        "deploying this capability at scale.",
        "<b>Diagnostic Adviser:</b> A Cosmos-driven point-of-care tool that alerts clinicians "
        "when an alternative diagnosis may better fit a patient's data pattern. Epic cited that "
        "10&ndash;20% of diagnoses may be incorrect, motivating the tool.",
        "<b>Disease Outbreak Prediction:</b> A Cosmos-based population health tool using AI "
        "to predict and monitor disease outbreaks.",
        "<b>AI Charting / Generative AI Patient Message Response:</b> Generative AI for "
        "auto-drafting clinician responses to patient messages. UNC Health was one of the "
        "first health systems to adopt the feature in 2023.",
    ], s)
    story.append(KeepTogether([highlight_box(
        "<b>Caution:</b> Epic's CoMET and Cosmos AI models are in active development and have "
        "not been published in peer-reviewed literature as of the date of this profile. Keep "
        "AI claims tied to UGM 2025 announcements and avoid characterizing model performance "
        "as clinically validated unless separately sourced.",
        s,
    )]))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "<i>Sources: CNBC [13]; Fierce Healthcare [11]; Healthcare IT News [7]; "
        "STAT News [15]; Fierce Healthcare [14].</i>",
        s["caution"],
    ))

    # ── COSMOS RESEARCH DATABASE ──────────────────────────────────────────────
    story += section("Cosmos Research Database and Academic Collaboration", s)
    story.append(Paragraph(
        "Cosmos is the most significant research-relevant asset in Epic's portfolio for academic "
        "partnership purposes. The database is structured as an opt-in collaborative: health "
        "systems must agree to contribute all their data to the Cosmos community and to not sell "
        "access to it. Epic coordinates the research program and publishes studies through an "
        "internal team, while also supporting external academic publication.",
        s["body"],
    ))
    story.append(Paragraph(
        "Cosmos participants with documented publications include Yale New Haven Health System "
        "and Yale University, Ohio State University Wexner Medical Center, Children's Hospital "
        "of Philadelphia, RUSH University System for Health, Loma Linda University Medical "
        "Center, University of Texas Southwestern Medical Center, and the University of "
        "Arkansas for Medical Sciences, among others.",
        s["body"],
    ))
    story.append(KeepTogether([highlight_box(
        "<b>Cosmos Genomics Expansion:</b> Cosmos is expanding to include genomic variant data, "
        "combining genetic and EHR-derived digital phenotypes in a single dataset &mdash; a "
        "development with direct implications for precision medicine research programs.",
        s,
    )]))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "The Cosmos AI Lab, announced at UGM 2025, provides a structured mechanism for "
        "researchers and data scientists to engage with Epic's Cosmos-trained foundation models, "
        "with the explicit goal of supporting external research collaboration alongside Epic's "
        "internal development program.",
        s["body"],
    ))
    story.append(Paragraph(
        "<b>Note on Cosmos participation:</b> UNC Health's status as an active Epic customer "
        "makes it eligible to participate in Cosmos if it has opted in. A follow-up research "
        "pass targeting UNC Health's Cosmos participation status is recommended before "
        "characterizing UNC as a Cosmos data contributor in any formal outreach.",
        s["body"],
    ))
    story.append(Paragraph(
        "<i>Sources: Epic Cosmos [3]; Cosmos publications [18]; Medscape [17]; "
        "Healthcare IT Today [19].</i>",
        s["caution"],
    ))

    # ── UNC HEALTH DOCUMENTED RELATIONSHIP ───────────────────────────────────
    story += section("UNC Health — Documented Operational and AI Relationship", s)
    story.append(Paragraph(
        "UNC Health has a documented, multi-year, and actively expanding relationship with Epic "
        "that is unique among the companies profiled in this series. The relationship is "
        "operational (Epic is UNC Health's EHR), research-enabling (UNC Health is "
        "Cosmos-eligible), and specifically AI-focused through documented co-adoption of Epic "
        "and Microsoft AI features.",
        s["body"],
    ))

    story.append(Paragraph("Documented Milestones", s["subsection_heading"]))
    story += bullets([
        "<b>EHR Implementation (~2014):</b> UNC Health Care completed implementation of Epic "
        "as its enterprise EHR system. Epic@UNC has served as the clinical backbone of UNC "
        "Health's 20 hospitals and more than 900 clinics.",
        "<b>Generative AI Patient Messaging (2023):</b> UNC Health was selected by Epic as one "
        "of the first health systems to test generative AI tools for auto-drafting clinician "
        "responses to patient messages. Initial rollout began with five to ten physicians at "
        "UNC Health. Leadership publicly cited the partnership as an effort to reduce "
        "clinician administrative burden.",
        "<b>Nuance DAX Copilot Expansion (2024):</b> UNC Health expanded the deployment of "
        "Nuance Dragon Ambient eXperience Copilot (DAX Copilot) &mdash; Microsoft's ambient "
        "clinical documentation AI embedded in Epic &mdash; to more providers across the "
        "health system. UNC Health was among 150 health systems deploying the tool at scale.",
        "<b>Rare Disease Coding Tool Launch (February 2026):</b> UNC Health launched what it "
        "described as the world's first standardized rare-disease coding tool, integrating "
        "Mondo Disease Ontology codes into its Epic EHR as part of Epic's February 2026 "
        "software update. The tool introduces nearly 5,000 new rare disease codes and revises "
        "more than 25,000 related disease codes within Epic, available across UNC Health's "
        "20 hospitals and 900-plus clinics.",
    ], s)
    story.append(KeepTogether([highlight_box(
        "These documented milestones establish UNC Health &mdash; and, by extension, UNC &mdash; "
        "as an active, publicly visible co-development and early-adoption partner for Epic's "
        "most strategically significant AI and clinical informatics initiatives.",
        s,
    )]))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "<i>Sources: Becker's [20]; Fierce Healthcare [16]; Fierce Healthcare [14]; "
        "Becker's [21].</i>",
        s["caution"],
    ))

    # ── UNC ALIGNMENT ─────────────────────────────────────────────────────────
    story += section("Alignment with UNC Research", s)
    story.append(Paragraph(
        "A direct UNC&ndash;Epic institutional research partnership has not been identified "
        "from the current source set beyond the UNC Health operational relationship documented "
        "above. The following represents additional strategic alignment based on documented "
        "Epic capabilities and UNC academic research strengths.",
        s["body"],
    ))

    story.append(Paragraph("Strategic Fit Areas", s["subsection_heading"]))
    story += bullets([
        "<b>Biomedical informatics and EHR-derived data science:</b> UNC's CHIP program and "
        "biomedical informatics groups work directly with clinical data types that Epic's "
        "Cosmos, Clarity, and Caboodle platforms are designed to support.",
        "<b>Clinical AI evaluation and implementation science:</b> Epic's AI features require "
        "clinical validation in real care environments. UNC health system researchers and "
        "implementation scientists are well positioned to study adoption, workflow integration, "
        "and outcomes for these tools.",
        "<b>Rare disease and precision medicine research:</b> UNC Health's February 2026 launch "
        "of the Mondo Disease Ontology coding tool in Epic positions UNC as a leader in rare "
        "disease classification within the Epic ecosystem.",
        "<b>Population health analytics and public health:</b> Cosmos's disease outbreak "
        "prediction initiative and population-level data assets align with UNC Gillings School "
        "of Global Public Health analytics and epidemiology groups.",
        "<b>Informatics education and clinical training pipelines:</b> UNC's CHIP program "
        "benefits from close engagement with the dominant EHR platform &mdash; creating natural "
        "alignment for curriculum, practicum, and research partnerships.",
        "<b>FHIR and interoperability research:</b> UNC biomedical informatics and computer "
        "science groups working on health data interoperability, SMART on FHIR app development, "
        "or clinical data exchange are well positioned to engage with Epic's open developer "
        "ecosystem.",
    ], s)

    story.append(Paragraph("Recommended Enrichment Targets", s["subsection_heading"]))
    story += bullets([
        "UNC Health IT leadership and Epic@UNC team &mdash; to confirm Cosmos participation "
        "and identify existing Epic research collaboration structures",
        "UNC Biomedical Informatics program (CHIP)",
        "UNC School of Medicine &mdash; clinical informatics, rare disease, and precision "
        "medicine programs",
        "UNC Gillings School of Global Public Health &mdash; population health analytics and "
        "epidemiology groups",
        "UNC Department of Computer Science &mdash; health data interoperability and NLP faculty",
        "UNC health behavior and implementation science groups",
        "UNC Eshelman School of Pharmacy &mdash; clinical trial management and drug information "
        "research",
    ], s)

    # ── TALKING POINTS ────────────────────────────────────────────────────────
    story += section("Talking Points", s)

    story.append(Paragraph("Organizational Context", s["subsection_heading"]))
    story += bullets([
        "Epic is the dominant U.S. EHR vendor by both hospital count and bed share: 43.7% of "
        "acute care hospitals and approximately 55% of acute care hospital beds as of "
        "year-end 2025 per KLAS Research. Its nearest competitor, Oracle Health, holds 22.9%.",
        "Revenue reached $5.7B in 2024, confirmed by a company spokesperson. As a private "
        "company, Epic does not publish SEC filings; revenue figures should be attributed "
        "to company-confirmed reporting.",
        "Epic should be framed as a clinical infrastructure company, not a general-purpose "
        "technology or consumer platform company. Its value to UNC is grounded in the fact "
        "that UNC Health runs on Epic, UNC Health has already served as an early-adoption "
        "site for Epic AI, and Epic's Cosmos database is one of the most significant clinical "
        "data assets available to participating health systems.",
        "Epic's AI roadmap is substantial &mdash; 160 to 200 features in development or deployed "
        "&mdash; and is increasingly built on proprietary foundation models trained on Cosmos "
        "data rather than exclusively on third-party model partnerships.",
    ], s)

    story.append(Paragraph("Alignment with UNC Research", s["subsection_heading"]))
    story += bullets([
        "UNC's positioning with Epic is not hypothetical. UNC Health was publicly selected by "
        "Epic to pilot generative AI patient message tools in 2023, expanded Nuance DAX Copilot "
        "embedded in Epic in 2024, and launched a world-first rare disease coding tool in Epic "
        "in February 2026. These are documented, public milestones.",
        "The strongest outreach angle for the Office of Innovation and Commercialization is "
        "not a cold partnership pitch &mdash; it is extending an already-active operational and "
        "AI co-development relationship into a structured research collaboration, potentially "
        "including Cosmos data access agreements, funded studies, or joint development of "
        "AI validation frameworks.",
        "For UNC researchers outside the health system, the most accessible entry points are "
        "Epic's open developer ecosystem (open.epic, fhir.epic.com) and the documented Cosmos "
        "academic publication program, which already includes peer-reviewed publications from "
        "Yale, Ohio State, and Children's Hospital of Philadelphia.",
    ], s)

    # ── RISK AND CAUTION NOTES ────────────────────────────────────────────────
    story += section("Risk and Caution Notes", s)
    story += bullets([
        "Do not overstate the UNC&ndash;Epic relationship as a formal research partnership. "
        "The documented relationship is between UNC Health (the clinical enterprise) and Epic. "
        "Confirm whether existing agreements cover academic research collaboration, IP licensing, "
        "or Cosmos data access before making partnership claims.",
        "Do not attribute Epic financial figures to audited disclosures; they come from "
        "company-confirmed reporting to Becker's Hospital Review. Epic does not publish "
        "SEC filings.",
        "Do not present CoMET or Cosmos AI models as clinically validated. As of August 2025, "
        "these are development-stage models with no peer-reviewed performance data identified "
        "in the current source set.",
        "Epic is subject to active antitrust litigation as of late 2025: a federal judge "
        "allowed Particle Health's Sherman Act Section 2 claims to proceed in September 2025, "
        "and the Texas Attorney General filed suit in December 2025 alleging monopolization. "
        "Do not characterize Epic's market position in ways that could be construed as "
        "endorsing challenged practices.",
        "Keep Cosmos participation claims about UNC Health conditional &mdash; confirm UNC "
        "Health's opt-in status through a direct follow-up before asserting it in "
        "partnership materials.",
    ], s)

    # ── EXPECTED REPORT ANGLE ─────────────────────────────────────────────────
    story += section("Expected Report Angle and Positioning", s)
    story.append(highlight_box(
        "<b>Positioning Summary:</b> Epic should be framed as (1) the dominant U.S. EHR "
        "platform with 43.7% of acute care hospitals and $5.7B in 2024 revenue, making it the "
        "primary clinical infrastructure partner for any academic medical center conducting "
        "EHR-linked research; (2) the operator of Cosmos, one of the largest deidentified "
        "clinical research databases in existence, with 300 million patient records and an "
        "active AI model development program; (3) an already-active operational and AI "
        "co-development partner for UNC Health specifically, with three publicly documented "
        "milestones between 2023 and 2026; (4) a different category of partner than Apple, "
        "Google, or Microsoft &mdash; not a cloud or consumer platform company, but the "
        "clinical data infrastructure layer inside which UNC Health already operates every "
        "day; and (5) a company whose strategic trajectory toward proprietary foundation "
        "models trained on clinical data, clinical AI agents, and ERP expansion makes the "
        "academic medical center relationship more, not less, valuable over time.",
        s,
    ))

    # ── REFERENCES ────────────────────────────────────────────────────────────
    story += section("References", s)
    refs = [
        ("[1]",  "Epic Systems corporate site",
                 "https://www.epic.com"),
        ("[2]",  "Becker's Hospital Review — Epic revenue climbs to $5.7B (September 2025)",
                 "https://www.beckershospitalreview.com/healthcare-information-technology/ehrs/epics-revenue-increases-to-5-7b/"),
        ("[3]",  "Epic Cosmos",
                 "https://cosmos.epic.com"),
        ("[4]",  "Becker's Hospital Review — 7 health systems moving to Epic (KLAS 2024 data)",
                 "https://www.beckershospitalreview.com/healthcare-information-technology/ehrs/7-health-systems-moving-to-epic/"),
        ("[5]",  "Fierce Healthcare — Epic grows EHR footprint, KLAS 2025 market share (May 2026)",
                 "https://www.fiercehealthcare.com/health-tech/epic-continues-grow-ehr-market-share-it-makes-gains-small-health-systems"),
        ("[6]",  "Dark Daily — Epic expands EHR market share, KLAS 2024 data (June 2025)",
                 "https://www.darkdaily.com/2025/06/04/epic-expands-ehr-market-share-as-rivals-lose-customers/"),
        ("[7]",  "Sacra — Epic company profile, market data, antitrust litigation",
                 "https://sacra.com/c/epic/"),
        ("[8]",  "open.epic — Technical Specifications",
                 "https://open.epic.com/TechnicalSpecifications"),
        ("[9]",  "Epic EHR integration — FHIR, Caboodle, Clarity technical documentation",
                 "https://fhir.epic.com/Documentation"),
        ("[10]", "Fierce Healthcare — Epic interoperability features, Clarity licensing, "
                 "MyChart Central (September 2025)",
                 "https://www.fiercehealthcare.com/health-tech/epic-previews-new-interoperability-features-patients-providers-and-developers"),
        ("[11]", "Fierce Healthcare — Epic AI features and Cosmos AI, UGM 2025 (August 2025)",
                 "https://www.fiercehealthcare.com/health-tech/epic-unveils-major-ai-features-ai-charting-microsoft-cosmos-ai-risk-prediction-and-rcm"),
        ("[12]", "Epic on FHIR — Developer resources",
                 "https://fhir.epic.com"),
        ("[13]", "CNBC — Epic UGM 2025 AI tools coverage (August 2025)",
                 "https://www.cnbc.com/2025/08/20/epic-ugm-2025-epic-touts-new-ai-tools.html"),
        ("[14]", "Fierce Healthcare — Microsoft Nuance DAX Copilot at UNC Health (January 2024)",
                 "https://www.fiercehealthcare.com/ai-and-machine-learning/microsofts-ai-copilot-takes-epic-unc-health-lifespan-expand-tech-more"),
        ("[15]", "STAT News — Epic's CoMET AI model (August 2025)",
                 "https://www.statnews.com/2025/08/27/epics-doctor-strange-moment-ai-for-possible-patient-futures-ai-prognosis/"),
        ("[16]", "Fierce Healthcare — Epic generative AI patient messages, UNC Health (June 2023)",
                 "https://www.fiercehealthcare.com/health-tech/epic-moves-forward-bring-generative-ai-healthcare-heres-why-handful-health-systems-are"),
        ("[17]", "Medscape — Inside Epic's Rapid-Fire Research Machine (October 2025)",
                 "https://www.medscape.com/viewarticle/inside-epics-rapid-fire-research-machine-2025a1000um9"),
        ("[18]", "Epic Cosmos — Publications listing",
                 "https://cosmos.epic.com/publications/"),
        ("[19]", "Healthcare IT Today — Epic XGM Cosmos genomics and AI (May 2025)",
                 "https://www.healthcareittoday.com/2025/05/14/epic-xgm-spotlights-whats-next-for-ai-usability-cosmos-and-much-more/"),
        ("[20]", "Becker's Hospital Review — UNC Health Care completes Epic implementation (2014)",
                 "https://www.beckershospitalreview.com/healthcare-information-technology/unc-health-care-rebounds-financially-after-epic-implementation.html"),
        ("[21]", "Becker's Hospital Review — UNC Health launches rare disease coding tool in "
                 "Epic (February 2026)",
                 "https://www.beckershospitalreview.com/healthcare-information-technology/ehrs/unc-health-unveils-rare-disease-coding-tool-in-epic/"),
    ]
    for num, title, url in refs:
        story.append(Paragraph(f"<b>{num}</b> {title} &mdash; {url}", s["ref"]))

    story.append(Spacer(1, 0.3 * inch))
    story.append(rule())
    story.append(Paragraph(
        "Partnership Intelligence Profile &mdash; Epic Systems Corporation &mdash; "
        "Internal Use Only &mdash; May 2026",
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
        title="Partnership Intelligence Profile — Epic Systems Corporation",
        author="UNC Office of Innovation and Commercialization",
        subject="Epic Systems Partnership Intelligence",
    )
    doc.build(build_story(s))
    print(f"PDF written to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
