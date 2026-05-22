import json, datetime, re
from pathlib import Path
from fpdf import FPDF

out_base = Path("data/processed/company-profiles")

class ProfessionalPDF(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 18)
        self.cell(0, 10, "STRATEGIC PARTNERSHIP BRIEF", align="C", new_x="LMARGIN", new_y="NEXT")
        self.line(10, 22, 200, 22)
        self.ln(10)

    def section(self, title, content):
        self.set_font("Helvetica", "B", 14)
        self.set_fill_color(220, 220, 220)
        self.cell(0, 10, title, new_x="LMARGIN", new_y="NEXT", fill=True)
        self.ln(2)
        self.set_font("Helvetica", "", 11)
        # Handle numbered lists by forcing newlines
        formatted = re.sub(r'(\d\.)', r'\n\1', content)
        self.multi_cell(0, 7, formatted.encode("latin-1", "replace").decode("latin-1"))
        self.ln(5)

def save_report(company, data):
    out_path = out_base / company
    out_path.mkdir(parents=True, exist_ok=True)
    
    # PDF
    pdf = ProfessionalPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, f"COMPANY: {company.upper()}", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(0, 50, 150)
    pdf.cell(0, 10, f"LOCATION: {data['basic_info']['location']}", new_x="LMARGIN", new_y="NEXT")
    pdf.set_text_color(0, 0, 0)
    pdf.ln(5)
    
    pdf.section("COMPANY OVERVIEW", data['overview'])
    pdf.section("UNC CONNECTION", data['unc_connection'])
    pdf.section("TALKING POINTS", data['talking_points'])
    pdf.section("REFERENCES", data['references'])
    pdf.output(str(out_path / "deliverable.pdf"))
    
    # Markdown
    md = f"# {company.upper()} PROFILE\n\n## Company Overview\n{data['overview']}\n\n## Basic Company Information\n{json.dumps(data['basic_info'], indent=2)}\n\n## UNC Connection\n{data['unc_connection']}\n\n## Talking Points\n{data['talking_points']}\n\n## References\n{data['references']}"
    (out_path / f"{company}-profile.md").write_text(md, encoding="utf-8")

    # JSONs
    (out_path / "profile.json").write_text(json.dumps(data, indent=4), encoding="utf-8")
    (out_path / "summary.json").write_text(json.dumps({"company": company, "status": "Ready"}, indent=4), encoding="utf-8")
    (out_path / "raw.txt").write_text(data['overview'], encoding="utf-8")

DATA = {
    "apple": {
        "basic_info": {"location": "Cupertino, CA", "type": "Public", "industry": "Consumer Tech"},
        "overview": "Apple Inc. is a global leader in consumer technology, focusing on the seamless integration of high-performance hardware, software, and services. They are currently scaling their 'Apple Intelligence' framework.",
        "unc_connection": "Strong alignment with UNC's mHealth, wearable sensors, and biomedical informatics programs. Apple's ResearchKit is widely used in academic clinical research.",
        "talking_points": "1. AI integration in consumer ecosystems: Leverage Apple's on-device NPU for clinical study data processing. 2. HealthKit/ResearchKit data pipelines: Partner with UNC to validate Apple's health-tracking algorithms against ground-truth clinical trial data. 3. Privacy-first ML architecture: Collaborate on secure multi-party computation for healthcare analytics.",
        "references": "[1] Apple Investor Relations, [2] Apple Health Platforms, [3] UNC mHealth Research Labs"
    },
    "google": {
        "basic_info": {"location": "Mountain View, CA", "type": "Public", "industry": "Technology / AI / Cloud"},
        "overview": "Google is a pioneer in cloud-scale computing and AI, specifically leveraging 'Gemini' for healthcare applications and DeepMind for computational biology. Their enterprise and research tooling align with university-scale data science operations.",
        "unc_connection": "Direct alignment with UNC's MATRIX project and RENCI initiatives. UNC's work using biomedical knowledge graphs to identify drug-disease connections mirrors the core logic of Google's 'Expert AI' target discovery engines.",
        "talking_points": "1. Multimodal LLMs for clinical note synthesis: Utilize Gemini for automating EHR transcription at UNC Health. 2. Knowledge graph-based drug target discovery: Collaborative research using MATRIX-based graphs on Google Cloud infrastructure. 3. Cloud-native EHR interoperability: Implementing FHIR-standard data transformation pipelines.",
        "references": "[1] Alphabet Financials, [2] Google DeepMind Health, [3] UNC RENCI/MATRIX Project"
    },
    "pfizer": {
        "basic_info": {"location": "New York, NY", "type": "Public", "industry": "Biopharmaceuticals"},
        "overview": "Pfizer is a global biopharmaceutical entity shifting toward an automated, digital-first oncology pipeline and mRNA vaccine distribution infrastructure. They are actively integrating AI to streamline drug development.",
        "unc_connection": "UNC Eshelman School of Pharmacy medicinal chemistry faculty and the Lineberger Comprehensive Cancer Center align with Pfizer's pipeline for kinase-inhibitor development.",
        "talking_points": "1. Oncology target discovery: Joint research on novel kinase-inhibitor candidates for difficult-to-treat cancers. 2. Automated clinical trial clinical data synthesis: Pilot digital workflows for streamlining patient recruitment data. 3. mRNA platform scalability: Translational research collaborations focused on HMPV and pandemic-readiness vaccine design.",
        "references": "[1] Pfizer Pipeline Doc, [2] UNC Eshelman Research Impact, [3] ClinicalTrials.gov"
    }
}

for comp, data in DATA.items():
    save_report(comp, data)
    print(f"Generated: {comp}")
