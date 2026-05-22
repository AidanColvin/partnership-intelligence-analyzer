import json
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
        self.multi_cell(0, 7, content)
        self.ln(5)

DATA = {
    "apple": {"overview": "Apple Inc. focuses on neural processing, spatial computing, and privacy-first health monitoring.", "unc_alignment": "UNC Biomedical Engineering sensors map to Apple's HealthKit infrastructure.", "talking_points": "1. AI integration in consumer ecosystems. 2. HealthKit pipelines.", "references": "[1] Apple IR, [2] UNC Labs"},
    "google": {"overview": "Google is invested in Gemini for healthcare, biomedical knowledge graphs, and DeepMind protein folding.", "unc_alignment": "UNC’s MATRIX project shares DNA with Google's target discovery tools.", "talking_points": "1. Multimodal LLMs for clinical note synthesis. 2. Cloud-native EHR interoperability.", "references": "[1] Alphabet Financials, [2] UNC RENCI"},
    "pfizer": {"overview": "Pfizer is moving toward a digital-first oncology pipeline, leveraging automated clinical trial optimization.", "unc_alignment": "UNC Eshelman School of Pharmacy drug discovery aligns with Pfizer's kinase-inhibitor research.", "talking_points": "1. Oncology target discovery. 2. mRNA platform scalability.", "references": "[1] Pfizer Pipeline, [2] UNC Eshelman"}
}

for company, intel in DATA.items():
    out_path = out_base / company
    pdf = ProfessionalPDF()
    pdf.add_page()
    pdf.section("COMPANY OVERVIEW", intel['overview'])
    pdf.section("UNC CONNECTION", intel['unc_alignment'])
    pdf.section("TALKING POINTS", intel['talking_points'])
    pdf.section("REFERENCES", intel['references'])
    pdf.output(str(out_path / f"{company}-profile.pdf"))
    md = f"# {company.upper()} PROFILE\n\n## Overview\n{intel['overview']}\n\n## UNC Connection\n{intel['unc_alignment']}\n\n## Talking Points\n{intel['talking_points']}\n\n## References\n{intel['references']}"
    (out_path / f"{company}-profile.md").write_text(md)
