"""Generate a formatted partnership intelligence PDF for Microsoft Corporation."""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, KeepTogether
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY

OUTPUT_PATH = "/Users/aidancolvin/partnership-intelligence-analyzer/data/processed/company-profiles/microsoft/deliverable.pdf"

# ── Color palette ──────────────────────────────────────────────────────────────
MSFT_BLUE    = colors.HexColor("#0078D4")
DARK_NAVY    = colors.HexColor("#1a1f36")
MID_GRAY     = colors.HexColor("#5f6368")
LIGHT_BLUE   = colors.HexColor("#f0f6fd")
ACCENT_DARK  = colors.HexColor("#005a9e")
RULE_COLOR   = colors.HexColor("#b8d8f5")


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
            fontSize=13, leading=17, textColor=MSFT_BLUE,
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
    story.append(Paragraph("Partnership Intelligence Profile", s["cover_sub"]))
    story.append(Paragraph("Microsoft Corporation", s["cover_title"]))
    story.append(Paragraph(
        "University of North Carolina at Chapel Hill &mdash; Office of Innovation and Commercialization",
        s["cover_sub"],
    ))
    story.append(Spacer(1, 0.1 * inch))
    story.append(Paragraph(
        "Prepared: May 2026 &#160;&#160;|&#160;&#160; Slug: microsoft &#160;&#160;|&#160;&#160; Classification: Internal Use",
        s["cover_meta"],
    ))
    story.append(Spacer(1, 0.25 * inch))
    story.append(rule())

    # ── COMPANY OVERVIEW ──────────────────────────────────────────────────────
    story += section("Company Overview", s)
    story.append(Paragraph(
        "Microsoft Corporation is a large public technology company headquartered in Redmond, "
        "Washington. The company develops and operates cloud infrastructure, enterprise software, "
        "productivity platforms, developer tools, AI services, gaming systems, and a growing "
        "portfolio of healthcare and life sciences technologies.",
        s["body"],
    ))
    story.append(Paragraph(
        "Microsoft is relevant for partnership discussions because it combines the world's "
        "second-largest cloud platform by revenue, a documented philanthropic and research grant "
        "program focused specifically on health AI, a dedicated Microsoft Cloud for Healthcare "
        "product line, and a suite of clinical data interoperability tools that align with UNC "
        "capabilities in biomedical informatics, clinical research infrastructure, health data "
        "science, public health analytics, and applied machine learning.",
        s["body"],
    ))
    story.append(Paragraph(
        "<i>Sources: Microsoft Investor Relations [1]; Microsoft FY2025 Annual Report [2]; "
        "Microsoft for Healthcare [3].</i>",
        s["caution"],
    ))

    # ── BASIC COMPANY INFORMATION ─────────────────────────────────────────────
    story += section("Basic Company Information", s)
    story.append(kv_table([
        ("Full Name",        "Microsoft Corporation"),
        ("Headquarters",     "Redmond, Washington, United States"),
        ("Website",          "https://www.microsoft.com"),
        ("Investor Relations","https://www.microsoft.com/en-us/investor"),
        ("SEC Filings",      "https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000789019"),
        ("Company Type",     "Public Company"),
        ("Ticker",           "MSFT (Nasdaq)"),
        ("Industry",         "Cloud Computing / Enterprise Software / AI / Productivity / Healthcare Technology"),
        ("Segments",         "Productivity and Business Processes; Intelligent Cloud; More Personal Computing"),
        ("Scale",            "Large Enterprise"),
    ], s))
    story.append(Paragraph(
        "<i>Sources: Microsoft FY2025 Annual Report [2]; Microsoft Investor Relations [1]; "
        "SEC EDGAR [4].</i>",
        s["caution"],
    ))

    # ── BUSINESS SIGNALS ─────────────────────────────────────────────────────
    story += section("Business Signals: FY2025 and FY2026 Q1–Q3", s)

    story.append(Paragraph("Full Fiscal Year 2025 (ended June 30, 2025)", s["subsection_heading"]))
    story.append(KeepTogether([highlight_box(
        "<b>FY2025 Key Metrics:</b> Total revenue $281.7B (+15% YoY) &nbsp;|&nbsp; "
        "Operating income $128.5B (+17% YoY) &nbsp;|&nbsp; "
        "Microsoft Cloud revenue $168.9B (+23% YoY) &nbsp;|&nbsp; "
        "Azure surpassed $75B in annual revenue (+34% YoY) &nbsp;|&nbsp; "
        "Full-year EPS $13.64 (+16% YoY).",
        s,
    )]))
    story.append(Spacer(1, 6))

    story.append(Paragraph("Fiscal Q1 FY2026 (ended September 30, 2025)", s["subsection_heading"]))
    story.append(KeepTogether([highlight_box(
        "<b>Q1 FY2026 Key Metrics:</b> Revenue $77.7B (+18% YoY) &nbsp;|&nbsp; "
        "Operating income $38.0B (+24% YoY) &nbsp;|&nbsp; "
        "Intelligent Cloud revenue $30.9B (+28% YoY) &nbsp;|&nbsp; "
        "Azure +40% YoY &nbsp;|&nbsp; "
        "Microsoft Cloud revenue $49.1B (+26% YoY) &nbsp;|&nbsp; "
        "Commercial remaining performance obligation $392B (+51% YoY).",
        s,
    )]))
    story.append(Spacer(1, 6))

    story.append(Paragraph("Fiscal Q2 FY2026 (ended December 31, 2025)", s["subsection_heading"]))
    story.append(KeepTogether([highlight_box(
        "<b>Q2 FY2026 Key Metrics:</b> Revenue $81.3B (+17% YoY) &nbsp;|&nbsp; "
        "Operating income $38.3B (+21% YoY) &nbsp;|&nbsp; "
        "Non-GAAP diluted EPS $4.14 (+24% YoY) &nbsp;|&nbsp; "
        "Intelligent Cloud revenue $32.9B (+29% YoY) &nbsp;|&nbsp; "
        "Azure revenue +39% YoY.",
        s,
    )]))
    story.append(Spacer(1, 6))

    story.append(Paragraph("Fiscal Q3 FY2026 (ended March 31, 2026)", s["subsection_heading"]))
    story.append(KeepTogether([highlight_box(
        "<b>Q3 FY2026 Key Metrics:</b> Revenue $82.9B (+18% YoY) &nbsp;|&nbsp; "
        "Operating income $38.4B (+20% YoY) &nbsp;|&nbsp; "
        "Diluted EPS $4.27 (+23% YoY) &nbsp;|&nbsp; "
        "Intelligent Cloud revenue $34.7B (+30% YoY) &nbsp;|&nbsp; "
        "Microsoft AI business surpassed $37B annual revenue run rate (+123% YoY). "
        "CEO Satya Nadella: “We are focused on delivering cloud and AI infrastructure and "
        "solutions that empower every business to eval-max their outcomes in the agentic "
        "computing era.”",
        s,
    )]))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "<i>Sources: Microsoft FY2025 Annual Report [2]; Microsoft FY26 Q1 press release [6]; "
        "Microsoft FY26 Q2 press release [8]; Microsoft FY26 Q3 press release [9].</i>",
        s["caution"],
    ))

    # ── PLATFORM STRUCTURE ────────────────────────────────────────────────────
    story += section("Platform Structure", s)
    story.append(Paragraph(
        "Microsoft organizes its operations around three reportable segments used consistently "
        "across SEC filings, investor communications, and the annual report.",
        s["body"],
    ))

    story.append(Paragraph("Productivity and Business Processes", s["subsection_heading"]))
    story += bullets([
        "Microsoft 365 Commercial products and cloud services, including Microsoft 365 Copilot, "
        "Exchange, SharePoint, Teams, Power BI, and enterprise security and compliance tools.",
        "Microsoft 365 Consumer products and cloud services.",
        "LinkedIn, including Talent Solutions, Marketing Solutions, and Premium Subscriptions.",
        "Dynamics 365 for ERP, CRM, and business operations.",
    ], s)

    story.append(Paragraph("Intelligent Cloud", s["subsection_heading"]))
    story += bullets([
        "Azure and other cloud services: public, private, and hybrid cloud infrastructure, AI "
        "infrastructure, data and analytics, cybersecurity, and developer services.",
        "Azure AI services: Azure OpenAI Service, Azure Machine Learning, and Azure Cognitive Services.",
        "Azure Health Data Services: FHIR-compliant APIs for ingesting, managing, and exchanging "
        "protected health information.",
        "GitHub, SQL Server, Windows Server, and enterprise infrastructure products.",
        "Nuance Communications: clinical documentation AI acquired in 2022, integrated into "
        "Microsoft for Healthcare.",
    ], s)

    story.append(Paragraph("More Personal Computing", s["subsection_heading"]))
    story += bullets([
        "Windows and Devices, including OEM licensing and Surface hardware.",
        "Gaming: Xbox hardware, Game Pass, Xbox Cloud Gaming, and first- and third-party content.",
        "Search and news advertising: Bing, Copilot, Microsoft News, and Microsoft Edge.",
    ], s)

    story.append(Paragraph("Health-Adjacent Public Platform Surfaces", s["subsection_heading"]))
    story += bullets([
        "Microsoft for Healthcare: https://www.microsoft.com/en-us/ai/health",
        "Microsoft Cloud for Healthcare",
        "Azure Health Data Services",
        "Microsoft AI for Health (philanthropic research program, 200+ grantee partnerships)",
        "Microsoft Research — AI and the Future of Health",
    ], s)
    story.append(Paragraph(
        "<i>Sources: Microsoft FY2025 Annual Report [2]; Microsoft for Healthcare [3]; "
        "Azure Health Data Services [11]; Microsoft AI for Health [13].</i>",
        s["caution"],
    ))

    # ── STRATEGIC THEMES ──────────────────────────────────────────────────────
    story += section("Strategic Themes", s)
    story += bullets([
        "Enterprise cloud platform growth led by Azure, now surpassing $75B in annual revenue.",
        "AI monetization at scale: AI business exceeding a $37B annual revenue run rate as of "
        "Q3 FY2026, up 123% YoY.",
        "Copilot as a cross-product AI integration layer across Microsoft 365, Azure, GitHub, "
        "Dynamics, and Bing.",
        "FHIR-compliant health data interoperability enabling research, clinical analytics, and "
        "EHR integration at scale.",
        "Philanthropic health AI grant program (AI for Health) with 200+ grantee partnerships "
        "since 2020.",
        "Clinical documentation AI through Nuance supporting care delivery workflows in health systems.",
        "OpenAI partnership providing access to frontier model capabilities integrated across "
        "Azure and consumer products.",
        "Data center capital investment of $80B planned in fiscal 2025 to support AI workloads.",
        "Commercial remaining performance obligation of $392B as of Q1 FY2026.",
    ], s)
    story.append(Paragraph(
        "<i>Sources: Microsoft FY2025 Annual Report [2]; Microsoft FY26 Q1 press release [6]; "
        "Microsoft FY26 Q3 press release [9]; Microsoft for Healthcare [3]; "
        "Microsoft AI for Health [13].</i>",
        s["caution"],
    ))

    # ── AI AND TECHNOLOGY SIGNALS ─────────────────────────────────────────────
    story += section("AI and Technology Signals", s)
    story.append(Paragraph(
        "Microsoft's AI posture in 2026 is defined by integration across its full platform stack. "
        "Azure OpenAI Service brings frontier model capabilities to enterprise customers. "
        "Microsoft 365 Copilot applies AI across productivity and workflow tools. Nuance brings "
        "ambient clinical intelligence to care delivery. Microsoft Research operates the AI for "
        "Health program as a philanthropic and scientific collaboration infrastructure.",
        s["body"],
    ))

    story.append(Paragraph("AI Business Scale", s["subsection_heading"]))
    story += bullets([
        "Q3 FY2026: AI business at $37B annual revenue run rate, up 123% YoY.",
        "Q1 FY2026: Azure AI services revenue grew 40% YoY.",
        "Q2 FY2025: AI business at $13B annual revenue run rate, up 175% YoY at that point.",
    ], s)

    story.append(Paragraph("Biomedical and Clinical AI Research", s["subsection_heading"]))
    story.append(Paragraph(
        "Microsoft Research has developed and published foundational biomedical NLP models "
        "including PubMedBERT and BioGPT. The research team has stated commitments to advancing "
        "large language model capabilities in biomedicine, including methods for fact-checking "
        "and provenance in clinical contexts. Microsoft Research's AI for Good Lab publishes "
        "health-focused research through peer-reviewed venues including Mayo Clinic Proceedings: "
        "Digital Health and the Journal of Graduate Medical Education, with collaborating "
        "institutions including Johns Hopkins University, New York University, and the Institute "
        "for Health Metrics and Evaluation at the University of Washington.",
        s["body"],
    ))

    story.append(Paragraph("Named AI Research Areas", s["subsection_heading"]))
    story += bullets([
        "Biomedical NLP and large language models in health.",
        "Multimodal health data analysis spanning clinical notes, imaging, and device data.",
        "AI for population health and disease prediction at the county and national level.",
        "Predictive modeling for health system optimization, disease screening, and outcomes forecasting.",
    ], s)
    story.append(KeepTogether([highlight_box(
        "<b>Caution:</b> Frame Microsoft as strong in enterprise AI integration, clinical data "
        "infrastructure, and applied health AI research — not as the developer of frontier "
        "models independent of its OpenAI partnership. Microsoft's AI business is documented "
        "through Azure OpenAI Service and Copilot integrations; the underlying models are "
        "primarily developed by OpenAI.",
        s,
    )]))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "<i>Sources: Microsoft FY26 Q3 press release [9]; Microsoft FY26 Q1 press release [6]; "
        "Microsoft Research — AI and the Future of Health [14]; "
        "Microsoft AI for Health [13].</i>",
        s["caution"],
    ))

    # ── HEALTH INFRASTRUCTURE ─────────────────────────────────────────────────
    story += section("Health, Clinical, and Data Infrastructure", s)

    story.append(Paragraph("Microsoft Cloud for Healthcare", s["subsection_heading"]))
    story.append(Paragraph(
        "Microsoft Cloud for Healthcare is a purpose-built industry cloud combining Azure "
        "infrastructure, Dynamics 365, Microsoft Teams, and Power BI with healthcare-specific "
        "data models and compliance capabilities. It supports unified patient data views, "
        "virtual health visits, remote patient monitoring, and clinical analytics. The platform "
        "is built on FHIR-compliant data models and is designed to support HIPAA compliance "
        "and PHI governance across clouds, apps, and devices.",
        s["body"],
    ))

    story.append(Paragraph("Azure Health Data Services and FHIR", s["subsection_heading"]))
    story.append(Paragraph(
        "Azure Health Data Services provides a FHIR-based infrastructure layer for ingesting, "
        "persisting, and querying protected health information across disparate clinical systems. "
        "The FHIR service supports EHR integration, IoT medical device data ingestion via the "
        "MedTech service, DICOM medical imaging support, and standardized data exchange with "
        "SMART on FHIR for mobile and web applications. IDC named Microsoft a leader in U.S. "
        "Healthcare Cloud IT Infrastructure in the 2025–2026 vendor assessment.",
        s["body"],
    ))

    story.append(Paragraph("Nuance and Clinical Documentation AI", s["subsection_heading"]))
    story.append(Paragraph(
        "Nuance, acquired by Microsoft in 2022, provides ambient clinical intelligence tools "
        "that reduce clinician documentation burden by capturing and structuring care "
        "conversations in real time. This capability is integrated into Microsoft for Healthcare "
        "and represents a documented enterprise-facing clinical AI deployment at scale.",
        s["body"],
    ))

    story.append(Paragraph("Microsoft AI for Health Program", s["subsection_heading"]))
    story.append(Paragraph(
        "Launched in January 2020 under the AI for Good Research Lab, the program has partnered "
        "with more than 200 grantees on projects designed to accelerate medical research, build "
        "research capabilities, generate global health insights, and address health inequities. "
        "The program provides Azure cloud computing credits, high-performance computing "
        "resources, and in-kind data science collaboration from Microsoft Research scientists. "
        "Named collaborating institutions include Johns Hopkins University, New York University, "
        "IHME at the University of Washington, and Tec Monterrey. Active co-funding programs "
        "include a partnership with the Ovarian Cancer Research Alliance providing grants up to "
        "$900,000 over three years plus Azure computing credits.",
        s["body"],
    ))
    story.append(Paragraph(
        "<i>Sources: Microsoft for Healthcare [3]; Azure Health Data Services [11]; "
        "Microsoft Cloud for Healthcare [12]; Microsoft AI for Health [13].</i>",
        s["caution"],
    ))

    # ── UNC ALIGNMENT ─────────────────────────────────────────────────────────
    story += section("Alignment with UNC Research", s)
    story.append(Paragraph(
        "No direct named UNC–Microsoft institutional partnership has been identified from "
        "the current source set. The following represents strategic alignment based on documented "
        "Microsoft capabilities and UNC research strengths. A second research pass targeting "
        "named UNC personnel, sponsored research activity, licensing records, alumni links, and "
        "existing Azure or Microsoft Research agreements is recommended before making "
        "partnership claims.",
        s["body"],
    ))

    story.append(Paragraph("Three Strategic Framing Pillars for UNC", s["subsection_heading"]))
    story += bullets([
        "<b>Health data infrastructure and clinical informatics:</b> Microsoft's FHIR-compliant "
        "Azure Health Data Services and Microsoft Cloud for Healthcare create direct alignment "
        "with UNC biomedical informatics programs. RENCI and UNC Research Computing are natural "
        "Azure infrastructure partnership candidates.",
        "<b>AI for Health research grants:</b> The Microsoft AI for Health program provides "
        "Azure credits and data science collaboration to 200+ academic grantees. UNC researchers "
        "in public health, biomedical informatics, and implementation science are well positioned "
        "to apply.",
        "<b>Enterprise AI and applied machine learning:</b> Azure AI services, Microsoft 365 "
        "Copilot, and Microsoft Research's biomedical NLP work align with UNC Computer Science "
        "and applied AI faculty, particularly in clinical NLP, predictive modeling, and "
        "multimodal data analysis.",
    ], s)

    story.append(Paragraph("Specific UNC Research Fit Areas", s["subsection_heading"]))
    story += bullets([
        "<b>Biomedical informatics and health data science:</b> Azure Health Data Services and "
        "FHIR infrastructure directly support UNC informatics groups working with clinical data, "
        "EHR-derived datasets, and longitudinal research cohorts.",
        "<b>Public health analytics:</b> Microsoft AI for Health's focus on population-level "
        "disease prediction and health equity modeling aligns with UNC Gillings School of Global "
        "Public Health.",
        "<b>Clinical research and implementation science:</b> Microsoft Cloud for Healthcare use "
        "cases in remote patient monitoring and clinical analytics are relevant to UNC health "
        "system and implementation science researchers.",
        "<b>Computer science and applied AI:</b> Microsoft Research's biomedical NLP work and "
        "AI for Good Lab publications align with UNC CS and applied ML faculty.",
        "<b>RENCI and research computing:</b> Azure cloud infrastructure, Microsoft Fabric, and "
        "data engineering capabilities are natural targets for RENCI and UNC Research Computing.",
    ], s)

    story.append(Paragraph("Recommended Enrichment Targets", s["subsection_heading"]))
    story += bullets([
        "RENCI (Renaissance Computing Institute)",
        "UNC Department of Computer Science",
        "UNC Biomedical Informatics program (CHIP)",
        "UNC Gillings School of Global Public Health — epidemiology and data analytics groups",
        "UNC Research Computing and data-intensive science infrastructure teams",
        "UNC School of Medicine — clinical informatics and digital health programs",
        "UNC Eshelman School of Pharmacy — computational drug research groups",
    ], s)
    story.append(Paragraph(
        "<i>Sources: Microsoft for Healthcare [3]; Microsoft AI for Health [13]; "
        "Azure Health Data Services [11]; Microsoft Research [14].</i>",
        s["caution"],
    ))

    # ── TALKING POINTS ────────────────────────────────────────────────────────
    story += section("Talking Points", s)

    story.append(Paragraph("Organizational Context", s["subsection_heading"]))
    story += bullets([
        "Microsoft is the world's second-largest cloud provider by revenue, with Azure surpassing "
        "$75B in annual revenue in fiscal 2025 and continuing to accelerate (+39–40% YoY).",
        "Total fiscal 2025 revenue was $281.7B (+15% YoY), and the AI business alone reached a "
        "$37B annual revenue run rate as of Q3 FY2026 — up 123% YoY.",
        "A commercial remaining performance obligation of $392B reflects long-duration enterprise "
        "commitments being built around Azure and AI infrastructure.",
        "Microsoft should not be framed as only a software or productivity company. Its 2026 "
        "operating profile is defined by cloud infrastructure, AI services, and a purpose-built "
        "healthcare platform.",
    ], s)

    story.append(Paragraph("Research and Innovation Relevance", s["subsection_heading"]))
    story += bullets([
        "The AI for Health program demonstrates a documented, active, and structured mechanism "
        "for academic research collaboration, with over 200 grantee partnerships and ongoing "
        "co-funding programs including the Ovarian Cancer Research Alliance partnership.",
        "Microsoft Research's biomedical NLP work — including PubMedBERT and BioGPT — "
        "and the AI for Good Lab's peer-reviewed health publications establish Microsoft as a "
        "credible scientific collaborator, not only a vendor.",
        "Azure Health Data Services and FHIR-compliant infrastructure position Microsoft as an "
        "enabler of large-scale health data assembly for machine learning and analytics.",
    ], s)

    story.append(Paragraph("Alignment with Academic Health Systems", s["subsection_heading"]))
    story += bullets([
        "Microsoft's healthcare platform maps to providers, payors, life sciences, and health "
        "solutions — directly relevant to UNC across its health system, schools of public "
        "health, pharmacy, and medicine.",
        "Academic health systems offer Microsoft what enterprise software sales alone cannot: "
        "validated clinical environments, IRB-governed research infrastructure, training "
        "pipelines, and domain-specific clinical expertise.",
        "The strongest defensible collaboration angles are health data infrastructure, clinical "
        "AI evaluation, biomedical informatics, and AI for Health grant-funded research.",
    ], s)

    # ── RISK AND CAUTION NOTES ────────────────────────────────────────────────
    story += section("Risk and Caution Notes", s)
    story += bullets([
        "Do not imply a formal UNC–Microsoft partnership without evidence from a dedicated "
        "follow-up research pass targeting named agreements, sponsored research activity, or "
        "existing Azure for Research relationships.",
        "Do not conflate Microsoft's AI capabilities with OpenAI's frontier model development. "
        "Frame Microsoft as the enterprise deployment and infrastructure layer, not the sole "
        "model developer.",
        "Do not overstate Nuance's clinical AI capabilities beyond what is publicly documented; "
        "the company's ambient documentation AI is an enterprise product, not a validated "
        "clinical decision support tool in the regulatory sense.",
        "Keep AI revenue and growth figures attributed to Microsoft investor communications and "
        "SEC filings rather than third-party projections.",
        "The AI for Health program is a philanthropic program under Microsoft Research, distinct "
        "from Azure commercial agreements. Do not conflate grant program participation with "
        "commercial licensing or cloud procurement relationships.",
    ], s)

    # ── EXPECTED REPORT ANGLE ─────────────────────────────────────────────────
    story += section("Expected Report Angle and Positioning", s)
    story.append(highlight_box(
        "<b>Positioning Summary:</b> Microsoft should be framed as (1) the world's second-largest "
        "cloud provider with Azure growing 39–40% YoY and an AI business at a $37B annual "
        "revenue run rate; (2) a purpose-built healthcare technology partner with FHIR-compliant "
        "data infrastructure, clinical documentation AI through Nuance, and a dedicated Microsoft "
        "Cloud for Healthcare product line; (3) a documented academic research collaborator "
        "through the AI for Health program with 200+ grantee partnerships and active co-funding "
        "with institutions including Johns Hopkins and NYU; (4) a technically credible fit for "
        "UNC biomedical informatics, health data science, applied AI, and research computing "
        "ecosystems; and (5) a different type of partner than J&amp;J or a biopharma company "
        "— stronger for cloud infrastructure, clinical data interoperability, health AI "
        "research grants, and enterprise software collaboration than for therapeutic pipeline or "
        "device development work.",
        s,
    ))

    # ── REFERENCES ────────────────────────────────────────────────────────────
    story += section("References", s)
    refs = [
        ("[1]",  "Microsoft Investor Relations",
                 "https://www.microsoft.com/en-us/investor"),
        ("[2]",  "Microsoft FY2025 Annual Report",
                 "https://www.microsoft.com/investor/reports/ar25/index.html"),
        ("[3]",  "Microsoft for Healthcare",
                 "https://www.microsoft.com/en-us/ai/health"),
        ("[4]",  "Microsoft SEC Filings (EDGAR)",
                 "https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000789019"),
        ("[5]",  "Microsoft FY2025 Q4 Press Release (July 30, 2025)",
                 "https://www.microsoft.com/en-us/investor/earnings/fy-2025-q4/press-release-webcast"),
        ("[6]",  "Microsoft FY2026 Q1 Press Release (October 29, 2025)",
                 "https://www.microsoft.com/en-us/investor/earnings/fy-2026-q1/press-release-webcast"),
        ("[7]",  "Microsoft FY2026 Q1 SEC Exhibit 99.1",
                 "https://www.sec.gov/Archives/edgar/data/0000789019/000119312525256310/msft-ex99_1.htm"),
        ("[8]",  "Microsoft FY2026 Q2 SEC Exhibit 99.1 (January 28, 2026)",
                 "https://www.sec.gov/Archives/edgar/data/0000789019/000119312526027198/msft-ex99_1.htm"),
        ("[9]",  "Microsoft FY2026 Q3 SEC Exhibit 99.1 (April 30, 2026)",
                 "https://www.sec.gov/Archives/edgar/data/0000789019/000119312526191457/msft-ex99_1.htm"),
        ("[10]", "Microsoft Learn — FHIR service in Azure Health Data Services",
                 "https://learn.microsoft.com/en-us/azure/healthcare-apis/fhir/overview"),
        ("[11]", "Azure Health Data Services",
                 "https://azure.microsoft.com/en-us/products/health-data-services"),
        ("[12]", "Microsoft Cloud for Healthcare",
                 "https://azure.microsoft.com/en-us/blog/microsoft-cloud-for-healthcare-unlocking-the-power-of-health-data-for-better-care/"),
        ("[13]", "Microsoft AI for Health",
                 "https://www.microsoft.com/en-us/research/project/ai-for-health/"),
        ("[14]", "Microsoft Research — AI and the Future of Health",
                 "https://www.microsoft.com/en-us/research/blog/ai-and-the-future-of-health/"),
        ("[15]", "Microsoft — Building Secure Foundations for Responsible AI in Healthcare (April 2026)",
                 "https://www.microsoft.com/en-us/microsoft-cloud/blog/healthcare/2026/04/16/building-secure-foundations-for-responsible-ai-in-healthcare-with-microsoft/"),
        ("[16]", "Ovarian Cancer Research Alliance — CRDG-AI Grant with Microsoft AI for Good Lab",
                 "https://ocrahope.org/news/ocras-collaborative-research-development-grant-microsoft-ai-for-health-grantees/"),
    ]
    for num, title, url in refs:
        story.append(Paragraph(f"<b>{num}</b> {title} &mdash; {url}", s["ref"]))

    story.append(Spacer(1, 0.3 * inch))
    story.append(rule())
    story.append(Paragraph(
        "Partnership Intelligence Profile — Microsoft Corporation — Internal Use Only — May 2026",
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
        title="Partnership Intelligence Profile — Microsoft Corporation",
        author="UNC Office of Innovation and Commercialization",
        subject="Microsoft Corporation Partnership Intelligence",
    )
    doc.build(build_story(s))
    print(f"PDF written to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
