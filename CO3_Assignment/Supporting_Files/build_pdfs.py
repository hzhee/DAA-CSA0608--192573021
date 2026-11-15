from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Preformatted
from reportlab.lib.units import inch
root=Path(__file__).resolve().parents[1];out=root/'Final_Report';styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='Body2',parent=styles['BodyText'],fontSize=10,leading=14,spaceAfter=7))
styles.add(ParagraphStyle(name='Code2',fontName='Courier',fontSize=8,leading=10,backColor=colors.HexColor('#f1f5f9'),borderPadding=6,spaceAfter=8))
def footer(c,d):
 c.saveState();c.setFont('Helvetica',8);c.setFillColor(colors.grey);c.drawString(40,25,'CSA06 CO3 Assignment');c.drawRightString(555,25,f'Page {d.page}');c.restoreState()
def build(src,target,title):
 story=[Paragraph(title,styles['Title']),Spacer(1,.15*inch)];code=False;buf=[]
 for raw in src.read_text().splitlines():
  s=raw.strip()
  if s.startswith('```'):
   if code:story.append(Preformatted('\n'.join(buf),styles['Code2']));buf=[]
   code=not code;continue
  if code:buf.append(raw);continue
  if not s:continue
  if s.startswith('# '):continue
  if s.startswith('## '):story.append(Paragraph(s[3:],styles['Heading1']));continue
  if s.startswith('|'):story.append(Paragraph(s.replace('|',' &nbsp; | &nbsp; '),styles['Body2']));continue
  story.append(Paragraph(s.replace('&','&amp;').replace('`','').replace('**',''),styles['Body2']))
 SimpleDocTemplate(str(target),pagesize=A4,leftMargin=42,rightMargin=42,topMargin=44,bottomMargin=42).build(story,onFirstPage=footer,onLaterPages=footer)
build(root/'Combined_Report.md',out/'Combined_Report.pdf','CO3 Assignment Combined Report')
build(root/'Combined_Pseudocode.md',out/'Combined_Pseudocode.pdf','CO3 Assignment Combined Pseudocode')
