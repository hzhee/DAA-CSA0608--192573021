"""Create printable PDF versions of the combined report and pseudocode."""
from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Preformatted, Image
from reportlab.pdfbase.pdfmetrics import stringWidth

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "Final_Design_and_Analysis"; OUT.mkdir(exist_ok=True)
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="Cover", parent=styles["Title"], alignment=TA_CENTER, fontSize=22, leading=27, textColor=colors.HexColor("#172554"), spaceAfter=18))
styles.add(ParagraphStyle(name="H1x", parent=styles["Heading1"], fontSize=16, leading=20, textColor=colors.HexColor("#172554"), spaceBefore=13, spaceAfter=8))
styles.add(ParagraphStyle(name="H2x", parent=styles["Heading2"], fontSize=12, leading=15, textColor=colors.HexColor("#1e3a8a"), spaceBefore=10, spaceAfter=5))
styles.add(ParagraphStyle(name="Bodyx", parent=styles["BodyText"], fontSize=9.5, leading=13.5, spaceAfter=6))
styles.add(ParagraphStyle(name="CodeX", fontName="Courier", fontSize=7.5, leading=9.5, leftIndent=8, rightIndent=8, backColor=colors.HexColor("#f1f5f9"), borderColor=colors.HexColor("#cbd5e1"), borderWidth=.3, borderPadding=6, spaceAfter=8))

def footer(canvas, doc):
    canvas.saveState(); canvas.setStrokeColor(colors.HexColor("#cbd5e1")); canvas.line(40, 35, 555, 35)
    canvas.setFont("Helvetica", 8); canvas.setFillColor(colors.HexColor("#475569"))
    canvas.drawString(40, 22, "CSA06 CO3 - KartIQ Divide and Conquer Case Study")
    canvas.drawRightString(555, 22, f"Page {doc.page}"); canvas.restoreState()

def esc(text): return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def build_from_markdown(markdown, output, title, include_charts=False):
    story = [Spacer(1, .45*inch), Paragraph(title, styles["Cover"]), Paragraph("CSA06 Design and Analysis of Algorithms", styles["Bodyx"]), Spacer(1, .22*inch)]
    code = False; code_lines = []
    for raw in markdown.read_text().splitlines():
        line = raw.strip()
        if line.startswith("```"):
            if code:
                story.append(Preformatted("\n".join(code_lines), styles["CodeX"])); code_lines=[]
            code = not code; continue
        if code: code_lines.append(raw); continue
        if not line: continue
        if line.startswith("# "): story.append(Paragraph(esc(line[2:]), styles["H1x"])); continue
        if line.startswith("## "):
            story.append(Paragraph(esc(line[3:]), styles["H1x"])); continue
        if line.startswith("### "):
            story.append(Paragraph(esc(line[4:]), styles["H2x"])); continue
        if line.startswith("|"):
            if set(line) <= set("|-: "): continue
            cells = [esc(cell.strip()) for cell in line.strip("|").split("|")]
            story.append(Paragraph("<b> | </b>".join(cells), styles["Bodyx"])); continue
        text = esc(line).replace("**", "").replace("`", "")
        story.append(Paragraph(text, styles["Bodyx"]))
    if include_charts:
        story.append(PageBreak()); story.append(Paragraph("Complexity Graphs", styles["H1x"]))
        for chart in sorted((ROOT / "Final_Design_and_Analysis" / "Graphs").glob("*.png")):
            story.append(Image(str(chart), width=6.6*inch, height=3.83*inch)); story.append(Spacer(1, 10))
    SimpleDocTemplate(str(output), pagesize=A4, rightMargin=40, leftMargin=40, topMargin=42, bottomMargin=45).build(story, onFirstPage=footer, onLaterPages=footer)

build_from_markdown(ROOT / "Combined_Case_Study_Report.md", OUT / "Combined_Case_Study_Report.pdf", "KartIQ Case Study Report", True)
build_from_markdown(ROOT / "Combined_Pseudocode.md", OUT / "Combined_Pseudocode.pdf", "KartIQ Combined Pseudocode", False)
