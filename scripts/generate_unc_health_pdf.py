"""Generate a formatted partnership intelligence PDF for UNC Health."""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, KeepTogether
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY

OUTPUT_PATH = "/Users/aidancolvin/partnership-intelligence-analyzer/data/processed/company-profiles/unc-health/deliverable.pdf"

# ── Color palette ──────────────────────────────────────────────────────────────
UNC_BLUE     = colors.HexColor("#4B9CD3")   # Carolina Blue
UNC_NAVY     = colors.HexColor("#13294B")   # UNC Navy
MID_GRAY     = colors.HexColor("#5f6368")
LIGHT_BLUE   = colors.HexColor("#f0f6fd")
ACCENT_DARK  = colors.HexColor("#005a8e")
RULE_COLOR   = colors.HexColor("#a8c8e8")


def build_styles():
    base = getSampleStyleSheet()
    return {
        "cover_title": ParagraphStyle(
            "cover_title", parent=base["Title"],
            fontSize=28, leading=34, textColor=UNC_NAVY,
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
            fontSize=13, leading=17, textColor=UNC_BLUE,
            spaceBefore=18, spaceAfter=6,
            fontName="Helvetica-Bold",
        ),
        "subsection_heading": ParagraphStyle(
            "subsection_heading", parent=base["Heading2"],
            fontSize=11, leading=15, textColor=UNC_NAVY,
            spaceBefore=10, spaceAfter=4,
            fontName="Helvetica-Bold",
        ),
        "body": ParagraphStyle(
            "body", parent=base["Normal"],
            fontSize=10, leading=15, textColor=UNC_NAVY,
            spaceAfter=6, alignment=TA_JUSTIFY,
        ),
        "bullet": ParagraphStyle(
            "bullet", parent=base["Normal"],
            fontSize=10, leading=15, textColor=UNC_NAVY,
            leftIndent=14, firstLineIndent=-10, spaceAfter=4,
        ),
        "label": ParagraphStyle(
            "label", parent=base["Normal"],
            fontSize=9, leading=13, textColor=MID_GRAY,
            fontName="Helvetica-Bold", spaceAfter=1,
        ),
        "value": ParagraphStyle(
            "value", parent=base["Normal"],
            fontSize=10, leading=14, textColor=UNC_NAVY,
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


def highlight_box(text, s, bg=LIGHT_BLUE):
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
    story.append(Paragraph("Partnership Intelligence Profile — Internal Asset Overview", s["cover_sub"]))
    story.append(Paragraph("UNC Health", s["cover_title"]))
    story.append(Paragraph(
        "University of North Carolina at Chapel Hill &mdash; Office of Innovation and Commercialization",
        s["cover_sub"],
    ))
    story.append(Spacer(1, 0.1 * inch))
    story.append(Paragraph(
        "Prepared: May 2026 &#160;&#160;|&#160;&#160; Slug: unc-health &#160;&#160;|&#160;&#160; Classification: Internal Use",
        s["cover_meta"],
    ))
    story.append(Spacer(1, 0.25 * inch))
    story.append(rule())

    # ── COMPANY OVERVIEW ──────────────────────────────────────────────────────
    story += section("Overview", s)
    story.append(Paragraph(
        "UNC Health is a state entity and affiliated enterprise of the University of North "
        "Carolina system, operating as North Carolina's academic health system. It is "
        "headquartered in Chapel Hill and serves patients across all 100 North Carolina counties "
        "through a network of hospitals, clinics, and the clinical programs of the UNC School "
        "of Medicine. As a $7.4 billion enterprise with 20 hospital campuses, more than 900 "
        "clinics, and approximately 56,000 employees, UNC Health is both the primary clinical "
        "platform of the UNC enterprise and the most direct institutional partner available to "
        "UNC researchers, the Office of Innovation and Commercialization, and external companies "
        "seeking to engage with a large, data-rich academic health system in the "
        "American Southeast.",
        s["body"],
    ))
    story.append(KeepTogether([highlight_box(
        "<b>Internal Asset Note:</b> Unlike the external companies profiled in this series, "
        "UNC Health is not a partner to be approached from the outside &mdash; it is an internal "
        "partner whose capabilities, data infrastructure, clinical programs, and research "
        "ecosystem should be understood by the OIC as assets to be articulated when positioning "
        "UNC to industry.",
        s,
    )]))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "<i>Sources: UNC Health [1]; Business North Carolina [2]; UNC Health Newsroom [3].</i>",
        s["caution"],
    ))

    # ── BASIC ORGANIZATIONAL INFORMATION ──────────────────────────────────────
    story += section("Basic Organizational Information", s)
    story.append(kv_table([
        ("Full Name",        "UNC Health (University of North Carolina Health Care System)"),
        ("Headquarters",     "Chapel Hill, North Carolina, United States"),
        ("Website",          "https://www.unchealth.org"),
        ("Newsroom",         "https://news.unchealthcare.org"),
        ("Org Type",         "State Entity / Affiliated Enterprise of the UNC System"),
        ("Revenue",          "$7.4 billion (Business North Carolina, 2026 — not audited)"),
        ("Employees",        "~56,000"),
        ("Hospitals",        "17 hospitals, 20 hospital campuses"),
        ("Clinics",          "900+"),
        ("CEO",              "Dr. Cristy Page (effective November 24, 2025; also Dean of UNC "
                             "School of Medicine and Vice Chancellor for Medical Affairs)"),
        ("EHR Platform",     "Epic (Epic@UNC, implemented ~2014)"),
    ], s))
    story.append(Paragraph(
        "<i>Sources: Business North Carolina [2]; UNC Health Newsroom [3]; "
        "UNC Hospitals [4].</i>",
        s["caution"],
    ))

    # ── SYSTEM SCALE AND STRUCTURE ────────────────────────────────────────────
    story += section("System Scale and Structure", s)

    story.append(Paragraph("Hospital Network", s["subsection_heading"]))
    story.append(Paragraph(
        "UNC Health comprises 17 hospitals and 20 hospital campuses. The system includes the "
        "flagship UNC Hospitals in Chapel Hill; UNC Health Rex and Rex Holly Springs in the "
        "Raleigh/Wake County area; UNC Health Blue Ridge in Morganton; UNC Health Rockingham "
        "in Eden; UNC Health Chatham in Siler City; UNC Health Lenoir in Kinston; UNC Health "
        "Onslow in Jacksonville; UNC Health Southeastern in Lumberton; and UNC Health Pardee "
        "in Hendersonville, among others. This statewide footprint extends clinical operations "
        "from the mountains to the coast, covering both urban academic medical centers and "
        "rural critical access hospitals across all 100 North Carolina counties.",
        s["body"],
    ))

    story.append(Paragraph("Academic Medical Center — UNC Hospitals, Chapel Hill", s["subsection_heading"]))
    story += bullets([
        "North Carolina Cancer Hospital (clinical base of UNC Lineberger Comprehensive "
        "Cancer Center)",
        "North Carolina Children's Hospital",
        "North Carolina Memorial Hospital",
        "North Carolina Neurosciences Hospital",
        "North Carolina Women's Hospital",
        "UNC Health Hillsborough Campus",
    ], s)
    story.append(Paragraph(
        "UNC Hospitals employs more than 7,100 people at the Chapel Hill campus, including "
        "1,100 medical staff and 780 resident physicians. Over 800,000 people are cared for "
        "at UNC practices and clinics each year.",
        s["body"],
    ))
    story.append(Paragraph(
        "<i>Sources: Business North Carolina [2]; UNC Health Newsroom [3]; "
        "UNC Hospitals [4]; US News [5].</i>",
        s["caution"],
    ))

    # ── QUALITY AND RANKINGS ──────────────────────────────────────────────────
    story += section("Quality, Rankings, and Accreditation", s)

    story.append(Paragraph("US News Best Hospitals 2025–26", s["subsection_heading"]))
    story += bullets([
        "No. 2 hospital in North Carolina and No. 2 in the Triangle region "
        "(US News 2025&ndash;26, released July 29, 2025).",
        "Four nationally ranked adult specialties: cancer (No. 48), ear nose and throat "
        "(No. 44), urology (No. 31), and rehabilitation (No. 46).",
        "High performing in five adult specialties and 14 common adult procedures and "
        "conditions, including COPD, colon cancer surgery, diabetes, and heart failure.",
        "Nationally ranked in eight pediatric specialties.",
        "UNC Health Rex: No. 4 in North Carolina, No. 3 in the Triangle; high-performing "
        "in gastroenterology and GI surgery.",
    ], s)

    story.append(Paragraph("Magnet Nursing Designation", s["subsection_heading"]))
    story.append(Paragraph(
        "UNC Hospitals has attained Magnet designation from the American Nurses Credentialing "
        "Center for the fourth time &mdash; a recognition earned by fewer than 10% of hospitals "
        "nationwide and widely cited as the highest national honor in nursing.",
        s["body"],
    ))
    story.append(Paragraph(
        "<i>Sources: UNC Health Newsroom [5]; CBS17 [8]; Business North Carolina [2].</i>",
        s["caution"],
    ))

    # ── RESEARCH INFRASTRUCTURE ───────────────────────────────────────────────
    story += section("Research Infrastructure", s)

    story.append(Paragraph("NIH and External Research Funding", s["subsection_heading"]))
    story.append(KeepTogether([highlight_box(
        "<b>Research Scale (July 2024&ndash;June 2025):</b> UNC School of Medicine research "
        "funding totaled more than $641 million, including $345 million from the NIH. Across "
        "UNC-Chapel Hill, 250 faculty experts are leading more than 500 AI and machine learning "
        "projects, totaling $163 million in research awards in the five years prior to mid-2025.",
        s,
    )]))
    story.append(Spacer(1, 6))

    story.append(Paragraph("NC TraCS Institute", s["subsection_heading"]))
    story.append(Paragraph(
        "The North Carolina Translational and Clinical Sciences Institute (NC TraCS) is UNC's "
        "NIH-funded Clinical and Translational Science Award (CTSA) hub, receiving funding "
        "from the NIH, UNC Health, the State of North Carolina, UNC Lineberger, the UNC "
        "School of Medicine, and the UNC Office of the Vice Chancellor for Research &amp; "
        "Economic Development. NC TraCS provides translational science infrastructure across "
        "the research enterprise and co-led the development of SHIRE.",
        s["body"],
    ))

    story.append(Paragraph("UNC Lineberger Comprehensive Cancer Center", s["subsection_heading"]))
    story += bullets([
        "One of only 49 NCI-designated Comprehensive Cancer Centers in the United States and "
        "the only public NCI-designated Comprehensive Cancer Center in North Carolina.",
        "Received an &ldquo;exceptional&rdquo; rating &mdash; the highest category &mdash; "
        "in its most recent NCI review.",
        "325 members drawn from more than 40 departments across UNC.",
        "200-plus clinical trials across all phases of investigation.",
        "$28 million ARPA-H award in 2025 for the EVOLVE trial for metastatic breast cancer "
        "&mdash; a biomarker-driven adaptive treatment trial modifying plans in near real-time.",
        "2024: Launched hybrid decentralized clinical trials bringing cancer trials to rural "
        "patients across North Carolina, with two trials enrolling and 20 in development.",
    ], s)
    story.append(Paragraph(
        "<i>Sources: UNC Research [9]; NC TraCS [10][11]; NCI [12]; Chapelboro [13]; "
        "UNC-Chapel Hill [14].</i>",
        s["caution"],
    ))

    # ── DIGITAL AND AI INFRASTRUCTURE ────────────────────────────────────────
    story += section("Digital and AI Infrastructure", s)

    story.append(Paragraph("SHIRE — Secure Health Informatics Research Environment", s["subsection_heading"]))
    story.append(Paragraph(
        "The single most significant recent development in UNC Health's research infrastructure "
        "is SHIRE, the Secure Health Informatics Research Environment. SHIRE was jointly built "
        "by UNC-Chapel Hill, the UNC School of Medicine, NC TraCS, and UNC Health, and was "
        "publicly announced by Chancellor Lee H. Roberts and UNC Health CEO Dr. Cristy Page "
        "on April 8, 2026.",
        s["body"],
    ))
    story.append(KeepTogether([highlight_box(
        "<b>SHIRE:</b> A HIPAA-compliant, secure, cloud-based analytics platform enabling "
        "credentialed researchers to develop and test advanced AI models using EHR data from "
        "UNC Health. Supports large-scale clinical dataset modeling with rigorous privacy "
        "safeguards, local LLMs deployed behind secure firewalls, multimodal data integration "
        "(imaging, genomics, clinical notes), and a structured IRB-governed data access review "
        "process. Went live November 3, 2025. Full transition from prior CDW-H system expected "
        "by end of 2026. Early research targets: precision oncology, rare disease, mental health.",
        s,
    )]))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "The launch of SHIRE opens documented opportunities for technology companies, life "
        "sciences organizations, and health AI developers to partner with UNC on AI-enabled "
        "solutions using real-world clinical data within a shared governance framework.",
        s["body"],
    ))

    story.append(Paragraph("Epic@UNC — EHR Platform and AI Co-Development", s["subsection_heading"]))
    story.append(Paragraph(
        "UNC Health operates on Epic as its enterprise EHR (~2014 implementation) and has "
        "served as a documented early-adoption and co-development site for several of Epic's "
        "highest-priority AI initiatives:",
        s["body"],
    ))
    story += bullets([
        "<b>Generative AI patient message drafting (2023):</b> UNC Health was selected by "
        "Epic as one of the first health systems in the country to pilot generative AI tools "
        "for auto-drafting clinician responses to patient messages. Initial rollout began with "
        "five to ten physicians.",
        "<b>Nuance DAX Copilot expansion (2024):</b> UNC Health expanded deployment of "
        "Nuance Dragon Ambient eXperience Copilot &mdash; Microsoft's ambient clinical "
        "documentation AI embedded in Epic &mdash; to more providers system-wide. UNC Health "
        "was among 150 health systems globally deploying the tool at scale.",
        "<b>Rare disease coding tool launch (February 2026):</b> UNC Health launched the "
        "world's first standardized rare-disease coding tool, integrating Mondo Disease Ontology "
        "codes into Epic across 20 hospitals and 900-plus clinics.",
    ], s)

    story.append(Paragraph("Ambient Clinical AI — Abridge (2025)", s["subsection_heading"]))
    story.append(Paragraph(
        "In 2025, UNC Health implemented Abridge, an ambient clinical documentation AI, as "
        "part of Abridge's broader rollout across 100-plus health systems. UNC Health was named "
        "alongside Duke Health, Johns Hopkins, Mayo Clinic, and Memorial Sloan Kettering as a "
        "2025 implementation site. Abridge raised a $250 million Series D tied to that "
        "milestone. UNC Health Southeastern also deployed ambient AI across approximately 60 "
        "providers in orthopedics, emergency services, primary care, and oncology.",
        s["body"],
    ))
    story.append(Paragraph(
        "<i>Sources: UNC-Chapel Hill [15]; NC TraCS [11]; UNC Research [9]; DistilINFO [16]; "
        "Becker's [17]; Fierce Healthcare [18][19]; Becker's [20]; Medical Economics [21]; "
        "UNC Health Southeastern [22].</i>",
        s["caution"],
    ))

    # ── STRATEGIC THEMES ──────────────────────────────────────────────────────
    story += section("Strategic Themes", s)
    story += bullets([
        "$7.4 billion enterprise across 17 hospitals and 900-plus clinics serving all 100 "
        "North Carolina counties.",
        "New CEO Dr. Cristy Page (November 2025) &mdash; primary care and rural health expert "
        "&mdash; with explicit focus on innovation, AI, and broadening access across NC.",
        "SHIRE as shared AI research infrastructure enabling external partners to engage with "
        "UNC Health clinical data under structured governance, launched April 2026.",
        "Epic-embedded AI co-development history: documented early-adoption of Epic generative "
        "AI (2023), Nuance DAX Copilot (2024), and rare disease coding tool (February 2026).",
        "Lineberger NCI Comprehensive Cancer Center status, ARPA-H funding, and decentralized "
        "trial innovation positioning UNC as a translational oncology research hub.",
        "NC TraCS as the translational science backbone connecting basic research, clinical "
        "investigation, and implementation.",
        "Gillings School's new Center for Artificial Intelligence and Public Health (CAIPH) "
        "expanding the AI-in-health footprint into population health informatics.",
        "$641 million in School of Medicine research funding (July 2024&ndash;June 2025), "
        "including $345 million from NIH.",
        "Abridge, DAX Copilot, and Epic generative AI adoption signaling active AI integration "
        "rather than passive evaluation.",
    ], s)

    # ── POSITIONING FOR EXTERNAL PARTNERSHIP ──────────────────────────────────
    story += section("Positioning for External Partnership Discussions", s)

    story.append(Paragraph("What UNC Health Offers External Partners", s["subsection_heading"]))
    story += bullets([
        "<b>Real-world clinical data at scale:</b> SHIRE enables external partners to engage "
        "with UNC Health EHR data under a responsible AI framework and structured governance.",
        "<b>Validated clinical environment:</b> UNC Health's early-adoption role for Epic AI, "
        "Abridge, and Nuance DAX Copilot establishes it as a health system capable of testing, "
        "deploying, and evaluating novel AI tools in live care delivery settings.",
        "<b>Translational research infrastructure:</b> NC TraCS, Lineberger, and the UNC "
        "School of Medicine provide the regulatory, clinical trial, and sponsored research "
        "infrastructure for external companies to design and execute studies at UNC Health.",
        "<b>Rural health reach:</b> Statewide footprint from urban academic medical centers to "
        "rural critical access hospitals, relevant to partners with documented rural health "
        "priorities and to federal funding opportunities targeting underserved populations.",
        "<b>Rare disease and precision medicine:</b> The Mondo Disease Ontology launch, "
        "Lineberger's NCI designation, and the ARPA-H EVOLVE trial establish validated "
        "infrastructure for complex, data-driven clinical work.",
    ], s)

    story.append(Paragraph("Partnership Framing by Company", s["subsection_heading"]))
    story += bullets([
        "<b>For Apple:</b> UNC Health's digital health adoption, ambulatory clinic scale, and "
        "patient-facing MyChart infrastructure create alignment with Apple's ResearchKit model, "
        "wearable health data research, and decentralized study designs.",
        "<b>For Google:</b> Statewide rural presence, NC TraCS infrastructure, and Gillings "
        "population health research capacity align with Google's documented investment in "
        "clinician education and rural health transformation.",
        "<b>For Microsoft:</b> The Nuance DAX Copilot deployment at UNC Health is already a "
        "documented partnership; SHIRE's cloud infrastructure creates additional Azure and "
        "data science collaboration opportunities.",
        "<b>For Epic:</b> The UNC Health&ndash;Epic relationship is the most operationally "
        "embedded of any company in this profile series, with documented co-development across "
        "generative AI, ambient documentation, interoperability, and rare disease coding "
        "&mdash; making UNC Health a reference site for Epic's Cosmos AI program.",
        "<b>For Johnson &amp; Johnson:</b> UNC Health's translational medicine, clinical trial "
        "infrastructure through NC TraCS and Lineberger, and MedTech evaluation capabilities "
        "create alignment with J&amp;J's Innovative Medicine and MedTech segments.",
    ], s)

    # ── RISK AND CAUTION NOTES ────────────────────────────────────────────────
    story += section("Risk and Caution Notes", s)
    story += bullets([
        "Do not cite the $7.4 billion revenue figure as audited; it is reported by Business "
        "North Carolina (2026) and has not been independently verified against UNC Health's "
        "official audited financial statements.",
        "UNC Health is a state entity subject to North Carolina governance requirements; "
        "partnership structures involving IP licensing, data sharing, or sponsored research "
        "must account for state governance and UNC System policies.",
        "Dr. Cristy Page became CEO in November 2025; strategy and key relationships under "
        "new leadership are still establishing their public record. Confirm current leadership "
        "positions before using in formal outreach.",
        "SHIRE went live November 2025 and is still transitioning from the prior CDW-H system; "
        "characterize it as operational but maturing, with full transition expected by end of 2026.",
    ], s)

    # ── EXPECTED REPORT ANGLE ─────────────────────────────────────────────────
    story += section("Expected Report Angle and Positioning", s)
    story.append(highlight_box(
        "<b>Positioning Summary:</b> UNC Health should be framed as (1) North Carolina's "
        "academic health system &mdash; a $7.4 billion state enterprise with 17 hospitals, "
        "900-plus clinics, and 56,000 employees serving all 100 counties; (2) a "
        "research-enabled clinical platform anchored by NC TraCS, UNC Lineberger (NCI "
        "Comprehensive Cancer Center), and $641 million in annual research funding; (3) the "
        "owner and operator of SHIRE &mdash; a cloud-based AI research environment launched "
        "April 2026 &mdash; the most direct mechanism for external partners to engage with "
        "UNC Health's real-world clinical data under responsible governance; (4) an active, "
        "documented early-adoption site for Epic generative AI, Nuance DAX Copilot, Abridge, "
        "and the world's first Epic-integrated rare disease coding system; and (5) a system "
        "undergoing leadership transition under CEO Dr. Cristy Page, with an explicit "
        "orientation toward AI, rural health innovation, and broadening partnership and "
        "commercialization relationships across North Carolina.",
        s,
    ))

    # ── REFERENCES ────────────────────────────────────────────────────────────
    story += section("References", s)
    refs = [
        ("[1]",  "UNC Health — About UNC Health",
                 "https://www.unchealth.org/about-us/who-we-are"),
        ("[2]",  "Business North Carolina — North Carolina's Best Hospitals 2026 (March 2026)",
                 "https://businessnc.com/north-carolinas-best-hospitals-2026/"),
        ("[3]",  "UNC Health Newsroom — Dr. Cristy Page named CEO (November 2025)",
                 "https://news.unchealthcare.org/2025/11/dr-cristy-page-named-ceo-of-unc-health-dean-of-unc-school-of-medicine/"),
        ("[4]",  "UNC Hospitals — About Us",
                 "https://www.uncmedicalcenter.org/uncmc/about/"),
        ("[5]",  "UNC Health Newsroom — US News Best Hospitals 2025-26 (July 2025)",
                 "https://news.unchealthcare.org/2025/07/unc-hospitals-and-unc-health-rex-ranked-as-top-hospitals-in-north-carolina-4/"),
        ("[6]",  "Glassdoor — UNC Health hospital network descriptions",
                 "https://www.glassdoor.com/Overview/Working-at-UNC-Health-EI_IE322749.11,21.htm"),
        ("[7]",  "UNC Health Foundation FY25 Annual Report",
                 "https://unchealthfoundation.org/gifts-at-work/unc-health-foundation-fy25-annual-report/"),
        ("[8]",  "CBS17 — UNC Hospitals ranked among nation's best, 2025-26 (July 2025)",
                 "https://www.cbs17.com/news/local-news/duke-university-unc-hospitals-ranked-among-nations-best-in-2025-26-report/"),
        ("[9]",  "UNC Research — UNC's AI Research: Paving the Way for the NIH's Data Science Vision (July 2025)",
                 "https://research.unc.edu/2025/07/10/uncs-ai-research-paving-the-way-for-the-nihs-data-science-vision/"),
        ("[10]", "NC TraCS Institute — About Us",
                 "https://tracs.unc.edu/index.php/about"),
        ("[11]", "NC TraCS — New Secure Cloud Computing Environment for EHR Data (October 2025)",
                 "https://tracs.unc.edu/index.php/news-articles/2369-new-secure-cloud-computing-environment-for-working-with-ehr-data"),
        ("[12]", "NCI — UNC Lineberger Comprehensive Cancer Center",
                 "https://www.cancer.gov/research/infrastructure/cancer-centers/find/unclineberger"),
        ("[13]", "Chapelboro — UNC Lineberger ARPA-H EVOLVE award $28M (June 2025)",
                 "https://chapelboro.com/news/unc/uncs-lineberger-cancer-center-awarded-28-million-for-new-clinical-trial"),
        ("[14]", "UNC-Chapel Hill — Lineberger expands cancer clinical trials access across NC (September 2025)",
                 "https://www.unc.edu/posts/2025/09/09/unc-lineberger-expands-cancer-clinical-trials-access-across-nc/"),
        ("[15]", "UNC-Chapel Hill — University, UNC Health unveil SHIRE (April 8, 2026)",
                 "https://www.unc.edu/posts/2026/04/08/university-unc-health-unveil-shire-health-care-innovation-platform/"),
        ("[16]", "DistilINFO — UNC Health Launches SHIRE AI Health Platform (April 2026)",
                 "https://distilinfo.com/2026/04/09/unc-health-launches-shire-ai-health-platform/"),
        ("[17]", "Becker's — UNC Health Care completes Epic implementation (2014)",
                 "https://www.beckershospitalreview.com/healthcare-information-technology/unc-health-care-rebounds-financially-after-epic-implementation.html"),
        ("[18]", "Fierce Healthcare — Epic generative AI patient messages, UNC Health (June 2023)",
                 "https://www.fiercehealthcare.com/health-tech/epic-moves-forward-bring-generative-ai-healthcare-heres-why-handful-health-systems-are"),
        ("[19]", "Fierce Healthcare — Microsoft Nuance DAX Copilot at UNC Health (January 2024)",
                 "https://www.fiercehealthcare.com/ai-and-machine-learning/microsofts-ai-copilot-takes-epic-unc-health-lifespan-expand-tech-more"),
        ("[20]", "Becker's — UNC Health launches rare disease coding tool in Epic (February 2026)",
                 "https://www.beckershospitalreview.com/healthcare-information-technology/ehrs/unc-health-unveils-rare-disease-coding-tool-in-epic/"),
        ("[21]", "Medical Economics — Abridge 2025 implementations including UNC Health (May 2026)",
                 "https://www.medicaleconomics.com/view/athenahealth-abridge-join-on-ai-clinical-documentation-venture"),
        ("[22]", "UNC Health Southeastern — Providers use AI to enhance patient experience (2025)",
                 "https://www.unchealthsoutheastern.org/about-us/news/2025/unc-health-southeastern-providers-use-ai-to-enhance-patient-expe/"),
        ("[23]", "UNC Gillings — New Gillings School center will leverage AI for improved public health (CAIPH)",
                 "https://sph.unc.edu/sph-news/new-gillings-school-center-will-leverage-ai-for-improved-public-health/"),
    ]
    for num, title, url in refs:
        story.append(Paragraph(f"<b>{num}</b> {title} &mdash; {url}", s["ref"]))

    story.append(Spacer(1, 0.3 * inch))
    story.append(rule())
    story.append(Paragraph(
        "Partnership Intelligence Profile &mdash; UNC Health &mdash; Internal Use Only &mdash; May 2026",
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
        title="Partnership Intelligence Profile — UNC Health",
        author="UNC Office of Innovation and Commercialization",
        subject="UNC Health Internal Asset Overview",
    )
    doc.build(build_story(s))
    print(f"PDF written to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
