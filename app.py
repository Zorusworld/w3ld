
import streamlit as st
import pdfplumber
from fpdf import FPDF
import tempfile

DEFAULT_RATE = 100

class QuotePDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 14)
        self.cell(0, 10, "STRUCTURAL STEEL QUOTE", ln=True, align="C")
        self.set_font("Arial", "", 10)
        self.cell(0, 10, "Field Welding & Installation Estimate", ln=True, align="C")
        self.ln(5)

    def section_title(self, title):
        self.set_font("Arial", "B", 11)
        self.cell(0, 10, title, ln=True)
        self.ln(2)

    def section_body(self, text):
        self.set_font("Arial", "", 10)
        self.multi_cell(0, 8, text)
        self.ln()

st.set_page_config(page_title="Steel Quote Generator", layout="centered")
st.title("📐 Structural Quote Generator")
st.subheader("Upload a PDF blueprint and generate a quote.")

uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])
rate = st.number_input("Rate ($ per linear foot)", min_value=1, max_value=1000, value=DEFAULT_RATE)

if uploaded_file and st.button("Generate Quote"):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_path = tmp_file.name

    pages_scanned = []
    with pdfplumber.open(tmp_path) as pdf:
        for i, page in enumerate(pdf.pages):
            text = page.extract_text() or ""
            if any(k in text for k in ["RTU", "stair", "platform", "C15x", "W", "HSS", "guard"]):
                pages_scanned.append((i + 1, text[:200]))

    quote = QuotePDF()
    quote.add_page()
    quote.section_title("Blueprint Analysis")
    for pg, preview in pages_scanned:
       File "/opt/render/project/src/app.py"
          quote.section_body(f"Page {pg}:
                             ^
SyntaxError: unterminated f-string literal (detected at line 50)
          quote.section_body(f"Page {pg}:
                             ^
SyntaxError: unterminated f-string literal (detected at line 50)
{preview}
")

    quote.section_title("Estimate Summary")
    quote.section_body(f"""
Detected Pages: {len(pages_scanned)}
Rate: ${rate} per linear foot

This is a preliminary estimate based on blueprint text scan.
""")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as out_file:
        quote.output(out_file.name)
        with open(out_file.name, "rb") as f:
            st.success("✅ Quote PDF ready!")
            st.download_button("📥 Download Quote", data=f.read(), file_name="steel_quote.pdf", mime="application/pdf")
